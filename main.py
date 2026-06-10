import math
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 웹앱 제목 및 기본 설정
st.set_page_config(page_title="스마트 다기능 계산기", page_icon="🧮", layout="centered")
st.title("🧮 스마트 파이썬 계산기 Pro")
st.write("단 하나의 수식 입력으로 모든 연산이 가능한 심플하고 강력한 계산기입니다.")

# 탭을 사용하여 기능 분리 (계산기 / 그래프)
tab1, tab2 = st.tabs(["🔢 스마트 계산기", "📈 함수 그래프"])

# --- Tab 1: 일반 및 다중 계산기 로직 (초간단 단순화) ---
with tab1:
    st.subheader("📝 계산할 수식 입력")
    st.write("사칙연산, 다중 연산, 괄호, 수학 함수를 자유롭게 입력하세요.")
    
    # 헬프 가이드 (동작 방식 안내)
    with st.expander("💡 사용 가능한 수식 예시 보기"):
        st.markdown("""
        * **기본/다중 사칙연산:** `10 + 20 * 3 / 2` (우선순위 자동 적용)
        * **괄호 연산:** `(10 + 20) * 3`
        * **거듭제곱 (제곱):** `2**3` (2의 3제곱 = 8)
        * **로그 및 수학 연산:** `math.log10(100)` 또는 `math.log(8, 2)` (밑이 2인 로그 8)
        * **원주율/삼각함수:** `math.pi`, `math.sin(math.pi/2)`
        """)

    # 단 하나의 텍스트 입력창으로 모든 연산 통합
    calc_str = st.text_input("수식을 입력하세요", value="(10 + 20) * 3 - 50", key="smart_calc_input")
    
    if st.button("계산 실행", type="primary", key="smart_calc_btn"):
        if calc_str.strip() == "":
            st.warning("⚠️ 수식을 입력해 주세요.")
        else:
            try:
                # 안전한 계산 환경을 위해 화이트리스트 제공
                # 사용자가 math.log, math.sqrt, np.sqrt 등을 자유롭게 쓸 수 있게 바인딩
                allowed_names = {"math": math, "np": np}
                
                # 수식 자동 계산
                result = eval(calc_str, {"__builtins__": None}, allowed_names)
                
                # 성공 메시지 출력
                st.success(f"📊 **계산 결과:** `{calc_str}` = **{result}**")
                
            except ZeroDivisionError:
                st.error("⚠️ 0으로 나눌 수 없습니다. 수식을 확인해 주세요.")
            except NameError as ne:
                st.error(f"⚠️ 인식할 수 없는 문자나 함수가 있습니다. (예: 곱하기는 `*`, 거듭제곱은 `**` 로 입력해야 합니다.)")
            except Exception as e:
                st.error(f"⚠️ 수식에 오류가 있습니다. 입력 내용을 확인해 주세요. (에러: {e})")

# --- Tab 2: 그래프 그리기 로직 (기존 코드 유지) ---
with tab2:
    st.subheader("📈 수학 함수 그리기")
    st.info("예시: np.sin(x), x**2, np.log(x), 3*x + 2")
    
    # 수식 입력
    func_str = st.text_input("함수 f(x)를 입력하세요", value="x**2")
    
    # X축 범위 설정
    col1, col2 = st.columns(2)
    with col1: x_min = st.number_input("X 최소값", value=-10.0)
    with col2: x_max = st.number_input("X 최대값", value=10.0)

    if st.button("그래프 생성", key="graph_gen_btn"):
        try:
            x = np.linspace(x_min, x_max, 500)
            # 안전하게 수식 계산
            y = eval(func_str, {"__builtins__": None}, {"np": np, "x": x, "math": math})
            
            fig, ax = plt.subplots()
            ax.plot(x, y, label=f"f(x) = {func_str}", color="#22c55e", linewidth=2)
            ax.axhline(0, color='black', lw=1)
            ax.axvline(0, color='black', lw=1)
            ax.grid(True, linestyle='--', alpha=0.6)
            ax.legend()
            
            st.pyplot(fig)
        except Exception as e:
            st.error(f"🚨 그래프를 그릴 수 없습니다: {e}")
