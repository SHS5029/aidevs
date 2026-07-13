student: dict[str, object] = {
    "name": "Jean",
    "ko": 95,
    "en": 80,
    "math": 90,
    "science": 80,
    "passed": True,
}

##Student의 점수 합과 평균을 구하고 "sum" "avg" 를 추가해서 출력하시오
total_sub_count = 0

for sub in student:
    if sub in ["ko", "en", "math", "science"]:
        total_sub_count += 1

print("과목 수:", total_sub_count)

sum_score = student["ko"] + student["en"] + student["math"] + student["science"]
avg_score = sum_score / total_sub_count


student["sum"] = sum_score
student["avg"] = avg_score


print("학생 정보:", student)
