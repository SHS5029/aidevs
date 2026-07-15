# 2026-07-14 Python 학습 일지

## 오늘의 학습 목표

오늘은 한 파일에 있던 기능을 별도 모듈과 패키지로 분리하고, 여러 종류의 예외를 직접 발생시키거나 처리하는 연습을 했다. 간단한 채팅 프로그램을 `main.py`, `models.py`, `services.py`로 나누면서 요청과 응답 데이터의 역할도 구분했다. 또한 Git과 GitHub에서 커밋, 푸시, 브랜치 생성 과정을 직접 실습해 로컬 작업을 원격 저장소에 공유하는 흐름을 익혔다.

## 1. 함수와 모듈 분리

`02_dict_parameter.py` 안에 있던 `build_chat_response()` 함수를 `my_team/llm.py`로 옮기고, 실행 파일에서는 `from my_team.llm import build_chat_response`로 불러오도록 변경했다. 함수의 정의와 실행 흐름을 분리하니 `02_dict_parameter.py`는 입력과 출력에 집중하고, 응답 생성 로직은 별도 모듈이 담당하게 되었다.

아래는 오늘 실제로 작성한 `my_team/llm.py`의 코드다.

```python
def build_chat_response(request_data: dict) -> dict:
    """질문 dict를 받아 응답 dict를 만듭니다.

    request_data 예시:
        {
            "user": "kim",
            "message": "FastAPI란?",
            "model": "practice-model"
        }
    """

    user = request_data.get("user", "anonymous")
    message = request_data.get("message", "").strip()
    model = request_data.get("model", "practice-model")

    return {
        "user": request_data.get("user", "anonymous"),
        "message": request_data.get("message", "").strip(),
        "model": request_data.get("model", "practice-model"),
        "answer": f"{user}님, '{message}'에 대한 연습용 답변입니다.",
    }
```

`dict.get()`을 사용하면 키가 없을 때 기본값을 지정할 수 있고, 문자열의 `strip()`으로 질문 앞뒤 공백을 제거할 수 있었다. 실행 파일에서는 사용자 입력으로 `request_data`를 만들고 이 함수를 호출한 뒤, 반환된 응답 dict의 `answer`를 출력했다.

## 2. 예외 발생과 처리

문자열을 정수로 바꿀 때의 `ValueError`를 실행해 보고, 0으로 나눌 때의 `ZeroDivisionError`, 파일이 없을 때의 `FileNotFoundError`, JSON 형식이 잘못됐을 때의 `json.JSONDecodeError`를 처리하는 코드도 작성했다. 예외마다 `except` 블록을 나누면 어떤 실패가 발생했는지 구체적으로 처리할 수 있다는 점을 배웠다. 현재 실행값인 `10 / 8`과 정상 `config.json`은 오류를 발생시키지 않으므로, 나머지 예외 경로는 0 또는 누락·손상된 파일을 입력해 추가로 실행할 필요가 있다.

빈 질문 처리에서는 `None`을 반환하는 방법과 `raise ValueError(...)`로 예외를 발생시키는 방법을 모두 비교했다. `None`을 반환하면 호출한 곳에서 매번 값의 존재 여부를 검사해야 하고, 예외를 발생시키면 정상 흐름과 오류 흐름을 `try/except`로 분리할 수 있다.

JSON 읽기 기능도 `my_package/file.py`로 분리했다. 아래 코드는 오늘 실제 작성한 파일 읽기 함수다.

```python
import json
from pathlib import Path


CURRENT_DIR = Path(__file__).parent


def read_json_safely(file_name: str) -> dict:
    """JSON 파일을 읽고 dict로 반환합니다.

    오류가 나면 프로그램을 바로 종료하지 않고 빈 dict를 반환합니다.
    """

    file_path = CURRENT_DIR / file_name
    try:
        text = file_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise FileNotFoundError(f"파일이 없습니다: {file_path}")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        raise json.JSONDecodeError(f"JSON 문법 오류: {file_path}", text, 0)
```

`Path(__file__).parent`를 사용하면 프로그램을 어느 위치에서 실행하더라도 모듈 파일을 기준으로 JSON 경로를 만들 수 있다. 파일 읽기와 JSON 변환을 두 단계로 나누면서 각 단계에서 발생하는 예외가 다르다는 것도 확인했다. 하위 함수에서 예외를 다시 발생시키고 `main.py`에서 처리하면, 파일 기능과 사용자 안내 기능의 역할을 나눌 수 있다.

