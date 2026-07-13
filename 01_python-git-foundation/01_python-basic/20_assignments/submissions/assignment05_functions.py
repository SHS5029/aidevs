students = [
    {"name": "Jean", "score": 95,},
    {"name": "Mina", "score": 82,},
    {"name": "Jun", "score": 58,},
    {"name": "Alice", "score": 80,},
    {"name": "Bob", "score": 90,},
    {"name": "Charlie", "score": 70,},
]

def get_grade(score: int) -> str:
    """점수에 따라 등급을 반환하는 함수입니다.
    90점 이상: A
    80점 이상: B
    70점 이상: C
    60점 이상: D"""
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    else:
        return "D"
    

def is_passed(score: int) -> bool:
    return score >= 60

def calculate_average(scores: list[int]) -> float:
    total = sum(scores)
    return total / len(scores)

def filter_passed_students(students: list[dict[str, object]]) -> list[dict[str, object]]:
    passed_students = []
    for student in students:
        if is_passed(student["score"]):
            passed_students.append(student)
    return passed_students

def print_students(students: list[dict[str, object]]):
    for student in students:
        grade = get_grade(student["score"])
        passed = is_passed(student["score"])
        print(f"이름: {student['name']}, \n점수: {student['score']}, \n등급: {grade}"
              f"\n통과 여부: {passed}\n{'-'*40}")



print_students(students)

filtered_students = filter_passed_students(students)
print(f"통과 학생 명단: {filtered_students}")

def under_average_students(students: list[dict[str, object]]) -> list[dict[str, object]]:
    avg_score = calculate_average([student["score"] for student in students])
    return [student for student in students if student["score"] < avg_score]

print(f"평균 점수 미만 학생 명단: {under_average_students(students)}\n"
      f"평균점수: {calculate_average([student['score'] for student in students]):.2f}")