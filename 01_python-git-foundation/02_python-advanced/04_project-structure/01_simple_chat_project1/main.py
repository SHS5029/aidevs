r"""01_simple_chat_project의 실행 시작점입니다.

실행 위치:
    C:\aidev\01_python-git-foundation

실행 명령:
    python .\02_python-advanced\04_project-structure\01_simple_chat_project2\main.py

이 파일의 역할:
    1. 예제 질문을 준비합니다.
    2. services.py의 함수로 질문과 답변 데이터를 만듭니다.
    3. 만들어진 결과를 화면에 출력합니다.

중요:
    이 예제는 프로젝트 구조를 익히기 위한 첫 단계입니다.
    그래서 JSON 저장, 빈 질문 검증, 예외 처리는 아직 넣지 않습니다.
"""

from app.services import create_chat_message


def main() -> None:
    while True:
        question = input("질문하세요: ")
        if question == "q":
            print("종료합니다.")
            break
        print(f"질문:{question}")
        print("처리중,,,,")
        try:
            message = create_chat_message(question)
            print(f"답변: {message.answer}  {message.model} {message.msg}")
            print()
        except ConnectionError as e:
            print(f"네트워크 에러 발생: {e}")
            continue

main()