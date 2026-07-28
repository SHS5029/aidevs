#weather.py

import streamlit as st
import httpx

st.title("날씨 정보")  # Streamlit 화면의 가장 큰 제목을 표시합니다.

Base_URL = "https://api.open-meteo.com/v1/forecast"  # Open-Meteo API의 기본 URL을 설정합니다.
regions = {
    "서울": {"latitude": 37.57, "longitude": 126.98},
    "부산": {"latitude": 35.18, "longitude": 129.08},
    "제주": {"latitude": 33.50, "longitude": 126.53},
}
selected_region = st.selectbox("지역 선택", regions.keys())

st.info("날씨 정보를 가져오려면 아래 버튼을 클릭하세요.")  # 사용자에게 안내 메시지를 표시합니다.

try:
    if st.button("날씨 정보 가져오기"):  # 버튼을 클릭하면 아래 코드 블록이 실행됩니다.
        with st.spinner("날씨 정보를 가져오는 중입니다..."):  # 날씨 정보를 가져오는 동안 로딩 메시지를 표시합니다.s
            params = {
                **regions[selected_region],
                "hourly": "temperature_2m",
            }
            response = httpx.get(Base_URL, params=params, timeout=5.0)  # Open-Meteo API에 GET 요청을 보내고 응답을 받습니다.
            if response.status_code == 200:  # HTTP 상태 코드가 200이면 정상 응답으로 처리합니다.
                data = response.json()  # JSON 응답을 딕셔너리로 변환합니다.
                st.success("날씨 정보를 성공적으로 가져왔습니다.")  # 성공 메시지를 표시합니다.
                st.json(data)  # 날씨 정보를 JSON 형식으로 화면에 표시합니다.
                weather_data = {
                    "시간": data["hourly"]["time"],
                    "온도(°C)": data["hourly"]["temperature_2m"],
                }
                st.dataframe(weather_data, use_container_width=True)  # 날씨 정보를 데이터프레임 형태로 화면에 표시합니다.
            else:  # HTTP 상태 코드가 200이 아닌 경우 오류 메시지를 표시합니다.
                st.error(f"날씨 정보 가져오기 실패: {response.status_code}")  # 오류 상황을 사용자에게 명확히 보여줍니다.
except httpx.RequestError as error:  # 요청 중 오류가 발생했을 때 사용자에게 안내 메시지를 표시합니다.
    st.error(f"요청 중 오류 발생: {error}")  # 오류 상황을 사용자에게 명확히 보여줍니다.
except httpx.HTTPStatusError as error:  # HTTP 상태 코드 오류가 발생했을 때 사용자에게 안내 메시지를 표시합니다.
    st.error(f"HTTP 상태 코드 오류 발생: {error}")  # 오류 상황을 사용자에게 명확히 보여줍니다.
except httpx.TimeoutException as error:  # 요청 시간 초과가 발생했을 때 사용자에게 안내 메시지를 표시합니다.
    st.error(f"요청 시간 초과: {error}")  # 오류 상황을 사용자에게 명확히 보여줍니다.
