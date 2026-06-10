import math
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="스마트 버튼 계산기", page_icon="🧮", layout="centered")

# --- 🎨 화면 테마에 영향을 받지 않는 선명한 커스텀 CSS ---
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

if 'calc_expr' not in st.session_state:
    st.session_state.calc_expr = ""

# --- Tab 1: 버튼 클릭형 계산기 ---
with tab1:
    st.subheader("📝 수식 입력 및 계산")

    user_input = st.text_input("현재 입력된 수식", value=st.session_state.calc_expr)
    st.session_state.calc_expr = user_input

    buttons = [
        ('7', '8', '9', '/'),
        ('4', '5', '6', '*'),
        ('1', '2', '3', '-'),
        ('0', '.', '(', ')'),
        ('**2', '**3', 'math.sqrt(', '+'),
        ('C', '←', '=', '로그')
    ]

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
                        st.session_state.calc_expr = str(eval(st.session_state.calc_expr, {"__builtins__": None}, {"math": math, "np": np}))
                    except:
                        st.session_state.calc_expr = "Error"
                elif btn == '로그':
                    st.session_state.calc_expr += "math.log10("
                else:
                    st.session_state.calc_expr += btn
                st.rerun()

    st.write("") 

    # 에러가 나던 결과 확인 부분을 단 5줄로 대폭 압축하여 잘림 현상을 방지했습니다.
    if st.button("결과 확인", type="primary", use_container_width=True, key="submit_btn"):
        try:
            st.success(f"결과: {eval(st.session_state.calc_expr, {'__builtins__': None}, {'math': math, 'np': np})}")
        except Exception as e:
            st.error(f"수식 오류: {e}")

# --- Tab 2: 그래프 그리기 ---
with tab2:
    st.subheader("📈 수학 함수 그리기")
    func_str = st.text_input("함수 f(x)를 입력하세요", value="x**2", key="graph_input")
    
    col1, col2 = st.columns(2)
    with col1: x_min = st.number_input("X 최소값", value=-10.0)
    with col2: x_max = st.number_input("X 최대값", value=10.0)

    if st.button("그래프 생성", key="graph_btn"):
        try:
            x = np.linspace(x_min, x_max, 500)
            y = eval(func_str, {"__builtins__": None}, {"np": np, "x": x, "math": math})
            fig, ax = plt.subplots()
            ax.plot(x, y, label=f"f(x) = {func_str}", color="#22c55e", linewidth=2)
            ax.axhline(0, color='black', lw=1); ax.axvline(0, color='black', lw=1)
            ax.grid(True, linestyle='--', alpha=0.6); ax.legend()
            st.pyplot(fig)
        except Exception as e:
            st.error(f"그래프 오류: {e}")
