import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.

st.title("간단 설문 폼")  # Streamlit 화면의 가장 큰 제목을 표시합니다.

with st.form("survey_form"):  # form 영역 안의 입력값은 제출 버튼을 눌렀을 때 한 번에 처리됩니다.
    name = st.text_input("이름")  # 사용자가 입력한 이름을 문자열로 저장합니다.
    topic = st.selectbox("가장 어려웠던 주제", ["실행", "입력", "레이아웃", "표", "차트"])  # 목록 중 하나를 선택해 topic 변수에 저장합니다.
    satisfaction = st.slider("수업 만족도", min_value=1, max_value=5, value=3)  # 1부터 5 사이의 만족도 점수를 숫자로 저장합니다.
    comment = st.text_area("추가 의견")  # 여러 줄 입력창에 작성한 의견을 문자열로 저장합니다.

    number_input = st.number_input("설문 참여자 수", min_value=0, value=0, step=1)
    email_input = st.text_input("설문 참여자 이메일", placeholder="이메일을 입력하세요")
    comment_input = st.text_area("설문 참여자 의견", placeholder="의견을 입력하세요")
    satisfaction_input = st.selectbox("설문 참여자 만족도", ["매우 불만족", "불만족", "보통", "만족", "매우 만족"])
    interest_input = st.multiselect("설문 참여자 관심 분야", ["AI", "Backend", "Frontend", "Data"])
    consent_input = st.checkbox("설문 참여자 동의 여부", value=False)
    age_input = st.slider("설문 참여자 나이", min_value=0, max_value=100, value=25)

    submitted = st.form_submit_button("설문 제출")  # 제출 버튼을 누르면 submitted 값이 True가 됩니다.



if submitted:  # 제출 버튼을 누른 뒤에만 설문 결과를 화면에 표시합니다.
    with st.form("survey_result_form"):  # 결과 영역을 form으로 감싸서 제출 버튼을 눌러야 결과가 표시되도록 합니다.
        st.write("설문 결과")  # 결과 영역의 제목을 표시합니다.
        st.write(f"이름: {name if name else '미입력'}")  # 이름이 비어 있으면 '미입력'으로 표시합니다.
        st.write(f"어려웠던 주제: {topic}")  # 선택한 주제를 화면에 출력합니다.
        st.write(f"만족도: {satisfaction}")  # 슬라이더로 선택한 만족도 점수를 화면에 출력합니다.
        st.write(f"설문 참여자 수: {number_input}")
        st.write(f"설문 참여자 이메일: {email_input}")
        st.write(f"설문 참여자 의견: {comment_input}")
        st.write(f"설문 참여자 만족도: {satisfaction_input}")
        st.write(f"설문 참여자 관심 분야: {', '.join(interest_input)}") 
        st.write(f"설문 참여자 동의 여부: {'동의' if consent_input else '비동의'}")
        st.write(f"설문 참여자 나이: {age_input}")
        if comment:  # 추가 의견이 입력된 경우에만 의견 내용을 표시합니다.
            st.caption(comment)  # 보조 설명 형태로 추가 의견을 표시합니다.
        else:  # 아직 제출 버튼을 누르지 않은 상태라면 안내 메시지를 표시합니다.
            st.info("설문 내용을 입력한 뒤 '설문 제출' 버튼을 눌러 주세요.")
