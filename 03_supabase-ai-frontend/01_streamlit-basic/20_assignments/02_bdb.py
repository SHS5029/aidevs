
from pathlib import Path
import tomllib
import yfinance as yf

import streamlit as st
THEME_FILE = Path(__file__).parent / ".streamlit" / "themes.toml"

st.set_page_config(page_title="기본 대시보드", page_icon="📊", layout="wide")


def load_themes():
    with THEME_FILE.open("rb") as file:
        return tomllib.load(file)


def select_theme():
    themes = load_themes()

    selected_theme = st.sidebar.selectbox(
        "화면 모드",
        ["☀️ 라이트", "🌙 다크"],
    )

    theme_name = "dark" if selected_theme == "🌙 다크" else "light"
    return themes[theme_name]

select_theme()
load_themes()

tab_mainpage, tab_memo, tab_image, tab_stock = st.tabs(["메인페이지", "메모", "이미지", "주식"])  # 탭 이름을 순서대로 지정합니다.

with tab_mainpage:
    st.title("Dashboard 예제 메인페이지")
    left_col, right_col = st.columns(2)
    with left_col:
        st.header("이름 입력 영역")
        name = st.text_input("이름")

    with right_col:
        st.header("결과 영역")
        if name:
            st.write(f"{name}님, 환영합니다.")
        else:
            st.write("왼쪽에서 이름을 입력하세요.")


with tab_memo:
    st.title("Dashboard 예제 메모페이지")
    st.header("메모")
    memo = st.text_area("메모를 입력하세요")
    st.write("입력한 메모:", memo)

with tab_image:
    st.title("Dashboard 예제 이미지페이지")
    st.header("이미지")
    image_path = Path(__file__).resolve().parent.parent / "imgs" / "springai.png"
    if image_path.exists():
        st.image(
            image_path,
            caption="imgs 폴더의 springai.png 이미지입니다.",
            use_container_width=True,
        )
    else:
        st.warning(f"이미지를 찾을 수 없습니다: {image_path}")

with tab_stock:
    st.title("Dashboard 예제 주식페이지")
    st.header("주식 정보")
    st.write("주식 정보를 여기에 표시합니다.")
    ticker = st.text_input("주식 티커를 입력하세요", "AAPL")
    if ticker:
        stock_data = yf.Ticker(ticker)
        stock_history = stock_data.history(period="1mo")
        stock_info = stock_data.insider_purchases
        st.write("Insider Purchases:", stock_info)

        if not stock_history.empty:
            st.line_chart(stock_history["Close"])
        else:
            st.warning("주식 데이터를 찾을 수 없습니다.")
