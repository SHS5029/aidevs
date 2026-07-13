import sys

print("start...")

while True:
    print(" -- 메뉴 선택 --\n 1. 점수, 등급 계산" \
    "\n 2. 숫자 양수/0/음수 판별 \n 3. 사용자 역할 안내")

    cmd = input("메뉴 번호 입력: ")
   

    if(cmd == "1"):
        print("점수, 등급 계산 메뉴 선택")
        score = int(input("점수 입력: "))
        if(score >= 90):
            print("A 등급")
        elif(score >= 80):
            print("B 등급")
        elif(score >= 70):
            print("C 등급")
        else:
            print("D 등급")

    elif(cmd == "2"):
        print("숫자 양수/0/음수 판별 메뉴 선택")
        number = int(input("숫자 입력: "))
        if(number > 0):
            print("양수입니다.")
        elif(number == 0):
            print("0입니다.")
        else:
            print("음수입니다.")
    
    elif(cmd == "3"):
        print("사용자 역할 안내 메뉴 선택")
        role = input("admin, member, guest 중 하나 입력: ")

        match role:
            case "admin":
                print("관리자 역할을 선택했습니다")
            case "member":
                print("회원 역할을 선택했습니다")
            case "guest":
                print("손님 역할을 선택했습니다")
            case _:
                print("알 수 없는 역할입니다")

    elif(cmd == "q"):
        print("bye")
        break

    else:
        print("알 수 없는 메뉴입니다")
        print("프로그램을 종료합니다.")
        break
