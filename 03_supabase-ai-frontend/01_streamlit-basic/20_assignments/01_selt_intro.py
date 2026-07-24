from html import escape
from pathlib import Path

import streamlit as st

input_text = st.text_input("이름을 입력하세요", "홍길동")

input_job = st.text_input("직업을 입력하세요", "학생")

input_self_intro = st.text_area("자기소개를 입력하세요", "안녕하세요, 저는 홍길동입니다.")

submitted = st.button("제출")


##~~~~

if submitted:
    if input_text and input_job and input_self_intro:
        safe_name = escape(input_text)
        safe_job = escape(input_job)
        safe_intro = escape(input_self_intro).replace("\n", "<br>")

        st.markdown(
            f"""
            <style>
                .profile-card {{
                    max-width: 560px;
                    margin: 1.5rem auto;
                    padding: 2rem;
                    border: 1px solid rgba(99, 102, 241, 0.18);
                    border-radius: 24px;
                    background:
                        radial-gradient(circle at top right, rgba(129, 140, 248, 0.24), transparent 38%),
                        linear-gradient(145deg, #ffffff 0%, #f8f7ff 100%);
                    box-shadow: 0 18px 45px rgba(67, 56, 202, 0.12);
                    color: #1f2937;
                }}
                .profile-card__badge {{
                    display: inline-block;
                    margin-bottom: 1rem;
                    padding: 0.35rem 0.75rem;
                    border-radius: 999px;
                    background: #ede9fe;
                    color: #6d28d9;
                    font-size: 0.8rem;
                    font-weight: 700;
                    letter-spacing: 0.04em;
                }}
                .profile-card__name {{
                    margin: 0;
                    color: #111827;
                    font-size: 2rem;
                    line-height: 1.2;
                }}
                .profile-card__job {{
                    margin: 0.45rem 0 1.25rem;
                    color: #6366f1;
                    font-size: 1rem;
                    font-weight: 700;
                }}
                .profile-card__divider {{
                    height: 1px;
                    margin-bottom: 1.25rem;
                    background: linear-gradient(90deg, #a5b4fc, transparent);
                }}
                .profile-card__intro {{
                    margin: 0;
                    color: #4b5563;
                    font-size: 1rem;
                    line-height: 1.8;
                }}
            </style>

            <div class="profile-card">
                <span class="profile-card__badge">ABOUT ME</span>
                <h2 class="profile-card__name">{safe_name}</h2>
                <p class="profile-card__job">{safe_job}</p>
                <div class="profile-card__divider"></div>
                <p class="profile-card__intro">{safe_intro}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.success("제출이 완료되었습니다!")
    else:
        st.error("모든 필드를 입력해주세요.")
