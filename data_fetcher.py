import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

class StockDataFetcher:
    def __init__(self):
        self.data = None
    
    def get_historical_data(self, ticker, start_date, end_date):
        """
        获取股票历史数据
        
        参数:
            ticker: 股票代码 (如 'AAPL')
            start_date: 开始日期 (如 '2023-01-01')
            end_date: 结束日期 (如 '2024-12-31')
        
        返回:
            DataFrame: 包含 OHLCV 数据的数据框
        """
        try:
            data = yf.download(
                ticker,
                start=start_date,
                end=end_date,
                progress=False
            )
            
            if data.empty:
                raise ValueError(f"无法获取 {ticker} 的数据")
            
            self.data = data.copy()
            return self.data
        
        except Exception as e:
            print(f"数据获取失败: {str(e)}")
            return None
    
    def get_realtime_price(self, ticker):
        """获取实时价格"""
        try:
            data = yf.Ticker(ticker)
            current_price = data.info.get('currentPrice', 'N/A')
            return current_price
        except Exception as e:
            print(f"获取实时价格失败: {str(e)}")
            return None
    
    def get_multiple_stocks(self, tickers, start_date, end_date):
        """获取多个股票数据"""
        result = {}
        for ticker in tickers:
            result[ticker] = self.get_historical_data(ticker, start_date, end_date)
        return result