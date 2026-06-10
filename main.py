import math
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="스마트 버튼 계산기", page_icon="🧮", layout="centered")

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

with tab1:
    st.subheader("📝 수식 입력 및 계산")

    if "widget_display" in st.session_state:
        st.session_state.calc_expr = st.session_state.widget_display

    st.text_input("현재 입력된 수식", value=st.session_state.calc_expr, key="widget_display")

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
                        expr = st.session_state.calc_expr
                        st.session_state.calc_expr = str(eval(expr, {"__builtins__": None}, {"math": math, "np": np}))
                    except:
                        st.session_state.calc_expr = "Error"
                elif btn == '로그':
                    st.session_state.calc_expr += "math.log10("
                else:
                    st.session_state.calc_expr += btn
                
                st.session_state.widget_display = st.session_state.calc_expr
                st.rerun()

    st.write("") 

    if st.button("결과 확인", type="primary", use_container_width=True, key="submit_btn"):
        try:
            result = eval(st.session_state.calc_expr, {"__builtins__": None}, {"math": math, "np": np})
            st.success(f"결과: {result}")
        except Exception as e:
            st.error(f"수식 오류: {e}")

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
