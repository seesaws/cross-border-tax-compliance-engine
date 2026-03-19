"""FastAPI REST API — 跨境财税合规计算引擎"""

from decimal import Decimal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from core.calculators import get_calculator
from core.models.tax_models import Country, Currency, Order, OrderItem, TaxType

app = FastAPI(
    title="跨境财税合规计算引擎 API",
    description="开源跨境税务计算 REST API — 支持英/德/美/日多国税制",
    version="0.1.0",
)


# ── Request / Response 模型 ──────────────────────────────────────────

class ItemRequest(BaseModel):
    name: str = "商品"
    quantity: int = Field(gt=0, default=1)
    unit_price: str = Field(description="金额字符串，如 '99.99'")
    category: str = "standard"
    hs_code: str = ""


class CalcRequest(BaseModel):
    order_id: str = "API-001"
    country: str = Field(description="国家代码: UK / DE / US / JP")
    currency: str | None = Field(default=None, description="币种，留空自动匹配")
    items: list[ItemRequest]
    shipping_cost: str = "0"
    state: str = Field(default="CA", description="美国州代码（仅 US 需要）")


class TaxLineResponse(BaseModel):
    item_name: str
    taxable_amount: str
    tax_type: str
    tax_rate: str
    tax_amount: str


class CalcResponse(BaseModel):
    order_id: str
    country: str
    currency: str
    subtotal: str
    shipping_cost: str
    total_before_tax: str
    tax_lines: list[TaxLineResponse]
    total_tax: str
    total_with_tax: str


class RateDetail(BaseModel):
    rate: str
    description: str


class RatesResponse(BaseModel):
    country: str
    tax_type: str
    currency: str
    rates: dict[str, RateDetail]


# ── 工具函数 ─────────────────────────────────────────────────────────

CURRENCY_MAP = {"UK": "GBP", "GB": "GBP", "DE": "EUR", "US": "USD", "JP": "JPY"}


def _build_order(req: CalcRequest) -> Order:
    code = req.country.upper()
    cur = req.currency or CURRENCY_MAP.get(code, "USD")
    return Order(
        order_id=req.order_id,
        country=Country(code if code != "GB" else "UK"),
        currency=Currency(cur),
        items=[
            OrderItem(
                name=i.name,
                quantity=i.quantity,
                unit_price=Decimal(i.unit_price),
                category=i.category,
                hs_code=i.hs_code,
            )
            for i in req.items
        ],
        shipping_cost=Decimal(req.shipping_cost),
    )


def _to_response(result) -> CalcResponse:
    return CalcResponse(
        order_id=result.order_id,
        country=result.country.value,
        currency=result.currency.value,
        subtotal=str(result.subtotal),
        shipping_cost=str(result.shipping_cost),
        total_before_tax=str(result.total_before_tax),
        tax_lines=[
            TaxLineResponse(
                item_name=l.item_name,
                taxable_amount=str(l.taxable_amount),
                tax_type=l.tax_type.value,
                tax_rate=str(l.tax_rate),
                tax_amount=str(l.tax_amount),
            )
            for l in result.tax_lines
        ],
        total_tax=str(result.total_tax),
        total_with_tax=str(result.total_with_tax),
    )


# ── 路由 ─────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/countries")
def list_countries():
    """获取支持的国家列表"""
    return {
        "countries": [
            {"code": "UK", "name": "英国", "tax_type": "VAT"},
            {"code": "DE", "name": "德国", "tax_type": "VAT"},
            {"code": "US", "name": "美国", "tax_type": "SALES_TAX"},
            {"code": "JP", "name": "日本", "tax_type": "CONSUMPTION_TAX"},
        ]
    }


@app.get("/api/rates/{country}", response_model=RatesResponse)
def get_rates(country: str):
    """查询指定国家的税率规则"""
    try:
        calc = get_calculator(country)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    rules = calc.rules
    return RatesResponse(
        country=rules["country"],
        tax_type=rules["tax_type"],
        currency=rules["currency"],
        rates={k: RateDetail(**v) for k, v in rules["rates"].items()},
    )


@app.post("/api/calculate", response_model=CalcResponse)
def calculate(req: CalcRequest):
    """单笔订单税费计算"""
    try:
        order = _build_order(req)
        calc = get_calculator(req.country)
        if req.country.upper() in ("US",):
            result = calc.calculate(order, state=req.state)
        else:
            result = calc.calculate(order)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return _to_response(result)


@app.post("/api/batch", response_model=list[CalcResponse])
def batch_calculate(orders: list[CalcRequest]):
    """批量订单税费计算"""
    results = []
    for req in orders:
        try:
            order = _build_order(req)
            calc = get_calculator(req.country)
            if req.country.upper() in ("US",):
                result = calc.calculate(order, state=req.state)
            else:
                result = calc.calculate(order)
            results.append(_to_response(result))
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"订单 {req.order_id}: {e}")
    return results
