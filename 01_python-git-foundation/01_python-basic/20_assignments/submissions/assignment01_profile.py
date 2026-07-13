print("start")

name: str = input("1. 이름을 입력받습니다.: ")
age: int = int(input("2. 나이를 입력받습니다.: "))
skill: str = input("3. 관심 있는 기술을 입력 받습니다.: ")
study_time: float = float(input("4. 하루 공부 가능 시간을 입력 받습니다.: "))

type_hint_example: str = f"타입 힌트 예시: {name}, {age}, {skill}, {study_time}"

print(type_hint_example)

print(f"이름은 {name}이고," 
      f"나이는 {age}살이며, 관심 있는 기술은 {skill}입니다."
      f"하루 공부 가능 시간은 {study_time}시간입니다.")

print("end")