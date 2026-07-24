#이미지 로딩, 여러가지 입력 창 만들고 마지막까지 입력하면 화면에 입력된 내용 출력

from pathlib import Path  
import streamlit as st  
from PIL import Image
import pandas as pd
import numpy as np
import yfinance as yf

st.title("이미지 출력 예제")  # Streamlit 화면의 가장 큰 제목을 표시합니다.

current_file = Path(__file__).resolve()

##이미지 입력

image_dir = current_file.parent.parent / "imgs"
image_files = list(image_dir.glob("*.png")) + list(image_dir.glob("*.jpg")) + list(image_dir.glob("*.jpeg"))


##텍스트 입력
text_input = st.text_input("텍스트를 입력하세요", "기본값")

##텍스트, 이미지 출력

if not image_files:  # 이미지 파일이 하나도 없으면, 화면에 오류 대신 안내 메시지를 보여 줍니다.
    st.warning(f"이미지 파일을 찾을 수 없습니다: {image_dir}")
    st.write("imgs 폴더에 png, jpg, jpeg 파일을 넣은 뒤 다시 실행해 보세요.")
else:
    # 이미지가 여러 개 있을 수도 있으므로 selectbox로 어떤 이미지를 보여 줄지 선택하게 합니다.
    selected_name = st.selectbox(
        "화면에 출력할 이미지를 선택하세요",
        [image_file.name for image_file in image_files],
    )

    # 사용자가 선택한 파일 이름과 일치하는 실제 이미지 경로를 찾습니다.
    selected_image = image_dir / selected_name

    st.caption(f"이미지 경로: {selected_image}")  # 현재 어떤 파일을 출력하는지 작은 설명으로 보여 줍니다.

    # st.image는 이미지 파일 경로, URL, 이미지 객체 등을 화면에 출력할 수 있습니다.
    # use_container_width=True를 사용하면 이미지가 화면 너비에 맞게 자연스럽게 조절됩니다.
    st.image(
        selected_image,
        caption=f"{selected_name} 파일을 Streamlit 화면에 출력했습니다.",
        use_container_width=True,
    )

    st.write(f"입력된 텍스트: {text_input}")
    st.write(f"입력된 텍스트: {text_input*299}")  # 사용자가 입력한 텍스트를 화면에 출력합니다.


uploaded_file = st.file_uploader(
    "이미지를 선택하세요",
    type=["png", "jpg", "jpeg", "webp"]
)
if uploaded_file is not None:
    image = Image.open(uploaded_file)

    st.image(image, caption="업로드한 이미지")

    # PIL 이미지로 처리
    st.write("크기:", image.size)
    st.write("형식:", image.format)



input_text = st.text_input("이름을 입력하세요", "홍길동")
input_score = st.number_input("점수를 입력하세요", min_value=0, max_value=100, value=90)

df = pd.DataFrame({
    "이름": [f"{input_text}"],
    "점수": [f"{input_score}"]
})

st.write(df)


st.success("성공했습니다")
st.info("안내 메시지입니다")
st.warning("주의하세요")
st.error("오류가 발생했습니다")
st.exception(ValueError("잘못된 값입니다"))


chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=["A", "B", "C"]
)

st.write(chart_data)
st.line_chart(chart_data)
st.bar_chart(chart_data)
st.area_chart(chart_data)




ticker = st.text_input("종목 코드를 입력하세요", "AAPL")

if st.button("주식 정보 불러오기"):
    stock = yf.Ticker(ticker)
    df = stock.history(period="1mo")

    if df.empty:
        st.warning("주식 정보를 찾지 못했습니다.")
    else:
        st.dataframe(df)
        st.line_chart(df["Close"])