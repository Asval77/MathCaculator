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

    # 세션 상태 변수(calc_expr)와 직접 연동된 텍스트 입력창
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
                
                # 💡 [해결 포인트] 따옴표가 중간에 끊기지 않도록 온전하게 문자열을 처리했습니다.
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
    with col1:
        x_min = st.number_input("X 최소값", value=-10.0)
    with col2:
        x_max = st.number_input("X 최대값", value=10.0)

    if st.button("그래프 생성", key="graph_btn"):
        try:
            x = np.linspace(x_min, x_max, 500)
            y = eval(func_str, {"__builtins__": None}, {"np": np, "x": x, "math": math})
            
            fig, ax = plt.subplots()
            ax.plot(x, y, label=f"f(x) = {func_str}", color="#22c55e", linewidth=2)
            ax.axhline(0, color='black', lw=1)
            ax.axvline(0, color='black', lw=1)
            ax.grid(True, linestyle='--', alpha=0.6)
            ax.legend()
            st.pyplot(fig)
        except Exception as e:
            st.error(f"그래프 오류: {e}")
