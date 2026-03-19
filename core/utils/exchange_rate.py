"""汇率转换工具（静态汇率表，后续可对接实时 API）"""

from decimal import Decimal

from core.utils.decimal_calc import round_tax

# 静态汇率表（对 CNY）
_RATES_TO_CNY: dict[str, Decimal] = {
    "CNY": Decimal("1.0000"),
    "USD": Decimal("7.2500"),
    "GBP": Decimal("9.1800"),
    "EUR": Decimal("7.8900"),
    "JPY": Decimal("0.0483"),
}


def get_rate_to_cny(currency: str) -> Decimal:
    """获取某币种对人民币的汇率"""
    code = currency.upper()
    if code not in _RATES_TO_CNY:
        raise ValueError(f"不支持的币种: {code}")
    return _RATES_TO_CNY[code]


def convert_to_cny(amount: Decimal, currency: str) -> Decimal:
    """将外币金额转换为人民币"""
    rate = get_rate_to_cny(currency)
    return round_tax(amount * rate)
