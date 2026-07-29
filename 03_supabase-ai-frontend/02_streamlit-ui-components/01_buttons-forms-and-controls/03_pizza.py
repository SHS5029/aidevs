import streamlit as st

st.title("Pizza")
p1, p2, p3 = st.columns(3)

def init_state():
    if "pizza" not in st.session_state:
        st.session_state["pizza"] = {
        }
    st.session_state.setdefault("dough", "얇은 도우")
    st.session_state.setdefault("cheese", "모짜렐라")
    st.session_state.setdefault("toppings", ["치즈"])

    if "count" not in st.session_state:
        st.session_state.count = 0

def reset_state():
    st.session_state.dough = "얇은 도우"
    st.session_state.cheese = "모짜렐라"
    st.session_state.toppings = ["치즈"]
    st.session_state.pizza = None
    st.session_state.count = 0
    st.toast("주문이 초기화되었습니다.")
def add_order():
    st.session_state.count += 1
    st.text(f"주문 수량: {st.session_state.count}")

def decrease_order():
    if st.session_state.count > 0:
        st.session_state.count -= 1
        st.text(f"주문 수량: {st.session_state.count}")
    else:
        st.toast("주문 수량은 0 이상이어야 합니다.")
        st.text(f"주문 수량: {st.session_state.count}")

if "pizza" not in st.session_state:
    init_state()

def make_p1():
    st.toast("P1 굽는중")
    st.session_state.pizza = "Pizza1"
    st.session_state.setdefault("dough", "P1 도우")
    st.session_state.setdefault("cheese", "체다")
    st.session_state.setdefault("toppings", ["치즈"])
def make_p2():
    st.toast("P2 굽는중")
    st.session_state.pizza = "Pizza2"
    st.session_state.setdefault("dough", "P2 도우")
    st.session_state.setdefault("cheese", "파마산")
    st.session_state.setdefault("toppings", ["치즈"])
def make_p3():
    st.toast("P3 굽는중")
    st.session_state.pizza = "Pizza3"
    st.session_state.setdefault("dough", "P3 도우")
    st.session_state.setdefault("cheese", "모짜렐라")
    st.session_state.setdefault("toppings", ["치즈"])
def summit_order():
    st.success(f"주문 완료! 도우: {dough}, 치즈: {cheese}, 토핑: {', '.join(toppings)}")

    
with p1:
    p1_clicked = st.button("P1", on_click = make_p1)
with p2:
    p2_clicked = st.button("P2", on_click = make_p2)
with p3:
    p3_clicked = st.button("P3", on_click = make_p3)


with st.form("pizza_form"):
    dough = st.selectbox("도우 선택", ["얇은 도우", "두꺼운 도우"], key="dough")
    cheese = st.selectbox("치즈 선택", ["모짜렐라", "체다", "파마산"], key="cheese")
    toppings = st.multiselect("토핑 선택", ["치즈", "페퍼로니", "버섯", "올리브"], key="toppings")
    submit_button = st.form_submit_button("주문하기")
    reset_button = st.form_submit_button("초기화", on_click=reset_state)

    st.text(f"주문 수량: {st.session_state.count}")
    if reset_button:
        st.session_state.count = 0
        st.toast("주문이 초기화되었습니다.")

    if submit_button:
        st.subheader(f"주문 완료! 도우: {dough}, 치즈: {cheese}, 토핑: {', '.join(toppings)}, 선택한 피자: {st.session_state.pizza}")
        summit_order()

        add_order_button = st.form_submit_button("주문 추가")
        decrease_order_button = st.form_submit_button("주문 감소")
        st.session_state.count = 0
        st.toast("주문이 초기화되었습니다.")
        if add_order_button:
            add_order()
            st.text(f"주문 수량: {st.session_state.count}")
        if decrease_order_button:
            decrease_order()
            st.text(f"주문 수량: {st.session_state.count}")



if st.session_state.pizza == "Pizza1":
    st.subheader("P1 피자를 선택했습니다.")
elif st.session_state.pizza == "Pizza2":
    st.subheader("P2 피자를 선택했습니다.")
elif st.session_state.pizza == "Pizza3":
    st.subheader("P3 피자를 선택했습니다.")

