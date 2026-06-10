import math
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 웹앱 제목 및 기본 설정
st.set_page_config(page_title="스마트 버튼 계산기", page_icon="🧮", layout="centered")

# --- 🎨 디자인 버그 해결을 위한 커스텀 CSS 주입 ---
st.markdown("""
    <style>
    div[data-testid="stTextInput"] input {
        color: #FFFFFF !important;
        background-color: #262730 !important;
        font-size: 22px !important;
        font-weight: bold !important;
        border: 2px solid #4a4b57 !important;
        border-radius: 8px !important;
    }
    div.stButton > button {
        font-size: 18px !important;
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🧮 스마트 버튼 계산기 Pro")

# 탭을 사용하여 기능 분리
tab1, tab2 = st.tabs(["🔢 버튼 계산기", "📈 함수 그래프"])

# --- Tab 1: 버튼 클릭형 계산기 로직 ---
with tab1:
    st.subheader("📝 수식 입력 및 계산")

    # 세션 상태(session_state)를 사용하여 수식 기억하기
    if 'calc_expr' not in st.session_state:
        st.session_state.calc_expr = ""

    # 수식 표시 창
    display = st.text_input("현재 수식", value=st.session_state.calc_expr, key="display")

    # 버튼 레이아웃 (6x4 그리드)
    buttons = [
        ('7', '8', '9', '/'),
        ('4', '5', '6', '*'),
        ('1', '2', '3', '-'),
        ('0', '.', '(', ')'),
        ('**2', '**3', 'math.sqrt(', '+'),
        ('C', '←', '=', '로그')
    ]

    for row in buttons:
        c1, c2, c3, c4 = st.columns(4)
        for btn, col in zip(row, [c1, c2, c3, c4]):
            if col.button(btn, use_container_width=True, key=f"btn_{btn}"):
                if btn == 'C':
                    st.session_state.calc_expr = ""
                elif btn == '←':
                    st.session_state.calc_expr = st.session_state.calc_expr[:-1]
                elif btn == '=':
                    try:
                        # 💡 [해결 포인트] 글자가 잘리지 않고 완벽하게 매핑되도록 수정했습니다.
                        result = eval(st.session_state.calc_expr, {"__builtins__": None}, {"math": math, "np": np})
                        st.session_state.calc_expr = str(result)
                    except Exception:
                        st.session_state.calc_expr = "Error"
                elif btn == '로그':
                    st.session_state.calc_expr += "math.log10("
                else:
                    st.session_state.calc_expr += btn
                st.rerun()

    st.write("") # 간격 띄우기

    # 계산 실행 버튼
    if st.button("결과 확인", type="primary", use_container_width=True, key="submit_btn"):
        try:
            result = eval(st.session_state.calc_expr, {"__builtins__": None}, {"math": math, "np": np})
            st.success(f"결과: {result}")
        except Exception as e:
            st.error(f"수식 오류: {e}")

# --- Tab 2: 그래프 그리기 로직 ---
with tab2:
    st.subheader("📈 수학 함수 그리기")
    func_str = st.text_input("함수 f(x)를 입력하세요", value="x**2", key="graph_input")
    col1, col2 = st.columns(2)
    with col1: x_min = st.number_input("X 최소값", value=-10.0)
    with col2:
