"""CLI 命令行工具"""

from decimal import Decimal

import click

from core.calculators import get_calculator
from core.models.tax_models import Country, Currency, Order, OrderItem


@click.group()
def cli():
    """跨境财税合规计算引擎 CLI"""
    pass


@cli.command()
@click.option("--country", "-c", required=True, type=click.Choice(["UK", "DE", "US", "JP"], case_sensitive=False), help="目标国家")
@click.option("--amount", "-a", required=True, type=str, help="商品金额")
@click.option("--category", "-t", default="standard", help="税率类别 (standard/reduced/zero)")
@click.option("--state", "-s", default="CA", help="美国州代码 (仅 US 需要)")
@click.option("--currency", default=None, help="币种 (默认根据国家自动选择)")
def calc(country: str, amount: str, category: str, state: str, currency: str | None):
    """单笔税费计算"""
    country_code = country.upper()
    currency_map = {"UK": "GBP", "DE": "EUR", "US": "USD", "JP": "JPY"}
    cur = currency or currency_map.get(country_code, "USD")

    order = Order(
        order_id="CLI-001",
        country=Country(country_code),
        currency=Currency(cur),
        items=[OrderItem(name="商品", quantity=1, unit_price=Decimal(amount), category=category)],
    )

    calculator = get_calculator(country_code)
    if country_code == "US":
        result = calculator.calculate(order, state=state)
    else:
        result = calculator.calculate(order)

    click.echo(f"\n{'='*40}")
    click.echo(f"国家: {result.country.value}  币种: {result.currency.value}")
    click.echo(f"商品金额: {result.subtotal}")
    for line in result.tax_lines:
        click.echo(f"  {line.tax_type.value} ({line.tax_rate*100}%): {line.tax_amount}")
    click.echo(f"税费合计: {result.total_tax}")
    click.echo(f"含税总额: {result.total_with_tax}")
    click.echo(f"{'='*40}\n")


@cli.command()
@click.option("--input", "-i", "input_file", required=True, type=click.Path(exists=True), help="输入文件路径 (Excel/CSV)")
@click.option("--output", "-o", "output_file", default=None, help="输出文件路径")
@click.option("--state", "-s", default="CA", help="美国州代码 (仅 US 订单需要)")
def batch(input_file: str, output_file: str | None, state: str):
    """批量订单税费计算"""
    from pathlib import Path

    file_path = Path(input_file)
    if file_path.suffix == ".csv":
        from connectors.csv_handler import read_orders_from_csv
        orders = read_orders_from_csv(file_path)
    else:
        from connectors.excel_handler import read_orders_from_excel
        orders = read_orders_from_excel(file_path)

    results = []
    for order in orders:
        calculator = get_calculator(order.country.value)
        if order.country.value == "US":
            result = calculator.calculate(order, state=state)
        else:
            result = calculator.calculate(order)
        results.append({
            "order_id": result.order_id,
            "country": result.country.value,
            "subtotal": str(result.subtotal),
            "total_tax": str(result.total_tax),
            "total_with_tax": str(result.total_with_tax),
        })
        click.echo(f"[{result.order_id}] {result.country.value}: 税费 {result.total_tax}, 含税 {result.total_with_tax}")

    if output_file:
        out = Path(output_file)
        if out.suffix == ".csv":
            from connectors.csv_handler import write_results_to_csv
            write_results_to_csv(results, out)
        else:
            from connectors.excel_handler import write_results_to_excel
            write_results_to_excel(results, out)
        click.echo(f"\n结果已导出至: {output_file}")


if __name__ == "__main__":
    cli()
