"""CSV 文件读写处理器"""

from decimal import Decimal
from pathlib import Path

import pandas as pd

from core.models.tax_models import Country, Currency, Order, OrderItem


def read_orders_from_csv(file_path: str | Path) -> list[Order]:
    """从 CSV 文件读取订单列表

    CSV 模板列: order_id, country, currency, item_name, quantity, unit_price, hs_code, category, shipping_cost
    """
    df = pd.read_csv(file_path, dtype=str)
    df.columns = df.columns.str.strip().str.lower()

    orders: dict[str, dict] = {}
    for _, row in df.iterrows():
        oid = str(row["order_id"])
        if oid not in orders:
            orders[oid] = {
                "order_id": oid,
                "country": Country(row["country"].strip().upper()),
                "currency": Currency(row["currency"].strip().upper()),
                "items": [],
                "shipping_cost": Decimal(str(row.get("shipping_cost", "0") or "0")),
            }
        orders[oid]["items"].append(OrderItem(
            name=str(row["item_name"]),
            quantity=int(row.get("quantity", 1)),
            unit_price=Decimal(str(row["unit_price"])),
            hs_code=str(row.get("hs_code", "")),
            category=str(row.get("category", "standard") or "standard"),
        ))

    return [Order(**data) for data in orders.values()]


def write_results_to_csv(results: list[dict], output_path: str | Path) -> None:
    """将计算结果写入 CSV 文件"""
    df = pd.DataFrame(results)
    df.to_csv(output_path, index=False)
