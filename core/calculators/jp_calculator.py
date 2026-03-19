"""日本消费税计算器"""

from decimal import Decimal

from core.calculators.base import BaseCalculator
from core.models.tax_models import Order, TaxLineItem, TaxResult, TaxType
from core.utils.decimal_calc import calculate_tax


class JPCalculator(BaseCalculator):
    country_code = "JP"
    rules_file = "jp.json"

    def calculate(self, order: Order) -> TaxResult:
        tax_lines: list[TaxLineItem] = []

        for item in order.items:
            category = item.category if item.category else "standard"
            rate = self.get_rate(category)
            taxable = item.subtotal
            tax_amount = calculate_tax(taxable, rate)

            tax_lines.append(TaxLineItem(
                item_name=item.name,
                taxable_amount=taxable,
                tax_type=TaxType.CONSUMPTION_TAX,
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
