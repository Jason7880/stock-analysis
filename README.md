# 股票数据分析系统

一个完整的 Python 股票数据分析程序，包含实时数据获取、技术指标分析、可视化、策略回测和价格预测。

## 功能特性

- ✅ **实时数据获取**: 使用 yfinance 获取实时和历史股票数据
- ✅ **技术指标分析**: SMA, EMA, RSI, MACD, 布林带, ATR 等
- ✅ **数据可视化**: 生成专业的技术分析图表
- ✅ **策略回测**: 支持多种交易策略回测
- ✅ **价格预测**: 使用机器学习预测未来价格

## 安装

```bash
pip install -r requirements.txt
```

## 快速开始

```python
from main import StockAnalysisSystem

# 创建分析系统
analysis = StockAnalysisSystem(
    ticker="AAPL",
    start_date="2023-01-01",
    end_date="2024-12-31"
)

# 运行完整分析
analysis.run_full_analysis()
```

## 使用示例

### 1. 获取股票数据

```python
from data_fetcher import StockDataFetcher

fetcher = StockDataFetcher()
data = fetcher.get_historical_data("AAPL", "2023-01-01", "2024-12-31")
```

### 2. 计算技术指标

```python
from technical_indicators import TechnicalIndicators

indicators = TechnicalIndicators(data)
indicators.calculate_all_indicators()
```

### 3. 数据可视化

```python
from visualization import Visualizer

visualizer = Visualizer(indicators.data)
visualizer.plot_all()
```

### 4. 策略回测

```python
from backtesting import BacktestEngine

backtester = BacktestEngine(indicators.data)
results = backtester.run_backtest(strategy='ma')
```

### 5. 价格预测

```python
from prediction import PredictionModel

predictor = PredictionModel(data)
predictions = predictor.predict(days=30)
```

## 支持的股票代码

- 美股: AAPL, MSFT, GOOGL, TSLA, META, NVDA 等
- 其他市场: 支持大多数国际股票代码

## 技术指标说明

| 指标 | 说明 | 用途 |
|------|------|------|
| SMA | 简单移动平均线 | 识别趋势 |
| EMA | 指数移动平均线 | 快速反应价格变化 |
| RSI | 相对强弱指数 | 超买超卖判断 |
| MACD | 移动平均收敛散离 | 趋势和动量分析 |
| 布林带 | 上下轨线 | 价格突破识别 |
| ATR | 平均真实波幅 | 波动率分析 |

## 交易策略

### 1. 移动平均线策略
- 当 EMA(12) > SMA(50) 时买入
- 当 EMA(12) <= SMA(50) 时卖出

### 2. RSI 策略
- 当 RSI < 30 时买入 (超卖)
- 当 RSI > 70 时卖出 (超买)

### 3. 布林带策略
- 当价格 < 布林带下轨时买入
- 当价格 > 布林带上轨时卖出

## 回测指标

- **总收益率**: 整个时期的收益百分比
- **年化收益率**: 换算成年化的收益率
- **最大回撤**: 最大的亏损幅度
- **夏普比率**: 风险调整后的收益
- **胜率**: 盈利交易的比例
- **交易次数**: 总交易笔数

## 注意事项

⚠️ **免责声明**: 本程序仅供学习和研究之用，不构成投资建议。交易有风险，投资需谨慎。

## 许可证

MIT License