numbers: list[int] = [1, 2, 3, 4, 5]

#출력

# 마지막에 6을 추가
numbers.append(6)

# 전체 합과 평균을 출력

total = sum(numbers)
average = total / len(numbers)

print("합계:", total)
print("평균:", average)


#for 문 사용

for number in numbers:
    print(number)

sum_numbers = 0
avg_numbers = 0

for number in numbers:
    sum_numbers += number

print("합계(for):", sum_numbers)
print(f"평균(for): {sum_numbers / len(numbers)}")

### 전체 합과 평균을 출력 단, 짝수만 합과 평균을 구할 것

num_sum = 0
jjaksoo_count = 0

for number in numbers:
    if number %2 ==0:
        num_sum += number
        jjaksoo_count += 1

print("짝수 합계:", num_sum)
print(f"짝수 평균: {num_sum / jjaksoo_count}")