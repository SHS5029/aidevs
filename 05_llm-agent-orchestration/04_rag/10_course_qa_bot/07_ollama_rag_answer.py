"""캠프 OT 검색 결과를 근거로 Ollama가 답변합니다."""

import os
from typing import Any

import httpx

from _pgvector_store import OLLAMA_BASE_URL, similarity_search


COLLECTION = "ai_campus_ot_2026"
CHAT_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
TOP_K = 4
SCORE_THRESHOLD = 0.44
THINK = False
NUM_PREDICT = 256
PROMPT_VERSION = "course-qa-grounding-v1"
QUESTION = "전체 교육 기간과 하루 교육 시간은 어떻게 되나요?"
CURRENT_INFO_NOTICE = (
    "이 답변은 2026년 OT PDF 기준입니다. 변경될 수 있는 내용은 최신 캠퍼스 "
    "FAQ 또는 담당 매니저에게 확인하세요."
)


def _source_label(item: dict[str, Any]) -> str:
    page = item["metadata"].get("page_number", "?")
    return f"{item['source']} p.{page}"


def answer_course_question(question: str) -> dict[str, Any]:
    """OT 근거가 충분할 때만 한국어 답변과 PDF 페이지를 반환합니다."""
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


if __name__ == "__main__":
    result = answer_course_question(QUESTION)
    print("질문:", QUESTION)
    print("답변:", result["answer"])
    print("출처:", ", ".join(result["sources"]) or "없음")
    if result["notice"]:
        print("안내:", result["notice"])