## 3. 프로젝트 구조와 dataclass

간단한 채팅 프로젝트를 `main.py`, `app/models.py`, `app/services.py`로 나눴다. `main.py`는 입력과 출력, `models.py`는 데이터 모양, `services.py`는 답변 생성 로직을 맡도록 구성했다. 파일의 역할을 나누면 코드가 길어져도 기능의 위치를 찾기 쉽고, 모델이나 서비스만 따로 재사용하기도 쉬워진다.

두 번째 프로젝트에서는 요청과 응답을 서로 다른 dataclass로 표현했다. 아래는 `01_simple_chat_project2/app/models.py`에 실제 작성한 모델 코드 일부다.

```python
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
```

`RequestChatMessage`에는 질문, 사용자, 전송 방식을 담고 `ResponseChatMessage`에는 답변, 모델명, 상태 메시지를 담았다. 단순한 dict보다 어떤 값이 필요한지 클래스 정의에서 바로 확인할 수 있었고, 기본값을 사용하면 객체를 만들 때 반복해서 같은 값을 전달하지 않아도 되었다.

서비스 함수는 요청 객체를 받아 응답 객체를 반환하도록 작성했다. 아래는 실제 서비스 코드 중 import와 함수 정의 부분이다.

```python
from app.models import ResponseChatMessage, RequestChatMessage


def create_mock_answer(question: RequestChatMessage) -> ResponseChatMessage:
    """실제 AI API 대신 연습용 답변 문장을 만듭니다."""

    return ResponseChatMessage(
        answer=f"'{question.prompt}'에 대한 첫 번째 프로젝트 구조 연습 답변입니다.",
        model="practice-model",
    )


def create_chat_message(question: RequestChatMessage) -> ResponseChatMessage:
    """질문을 받아 ResponseChatMessage object를 만듭니다."""

    answer = create_mock_answer(question)

    return ResponseChatMessage(
        answer=answer.answer,
        model=answer.model,
        msg=answer.msg,
    )
```

입력과 출력의 타입을 구분하니 함수가 어떤 데이터를 받고 돌려주는지가 더 분명해졌다. `main.py`에서는 `while True`로 질문을 반복해서 받고, `q`를 입력하면 종료하며, `ConnectionError`가 발생하면 메시지를 출력한 뒤 다음 질문을 받도록 구성했다.

## 4. 반복문과 상태 변경 추가 연습

지폐와 지갑의 가로·세로 길이를 입력받아 지폐가 들어갈 때까지 반복해서 반으로 접는 코드도 작성했다. 입력 문자열을 `split(",")`로 나누고 `int()`로 변환해 list에 저장했으며, `while True`에서 크기를 비교하고 조건을 만족하면 `break`로 종료했다.

이 실습을 통해 list의 값을 함수 안에서 변경하는 방식과 반복 횟수를 상태로 관리하는 방법을 확인했다. 다만 현재 `flip()`은 지폐의 두 길이를 동시에 절반으로 만들고 전역 변수 `answer`를 사용한다. 다음에는 실제 접기 규칙처럼 더 긴 변 하나만 선택해서 접고, 반복 횟수도 함수의 반환값으로 관리하는 방법을 연습할 필요가 있다.

## 5. Git과 GitHub 실습

오늘은 메인 저장소와 팀 실습 저장소에서 커밋과 푸시를 연습했다. 메인 저장소에서는 `32b6c34`와 `bbb72cd` 커밋을 만들고 `origin/main`으로 푸시했다. 현재 로컬 `main`과 `origin/main`의 차이가 `0 / 0`이므로 두 저장소가 같은 커밋을 가리키는 것도 확인했다.

`teamtest` 저장소에서는 `main`에서 `SHS` 브랜치를 생성하고 이동한 뒤, 먼저 `origin/SHS` 원격 브랜치를 만들었다. 이후 `01_simple_chat_project2/shs.py`를 추가하고 `0714_hwanseok_test`라는 메시지로 `c77f7b5` 커밋을 만든 다음 다시 푸시했다. 로컬 `SHS`와 원격 `origin/SHS`가 같은 커밋을 가리키므로 브랜치 푸시가 완료된 상태다.

