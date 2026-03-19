"""抽象基类：所有国家计算器的基础"""

import json
from abc import ABC, abstractmethod
from decimal import Decimal
from pathlib import Path

from core.models.tax_models import Order, TaxResult


class BaseCalculator(ABC):
    """税务计算器抽象基类"""

    country_code: str = ""
    rules_file: str = ""

    def __init__(self):
        self.rules = self._load_rules()

    def _load_rules(self) -> dict:
        rules_dir = Path(__file__).parent.parent / "rules"
        rules_path = rules_dir / self.rules_file
        with open(rules_path, encoding="utf-8") as f:
            return json.load(f)

    def get_rate(self, category: str = "standard") -> Decimal:
        """获取指定类别的税率"""
        rates = self.rules.get("rates", {})
        if category in rates:
            return Decimal(rates[category]["rate"])
        # US 按州查找
        if category in rates:
            return Decimal(rates[category]["rate"])
        return Decimal(rates.get("standard", {}).get("rate", "0"))

    def get_standard_rate(self) -> Decimal:
        return self.get_rate("standard")

    @abstractmethod
    def calculate(self, order: Order) -> TaxResult:
        """计算订单税费，子类必须实现"""
        ...
