from __future__ import annotations

import os
from time import perf_counter
from typing import TypeVar

from dotenv import load_dotenv
from pydantic import BaseModel

from shared.travel_contracts import LearningAgentResult


load_dotenv()
T = TypeVar("T", bound=BaseModel)
SUPPORTED_PROVIDERS = ("gemini",)
DEFAULT_AGENT_PROVIDERS = {
    "weather_agent": "gemini",
    "place_agent": "gemini",
    "budget_agent": "gemini",
    "safety_agent": "gemini",
    "research_agent": "gemini",
    "writer_agent": "gemini",
    "reviewer_agent": "gemini",
    "router_agent": "gemini",
    "supervisor_agent": "gemini",
    "analyst_agent": "gemini",
    "developer_agent": "gemini",
    "support_agent": "gemini",
    "delivery_agent": "gemini",
    "technical_support_agent": "gemini",
    "refund_agent": "gemini",
    "evaluator_agent": "gemini",
    "reviser_agent": "gemini",
    "itinerary_agent": "gemini",
}


def provider_model(provider: str) -> str:
    if provider != "gemini":
        raise ValueError(f"이 예제는 Gemini Provider만 지원합니다: {provider}")
    model = os.getenv("GEMINI_MODEL", "").strip()
    if not model:
        raise ValueError("GEMINI_MODEL 환경 변수를 설정하세요.")
    return model


def run_structured(provider: str, prompt: str, schema: type[T]) -> T:
    """Pydantic 계약을 Gemini API의 구조화된 출력으로 검증합니다."""
    model = provider_model(provider)
    from google import genai

    with genai.Client(api_key=os.environ["GEMINI_API_KEY"]) as client:
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_json_schema": schema.model_json_schema(),
            },
        )
    if not response.text:
        raise RuntimeError("Gemini가 구조화된 결과를 반환하지 않았습니다.")
    return schema.model_validate_json(response.text)


def run_with_metadata(provider: str, prompt: str, schema: type[T]) -> dict:
    model = provider_model(provider)
    started = perf_counter()
    try:
        result = run_structured(provider, prompt, schema)
        return {
            "provider_requested": provider,
            "provider_used": provider,
            "model": model,
            "fallback_used": False,
            "latency_ms": round((perf_counter() - started) * 1000, 2),
            "result": result.model_dump(),
            "error": None,
        }
    except Exception as error:
        return {
            "provider_requested": provider,
            "provider_used": None,
            "model": model,
            "fallback_used": False,
            "latency_ms": round((perf_counter() - started) * 1000, 2),
            "result": None,
            "error": f"{type(error).__name__}: {error}",
        }


def provider_for_agent(agent_id: str) -> str:
    """공통 .env의 다른 Provider 설정과 관계없이 Gemini를 사용합니다."""
    return "gemini"


def run_learning_agent(agent_id: str, goal: str, request: str, context: object | None = None) -> dict:
    """초보자 예제용 공통 AI Agent 실행 함수입니다."""
    provider = provider_for_agent(agent_id)
    prompt = f"""
당신은 {agent_id}입니다.
Goal: {goal}
다른 Agent의 역할을 대신하지 마세요.
요청: {request}
이전 Agent가 전달한 Context: {context}
LearningAgentResult 형식으로 반환하고 agent_id는 반드시 {agent_id}로 작성하세요.
""".strip()
    response = run_with_metadata(provider, prompt, LearningAgentResult)
    if response["result"] is not None:
        # Agent identity belongs to the orchestrator, not to model-generated content.
        response["result"]["agent_id"] = agent_id
    return response


def run_learning_agent_with_failover(
    agent_id: str,
    goal: str,
    request: str,
    providers: tuple[str, ...],
) -> dict:
    """기존 호출 인터페이스를 유지하며 Gemini만 한 번 시도합니다."""
    prompt = f"당신은 {agent_id}입니다. Goal: {goal}\n요청: {request}\nagent_id는 반드시 {agent_id}입니다."
    response = run_with_metadata("gemini", prompt, LearningAgentResult)
    if response["result"] is not None:
        response["result"]["agent_id"] = agent_id
    return {
        **response,
        "attempts": [{"provider": "gemini", "model": response["model"], "error": response["error"]}],
        "failover_used": False,
    }
