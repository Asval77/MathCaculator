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

# 데이터 저장용 세션 상태 독립 초기화
if 'calc_expr' not in st.session_state:
    st.session_state.calc_expr = ""

# --- Tab 1: 버튼 클릭형 계산기 로직 ---
with tab1:
    st.subheader("📝 수식 입력 및 계산")

    # 사용자가 타이핑으로 수식을 직접 수정했을 때도 반영되도록 처리
    if "widget_display" in st.session_state:
        st.session_state.calc_expr = st.session_state.widget_display

    # 위젯의 key를 "widget_display"로 분리하고, value에 실제 값을 바인딩합니다.
    display = st.text_input(
        "현재 입력된 수식", 
        value=st.session_state.calc_expr, 
        key="widget_display"
    )

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
                
                # 버튼 클릭 시 백엔드 데이터 변수 안전하게 수정
                if btn == 'C':
                    st.session_state.calc_expr = ""
                elif btn == '←':
                    st.session_state.calc_expr = st.session_state.calc_expr[:-1]
                elif btn == '=':
                    try:
                        result = eval(st
