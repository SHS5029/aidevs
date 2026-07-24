import streamlit as st
import yfinance as yf

ticker = st.text_input("종목 코드를 입력하세요", "AAPL")

if st.button("주식 정보 불러오기"):
    stock = yf.Ticker(ticker)
    df = stock.history(period="1mo")

    if df.empty:
        st.warning("주식 정보를 찾지 못했습니다.")
    else:
        st.dataframe(df)
        st.line_chart(df["Close"])