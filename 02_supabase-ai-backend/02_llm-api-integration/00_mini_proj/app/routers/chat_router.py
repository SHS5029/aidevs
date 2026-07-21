from fastapi import APIRouter, HTTPException, status
from app.schemas.ChatSchema import ChatResponse, ChatRequest
import os
from google import genai
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(".env"))

chat_router = APIRouter()

@chat_router.get("/health")
def health_check() -> dict[str, str]:
    """서버 상태 확인 응답을 반환합니다."""

    return {"status": "ok"}


@chat_router.post("/chat/gemini")
def chat_gemini(request: ChatRequest) -> ChatResponse:
    """Gemini 모델과 상호작용하는 채팅 엔드포인트입니다."""

    api_key = os.getenv("GEMINI_API_KEY")
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=model,
        contents=[
            {
                "role": "user",
                "parts": [{"text": request.prompt}],
            }
        ],
    )

    return ChatResponse(user_id=request.user_id, answer=response.text)
