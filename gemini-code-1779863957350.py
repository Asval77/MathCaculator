import math
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 웹앱 제목 및 기본 설정
st.set_page_config(page_title="다기능 계산기 & 그래프", page_icon="🧮", layout="centered")
st.title("🧮 다기능 파이썬 계산기 Pro")
st.write("사칙연산부터 함수 그래프 시각화까지 지원하는 강력한 계산기입니다.")

# 탭을 사용하여 기능 분리 (계산기 / 그래프)
tab1, tab2 = st.tabs(["🔢 일반 계산기", "📈 함수 그래프"])

# --- Tab 1: 일반 계산기 로직 ---
with tab1:
    operation = st.selectbox(
        "원하는 연산을 선택하세요",
        ["더하기 (+)", "빼기 (-)", "곱하기 (*)", "나누기 (/)", "나머지 (%)", "지수 (^)", "로그 (Log)"]
    )

    if operation in ["더하기 (+)", "빼기 (-)", "곱하기 (*)", "나누기 (/)", "나머지 (%)", "지수 (^)"]:
        num1 = st.number_input("첫 번째 숫자(X)", value=0.0)
        num2 = st.number_input("두 번째 숫자(Y)", value=0.0)
        
        if st.button("계산 실행", key="calc_btn"):
            if operation == "더하기 (+)": st.success(f"결과: {num1 + num2}")
            elif operation == "빼기 (-)": st.success(f"결과: {num1 - num2}")
            elif operation == "곱하기 (*)": st.success(f"결과: {num1 * num2}")
            elif operation == "나누기 (/)":
                if num2 != 0: st.success(f"결과: {num1 / num2}")
                else: st.error("0으로 나눌 수 없습니다.")
            elif operation == "나머지 (%)": st.success(f"결과: {num1 % num2}")
            elif operation == "지수 (^)": st.success(f"결과: {math.pow(num1, num2)}")

    elif operation == "로그 (Log)":
        x = st.number_input("진수(X)", value=1.0)
        base = st.number_input("밑(Base)", value=10.0)
        if st.button("로그 계산"):
            if x > 0 and base > 0 and base != 1:
                st.success(f"결과: {math.log(x, base)}")
            else:
                st.error("입력값이 로그 조건을 만족하지 않습니다.")

# --- Tab 2: 그래프 그리기 로직 ---
with tab2:
    st.subheader("📈 수학 함수 그리기")
    st.info("예시: np.sin(x), x**2, np.log(x), 3*x + 2")
    
    # 수식 입력
    func_str = st.text_input("함수 f(x)를 입력하세요", value="x**2")
    
    # X축 범위 설정
    col1, col2 = st.columns(2)
    with col1: x_min = st.number_input("X 최소값", value=-10.0)
    with col2: x_max = st.number_input("X 최대값", value=10.0)

    if st.button("그래프 생성"):
        try:
            x = np.linspace(x_min, x_max, 500)
            # 안전하게 수식 계산
            y = eval(func_str, {"np": np, "x": x, "math": math})
            
            fig, ax = plt.subplots()
            ax.plot(x, y, label=f"f(x) = {func_str}", color="#22c55e", linewidth=2)
            ax.axhline(0, color='black', lw=1)
            ax.axvline(0, color='black', lw=1)
            ax.grid(True, linestyle='--', alpha=0.6)
            ax.legend()
            
            st.pyplot(fig)
        except Exception as e:
            st.error(f"그래프를 그릴 수 없습니다: {e}")

**💡 팁:** 깃허브에 올리실 때 `requirements.txt` 파일에 `numpy`와 `matplotlib`을 반드시 추가해 주세요! 궁금한 점이 있으시면 언제든 말씀해 주세요.
