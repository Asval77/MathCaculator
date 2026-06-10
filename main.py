import math
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 웹앱 제목 및 기본 설정
st.set_page_config(page_title="클릭형 스마트 계산기", page_icon="🔘", layout="centered")

# --- 스타일 설정 (버튼을 예쁘게 만들기 위해) ---
st.markdown("""
    <style>
    div.stButton > button {
        width: 100%;
        height: 60px;
        font-size: 20px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🔘 클릭형 스마트 계산기")
st.write("버튼을 눌러 수식을 완성하세요. 타이핑할 필요가 없어 훨씬 편합니다!")

# 세션 상태 초기화 (입력된 수식을 저장하는 창고)
if 'calc_input' not in st.session_state:
    st.session_state.calc_input = ""

# 탭 구성
tab1, tab2 = st.tabs(["🔢 버튼 계산기", "📈 함수 그래프"])

# --- Tab 1: 버튼 클릭형 계산기 ---
with tab1:
    # 1. 현재 입력창 (수정 가능하게 텍스트 박스로 유지하되 세션과 연동)
    current_expr = st.text_input("수식 입력창", value=st.session_state.calc_input, key="display")

    # 2. 버튼 배치 (4x5 그리드)
    # 첫 번째 줄: 지우기, 괄호, 나누기
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("C", help="모두 지우기"):
        st.session_state.calc_input = ""
        st.rerun()
    if c2.button("("): st.session_state.calc_input += "("; st.rerun()
    if c3.button(")"): st.session_state.calc_input += ")"; st.rerun()
    if c4.button("÷"): st.session_state.calc_input += "/"; st.rerun()

    # 두 번째 줄: 7, 8, 9, 곱하기
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("7"): st.session_state.calc_input += "7"; st.rerun()
    if c2.button("8"): st.session_state.calc_input += "8"; st.rerun()
    if c3.button("9"): st.session_state.calc_input += "9"; st.rerun()
    if c4.button("×"): st.session_state.calc_input += "*"; st.rerun()

    # 세 번째 줄: 4, 5, 6, 빼기
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("4"): st.session_state.calc_input += "4"; st.rerun()
    if c2.button("5"): st.session_state.calc_input += "5"; st.rerun()
    if c3.button("6"): st.session_state.calc_input += "6"; st.rerun()
    if c4.button("-"): st.session_state.calc_input += "-"; st.rerun()

    # 네 번째 줄: 1, 2, 3, 더하기
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("1"): st.session_state.calc_input += "1"; st.rerun()
    if c2.button("2"): st.session_state.calc_input += "2"; st.rerun()
    if c3.button("3"): st.session_state.calc_input += "3"; st.rerun()
    if c4.button("+"): st.session_state.calc_input += "+"; st.rerun()

    # 다섯 번째 줄: 0, 점, 제곱, 계산(=)
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("0"): st.session_state.calc_input += "0"; st.rerun()
    if c2.button("."): st.session_state.calc_input += "."; st.rerun()
    if c3.button("x²"): st.session_state.calc_input += "**2"; st.rerun()
    if c4.button("=", type="primary"):
        try:
            # 안전하게 수식 계산
            allowed_names = {"math": math, "np": np}
            result = eval(st.session_state.calc_input, {"__builtins__": None}, allowed_names)
            st.success(f"**결과: {result}**")
            st.session_state.calc_input = str(result) # 다음 계산을 위해 결과를 입력창에 유지
        except Exception as e:
            st.error("⚠️ 잘못된 수식입니다.")

    # 추가 기능 (로그/루트 등)
    with st.expander("➕ 고급 연산 버튼"):
        ac1, ac2, ac3 = st.columns(3)
        if ac1.button("√ (루트)"): st.session_state.calc_input += "math.sqrt("; st.rerun()
        if ac2.button("log10"): st.session_state.calc_input += "math.log10("; st.rerun()
        if ac3.button("π (파이)"): st.session_state.calc_input += "math.pi"; st.rerun()

# --- Tab 2: 그래프 그리기 로직 (기존 유지) ---
with tab2:
    st.subheader("📈 수학 함수 그리기")
    func_str = st.text_input("함수 f(x)를 입력하세요", value="x**2")
    col1, col2 = st.columns(2)
    with col1: x_min = st.number_input("X 최소값", value=-10.0)
    with col2: x_max = st.number_input("X 최대값", value=10.0)

    if st.button("그래프 생성"):
        try:
            x = np.linspace(x_min, x_max, 500)
            y = eval(func_str, {"__builtins__": None}, {"np": np, "x": x, "math": math})
            fig, ax = plt.subplots()
            ax.plot(x, y, label=f"f(x) = {func_str}", color="#22c55e")
            ax.axhline(0, color='black', lw=1); ax.axvline(0, color='black', lw=1)
            ax.grid(True, linestyle=':', alpha=0.6)
            st.pyplot(fig)
        except Exception as e:
            st.error(f"🚨 그래프 에러: {e}")
