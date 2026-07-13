r"""타입 힌트 기초 예제입니다.

실행:
    cd C:\aidev\01_python-git-foundation
    .\.venv\Scripts\Activate.ps1
    python .\01_python-basic\02_variables-and-data-types\03_type_hint_basic.py

타입 힌트는 변수가 어떤 종류의 값을 사용할 예정인지 표시하는 문법입니다.
Python은 기본적으로 실행 중에 타입 힌트를 강제로 검사하지는 않습니다.
하지만 VS Code가 코드를 이해하고, 잘못된 값을 넣었을 때 미리 알려 주는 데 도움이 됩니다.

함수에 타입 힌트를 붙이는 방법은 나중에 06_function-basic에서 다시 다룹니다.
"""

# 타입 힌트를 붙인 변수 선언입니다.
# name: str = "kim"은 name 변수에 문자열(str)을 넣어 사용할 예정이라는 뜻입니다.
name: str = "kim"
age: int = 20
height: float = 175.5
is_student: bool = True

print("이름:", name)
print("나이:", age)
print("키:", height)
print("학생인가요?", is_student)


##

print(f"타입 힌트 예시: {name}, {age}, {is_student}")
print(type(name), type(age), type(is_student))

msg = "   1000   "
print(f"입력{msg}입니다.")
print(f"입력{msg.strip()}입니다.") # strip()은 문자열 양쪽 공백을 제거하는 함수입니다.

####

print("-------------------------------\n")

msg2: str = "12,000,000"

print(f"입력{msg2}입니다.")
num2 = int(msg2.replace(",", "")) # replace()는 문자열 안의 특정 문자를 다른 문자로 바꾸는 함수입니다.
print(f"입력{num2}입니다.")

## jmlee@tonesol.com 에서 id 변수에 jmlee 입력, domain 변수에 tonesol.com 입력, id + domain을 합쳐서 
## 이메일 주소를 출력하는 예제를 만들어 보세요.

data: str = "jmlee@tonesol.com"

id: str = "jmlee"
domain: str = "tonesol.com"

email:str = id + "@" + domain

print(f"이메일 주소: {email}")

print("data와 email이 같은가요?", data == email)

print("-------------------------------\n")

id: str = data[:data.index("@")]
domain: str = data[data.index("@") + 1:data.index(".")]
print(f"data에서 id: {id}, domain: {domain} 입니다")