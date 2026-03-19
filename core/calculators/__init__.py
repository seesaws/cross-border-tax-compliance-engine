from core.calculators.uk_calculator import UKCalculator
from core.calculators.de_calculator import DECalculator
from core.calculators.us_calculator import USCalculator
from core.calculators.jp_calculator import JPCalculator


_CALCULATORS = {
    "UK": UKCalculator,
    "GB": UKCalculator,
    "DE": DECalculator,
    "US": USCalculator,
    "JP": JPCalculator,
}


def get_calculator(country_code: str):
    """工厂函数：根据国家代码返回对应的税务计算器实例"""
    code = country_code.upper()
    if code not in _CALCULATORS:
        raise ValueError(f"不支持的国家代码: {code}，当前支持: {list(_CALCULATORS.keys())}")
    return _CALCULATORS[code]()
