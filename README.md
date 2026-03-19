# 跨境财税合规计算引擎

开源跨境税务计算引擎 — 本地优先，数据不出境，规则透明可信。

## 功能特性

- 多国税制支持：英国 VAT、德国 VAT、美国 Sales Tax、日本消费税
- 高精度计算：基于 `Decimal` 类型，杜绝浮点误差
- JSON 规则热加载：自定义税率无需改代码
- Excel/CSV 批量导入导出
- CLI 命令行 + Streamlit Web 界面
- Docker 一键部署

## 快速开始

```bash
# 安装
pip install -e ".[dev]"

# 单笔计算
tax-calc calc --country UK --amount 100

# 批量计算
tax-calc batch --input orders.xlsx --output results.xlsx

# 启动 Web 界面
streamlit run interface/web/app.py

# Docker 部署
docker-compose up
```

## CLI 用法

```bash
# 英国 VAT 标准税率
tax-calc calc -c UK -a 100

# 德国 VAT 减免税率
tax-calc calc -c DE -a 200 -t reduced

# 美国德州销售税
tax-calc calc -c US -a 50 -s TX

# 日本消费税（食品轻减税率）
tax-calc calc -c JP -a 1000 -t reduced

# 批量导入 CSV 并导出结果
tax-calc batch -i orders.csv -o results.csv
```

## 项目结构

```
├── core/                  # 核心计算引擎
│   ├── calculators/       # 各国计算器 (UK, DE, US, JP)
│   ├── models/            # Pydantic 数据模型
│   ├── utils/             # 汇率、精度工具
│   └── rules/             # 税率规则 JSON
├── connectors/            # Excel/CSV 读写
├── ee/                    # 企业版功能 (预留)
├── interface/
│   ├── cli/               # Click 命令行
│   └── web/               # Streamlit 网页
├── tests/                 # 测试用例
├── Dockerfile
└── docker-compose.yml
```

## 许可证

本项目采用双重许可模式：
- 开源版：MIT License（见 LICENSE-MIT）
- 商业版：Commercial License（见 LICENSE-COMMERCIAL）

## 免责声明

⚠️ 本工具计算结果仅供参考，正式申报请以官方税务师意见为准。税率数据可能因政策调整而变化，请以各国税务机关最新公告为准。
