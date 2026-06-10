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

# 세션 상태 창고 초기화
if 'calc_expr' not in st.session_state:
    st.session_state.calc_expr = ""

# --- Tab 1: 버튼 클릭형 계산기 로직 ---
with tab1:
    st.subheader("📝 수식 입력 및 계산")

    # 사용자가 키보드로 수식을 직접 수정했을 때도 세션에 반영
    if "widget_display" in st.session_state:
        st.session_state.calc_expr = st.session_state.widget_display

    # 위젯과 세션 변수 안전하게 연동
    st.text_input("현재 입력된 수식", value=st.session_state.calc_expr, key="widget_display")

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
                if btn == 'C':
                    st.session_state.calc_expr = ""
                elif btn == '←':
                    st.session_state.calc_expr = st.session_state.calc_expr[:-1]
                elif btn == '=':
                    try:
                        # 💡 [해결 포인트] 끊
