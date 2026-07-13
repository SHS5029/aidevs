#놀이기구 리스트
attraction = ["롤러코스터", "관람차", "어린이 기차"]

#고객 정보
name = input("이름을 입력하세요: ")
print(f"입력된 이름은 {name} 입니다.")
age = int(input("나이를 입력하세요: "))
print(f"입력된 나이는 {age} 입니다.")
height = float(input("키를 입력하세요(cm): "))
print(f"입력된 키는 {height}cm 입니다.")


#나이 판별
if age < 12:
    print(f"{name}님은 {age}세로 어린이에 해당합니다.")

elif age < 18:
    print(f"{name}님은 {age}세로 청소년에 해당합니다.")
else:
    print(f"{name}님은 {age}세로 성인에 해당합니다.")


print("------------------\n")
print("탑승할 놀이기구를 선택하세요 (번호를 입력하세요): ")

for i, item in enumerate(attraction):
    print(f"{i+1}. {item}")

number = int(input())

#번호에 따른 놀이기구 탑승 가능여부 확인
while True:
    match number:
        case 1:
            if age >= 12 and height >= 140:
                print(f"{name}님은 {attraction[0]}에 탑승 가능합니다.")
            else:
                print(f"{name}님은 {attraction[0]}에 탑승 불가능합니다. (나이: {age}, 키: {height}cm)")
            break
        case 2:
            if age >= 8 and height >= 120:
                print(f"{name}님은 {attraction[1]}에 탑승 가능합니다.")
            else:       
                print(f"{name}님은 {attraction[1]}에 탑승 불가능합니다. (나이: {age}, 키: {height}cm)")
            break
        case 3:
            if age >= 3 and height >= 90:
                print(f"{name}님은 {attraction[2]}에 탑승 가능합니다.")
            else:
                print(f"{name}님은 {attraction[2]}에 탑승 불가능합니다. (나이: {age}, 키: {height}cm)")
            break
        case _:
            print("잘못된 번호입니다. 1~3 사이의 번호를 입력하세요.")
            number = int(input())