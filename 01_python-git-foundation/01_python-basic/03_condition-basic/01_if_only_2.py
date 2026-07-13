## 숫자를 입력받는다
## 숫자가 아니면 프로그램 종료
## 숫자이면 출력

import sys

num1 = input("숫자를 입력하세요:")

if num1.lstrip("+-").isdigit():
    num1 = int(num1)
    print(num1)
else:
    print("숫자로 입력하세요")