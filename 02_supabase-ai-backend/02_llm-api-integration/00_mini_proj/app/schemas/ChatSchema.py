## 채팅 요청 스키마

from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    """
    채팅 요청 스키마
    """
    user_id: str = Field(..., min_length=1, description="사용자 ID")
    prompt: str = Field(..., min_length=1, description="사용자 입력 메시지")

class ChatResponse(BaseModel):
    """
    채팅 응답 스키마
    """
    user_id: str = Field(..., min_length=1, description="사용자 ID")
    answer: str = Field(..., min_length=1, description="모델 응답 메시지")