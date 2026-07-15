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

