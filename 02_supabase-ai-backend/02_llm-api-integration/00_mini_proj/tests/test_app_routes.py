r"""00_mini_proj의 FastAPI 엔드포인트를 확인하는 자동화 테스트입니다.

실행 방법:
    cd 02_supabase-ai-backend/02_llm-api-integration/00_mini_proj
    python -m pytest tests -v

FastAPI TestClient가 uvicorn 없이 애플리케이션을 메모리에서 실행합니다.
Gemini 클라이언트는 테스트용 가짜 객체로 교체하므로 실제 API, 네트워크,
Supabase 또는 OpenAI 서비스를 호출하지 않습니다.
"""

from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.routers import chat_router


client = TestClient(app)


def test_health_returns_ok() -> None:
    """상태 확인 API가 정상 응답을 반환하는지 확인합니다."""

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_chat_gemini_returns_fake_answer_without_external_call(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Gemini 요청 구조와 API 응답을 실제 네트워크 호출 없이 확인합니다."""

    captured: dict[str, object] = {}

    class FakeModels:
        def generate_content(self, *, model: str, contents: list[dict]) -> SimpleNamespace:
            captured["model"] = model
            captured["contents"] = contents
            return SimpleNamespace(text="테스트용 Gemini 답변")

    class FakeClient:
        def __init__(self, *, api_key: str | None) -> None:
            captured["api_key"] = api_key
            self.models = FakeModels()

    monkeypatch.setenv("GEMINI_API_KEY", "test-only-key")
    monkeypatch.setenv("GEMINI_MODEL", "test-gemini-model")
    monkeypatch.setattr(chat_router.genai, "Client", FakeClient)

    response = client.post(
        "/chat/gemini",
        json={"user_id": "student-1", "prompt": "FastAPI를 설명해 주세요."},
    )

    assert response.status_code == 200
    assert response.json() == {
        "user_id": "student-1",
        "answer": "테스트용 Gemini 답변",
    }
    assert captured == {
        "api_key": "test-only-key",
        "model": "test-gemini-model",
        "contents": [
            {
                "role": "user",
                "parts": [{"text": "FastAPI를 설명해 주세요."}],
            }
        ],
    }


@pytest.mark.parametrize(
    "payload",
    [
        {"prompt": "질문"},
        {"user_id": "student-1"},
        {"user_id": "", "prompt": "질문"},
        {"user_id": "student-1", "prompt": ""},
    ],
)
def test_chat_rejects_missing_or_empty_fields(payload: dict[str, str]) -> None:
    """필수 채팅 값이 누락되거나 비어 있으면 요청을 거절하는지 확인합니다."""

    response = client.post("/chat/gemini", json=payload)

    assert response.status_code == 422


def test_create_product_returns_submitted_product() -> None:
    """상품 생성 API가 전달받은 상품을 반환하는지 확인합니다."""

    product = {"id": 10, "name": "AI 노트", "price": 15000}

    response = client.post("/product/create", json=product)

    assert response.status_code == 200
    assert response.json() == product


def test_get_product_uses_requested_id() -> None:
    """상품 단건 조회가 경로의 상품 ID를 응답에 반영하는지 확인합니다."""

    response = client.get("/product/get/42")

    assert response.status_code == 200
    assert response.json() == {
        "id": 42,
        "name": "Sample Product",
        "price": 30000,
    }


def test_get_all_products_returns_sample_products() -> None:
    """상품 전체 조회가 현재 서비스의 샘플 상품 세 개를 반환하는지 확인합니다."""

    response = client.get("/product/get_all")

    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "Sample Product", "price": 100},
        {"id": 2, "name": "Sample Product 2", "price": 200},
        {"id": 3, "name": "Sample Product 3", "price": 300},
    ]


def test_create_product_rejects_invalid_body() -> None:
    """상품 필수 필드가 빠진 요청 본문을 거절하는지 확인합니다."""

    response = client.post(
        "/product/create",
        json={"name": "가격 없는 상품"},
    )

    assert response.status_code == 422


def test_get_product_rejects_non_integer_id() -> None:
    """정수가 아닌 상품 ID를 경로에 사용하면 요청을 거절하는지 확인합니다."""

    response = client.get("/product/get/not-a-number")

    assert response.status_code == 422
