#login.py

#임포트
import streamlit as st

#선언
loginout = st.query_params.get("loginout", "logout")  # URL 쿼리 파라미터에서 'loginout' 값을 가져옵니다. 없으면 빈 문자열을 기본값으로 사용합니다.

if "login" not in st.session_state:
    st.session_state.login = False

submitted = None  # 제출 버튼이 눌렸는지 여부를 저장하는 변수입니다.



#화면
if loginout == "logout": # 로그인 상태가 False일 때만 로그인 화면을 표시합니다.
    st.title("로그인")  # 로그인 화면의 가장 큰 제목을 표시합니다.
    with st.form("login_form"):  # form 영역 안의 입력값은 제출 버튼을 눌렀을 때 한 번에 처리됩니다.
        username = st.text_input("", key="username")  # 사용자가 입력한 이름을 문자열로 저장합니다.
        password = st.text_input("", key="password", type="password")  # 비밀번호 입력창을 생성하고, 입력값을 문자열로 저장합니다.
        submitted = st.form_submit_button("로그인")  # 제출 버튼을 누르면 submitted 값이 True가 됩니다.
        reset_button = st.form_submit_button("초기화")  # 초기화 버튼을 누르면 입력값이 초기화됩니다.
else:
    st.title("로그인 성공")  # 로그인 성공 화면의 가장 큰 제목을 표시합니다.
    st.success("로그인에 성공했습니다!")  # 로그인 성공 메시지를 초록색으로 표시합니다.
    if logout := st.button("로그아웃"):  # 로그아웃 버튼을 생성하고, 클릭 시 login 상태를 False로 변경합니다.
        st.session_state.login = False
        st.toast("로그아웃 되었습니다.")  # 로그아웃 메시지를 화면에 표시합니다.
        st.query_params["loginout"] = "logout"  # URL 쿼리 파라미터에 'loginout' 값을 설정합니다.
        st.rerun()


#코드

if reset_button:
    st.session_state.update({"username": "", "password": ""})
    st.toast("입력값이 초기화되었습니다.")  # 초기화 메시지를 화면에 표시합니다.
if submitted:  # 제출 버튼을 누른 뒤에만 로그인 결과를 화면에 표시합니다.
    if username == "admin" and password == "password":  # 사용자 이름과 비밀번호가 일치하는지 확인합니다.
        st.session_state.login = True  # 로그인 상태를 True로 설정합니다.
        st.query_params["loginout"] = "login"  # 로그인 성공 상태를 URL 쿼리 파라미터에 저장합니다.
        st.rerun()
    else:
        st.toast("사용자 이름 또는 비밀번호가 올바르지 않습니다.")  # 로그인 실패 메시지를 빨간색으로 표시합니다.
