student: list[dict[str, object]] = [
    {
        "name": "Jean",
        "score": 95,
    },
    {
        "name": "Alice",
        "score": 80,
    },
    {
        "name": "Bob",
        "score": 90,
    },
]

# 학생들 정보를 출력한다.
for stu in student:
    print(f"이름: {stu['name']}, \n점수: {stu['score']}"
          "\n--------------------")


#학생들의 성적의 합과 평균을 출력하세요
total_score = 0

for stu in student:
    total_score += stu["score"]
avg_score = total_score / len(student)

print(f"합: {total_score}, \n평균: {avg_score:.2f}")