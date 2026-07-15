"""데이터 모양을 정의하는 파일입니다.

이 예제에서는 질문과 답변 하나를 ChatMessage라는 dataclass object로 표현합니다.

초보자는 dataclass를 아래처럼 이해하면 됩니다.

dict:
    {"question": "...", "answer": "..."}처럼 key/value로 데이터를 담습니다.

dataclass:
    ChatMessage(question="...", answer="...", model="...")처럼
    어떤 값이 필요한지 코드에서 더 분명하게 보여 줍니다.
"""

from dataclasses import dataclass



@dataclass
class ResponseChatMessage:
    """LLM을 통해 질문의 답변을 응답 합니다.
    응답, 상태메시지, 모델명을 전송합니다.
    """

    answer: str
    model: str
    msg: str = "OK"

@dataclass
class RequestChatMessage:
    """LLM에 질문을 전송합니다.
    질문(prompt), 사용자(user), 전송 방식을 전송합니다.
    """

    prompt: str
    user: str
    method: str = "온화하게"
