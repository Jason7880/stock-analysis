import pandas as pd
import numpy as np

class TechnicalIndicators:
    def __init__(self, data):
        self.data = data.copy()
    
    def calculate_sma(self, period=20):
        """简单移动平均线 (SMA)"""
        self.data[f'SMA_{period}'] = self.data['Close'].rolling(window=period).mean()
        return self.data[f'SMA_{period}']
    
    def calculate_ema(self, period=20):
        """指数移动平均线 (EMA)"""
        self.data[f'EMA_{period}'] = self.data['Close'].ewm(span=period).mean()
        return self.data[f'EMA_{period}']
    
    def calculate_rsi(self, period=14):
        """相对强弱指数 (RSI)"""
        delta = self.data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        self.data[f'RSI_{period}'] = rsi
        return rsi
    
    def calculate_macd(self, fast=12, slow=26, signal=9):
        """MACD 指标"""
        ema_fast = self.data['Close'].ewm(span=fast).mean()
        ema_slow = self.data['Close'].ewm(span=slow).mean()
        macd = ema_fast - ema_slow
        signal_line = macd.ewm(span=signal).mean()
        histogram = macd - signal_line
        
        self.data['MACD'] = macd
        self.data['MACD_Signal'] = signal_line
        self.data['MACD_Hist'] = histogram
        return self.data[['MACD', 'MACD_Signal', 'MACD_Hist']]
    
    def calculate_bollinger_bands(self, period=20, std_dev=2):
        """布林带 (Bollinger Bands)"""
        sma = self.data['Close'].rolling(window=period).mean()
        std = self.data['Close'].rolling(window=period).std()
        
        upper_band = sma + (std * std_dev)
        lower_band = sma - (std * std_dev)
        
        self.data['BB_Upper'] = upper_band
        self.data['BB_Middle'] = sma
        self.data['BB_Lower'] = lower_band
        return self.data[['BB_Upper', 'BB_Middle', 'BB_Lower']]
    
    def calculate_atr(self, period=14):
        """平均真实波幅 (ATR)"""
        high_low = self.data['High'] - self.data['Low']
        high_close = abs(self.data['High'] - self.data['Close'].shift())
        low_close = abs(self.data['Low'] - self.data['Close'].shift())
        
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = ranges.max(axis=1)
        atr = true_range.rolling(period).mean()
        
        self.data[f'ATR_{period}'] = atr
        return atr
    
    def calculate_volume_ma(self, period=20):
        """成交量移动平均"""
        self.data[f'Volume_MA_{period}'] = self.data['Volume'].rolling(window=period).mean()
        return self.data[f'Volume_MA_{period}']
    
    def calculate_all_indicators(self):
        """计算所有指标"""
        self.calculate_sma(20)
        self.calculate_sma(50)
        self.calculate_ema(12)
        self.calculate_ema(26)
        self.calculate_rsi(14)
        self.calculate_macd()
        self.calculate_bollinger_bands()
        self.calculate_atr()
        self.calculate_volume_ma()
        return self.data