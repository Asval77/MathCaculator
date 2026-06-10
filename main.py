import math
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 웹앱 제목 및 기본 설정
st.set_page_config(page_title="스마트 버튼 계산기", page_icon="🧮", layout="centered")

# --- 🎨 어떤 테마에서도 글자가 선명하게 보이는 커스텀 CSS ---
st.markdown("""
    <style>
    div[data-testid="stTextInput"] input {
        color: #FFD700 !important;
        background-color: #000000 !important;
        font-size: 26px !important;
        font-weight: bold !important;
        border: 3px solid #22c55e !important;
        border-radius: 10px !important;
        padding: 15px !important;
    }
    div[data-testid="stTextInput"] label p {
        color: #FFFFFF !important;
        font-size: 16px !important;
        font-weight: bold !important;
    }
    div.stButton > button {
        font-size: 20px !important;
        font-weight: bold !important;
        height: 55px !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🧮 스마트 버튼 계산기 Pro")

tab1, tab2 = st.tabs(["🔢 버튼 계산기", "📈 함수 그래프"])

# 수식을 저장할 독립적인 창고 생성
if 'calc_expr' not in st.session_state:
    st.session_state.calc_expr = ""

# --- Tab 1: 버튼 클릭형 계산기 로직 ---
with tab1:
    st.subheader("📝 수식 입력 및 계산")

    # 💡 [해결 포인트 1] 위젯에 직접 key를 바인딩하지 않고, value에만 세션 값을 넣어 충돌을 방지합니다.
    # 사용자가 키보드로 직접 칠 수도 있으므로 입력된 값을 즉시 세션에 동기화합니다.
    user_input = st.text_input("현재 입력된 수식", value=st.session_state.calc_expr)
    st.session_state.calc_expr = user_input

    # 계산기 버튼 배열 (6행 4열)
    buttons = [
        ('7', '8', '9', '/'),
        ('4', '5', '6', '*'),
        ('1', '2', '3', '-'),
        ('0', '.', '(', ')'),
        ('**2', '**3', 'math.sqrt(', '+'),
        ('C', '←', '=', '로그')
    ]

    # 반복문을 돌며 버튼 생성 및 기능 매핑
    for row in buttons:
        cols = st.columns(4)
        for btn, col in zip(row, cols):
            if col.button(btn, use_container_width=True, key=f"btn_{btn}"):
                # 💡 [해결 포인트 2] 위젯의 내부 락을 건드리지 않고 오직 순수 데이터 창고만 변경합니다.
                if btn == 'C':
                    st.session_state.calc_expr = ""
                elif btn == '←':
                    st.session_state.calc_expr = st.session_state.calc_expr[:-1]
                elif btn == '=':
                    try:
                        expr = st.session_state.calc_expr
                        st.session_state.calc_expr = str(eval(expr, {"__builtins__": None}, {"math": math, "np": np}))
                    except:
                        st.session_state.calc_expr = "Error"
                elif btn == '로그':
                    st.session_state.calc_expr += "math.log10("
                else:
                    st.session_state.calc_expr += btn
                
                # 안전하게 백엔드 데이터를 바꾼 뒤 화면을 완전히 새로고침하여 반영합니다.
                st.rerun()

    st.write("") 

    # 하단 결과 확인 버튼
    if st.button("결과 확인", type="primary", use_container_width=True, key="submit_btn"):
        try:
            result = eval(st.session_state.calc_expr, {"__builtins__": None}, {"math": math, "np": np})
            st.success(f"결과: {result}")
