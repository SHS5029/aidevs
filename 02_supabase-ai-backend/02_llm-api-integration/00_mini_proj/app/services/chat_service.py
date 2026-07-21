from app.schemas.ChatSchema import ChatRequest
import os
from google import genai
from app.schemas.ChatSchema import ChatResponse
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(".env"))

api_key = os.getenv("GEMINI_API_KEY")
model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")


# Google Gen AI SDK 클라이언트를 만듭니다.
# 여기서 api_key가 비어 있거나 잘못되어 있으면 실제 호출 시 오류가 날 수 있습니다.
client = genai.Client(api_key=api_key)

def call_gemini(chat_request: ChatRequest) -> ChatResponse:
    response = client.models.generate_content(
        model=model,
        contents=chat_request.prompt
    )
    return ChatResponse(user_id=chat_request.user_id, answer=response.text)