num1, num2 = 1,2
total = num1 + num2
avg = total / 2
print(f"합계: {total}, 평균: {avg:.2f}")

num3, num4 = 3, 4
total = num3 + num4
avg = total / 2
print(f"합계: {total}, 평균: {avg:.2f}")


print("###########################################################\n")

def add_numvers(num1, num2):
    total = num1 + num2
    return total



total_1_2 = add_numvers(1, 2)
avg_1_2 = total_1_2 / 2
print(f"합계: {total_1_2}, 평균: {avg_1_2:.2f}")

total_3_4 = add_numvers(3, 4)
avg_3_4 = total_3_4 / 2
print(f"합계: {total_3_4}, 평균: {avg_3_4:.2f}")

print("###########################################################\n")
print("###########################################################\n")

#datas1, datas2라는 리스트를 입력하면 합계와 평균을 구해라
datas1 = [1, 2, 3, 4, 5]
datas2 = [6, 7, 8, 9, 10]

def cal_sum_avg(numbers: list[float]) -> tuple[float, float]:
    """리스트를 입력하면 합계와 평균을 반환하는 함수입니다."""
    total = sum(numbers)
    avg = total / len(numbers)
    return total, avg


avg_datas1 = sum(datas1) / len(datas1)
print(f"datas1 합계: {sum(datas1)}, 평균: {avg_datas1:.2f}")
avg_datas2 = sum(datas2) / len(datas2)
print(f"datas2 합계: {sum(datas2)}, 평균: {avg_datas2:.2f}")

print("----------------------------------------------------\n")

cal_sum_avg_datas1 = cal_sum_avg(datas1)
print(f"datas1 합계: {cal_sum_avg_datas1[0]}, 평균: {cal_sum_avg_datas1[1]:.2f}")
cal_sum_avg_datas2 = cal_sum_avg(datas2)
print(f"datas2 합계: {cal_sum_avg_datas2[0]}, 평균: {cal_sum_avg_datas2[1]:.2f}")


#각 데이터의 평균보다 큰 수를 리턴하는 함수 구현
def more_than_avg(numbers: list[float]) -> tuple[float]:
    """리스트를 입력하면 평균보다 큰 수를 반환하는 함수입니다."""
    total, avg = cal_sum_avg(numbers) #평균구함 
    result = [] #임시 리스트 result[] 를 만든다. 튜플은 값 변경이 불가능하기 때문에
    for number in numbers:
        if number > avg:
            result.append(number)
    return tuple(result) #요구사항대로 튜플로 변경해서 리턴

more_than_avg_datas1 = more_than_avg(datas1)
print(f"datas1 평균보다 큰 수: {more_than_avg_datas1}")
more_than_avg_datas2 = more_than_avg(datas2)
print(f"datas2 평균보다 큰 수: {more_than_avg_datas2}")

bigdata: tuple = more_than_avg(datas2)
print(bigdata)


