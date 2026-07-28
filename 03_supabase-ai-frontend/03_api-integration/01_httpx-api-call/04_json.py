# 04_json.py
#https://jsonplaceholder.typicode.com/ 의 posts API를 호출하여 JSON 출력 userID, title, body
import httpx

API_URL = "https://jsonplaceholder.typicode.com/posts"

response = httpx.get(API_URL, timeout=5.0)  # GET 요청을 보내고 응답 객체를 response 변수에 저장합니다.

print("status code:", response.status_code)  # HTTP 요청이 성공했는지 확인할 수 있는 상태 코드를 출력합니다.
result = response.json()

print(result[29]["userId"], result[19]["title"], result[76]["body"])  # JSON 응답 내용을 출력합니다.