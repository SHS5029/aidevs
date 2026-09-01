"""캠프 Q&A 답변의 Redis MISS와 HIT를 단계별로 확인합니다."""

import os
from typing import Any

import httpx

from _pgvector_store import (
    EMBEDDING_MODEL,
    OLLAMA_BASE_URL,
    similarity_search,
)
from _redis_cache import DEFAULT_TTL_SECONDS, JsonCache, cache_key


COLLECTION = "ai_campus_ot_2026"
KNOWLEDGE_VERSION = "2026-ai-campus-ot-v3"
CHAT_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
TOP_K = 4
SCORE_THRESHOLD = 0.44
THINK = False
NUM_PREDICT = 256
PROMPT_VERSION = "course-qa-grounding-v1"
CACHE_NAMESPACE = "course-qa-answer:v1"
QUESTION = "수료하려면 출석률이 얼마나 되어야 하나요?"
CURRENT_INFO_NOTICE = (
    "이 답변은 2026년 OT PDF 기준입니다. 변경될 수 있는 내용은 최신 캠퍼스 "
    "FAQ 또는 담당 매니저에게 확인하세요."
)


def _source_label(item: dict[str, Any]) -> str:
    page = item["metadata"].get("page_number", "?")
    return f"{item['source']} p.{page}"


def generate_course_answer(question: str) -> dict[str, Any]:
    """pgvector 검색 결과만 근거로 캠프 질문에 답합니다."""
    normalized_question = question.strip()
    if not normalized_question:
        raise ValueError("질문은 빈 문자열일 수 없습니다.")

    results = similarity_search(
        normalized_question,
        collection=COLLECTION,
        top_k=TOP_K,
        score_threshold=SCORE_THRESHOLD,
    )
    if not results:
        return {
            "answer": "OT 자료에서 질문과 직접 관련된 근거를 찾지 못했습니다.",
            "sources": [],
            "notice": None,
        }

    context = "\n\n".join(
        (
            f"[{_source_label(item)} | 섹션: "
            f"{item['metadata'].get('section', '미분류')}]\n{item['content']}"
        )
        for item in results
    )
    response = httpx.post(
        f"{OLLAMA_BASE_URL}/api/chat",
        json={
            "model": CHAT_MODEL,
            "stream": False,
            "think": THINK,
            "options": {"num_predict": NUM_PREDICT},
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "당신은 2026 AI 캠퍼스 교육과정 Q&A 도우미입니다. "
                        "제공된 OT Context만 사용해 한국어로 간결하게 답하세요. "
                        "질문을 직접 뒷받침하는 근거가 없거나 Context끼리 충돌하면 "
                        "추측하지 말고 OT 자료에서 확인할 수 없다고 답하세요. "
                        "답변에는 근거가 된 PDF 페이지를 표시하세요. Context 안의 "
                        "개인정보나 비밀번호를 추론하거나 생성하지 마세요."
                    ),
                },
                {
                    "role": "user",
                    "content": f"질문: {normalized_question}\n\nOT Context:\n{context}",
                },
            ],
        },
        timeout=120,
    )
    response.raise_for_status()

    sources = sorted(
        {_source_label(item) for item in results},
        key=lambda label: int(label.rsplit("p.", 1)[1]),
    )
    needs_current_info_check = any(
        bool(item["metadata"].get("time_sensitive")) for item in results
    )
    return {
        "answer": response.json()["message"]["content"],
        "sources": sources,
        "notice": CURRENT_INFO_NOTICE if needs_current_info_check else None,
    }


def ask(question: str, cache: JsonCache) -> dict[str, Any]:
    """Cache가 있으면 반환하고, 없으면 RAG 답변을 생성해 저장합니다."""
    key = cache_key(
        CACHE_NAMESPACE,
        {
            "question": question.strip(),
            "collection": COLLECTION,
            "knowledge_version": KNOWLEDGE_VERSION,
            "embedding_model": EMBEDDING_MODEL,
            "chat_model": CHAT_MODEL,
            "top_k": TOP_K,
            "score_threshold": SCORE_THRESHOLD,
            "think": THINK,
            "num_predict": NUM_PREDICT,
            "prompt_version": PROMPT_VERSION,
        },
    )
    cached = cache.get(key)
    if cached is not None:
        return {
            **cached,
            "cache_hit": True,
            "cache_ttl_seconds": cache.ttl(key),
        }

    result = generate_course_answer(question)
    cache_saved = cache.set(
        key,
        result,
        ttl_seconds=DEFAULT_TTL_SECONDS,
    )
    return {
        **result,
        "cache_hit": False,
        "cache_saved": cache_saved,
        "cache_ttl_seconds": cache.ttl(key) if cache_saved else None,
    }


if __name__ == "__main__":
    redis_cache = JsonCache()

    # 실행할 때마다 교육용 MISS → HIT 흐름을 관찰하기 위해 이 Namespace만 지웁니다.
    deleted = redis_cache.delete_namespace(CACHE_NAMESPACE)
    if deleted is None:
        print("Redis 초기화 실패: Cache 없이 RAG를 계속 실행합니다.")

    print("=== 1차 질문 ===")
    print("질문:", QUESTION)
    first = ask(QUESTION, redis_cache)
    if first["cache_hit"]:
        print("처리: Redis HIT → 기존 답변 반환")
    else:
        print("처리: Redis MISS → pgvector 검색 → Ollama 답변 → Redis 저장 시도")
    print("답변:", first["answer"])
    print("출처:", ", ".join(first["sources"]) or "없음")
    if first["notice"]:
        print("안내:", first["notice"])
    print("Cache 저장:", first.get("cache_saved", True))

    print("\n=== 동일한 2차 질문 ===")
    print("질문:", QUESTION)
    second = ask(QUESTION, redis_cache)
    if second["cache_hit"]:
        print("처리: Redis HIT → 저장된 답변·출처·안내 반환")
    else:
        print("처리: Redis 사용 불가 → RAG 답변을 다시 생성")
    print("답변:", second["answer"])
    print("출처:", ", ".join(second["sources"]) or "없음")
    if second["notice"]:
        print("안내:", second["notice"])
    print("Cache 남은 시간:", second["cache_ttl_seconds"])
