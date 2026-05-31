import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle
import numpy as np
import pandas as pd

class Visualizer:
    def __init__(self, data):
        self.data = data
        self.data.index = pd.to_datetime(self.data.index)
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 中文字体
        plt.rcParams['axes.unicode_minus'] = False
    
    def plot_price_with_ma(self):
        """绘制价格和移动平均线"""
        fig, ax = plt.subplots(figsize=(14, 6))
        
        ax.plot(self.data.index, self.data['Close'], label='收盘价', linewidth=2, color='black')
        ax.plot(self.data.index, self.data['SMA_20'], label='SMA 20', alpha=0.7)
        ax.plot(self.data.index, self.data['SMA_50'], label='SMA 50', alpha=0.7)
        ax.plot(self.data.index, self.data['EMA_12'], label='EMA 12', alpha=0.7)
        
        ax.set_title('股价与移动平均线', fontsize=14, fontweight='bold')
        ax.set_xlabel('日期')
        ax.set_ylabel('价格 (USD)')
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)
        fig.tight_layout()
        plt.savefig('price_ma.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_bollinger_bands(self):
        """绘制布林带"""
        fig, ax = plt.subplots(figsize=(14, 6))
        
        ax.plot(self.data.index, self.data['Close'], label='收盘价', color='black', linewidth=2)
        ax.fill_between(
            self.data.index,
            self.data['BB_Upper'],
            self.data['BB_Lower'],
            alpha=0.2,
            color='blue',
            label='布林带'
        )
        ax.plot(self.data.index, self.data['BB_Upper'], color='red', alpha=0.5, linestyle='--')
        ax.plot(self.data.index, self.data['BB_Lower'], color='red', alpha=0.5, linestyle='--')
        
        ax.set_title('布林带分析', fontsize=14, fontweight='bold')
        ax.set_xlabel('日期')
        ax.set_ylabel('价格 (USD)')
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)
        fig.tight_layout()
        plt.savefig('bollinger_bands.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_rsi(self):
        """绘制 RSI 指标"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8))
        
        # 价格图
        ax1.plot(self.data.index, self.data['Close'], color='black', linewidth=2)
        ax1.set_ylabel('价格 (USD)')
        ax1.set_title('RSI 分析', fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        
        # RSI 图
        ax2.plot(self.data.index, self.data['RSI_14'], color='blue', linewidth=2)
        ax2.axhline(y=70, color='r', linestyle='--', alpha=0.5, label='超买 (70)')
        ax2.axhline(y=30, color='g', linestyle='--', alpha=0.5, label='超卖 (30)')
        ax2.fill_between(self.data.index, 70, 100, alpha=0.1, color='red')
        ax2.fill_between(self.data.index, 0, 30, alpha=0.1, color='green')
        ax2.set_ylabel('RSI 值')
        ax2.set_xlabel('日期')
        ax2.set_ylim(0, 100)
        ax2.legend(loc='best')
        ax2.grid(True, alpha=0.3)
        
        fig.tight_layout()
        plt.savefig('rsi.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_macd(self):
        """绘制 MACD 指标"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8))
        
        # 价格图
        ax1.plot(self.data.index, self.data['Close'], color='black', linewidth=2)
        ax1.set_ylabel('价格 (USD)')
        ax1.set_title('MACD 分析', fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        
        # MACD 图
        ax2.plot(self.data.index, self.data['MACD'], label='MACD', color='blue', linewidth=2)
        ax2.plot(self.data.index, self.data['MACD_Signal'], label='信号线', color='red', linewidth=2)
        colors = ['green' if x > 0 else 'red' for x in self.data['MACD_Hist']]
        ax2.bar(self.data.index, self.data['MACD_Hist'], label='柱状图', color=colors, alpha=0.3)
        ax2.set_ylabel('MACD 值')
        ax2.set_xlabel('日期')
        ax2.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        ax2.legend(loc='best')
        ax2.grid(True, alpha=0.3)
        
        fig.tight_layout()
        plt.savefig('macd.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_volume(self):
        """绘制成交量"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8))
        
        # 价格图
        ax1.plot(self.data.index, self.data['Close'], color='black', linewidth=2)
        ax1.set_ylabel('价格 (USD)')
        ax1.set_title('成交量分析', fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        
        # 成交量图
        colors = ['green' if self.data['Close'].iloc[i] > self.data['Open'].iloc[i] else 'red' 
                 for i in range(len(self.data))]
        ax2.bar(self.data.index, self.data['Volume'], color=colors, alpha=0.6)
        ax2.plot(self.data.index, self.data['Volume_MA_20'], color='blue', 
                linewidth=2, label='成交量MA20')
        ax2.set_ylabel('成交量')
        ax2.set_xlabel('日期')
        ax2.legend(loc='best')
        ax2.grid(True, alpha=0.3)
        
        fig.tight_layout()
        plt.savefig('volume.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_all(self):
        """绘制所有图表"""
        self.plot_price_with_ma()
        self.plot_bollinger_bands()
        self.plot_rsi()
        self.plot_macd()
        self.plot_volume()