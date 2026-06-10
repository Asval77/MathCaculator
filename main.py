import math
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 웹앱 제목 및 기본 설정
st.set_page_config(page_title="스마트 버튼 계산기", page_icon="🧮", layout="centered")

# --- 🎨 테마에 영향을 받지 않도록 강력한 커스텀 CSS 주입 ---
st.markdown("""
    <style>
    /* 입력창 배경을 완전한 검은색(#000000)으로, 글자를 선명한 노란색(#FFD700)으로 강제 고정 */
    div[data-testid="stTextInput"] input {
        color: #FFD700 !important;
        background-color: #000000 !important;
        font-size: 26px !important;
        font-weight: bold !important;
        border: 3px solid #22c55e !important;
        border-radius: 10px !important;
        padding: 15px !important;
    }
    /* 입력창 상단의 레이블 글자색을 흰색으로 고정 */
    div[data-testid="stTextInput"] label p {
        color: #FFFFFF !important;
        font-size: 16px !important;
        font-weight: bold !important;
    }
    /* 계산기 버튼 글자 스타일 설정 */
    div.stButton > button {
        font-size: 20px !important;
        font-weight: bold !important;
        height: 55px !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🧮 스마트 버튼 계산기 Pro")

# 탭을 사용하여 기능 분리
tab1, tab2 = st.tabs(["🔢 버튼 계산기", "📈 함수 그래프"])

# 세션 상태(session_state)를 사용하여 수식 기억하기 (앱 최상단에서 초기화)
if 'calc_expr' not in st.session_state:
    st.session_state.calc_expr = ""

# --- Tab 1: 버튼 클릭형 계산기 로직 ---
with tab1:
    st.subheader("📝 수식 입력 및 계산")

    # 💡 [해결 포인트 1] value 매핑 대신 key="calc_expr"를 직접 연동하여 
    # 세션 상태의 변화가 화면에 즉각적으로 반영되도록 수정했습니다.
    display = st.text_input("현재 입력된 수식", key="calc_expr")

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
                # 💡 [해결 포인트 2] 모든 수식 변경 제어를 세션 상태 변수에 직접 수행합니다.
                if btn == 'C':
                    st.session_state.calc_expr = ""
                elif btn == '←':
                    st.session_state.calc_expr = st.session_state.calc_expr[:-1]
                elif btn == '=':
                    try:
                        result = eval(st.session_state.calc_expr, {"__builtins__": None}, {"math": math, "np": np})
                        st.session_state.calc_expr = str(result)
                    except Exception:
                        st.session_state.calc_expr = "Error"
                elif btn == '로그':
                    st.session_state.calc_expr += "
