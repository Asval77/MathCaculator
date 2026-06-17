import math
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="스마트 버튼 계산기", page_icon="🧮", layout="centered")

# --- 🎨 아름다운 그래디언트 배경과 현대적인 디자인 ---
st.markdown("""
    <style>
    /* 메인 배경: 그래디언트 (보라색 → 파란색) */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #4c63d2 50%, #2e5090 75%, #1a237e 100%);
        background-attachment: fixed;
    }
    
    /* 컨테이너 배경 */
    [data-testid="stAppViewContainer"] {
        background-color: transparent;
    }
    
    [data-testid="stHeader"] {
        background-color: transparent;
    }
    
    /* 텍스트 입력창 */
    div[data-testid="stTextInput"] input {
        color: #000000 !important;
        background-color: rgba(255, 255, 255, 0.15) !important;
        font-size: 26px !important;
        font-weight: bold !important;
        border: 2px solid rgba(255, 255, 255, 0.4) !important;
        border-radius: 15px !important;
        padding: 15px !important;
        backdrop-filter: blur(10px) !important;
    }
    
    div[data-testid="stTextInput"] input::placeholder {
        color: rgba(0, 0, 0, 0.6) !important;
    }
    
    div[data-testid="stTextInput"] label p {
        color: #000000 !important;
        font-size: 16px !important;
        font-weight: bold !important;
    }
    
    /* 버튼 스타일 */
    div.stButton > button {
        color: #000000 !important;
        background-color: rgba(255, 255, 255, 0.2) !important;
        font-size: 20px !important;
        font-weight: bold !important;
        height: 55px !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
        backdrop-filter: blur(10px) !important;
    }
    
    div.stButton > button:hover {
        background-color: rgba(255, 255, 255, 0.35) !important;
        border-color: rgba(255, 255, 255, 0.6) !important;
        box-shadow: 0 0 20px rgba(255, 255, 255, 0.3) !important;
    }
    
    /* Primary 버튼 (결과 확인) */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #00d4ff 0%, #0099ff 100%) !important;
        border: none !important;
        color: #000000 !important;
    }
    
    div.stButton > button[kind="primary"]:hover {
        box-shadow: 0 0 30px rgba(0, 212, 255, 0.5) !important;
    }
    
    /* Tab 스타일 */
    [data-testid="stTabs"] {
        background-color: transparent;
    }
    
    button[data-baseweb="tab"] {
        color: rgba(0, 0, 0, 0.7) !important;
        background-color: transparent !important;
        border-bottom: 2px solid transparent !important;
        font-weight: 600 !important;
    }
    
    button[data-baseweb="tab"]:hover {
        color: #000000 !important;
        border-bottom: 2px solid rgba(0, 0, 0, 0.5) !important;
    }
    
    button[aria-selected="true"][data-baseweb="tab"] {
        color: #000000 !important;
        border-bottom: 2px solid #00d4ff !important;
    }
    
    /* 제목 스타일 */
    h1, h2, h3 {
        color: #000000 !important;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* 일반 텍스트 */
    p, span, label {
        color: #000000 !important;
    }
    
    /* Number 입력 */
    div[data-testid="stNumberInput"] input {
        color: #000000 !important;
        background-color: rgba(255, 255, 255, 0.15) !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 10px !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Success/Error 메시지 */
    .stSuccess {
        background-color: rgba(34, 197, 94, 0.2) !important;
        border: 2px solid rgba(34, 197, 94, 0.5) !important;
        border-radius: 10px !important;
        color: #000000 !important;
    }
    
    .stError {
        background-color: rgba(239, 68, 68, 0.2) !important;
        border: 2px solid rgba(239, 68, 68, 0.5) !important;
        border-radius: 10px !important;
        color: #000000 !important;
    }
    
    /* 컬럼 배경 */
    [data-testid="column"] {
        background-color: transparent !important;
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
            fig, ax = plt.subplots(facecolor='rgba(0,0,0,0)')
            ax.plot(x, y, label=f"f(x) = {func_str}", color="#00d4ff", linewidth=3)
            ax.axhline(0, color='rgba(255,255,255,0.3)', lw=1.5)
            ax.axvline(0, color='rgba(255,255,255,0.3)', lw=1.5)
            ax.grid(True, linestyle='--', alpha=0.2, color='white')
            ax.legend(facecolor='rgba(0,0,0,0.3)', edgecolor='white', labelcolor='white')
            ax.set_facecolor('rgba(0,0,0,0.1)')
            ax.tick_params(colors='white')
            ax.spines['bottom'].set_color('white')
            ax.spines['left'].set_color('white')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            st.pyplot(fig)
        except Exception as e:
            st.error(f"그래프 오류: {e}")
