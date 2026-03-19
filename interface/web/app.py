"""Streamlit 网页税务计算器"""

import streamlit as st
from decimal import Decimal

from core.calculators import get_calculator
from core.models.tax_models import Country, Currency, Order, OrderItem

st.set_page_config(page_title="跨境财税合规计算器", page_icon="🧮", layout="centered")
st.title("🧮 跨境财税合规计算器")
st.caption("开源跨境税务计算引擎 — 数据不出境，规则透明可信")

COUNTRY_OPTIONS = {"英国 (UK)": "UK", "德国 (DE)": "DE", "美国 (US)": "US", "日本 (JP)": "JP"}
CURRENCY_MAP = {"UK": "GBP", "DE": "EUR", "US": "USD", "JP": "JPY"}
US_STATES = {"加利福尼亚 CA": "CA", "德克萨斯 TX": "TX", "纽约 NY": "NY", "佛罗里达 FL": "FL"}

with st.sidebar:
    st.header("设置")
    country_label = st.selectbox("目标国家", list(COUNTRY_OPTIONS.keys()))
    country_code = COUNTRY_OPTIONS[country_label]
    state = "CA"
    if country_code == "US":
        state_label = st.selectbox("州", list(US_STATES.keys()))
        state = US_STATES[state_label]
    category = st.selectbox("税率类别", ["standard", "reduced", "zero"])

st.subheader("商品信息")
col1, col2 = st.columns(2)
with col1:
    item_name = st.text_input("商品名称", value="示例商品")
    quantity = st.number_input("数量", min_value=1, value=1)
with col2:
    unit_price = st.number_input("单价", min_value=0.01, value=100.00, format="%.2f")
    shipping = st.number_input("运费", min_value=0.00, value=0.00, format="%.2f")

if st.button("计算税费", type="primary", use_container_width=True):
    cur = CURRENCY_MAP[country_code]
    order = Order(
        order_id="WEB-001",
        country=Country(country_code),
        currency=Currency(cur),
        items=[OrderItem(
            name=item_name,
            quantity=quantity,
            unit_price=Decimal(str(unit_price)),
            category=category,
        )],
        shipping_cost=Decimal(str(shipping)),
    )

    calculator = get_calculator(country_code)
    if country_code == "US":
        result = calculator.calculate(order, state=state)
    else:
        result = calculator.calculate(order)

    st.divider()
    st.subheader("计算结果")

    c1, c2, c3 = st.columns(3)
    c1.metric("商品小计", f"{result.subtotal} {cur}")
    c2.metric("税费合计", f"{result.total_tax} {cur}")
    c3.metric("含税总额", f"{result.total_with_tax} {cur}")

    with st.expander("税费明细"):
        for line in result.tax_lines:
            st.write(f"- {line.item_name}: {line.tax_type.value} {line.tax_rate*100}% = {line.tax_amount} {cur}")

st.divider()
st.caption("⚠️ 本工具计算结果仅供参考，正式申报请以官方税务师意见为准。")
