"""Chat 탭입니다."""

import streamlit as st
import httpx


from frontend_common import require_login

API_BASE_URL = "https://render-page-01.onrender.com/docs"  # 프론트엔드가 호출할 백엔드 서버의 기본 주소를 한 곳에서 관리합니다.

def render_chat_tab() -> None:
    """로그인 후 mock 대화를 입력하고 누적 표시합니다."""

    st.subheader("Chat")
    st.caption("로그인 후 mock 대화를 입력하고 누적 표시합니다.")

    with st.form("chat_form", clear_on_submit=True):
        message = st.text_input("메시지 입력", placeholder="오늘 배운 내용을 정리해줘.")
        submitted = st.form_submit_button("전송")
        payload = {"user_id": "id01", "prompt": message}

    if submitted:
        message = message.strip()
        payload = {"user_id": "id01", "prompt": message}
        with st.spinner("메시지를 전송 중입니다..."):
            response = httpx.post(f"{API_BASE_URL}chat", json=payload, timeout=15.0)


        if not message:
            st.warning("메시지를 입력하세요.")
        else:
            st.info(f"전송된 메시지: {message}")
            message = message.strip()
            payload = {"user_id": "id01", "prompt": message}
            with st.spinner("메시지를 전송 중입니다..."):
                response = httpx.post(f"{API_BASE_URL}chat", json=payload, timeout=15.0)
            if response.status_code == 200:
                result = response.json()
                st.success(f"응답 메시지: {result.get('response', '')}")
            else:
                st.error(f"메시지 전송 실패: {response.status_code} - {response.text}")
