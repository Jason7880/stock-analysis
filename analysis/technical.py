"""
技术分析模块
实现常见的技术指标计算
"""

import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)


class TechnicalAnalysis:
    """技术分析类"""
    
    @staticmethod
    def calculate_ma(df: pd.DataFrame, periods: list = [5, 10, 20, 60]) -> pd.DataFrame:
        """计算移动平均线 (MA)"""
        df = df.copy()
        for period in periods:
            df[f'MA{period}'] = df['收盘价'].rolling(window=period).mean()
        return df
    
    @staticmethod
    def calculate_ema(df: pd.DataFrame, periods: list = [12, 26]) -> pd.DataFrame:
        """计算指数移动平均线 (EMA)"""
        df = df.copy()
        for period in periods:
            df[f'EMA{period}'] = df['收盘价'].ewm(span=period, adjust=False).mean()
        return df
    
    @staticmethod
    def calculate_rsi(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
        """计算相对强弱指数 (RSI)"""
        df = df.copy()
        delta = df['收盘价'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        return df
    
    @staticmethod
    def calculate_macd(df: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
        """计算MACD指标"""
        df = df.copy()
        ema_fast = df['收盘价'].ewm(span=fast, adjust=False).mean()
        ema_slow = df['收盘价'].ewm(span=slow, adjust=False).mean()
        df['DIF'] = ema_fast - ema_slow
        df['DEA'] = df['DIF'].ewm(span=signal, adjust=False).mean()
        df['MACD'] = 2 * (df['DIF'] - df['DEA'])
        return df
    
    @staticmethod
    def calculate_kdj(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
        """计算KDJ指标"""
        df = df.copy()
        high_max = df['最高价'].rolling(window=period).max()
        low_min = df['最低价'].rolling(window=period).min()
        rsv = 100 * (df['收盘价'] - low_min) / (high_max - low_min)
        df['K'] = rsv.ewm(span=3, adjust=False).mean()
        df['D'] = df['K'].ewm(span=3, adjust=False).mean()
        df['J'] = 3 * df['K'] - 2 * df['D']
        return df
    
    @staticmethod
    def calculate_bollinger_bands(df: pd.DataFrame, period: int = 20, std_dev: float = 2) -> pd.DataFrame:
        """计算布林带"""
        df = df.copy()
        sma = df['收盘价'].rolling(window=period).mean()
        std = df['收盘价'].rolling(window=period).std()
        df['BB_MIDDLE'] = sma
        df['BB_UPPER'] = sma + (std * std_dev)
        df['BB_LOWER'] = sma - (std * std_dev)
        return df
    
    @staticmethod
    def calculate_atr(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
        """计算平均真实波幅 (ATR)"""
        df = df.copy()
        high_low = df['最高价'] - df['最低价']
        high_close = abs(df['最高价'] - df['收盘价'].shift())
        low_close = abs(df['最低价'] - df['收盘价'].shift())
        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        df['ATR'] = tr.rolling(window=period).mean()
        return df
    
    @staticmethod
    def generate_signals(df: pd.DataFrame) -> pd.DataFrame:
        """生成技术面交易信号"""
        df = df.copy()
        df['Signal'] = 0
        
        if 'MACD' in df.columns and 'DEA' in df.columns:
            df.loc[df['DIF'] > df['DEA'], 'MACD_Signal'] = 1
            df.loc[df['DIF'] < df['DEA'], 'MACD_Signal'] = -1
        
        if 'RSI' in df.columns:
            df.loc[df['RSI'] > 70, 'RSI_Signal'] = -1
            df.loc[df['RSI'] < 30, 'RSI_Signal'] = 1
        
        if 'K' in df.columns and 'D' in df.columns:
            df.loc[df['K'] > df['D'], 'KDJ_Signal'] = 1
            df.loc[df['K'] < df['D'], 'KDJ_Signal'] = -1
        
        return df


def analyze_stock(df: pd.DataFrame) -> pd.DataFrame:
    """完整的技术面分析流程"""
    ta = TechnicalAnalysis()
    df = ta.calculate_ma(df)
    df = ta.calculate_ema(df)
    df = ta.calculate_rsi(df)
    df = ta.calculate_macd(df)
    df = ta.calculate_kdj(df)
    df = ta.calculate_bollinger_bands(df)
    df = ta.calculate_atr(df)
    df = ta.generate_signals(df)
    return df
