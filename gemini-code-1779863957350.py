import math
import streamlit as st

# 웹앱 제목 및 기본 설정
st.set_page_config(page_title="다기능 계산기", page_icon="🧮", layout="centered")
st.title("🧮 다기능 파이썬 계산기")
st.write("사칙연산부터 로그연산까지 지원하는 깔끔한 스트림릿 계산기입니다.")

st.divider()

# 1. 연산 종류 선택 메뉴
operation = st.selectbox(
    "원하는 연산을 선택하세요",
    [
        "더하기 (+)",
        "빼기 (-)",
        "곱하기 (*)",
        "나누기 (/)",
        "나머지 연산 (Modulus, %)",
        "지수 연산 (Power, ^)",
        "로그 연산 (Logarithm)",
    ],
)

st.subheader(f"🔍 {operation} 수행 중")

# 2. 연산별 입력 및 계산 로직
# 두 개의 숫자 입력이 필요한 기본 연산들
if operation in [
    "더하기 (+)",
    "빼기 (-)",
    "곱하기 (*)",
    "나누기 (/)",
    "나머지 연산 (Modulus, %)",
    "지수 연산 (Power, ^)",
]:
    num1 = st.number_input("첫 번째 숫자를 입력하세요 (X)", value=0.0, format="%f")
    num2 = st.number_input("두 번째 숫자를 입력하세요 (Y)", value=0.0, format="%f")

    if st.button("계산하기"):
        if operation == "더하기 (+)":
            result = num1 + num2
            st.success(f"결과: {num1} + {num2} = **{result}**")

        elif operation == "빼기 (-)":
            result = num1 - num2
            st.success(f"결과: {num1} - {num2} = **{result}**")

        elif operation == "곱하기 (*)":
            result = num1 * num2
            st.success(f"결과: {num1} × {num2} = **{result}**")

        elif operation == "나누기 (/)":
            if num2 == 0:
                st.error("⚠️ 0으로 나눌 수 없습니다!")
            else:
                result = num1 / num2
                st.success(f"결과: {num1} ÷ {num2} = **{result}**")

        elif operation == "나머지 연산 (Modulus, %)":
            if num2 == 0:
                st.error("⚠️ 0으로 나머지 연산을 할 수 없습니다!")
            else:
                result = num1 % num2
                st.success(f"결과: {num1} % {num2} = **{result}**")

        elif operation == "지수 연산 (Power, ^)":
            try:
                result = math.pow(num1, num2)
                st.success(f"결과: {num1} ^ {num2} = **{result}**")
            except OverflowError:
                st.error("⚠️ 결과값이 너무 커서 계산할 수 없습니다 (오버플로우).")
            except ValueError:
                st.error("⚠️ 잘못된 연산입니다 (예: 음수의 소수점 제곱).")

# 로그 연산 (밑과 진수 입력 조건이 다름)
elif operation == "로그 연산 (Logarithm)":
    log_type = st.radio("로그 종류 선택", ["상용로그 (밑 10)", "자연로그 (밑 e)", "사용자 지정 밑"])

    if log_type == "상용로그 (밑 10)":
        x = st.number_input("진수를 입력하세요 (X > 0)", value=1.0, format="%f")
        if st.button("계산하기"):
            if x <= 0:
                st.error("⚠️ 진수는 0보다 커야 합니다.")
            else:
                st.success(f"결과: log10({x}) = **{math.log10(x)}**")

    elif log_type == "자연로그 (밑 e)":
        x = st.number_input("진수를 입력하세요 (X > 0)", value=1.0, format="%f")
        if st.button("계산하기"):
            if x <= 0:
                st.error("⚠️ 진수는 0보다 커야 합니다.")
            else:
                st.success(f"결과: ln({x}) = **{math.log(x)}**")

    elif log_type == "사용자 지정 밑":
        x = st.number_input("진수를 입력하세요 (X > 0)", value=1.0, format="%f")
        base = st.number_input(
            "밑을 입력하세요 (Base > 0, Base ≠ 1)", value=2.0, format="%f"
        )
        if st.button("계산하기"):
            if x <= 0:
                st.error("⚠️ 진수는 0보다 커야 합니다.")
            elif base <= 0 or base == 1: