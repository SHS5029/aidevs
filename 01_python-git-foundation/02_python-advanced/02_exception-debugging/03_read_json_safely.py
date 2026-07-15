r"""JSON 파일을 안전하게 읽는 예제입니다.

실행 위치:
    C:\aidev\01_python-git-foundation

실행 명령:
    python .\02_python-advanced\02_exception-debugging\03_read_json_safely.py

이 예제의 목표:
    1. JSON 파일을 읽습니다.
    2. 파일이 없을 때의 오류를 처리합니다.
    3. JSON 문법이 깨졌을 때의 오류를 처리합니다.
"""
import json
from my_package.file import read_json_safely

def main() -> None:

    try:
        file = read_json_safely("config.json") #에러 확인용
        print(file)     ## try 블록 안에서 정상적으로 읽은 경우에 여기서 끝나고 하단 코드는 실행X
    except FileNotFoundError as e:
        print("오류 발생:", e)
    except json.JSONDecodeError as e:
        print("오류 발생:", e)
    

main()