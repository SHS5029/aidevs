import httpx  # FastAPI 같은 백엔드 API에 HTTP 요청을 보내기 위해 httpx 클라이언트를 가져옵니다.
import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.

API_URL = "http://192.100.200.72:8000/health"  # 호출할 백엔드 health check API 주소입니다.

st.title("백엔드 Health Check")

if st.button("서버 상태 확인", key="health_check_button"):
    try:
        response = httpx.get(API_URL, timeout=5.0)  # GET 요청을 보내고 응답 객체를 response 변수에 저장합니다.
        result = response.json()

        if response.status_code == 200 and result.get("status") == "ok":
            st.success("백엔드 서버가 정상 실행 중입니다.")
        else:
            st.error("백엔드 서버 상태가 정상이 아닙니다.")

        st.json(result)
    except (httpx.HTTPError, ValueError) as error:
        st.error(f"백엔드 서버에 연결할 수 없습니다: {error}")
