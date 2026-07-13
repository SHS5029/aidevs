#리스트생성

students: list[dict[str, object]] = [
    {"name": "Jean", "score": 95, "tags": ["python", "backend"]},
    {"name": "Mina", "score": 82, "tags": ["python", "ui"]},
    {"name": "Jun", "score": 58, "tags": ["python", "backend"]},
    {"name": "Alice", "score": 80, "tags": ["python", "backend"]},
]

#학생들 이름 점수 출력
upper_60_students: list[dict[str, object]] = []
for stu in students:
    print(f"이름: {stu['name']}, 점수: {stu['score']}")
    if stu["score"] >= 60:
        print(f"이름: {stu['name']} 60점 이상 명단에추가")
        upper_60_students.append(stu)

print(f"60점 이상 학생 명단: {upper_60_students}")
avg_score = sum(stu["score"] for stu in students) / len(students)

print(f"avg_score: {avg_score}")


#중복태그제거
tags: set[str] = set()
for stu in students:
    tags.update(stu["tags"])
print(f"모든 중복제거 태그: {tags}")