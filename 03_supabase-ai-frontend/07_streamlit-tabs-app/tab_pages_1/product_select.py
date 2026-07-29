"""상품 조회·수정·삭제 탭입니다."""

import httpx
import streamlit as st

API_BASE_URL = "https://render-page-01.onrender.com"
REQUEST_TIMEOUT = 15.0


def get_products() -> list[dict[str, object]]:
    """전체 상품을 조회합니다."""

    response = httpx.get(
        f"{API_BASE_URL}/product/getall",
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()
    return response.json()


def update_product(
    product_id: int,
    name: str,
    price: int,
) -> dict[str, object]:
    """선택한 상품을 백엔드 API에서 수정합니다."""

    response = httpx.put(
        f"{API_BASE_URL}/product/{product_id}",
        json={"name": name, "price": price},
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()
    return response.json()


def delete_product(product_id: int) -> dict[str, object]:
    """선택한 상품을 백엔드 API에서 삭제합니다."""

    response = httpx.delete(
        f"{API_BASE_URL}/product/delete/{product_id}",
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()
    return response.json()


def render_product_select_tab() -> None:
    """상품 목록과 수정·삭제 기능을 표시합니다."""

    st.subheader("상품 조회")
    st.caption("모든 상품 정보를 조회하고 수정하거나 삭제합니다.")

    if st.button("모든 상품 조회", use_container_width=True):
        st.rerun()

    try:
        with st.spinner("모든 상품을 조회 중입니다..."):
            products = get_products()
    except httpx.HTTPStatusError as error:
        st.error(
            f"상품 조회 실패: {error.response.status_code} - "
            f"{error.response.text}"
        )
        return
    except httpx.RequestError as error:
        st.error(f"백엔드 서버에 연결할 수 없습니다: {error}")
        return

    if not products:
        st.warning("조회된 상품이 없습니다.")
        return

    for product in products:
        product_id = int(product["id"])
        with st.container(border=True):
            st.write(f"상품 ID: {product_id}")

            update_col, delete_col = st.columns([4, 1])
            with update_col:
                with st.form(f"product_update_form_{product_id}"):
                    product_name = st.text_input(
                        "상품명",
                        value=str(product["name"]),
                    )
                    price = st.number_input(
                        "상품 가격",
                        min_value=0,
                        step=1,
                        value=int(product["price"]),
                        format="%d",
                    )
                    submitted_update = st.form_submit_button("수정")

            with delete_col:
                submitted_delete = st.button(
                    "삭제",
                    key=f"delete_product_{product_id}",
                    use_container_width=True,
                )

            if submitted_update:
                product_name = product_name.strip()
                if not product_name:
                    st.warning("상품명을 입력하세요.")
                else:
                    try:
                        update_product(
                            product_id,
                            product_name,
                            int(price),
                        )
                        st.toast(f"{product_id}번 상품을 수정했습니다.")
                        st.rerun()
                    except httpx.HTTPStatusError as error:
                        st.error(
                            f"상품 수정 실패: {error.response.status_code} - "
                            f"{error.response.text}"
                        )
                    except httpx.RequestError as error:
                        st.error(f"백엔드 서버에 연결할 수 없습니다: {error}")

            if submitted_delete:
                try:
                    delete_product(product_id)
                    st.toast(f"{product_id}번 상품을 삭제했습니다.")
                    st.rerun()
                except httpx.HTTPStatusError as error:
                    st.error(
                        f"상품 삭제 실패: {error.response.status_code} - "
                        f"{error.response.text}"
                    )
                except httpx.RequestError as error:
                    st.error(f"백엔드 서버에 연결할 수 없습니다: {error}")
