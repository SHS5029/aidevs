"""for 반복문 예제입니다.

반복문은 같은 형태의 작업을 여러 번 실행할 때 사용합니다.
`for` 반복문은 리스트, 문자열, range 같은 값을 하나씩 꺼내며 실행합니다.
"""





## 1~5 까지의 합과 평균을 구하시오

datas: list = [1,2,3,4,5,6,7,8,9,10]

print(type(datas))

total_number:int = 0
print(total_number)

print(sum(datas))

for data in datas:
    total_number += data
print(total_number)

print(f"avg= {total_number / len(datas)}")

print("------------------\n")

for data in datas:
    total_number += data
print(total_number)