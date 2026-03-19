"""高精度 Decimal 计算工具"""

from decimal import ROUND_HALF_UP, Decimal


def round_tax(value: Decimal, places: int = 2) -> Decimal:
    """税额四舍五入到指定小数位"""
    quantize_str = "0." + "0" * places
    return value.quantize(Decimal(quantize_str), rounding=ROUND_HALF_UP)


def calculate_tax(amount: Decimal, rate: Decimal, places: int = 2) -> Decimal:
    """计算税额 = 金额 × 税率，四舍五入"""
    return round_tax(amount * rate, places)


def sum_items_total(amounts: list[Decimal]) -> Decimal:
    """汇总金额列表"""
    return sum(amounts, Decimal("0"))
