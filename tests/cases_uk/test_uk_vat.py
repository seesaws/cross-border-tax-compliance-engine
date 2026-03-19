"""UK VAT 基础测试"""

from decimal import Decimal

from core.calculators import get_calculator
from core.models.tax_models import Country, Currency, Order, OrderItem, TaxType


class TestUKVAT:
    def test_standard_rate_20_percent(self):
        order = Order(
            order_id="UK-001",
            country=Country.UK,
            currency=Currency.GBP,
            items=[OrderItem(name="电子产品", quantity=1, unit_price=Decimal("100.00"))],
        )
        calc = get_calculator("UK")
        result = calc.calculate(order)

        assert result.total_tax == Decimal("20.00")
        assert result.total_with_tax == Decimal("120.00")
        assert result.tax_lines[0].tax_rate == Decimal("0.20")
        assert result.tax_lines[0].tax_type == TaxType.VAT

    def test_zero_rate(self):
        order = Order(
            order_id="UK-002",
            country=Country.UK,
            currency=Currency.GBP,
            items=[OrderItem(name="儿童服装", quantity=1, unit_price=Decimal("25.00"), category="zero")],
        )
        calc = get_calculator("UK")
        result = calc.calculate(order)

        assert result.total_tax == Decimal("0.00")
        assert result.total_with_tax == Decimal("25.00")

    def test_reduced_rate_5_percent(self):
        order = Order(
            order_id="UK-003",
            country=Country.UK,
            currency=Currency.GBP,
            items=[OrderItem(name="儿童安全座椅", quantity=1, unit_price=Decimal("200.00"), category="reduced")],
        )
        calc = get_calculator("UK")
        result = calc.calculate(order)

        assert result.total_tax == Decimal("10.00")
        assert result.total_with_tax == Decimal("210.00")

    def test_multiple_items_mixed_rates(self, sample_order_uk):
        calc = get_calculator("UK")
        result = calc.calculate(sample_order_uk)

        # 蓝牙耳机: 2 * 49.99 = 99.98, VAT 20% = 20.00
        # 儿童T恤: 15.00, VAT 0% = 0.00
        assert result.total_tax == Decimal("20.00")
        assert result.subtotal == Decimal("114.98")

    def test_factory_gb_alias(self):
        calc = get_calculator("GB")
        assert calc.country_code == "UK"
