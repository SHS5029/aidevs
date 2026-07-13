import sys

while True:
    print("첫 번째 숫자 입력: ")
    num1 = input()

    if num1 == "q":
        print("프로그램을 종료합니다.")
        sys.exit()

    print("두 번째 숫자 입력: ")
    num2 = input()

    print("연산자 입력: ")
    opt = input()

    if opt == "-":
        print(f"{num1} - {num2} = {int(num1) - int(num2)}")
    elif opt == "+":
        print(f"{num1} + {num2} = {int(num1) + int(num2)}")
    elif opt == "*":
        print(f"{num1} * {num2} = {int(num1) * int(num2)}")
    elif opt == "/":
        if num2 == "0":
            print("0으로 나눌 수 없습니다.")
        else:
            print(f"{num1} / {num2} = {int(num1) / int(num2)}")
