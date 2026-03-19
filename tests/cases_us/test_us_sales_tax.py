"""US Sales Tax 基础测试"""

from decimal import Decimal

from core.calculators import get_calculator
from core.models.tax_models import Country, Currency, Order, OrderItem, TaxType


class TestUSSalesTax:
    def test_california_7_25_percent(self):
        order = Order(
            order_id="US-001",
            country=Country.US,
            currency=Currency.USD,
            items=[OrderItem(name="手机壳", quantity=1, unit_price=Decimal("100.00"))],
        )
        calc = get_calculator("US")
        result = calc.calculate(order, state="CA")

        assert result.total_tax == Decimal("7.25")
        assert result.total_with_tax == Decimal("107.25")
        assert result.tax_lines[0].tax_type == TaxType.SALES_TAX

    def test_texas_6_25_percent(self):
        order = Order(
            order_id="US-002",
            country=Country.US,
            currency=Currency.USD,
            items=[OrderItem(name="书包", quantity=2, unit_price=Decimal("50.00"))],
        )
        calc = get_calculator("US")
        result = calc.calculate(order, state="TX")

        # 2 * 50 = 100, tax 6.25% = 6.25
        assert result.total_tax == Decimal("6.25")
        assert result.total_with_tax == Decimal("106.25")

    def test_multiple_items(self, sample_order_us):
        calc = get_calculator("US")
        result = calc.calculate(sample_order_us, state="CA")

        # 3 * 12.99 = 38.97, tax 7.25% = 2.83
        assert result.subtotal == Decimal("38.97")
        assert result.total_tax == Decimal("2.83")

    def test_invalid_state_raises(self):
        import pytest

        calc = get_calculator("US")
        order = Order(
            order_id="US-ERR",
            country=Country.US,
            currency=Currency.USD,
            items=[OrderItem(name="test", quantity=1, unit_price=Decimal("10"))],
        )
        with pytest.raises(ValueError, match="未找到州"):
            calc.calculate(order, state="ZZ")
