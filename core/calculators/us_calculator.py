"""美国 Sales Tax 计算器"""

from decimal import Decimal

from core.calculators.base import BaseCalculator
from core.models.tax_models import Order, TaxLineItem, TaxResult, TaxType
from core.utils.decimal_calc import calculate_tax


class USCalculator(BaseCalculator):
    country_code = "US"
    rules_file = "us.json"

    def get_state_rate(self, state: str) -> Decimal:
        """获取州级销售税率"""
        rates = self.rules.get("rates", {})
        state = state.upper()
        if state in rates:
            return Decimal(rates[state]["rate"])
        raise ValueError(f"未找到州 {state} 的税率")

    def calculate(self, order: Order, state: str = "CA") -> TaxResult:
        rate = self.get_state_rate(state)
        tax_lines: list[TaxLineItem] = []

        for item in order.items:
            taxable = item.subtotal
            tax_amount = calculate_tax(taxable, rate)

            tax_lines.append(TaxLineItem(
                item_name=item.name,
                taxable_amount=taxable,
                tax_type=TaxType.SALES_TAX,
                tax_rate=rate,
                tax_amount=tax_amount,
            ))

        total_tax = sum((line.tax_amount for line in tax_lines), Decimal("0"))

        return TaxResult(
            order_id=order.order_id,
            country=order.country,
            currency=order.currency,
            subtotal=order.items_total,
            shipping_cost=order.shipping_cost,
            total_before_tax=order.total_before_tax,
            tax_lines=tax_lines,
            total_tax=total_tax,
            total_with_tax=order.total_before_tax + total_tax,
        )