Git 기록에서 확인한 순서를 재현 가능한 명령어로 정리하면 다음과 같다.

```bash
git switch -c SHS
git push -u origin SHS
git add 01_simple_chat_project2/shs.py
git commit -m "0714_hwanseok_test"
git push
git status -sb
```

- 브랜치는 기존 작업과 분리된 공간에서 변경할 수 있게 한다.
- 커밋은 스테이징한 변경사항을 하나의 기록으로 남긴다.
- 푸시는 로컬 커밋을 GitHub의 원격 저장소로 보낸다.
- `-u` 옵션으로 upstream을 연결하면 이후에는 `git push`와 `git pull`을 간단히 사용할 수 있다.
- `git status -sb`와 `git branch -vv`로 현재 브랜치와 원격 추적 상태를 확인할 수 있다.

## 미커밋 변경사항에서 확인한 시행착오와 보완할 점

- `validate_question()`은 타입 힌트가 `-> str`인데 빈 질문에서 `None`을 반환한다. `None` 방식을 유지한다면 `-> str | None`으로 표시하고, 예외 방식을 사용한다면 모든 오류 흐름을 `raise ValueError(...)`로 통일해야 한다.
- `None` 비교에는 `cleaned_question == None`보다 `cleaned_question is None`을 사용하는 것이 의도를 더 분명하게 나타낸다.
- `to_int_or_default()` 안에서 `default = 0`으로 다시 대입하면 호출할 때 전달한 기본값이 무시된다. 매개변수를 그대로 사용해야 함수의 이름과 동작이 일치한다.
- `devided()`는 `divide()`처럼 의미가 맞는 이름으로 고치고, 매개변수 타입 힌트의 공백도 Python 스타일에 맞게 정리할 필요가 있다.
- `02_raise_validation_ok.py`에서는 예외가 발생한 뒤에도 `cleaned_question`을 출력한다. 현재 입력 순서에서는 이전 반복의 정상 질문이 빈 질문의 결과처럼 다시 출력되고, 첫 입력부터 예외가 나면 변수가 없어 오류가 발생할 수 있으므로 `except` 처리 후 `continue`가 필요하다.
- `read_json_safely()`의 현재 동작은 빈 dict를 반환하지 않고 예외를 다시 발생시키므로, docstring도 실제 동작에 맞게 수정해야 한다.
- `01_simple_chat_project2`의 `main.py`는 `ConnectionError`를 처리하지만 현재 서비스 함수는 이 예외를 발생시키지 않는다. 오류 처리 경로를 연습하려면 예외가 실제로 발생하는 입력이나 테스트가 필요하다.
- 새 프로젝트의 README에는 이전 폴더명과 아직 존재하지 않는 테스트 경로가 남아 있다. 프로젝트 구조를 바꿀 때 설명 문서와 실행 명령도 함께 갱신해야 한다.
- 실습 과정에서 생성된 `__pycache__`와 `.pyc` 파일은 소스 코드가 아니며, 현재 `.gitignore` 규칙으로 Git에서 제외되고 있음을 확인했다.
- 기존 `01_simple_chat_project`는 삭제되고 `01_simple_chat_project1`, `01_simple_chat_project2`가 새로 생긴 상태다. 커밋 전 `git status`와 `git diff --stat`로 의도한 이름 변경과 복사인지 다시 확인해야 한다.

## 오늘의 회고

오늘은 함수 하나를 작성하는 연습에서 한 단계 더 나아가, 기능을 모듈과 패키지로 나누고 요청·응답 데이터를 dataclass로 표현했다. 예외를 어디에서 발생시키고 어디에서 처리할지에 따라 파일의 역할이 달라진다는 점도 이해했다. 또한 브랜치 생성, 커밋, 푸시를 직접 진행하면서 코드 작성과 버전 관리가 하나의 개발 흐름으로 연결된다는 것을 확인했다.

다음 실습에서는 현재 발견한 타입 힌트와 예외 흐름의 불일치를 수정하고, 각 서비스 함수에 대한 테스트를 추가해 정상 입력과 오류 입력을 모두 확인해 보고 싶다.
