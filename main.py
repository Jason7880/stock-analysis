import pandas as pd
from data_fetcher import StockDataFetcher
from technical_indicators import TechnicalIndicators
from visualization import Visualizer
from backtesting import BacktestEngine
from prediction import PredictionModel
import warnings
warnings.filterwarnings('ignore')

class StockAnalysisSystem:
    def __init__(self, ticker, start_date, end_date):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.data = None
        self.indicators = None
        
    def fetch_data(self):
        """获取实时股票数据"""
        print(f"正在获取 {self.ticker} 的股票数据...")
        fetcher = StockDataFetcher()
        self.data = fetcher.get_historical_data(
            self.ticker, 
            self.start_date, 
            self.end_date
        )
        print(f"成功获取 {len(self.data)} 条数据")
        return self.data
    
    def analyze_indicators(self):
        """计算技术指标"""
        print("正在计算技术指标...")
        analyzer = TechnicalIndicators(self.data)
        self.indicators = analyzer.calculate_all_indicators()
        return self.indicators
    
    def visualize(self):
        """数据可视化"""
        print("正在生成可视化图表...")
        visualizer = Visualizer(self.indicators)
        visualizer.plot_all()
    
    def backtest(self, strategy_params=None):
        """策略回测"""
        print("正在执行回测...")
        backtester = BacktestEngine(self.indicators)
        results = backtester.run_backtest(strategy_params)
        return results
    
    def predict(self, days=30):
        """预测模型"""
        print(f"正在预测未来 {days} 天的股价...")
        predictor = PredictionModel(self.data)
        predictions = predictor.predict(days)
        return predictions
    
    def run_full_analysis(self):
        """运行完整分析流程"""
        self.fetch_data()
        self.analyze_indicators()
        self.visualize()
        backtest_results = self.backtest()
        predictions = self.predict()
        
        print("\n" + "="*50)
        print("分析完成！")
        print("="*50)
        print(f"\n回测结果：\n{backtest_results}")
        print(f"\n预测结果（未来30天）：\n{predictions}")

if __name__ == "__main__":
    # 示例：分析苹果股票
    analysis = StockAnalysisSystem(
        ticker="AAPL",
        start_date="2023-01-01",
        end_date="2024-12-31"
    )
    
    # 运行完整分析
    analysis.run_full_analysis()