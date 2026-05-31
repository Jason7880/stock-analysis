import pandas as pd
import numpy as np

class BacktestEngine:
    def __init__(self, data):
        self.data = data.copy()
        self.trades = []
        self.initial_capital = 10000
        self.position = 0
        self.cash = self.initial_capital
    
    def moving_average_strategy(self):
        """简单移动平均线策略"""
        self.data['Signal'] = 0
        
        # 生成交易信号：EMA12 > SMA50 时买入，反之卖出
        self.data.loc[self.data['EMA_12'] > self.data['SMA_50'], 'Signal'] = 1
        self.data.loc[self.data['EMA_12'] <= self.data['SMA_50'], 'Signal'] = 0
        
        # 计算位置变化
        self.data['Position'] = self.data['Signal'].diff()
        return self.data
    
    def rsi_strategy(self):
        """RSI 策略"""
        self.data['Signal'] = 0
        
        # RSI < 30 买入，RSI > 70 卖出
        self.data.loc[self.data['RSI_14'] < 30, 'Signal'] = 1
        self.data.loc[self.data['RSI_14'] > 70, 'Signal'] = 0
        
        self.data['Position'] = self.data['Signal'].diff()
        return self.data
    
    def bollinger_bands_strategy(self):
        """布林带策略"""
        self.data['Signal'] = 0
        
        # 价格触及下轨买入，触及上轨卖出
        self.data.loc[self.data['Close'] < self.data['BB_Lower'], 'Signal'] = 1
        self.data.loc[self.data['Close'] > self.data['BB_Upper'], 'Signal'] = 0
        
        self.data['Position'] = self.data['Signal'].diff()
        return self.data
    
    def calculate_returns(self):
        """计算收益"""
        self.data['Daily_Return'] = self.data['Close'].pct_change()
        self.data['Strategy_Return'] = self.data['Position'].shift(1) * self.data['Daily_Return']
        return self.data
    
    def calculate_metrics(self):
        """计算回测指标"""
        # 累积收益
        self.data['Cumulative_Return'] = (1 + self.data['Strategy_Return']).cumprod()
        
        # 总收益率
        total_return = (self.data['Cumulative_Return'].iloc[-1] - 1) * 100
        
        # 年化收益率
        days = len(self.data)
        years = days / 252
        annualized_return = ((self.data['Cumulative_Return'].iloc[-1] ** (1/years)) - 1) * 100
        
        # 最大回撤
        running_max = self.data['Cumulative_Return'].expanding().max()
        drawdown = (self.data['Cumulative_Return'] - running_max) / running_max
        max_drawdown = drawdown.min() * 100
        
        # 夏普比率
        sharpe_ratio = (self.data['Strategy_Return'].mean() / self.data['Strategy_Return'].std()) * np.sqrt(252)
        
        # 胜率
        positive_returns = (self.data['Strategy_Return'] > 0).sum()
        total_trades = (self.data['Strategy_Return'] != 0).sum()
        win_rate = (positive_returns / total_trades * 100) if total_trades > 0 else 0
        
        return {
            '总收益率 (%)': total_return,
            '年化收益率 (%)': annualized_return,
            '最大回撤 (%)': max_drawdown,
            '夏普比率': sharpe_ratio,
            '胜率 (%)': win_rate,
            '交易次数': total_trades
        }
    
    def run_backtest(self, strategy='ma'):
        """运行回测"""
        if strategy == 'ma':
            self.moving_average_strategy()
        elif strategy == 'rsi':
            self.rsi_strategy()
        elif strategy == 'bb':
            self.bollinger_bands_strategy()
        
        self.calculate_returns()
        metrics = self.calculate_metrics()
        
        return pd.DataFrame([metrics]).to_string()