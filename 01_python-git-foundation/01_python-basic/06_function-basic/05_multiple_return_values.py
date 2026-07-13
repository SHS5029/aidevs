"""여러 값을 반환하는 함수 예제입니다.

Python 함수는 여러 값을 한 번에 반환할 수 있습니다.
실제로는 tuple 형태로 반환되고, 이를 여러 변수에 나누어 받을 수 있습니다.
"""


def calculate(a, b):
    add_result = a + b
    subtract_result = a - b
    multiply_result = a * b
    divide_result = a / b

    return add_result, subtract_result, multiply_result, divide_result

results: tuple[float, float, float, float] = calculate(10, 2)
for result in results:
    print(result)

#tuple unpacking을 사용하면 반환값을 여러 변수에 나누어 담을 수 있습니다.
plus, minus, multiply, divide = calculate(10, 2)

print("더하기:", plus)
print("빼기:", minus)
print("곱하기:", multiply)
print("나누기:", divide)


def get_min_max(numbers: list[float]) -> tuple[float, float]:
    smallest = min(numbers)
    largest = max(numbers)
    return smallest, largest


scores = [80, 95, 70, 88]
min_score, max_score = get_min_max(scores)

print("최저 점수:", min_score)
print("최고 점수:", max_score)

###########

print("----------------------------------------------------\n")

#숫자로 되어있는 리스트를 입력하면 가장 작은 값과 가장 큰 값, 합계, 평균을 반환하는 함수를 만들어보세요.
# dict로 반환하면 좋음
#함수명: maxmin_hamsu

datas: list[float] = [10, 30, 40, 10, 20, 50, 60]

def maxmin_hamsu(numbers: list[float]) -> dict[str, float]:
    smallest = min(numbers)
    largest = max(numbers)
    total = sum(numbers)
    average = total / len(numbers)
    return {
        "min": smallest,
        "max": largest,
        "sum": total,
        "avg": average
    }

result = maxmin_hamsu(datas)
print(f"최소: {result['min']}")
print(f"최대: {result['max']}")
print(f"합계: {result['sum']}")
print(f"평균: {result['avg']}")