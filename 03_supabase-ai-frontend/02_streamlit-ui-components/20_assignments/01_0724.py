##로그인화면~~~로그인시 다양한 컴포넌트를 활용해 설문 작성 후 제출

#순서 1. 로그인화면 2. 설문화면 3. 설문 결과, 완료화면

import streamlit as st
from streamlit_session_browser_storage import SessionStorage
storage = SessionStorage()
loginout = storage.getItem("loginout")

if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False
if "input_login_id" not in st.session_state:
    st.session_state.input_login_id = ""

if "input_login_pwd" not in st.session_state:
    st.session_state.input_login_pwd = ""

if "display_state" not in st.session_state:
    st.session_state.display_state = "survey"

submitted = False  # 설문 제출 여부를 추적하는 변수입니다.

if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False
if "input_login_id" not in st.session_state:
    st.session_state.input_login_id = ""

if "input_login_pwd" not in st.session_state:
    st.session_state.input_login_pwd = ""

def reset():
    st.session_state.input_login_id = ""
    st.session_state.input_login_pwd = ""

def load_survey_form():
    st.title("간단 설문 폼")

    with st.form("survey_form"):
        name = st.text_input("이름")
        topic = st.selectbox(
            "가장 어려웠던 주제",
            ["실행", "입력", "레이아웃", "표", "차트"],
        )
        satisfaction = st.slider(
            "수업 만족도",
            min_value=1,
            max_value=5,
            value=3,
        )
        comment = st.text_area("추가 의견")

        submitted = st.form_submit_button("설문 제출")

    # with st.form 밖에서 처리
    if submitted:
        st.session_state.saved_data = {
            "name": name,
            "topic": topic,
            "satisfaction": satisfaction,
            "comment": comment,
        }
        st.session_state.display_state = "result"
        st.rerun()

def load_survey_result():
    result = st.session_state.saved_data

    st.title("설문 결과")
    st.write(f"이름: {result['name'] or '미입력'}")
    st.write(f"어려웠던 주제: {result['topic']}")
    st.write(f"만족도: {result['satisfaction']}")

    if result["comment"]:
        st.caption(result["comment"])
    else:
        st.info("추가 의견이 없습니다.")

    if st.button("설문 다시 작성"):
        st.session_state.display_state = "survey"
        st.rerun()

if loginout == "logout":
    
    st.title("LOGIN")
    with st.form("login_form"):
        input_id = st.text_input("ID입력", key="input_login_id")
        input_pwd = st.text_input("PWD입력",type="password", key="input_login_pwd")

        submit_area , reset_area = st.columns(2)
        with submit_area:
            login_submit = st.form_submit_button("LOGIN")
        with reset_area:
            reset_submit = st.form_submit_button("RESET", on_click=reset)

        if login_submit:
            if input_id == "id01" and input_pwd == "pwd01":
               storage.setItem("loginout", "login")
            else:
                st.toast("로그인 실패")
else:
    st.info("로그인 했습니다.")
    logout = st.button("LOGOUT")

    # 화면을 그리기 전에 로그아웃부터 처리
    if logout:
        storage.setItem("loginout", "logout")
        st.session_state.display_state = "survey"
        st.stop()

    if st.session_state.display_state == "survey":
        load_survey_form()
    elif st.session_state.display_state == "result":
        load_survey_result()