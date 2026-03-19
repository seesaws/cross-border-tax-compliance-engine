"""跨境税务核心数据模型"""

from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, Field


class Country(str, Enum):
    UK = "UK"
    DE = "DE"
    US = "US"
    JP = "JP"


class Currency(str, Enum):
    GBP = "GBP"
    EUR = "EUR"
    USD = "USD"
    JPY = "JPY"
    CNY = "CNY"


class TaxType(str, Enum):
    VAT = "VAT"
    GST = "GST"
    SALES_TAX = "SALES_TAX"
    CONSUMPTION_TAX = "CONSUMPTION_TAX"


class TaxRate(BaseModel):
    country: Country
    tax_type: TaxType
    rate: Decimal = Field(ge=0, le=1, description="税率，如 0.20 表示 20%")
    category: str = "standard"
    description: str = ""


class OrderItem(BaseModel):
    name: str
    quantity: int = Field(gt=0)
    unit_price: Decimal = Field(gt=0)
    hs_code: str = ""
    category: str = "standard"

    @property
    def subtotal(self) -> Decimal:
        return self.unit_price * self.quantity


class Order(BaseModel):
    order_id: str
    country: Country
    currency: Currency
    items: list[OrderItem]
    shipping_cost: Decimal = Decimal("0")

    @property
    def items_total(self) -> Decimal:
        return sum((item.subtotal for item in self.items), Decimal("0"))

    @property
    def total_before_tax(self) -> Decimal:
        return self.items_total + self.shipping_cost


class TaxLineItem(BaseModel):
    item_name: str
    taxable_amount: Decimal
    tax_type: TaxType
    tax_rate: Decimal
    tax_amount: Decimal


class TaxResult(BaseModel):
    order_id: str
    country: Country
    currency: Currency
    subtotal: Decimal
    shipping_cost: Decimal
    total_before_tax: Decimal
    tax_lines: list[TaxLineItem]
    total_tax: Decimal
    total_with_tax: Decimal
