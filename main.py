import math
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 웹앱 제목 및 기본 설정
st.set_page_config(page_title="다기능 계산기 & 그래프", page_icon="🧮", layout="centered")
st.title("🧮 다기능 파이썬 계산기 Pro")
st.write("여러 숫자의 동시 연산 및 수식 계산, 함수 그래프 시각화를 지원하는 강력한 계산기입니다.")

# 탭을 사용하여 기능 분리 (계산기 / 그래프)
tab1, tab2 = st.tabs(["🔢 일반 및 다중 계산기", "📈 함수 그래프"])

# --- Tab 1: 일반 및 다중 계산기 로직 ---
with tab1:
    operation = st.selectbox(
        "원하는 연산을 선택하세요",
        [
            "여러 숫자 연산 (더하기/곱하기 등)",
            "자유 수식 직접 입력 (일반 계산기)",
            "로그 연산 (Log)"
        ]
    )

    st.divider()

    # 1. 여러 숫자 연산 기능
    if operation == "여러 숫자 연산 (더하기/곱하기 등)":
        st.subheader("🔢 여러 숫자 한 번에 연산하기")
        
        # 사용자로부터 숫자 리스트 입력 받기
        numbers_input = st.text_input("연산할 숫자들을 공백이나 쉼표(,)로 구분해서 입력하세요.", value="10, 20, 30, 40")
        
        sub_op = st.radio(
            "수행할 연산을 선택하세요",
            ["모두 더하기 (+)", "모두 빼기 (-)", "모두 곱하기 (*)", "모두 나누기 (/)"]
        )

        if st.button("계산 실행", key="multi_calc_btn"):
            try:
                # 입력된 문자열에서 숫자만 추출하여 리스트로 변환 (공백 및 쉼표 처리)
                cleaned_input = numbers_input.replace(",", " ")
                nums = [float(n) for n in cleaned_input.split()]
                
                if not nums:
                    st.warning("⚠️ 입력된 숫자가 없습니다.")
                else:
                    if sub_op == "모두 더하기 (+)":
                        result = sum(nums)
                        expression = " + ".join(map(str, nums))
                        st.success(f"**결과:** {expression} = **{result}**")
                        
                    elif sub_op == "모두 빼기 (-)":
                        result = nums[0] - sum(nums[1:])
                        expression = " - ".join(map(str, nums))
                        st.success(f"**결과:** {expression} = **{result}**")
                        
                    elif sub_op == "모두 곱하기 (*)":
                        result = 1.0
                        for n in nums:
                            result *= n
                        expression = " × ".join(map(str, nums))
                        st.success(f"**결과:** {expression} = **{result}**")
                        
                    elif sub_op == "모두 나누기 (/)":
                        if 0 in nums[1:]:
                            st.error("⚠️ 0으로 나눌 수 없습니다.")
                        else:
                            result = nums[0]
                            for n in nums[1:]:
                                result /= n
                            expression = " ÷ ".join(map(str, nums))
                            st.success(f"**결과:** {expression} = **{result}**")
            except ValueError:
                st.error("⚠️ 올바른 숫자 형식으로 입력해 주세요. (예: 10, 20.5, 30)")

    # 2. 자유 수식 직접 입력 기능 (괄호 및 사칙연산 우선순위 미적용 문제 해결)
    elif operation == "자유 수식 직접 입력 (일반 계산기)":
        st.subheader("📝 수식 직접 입력하기")
        st.info("예시: (10 + 5) * 2 / 3 또는 2**3 (2의 3제곱)")
        
        calc_str = st.text_input("계산할 수식을 입력하세요", value="(10 + 20) * 3")
        
        if st.button("수식 계산", key="expr_calc_btn"):
            try:
                # 안전한 계산 환경을 위해 화이트리스트 제공
                allowed_names = {"math": math, "np": np}
                result = eval(calc_str, {"__builtins__": None}, allowed_names)
                st.success(f"**계산 결과:** {calc_str} = **{result}**")
            except ZeroDivisionError:
                st.error("⚠️ 0으로 나눌 수 없습니다.")
            except Exception as e:
                st.error(f"⚠️ 수식에 오류가 있습니다. 입력 내용을 확인해 주세요. (에러: {e})")

    # 3. 로그 연산 기능 (기존 코드 유지 및 보완)
    elif operation == "로그 연산 (Log)":
        st.subheader("🪵 로그 계산")
        x = st.number_input("진수(X)", value=1.0, min_value=0.000001, format="%f")
        base = st.number_input("밑(Base)", value=10.0, min_value=0.000001, format="%f")
        
        if st.button("로그 계산", key="log_calc_btn"):
            if x > 0 and base > 0 and base != 1:
                st.success(f"**결과:** log_{base}({x}) = **{math.log(x, base)}**")
            else:
                st.error("⚠️ 입력값이 로그 조건(진수 > 0, 밑 > 0, 밑 ≠ 1)을 만족하지 않습니다.")

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
            # 안전하게 수식 계산 (진수 조건 등으로 인한 에러 방지를 위해 np 로그 등 활용 권장)
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
