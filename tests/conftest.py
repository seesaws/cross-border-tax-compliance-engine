"""共享测试 fixtures"""

from decimal import Decimal

import pytest

from core.models.tax_models import Country, Currency, Order, OrderItem


@pytest.fixture
def sample_order_uk() -> Order:
    return Order(
        order_id="TEST-UK-001",
        country=Country.UK,
        currency=Currency.GBP,
        items=[
            OrderItem(name="蓝牙耳机", quantity=2, unit_price=Decimal("49.99"), category="standard"),
            OrderItem(name="儿童T恤", quantity=1, unit_price=Decimal("15.00"), category="zero"),
        ],
        shipping_cost=Decimal("5.00"),
    )


@pytest.fixture
def sample_order_us() -> Order:
    return Order(
        order_id="TEST-US-001",
        country=Country.US,
        currency=Currency.USD,
        items=[
            OrderItem(name="手机壳", quantity=3, unit_price=Decimal("12.99")),
        ],
        shipping_cost=Decimal("4.99"),
    )


@pytest.fixture
def sample_order_de() -> Order:
    return Order(
        order_id="TEST-DE-001",
        country=Country.DE,
        currency=Currency.EUR,
        items=[
            OrderItem(name="键盘", quantity=1, unit_price=Decimal("89.00"), category="standard"),
        ],
    )


@pytest.fixture
def sample_order_jp() -> Order:
    return Order(
        order_id="TEST-JP-001",
        country=Country.JP,
        currency=Currency.JPY,
        items=[
            OrderItem(name="抹茶粉", quantity=5, unit_price=Decimal("1200"), category="reduced"),
        ],
    )
