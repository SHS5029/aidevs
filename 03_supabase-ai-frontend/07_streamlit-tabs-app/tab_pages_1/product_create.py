"""Product Create 탭입니다."""

import httpx
import streamlit as st

API_BASE_URL = "https://render-page-01.onrender.com"  # 프론트엔드가 호출할 백엔드 서버의 기본 주소를 한 곳에서 관리합니다.


def render_product_create_tab() -> None:
    """로그인 후 상품을 생성합니다."""

    st.subheader("Product Create")
    st.caption("로그인 후 상품을 생성합니다.")

    with st.form("product_create_form", clear_on_submit=True):
        product_id = st.number_input("상품 ID 입력", min_value=1, step=1, format="%d")
        product_name = st.text_input("상품명 입력", placeholder="예: 새로운 상품")
        price = st.number_input("상품 가격 입력", min_value=0, step=1, format="%d")
        submitted = st.form_submit_button("생성")

    if submitted:
        product_name = product_name.strip()
        if not product_name:
            st.warning("상품명을 입력하세요.")
        else:
            payload = {
                "id": int(product_id),
                "name": product_name,
                "price": int(price),
            }
            with st.spinner("상품을 생성 중입니다..."):
                response = httpx.post(f"{API_BASE_URL}/product/create", json=payload, timeout=15.0)

            if response.status_code == 200:
                result = response.json()
                st.success("상품을 생성했습니다.")
                st.json(result)
            else:
                st.error(f"상품 생성 실패: {response.status_code} - {response.text}")
