"""
数据可视化模块 - 使用 Plotly 生成交互式图表
"""

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import logging

logger = logging.getLogger(__name__)


class StockCharts:
    """股票图表类"""
    
    @staticmethod
    def create_candlestick_chart(df: pd.DataFrame, symbol: str = "", title: str = "", show_ma: bool = True) -> go.Figure:
        """创建K线图"""
        try:
            fig = go.Figure()
            
            fig.add_trace(go.Candlestick(
                x=df['日期'],
                open=df['开盘价'],
                high=df['最高价'],
                low=df['最低价'],
                close=df['收盘价'],
                name='K线',
                increasing_line_color='#ec0000',
                decreasing_line_color='#00ab29'
            ))
            
            if show_ma:
                for ma_col in ['MA5', 'MA10', 'MA20', 'MA60']:
                    if ma_col in df.columns:
                        colors = {'MA5': '#ffb800', 'MA10': '#ff6b00', 'MA20': '#0096ff', 'MA60': '#c000ff'}
                        fig.add_trace(go.Scatter(
                            x=df['日期'],
                            y=df[ma_col],
                            name=ma_col,
                            line=dict(color=colors.get(ma_col, '#000000'), width=1),
                            mode='lines'
                        ))
            
            title = title or f"{symbol} K线图"
            fig.update_layout(
                title=title,
                yaxis_title='价格 (元)',
                xaxis_title='日期',
                template='plotly_white',
                xaxis_rangeslider_visible=False,
                height=600,
                hovermode='x unified',
                font=dict(family="SimHei, monospace")
            )
            
            return fig
        except Exception as e:
            logger.error(f"生成K线图失败: {e}")
            return None
    
    @staticmethod
    def create_macd_chart(df: pd.DataFrame, symbol: str = "") -> go.Figure:
        """创建MACD指标图表"""
        try:
            fig = make_subplots(specs=[[{"secondary_y": False}]])
            
            fig.add_trace(go.Scatter(
                x=df['日期'],
                y=df['收盘价'],
                name='收盘价',
                line=dict(color='#0096ff', width=2)
            ))
            
            fig.add_trace(go.Scatter(
                x=df['日期'],
                y=df['DIF'],
                name='DIF',
                line=dict(color='#ffb800', width=1),
                secondary_y=True
            ))
            
            fig.add_trace(go.Scatter(
                x=df['日期'],
                y=df['DEA'],
                name='DEA',
                line=dict(color='#ff6b00', width=1),
                secondary_y=True
            ))
            
            colors = ['#ec0000' if val > 0 else '#00ab29' for val in df['MACD']]
            fig.add_trace(go.Bar(
                x=df['日期'],
                y=df['MACD'],
                name='MACD',
                marker=dict(color=colors),
                secondary_y=True
            ))
            
            fig.update_layout(
                title=f"{symbol} MACD指标",
                yaxis_title='价格 (元)',
                template='plotly_white',
                height=600,
                hovermode='x unified',
                font=dict(family="SimHei, monospace")
            )
            
            return fig
        except Exception as e:
            logger.error(f"生成MACD图表失败: {e}")
            return None
    
    @staticmethod
    def create_rsi_chart(df: pd.DataFrame, symbol: str = "") -> go.Figure:
        """创建RSI指标图表"""
        try:
            fig = make_subplots(
                rows=2, cols=1,
                shared_xaxes=True,
                vertical_spacing=0.1,
                row_heights=[0.7, 0.3]
            )
            
            fig.add_trace(go.Candlestick(
                x=df['日期'],
                open=df['开盘价'],
                high=df['最高价'],
                low=df['最低价'],
                close=df['收盘价'],
                name='K线'
            ), row=1, col=1)
            
            fig.add_trace(go.Scatter(
                x=df['日期'],
                y=df['RSI'],
                name='RSI',
                line=dict(color='#0096ff', width=2)
            ), row=2, col=1)
            
            fig.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="超买(70)", row=2, col=1)
            fig.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="超卖(30)", row=2, col=1)
            
            fig.update_layout(
                title=f"{symbol} RSI指标",
                template='plotly_white',
                height=700,
                hovermode='x unified',
                font=dict(family="SimHei, monospace")
            )
            
            fig.update_yaxes(title_text="价格 (元)", row=1, col=1)
            fig.update_yaxes(title_text="RSI", row=2, col=1)
            
            return fig
        except Exception as e:
            logger.error(f"生成RSI图表失败: {e}")
            return None
    
    @staticmethod
    def create_volume_chart(df: pd.DataFrame, symbol: str = "") -> go.Figure:
        """创建成交量图表"""
        try:
            fig = make_subplots(
                rows=2, cols=1,
                shared_xaxes=True,
                vertical_spacing=0.1,
                row_heights=[0.7, 0.3]
            )
            
            fig.add_trace(go.Candlestick(
                x=df['日期'],
                open=df['开盘价'],
                high=df['最高价'],
                low=df['最低价'],
                close=df['收盘价'],
                name='K线'
            ), row=1, col=1)
            
            colors = ['#ec0000' if df['收盘价'].iloc[i] >= df['开盘价'].iloc[i] else '#00ab29' for i in range(len(df))]
            
            fig.add_trace(go.Bar(
                x=df['日期'],
                y=df['成交量'],
                name='成交量',
                marker=dict(color=colors)
            ), row=2, col=1)
            
            fig.update_layout(
                title=f"{symbol} 成交量分析",
                template='plotly_white',
                height=700,
                hovermode='x unified',
                font=dict(family="SimHei, monospace")
            )
            
            fig.update_yaxes(title_text="价格 (元)", row=1, col=1)
            fig.update_yaxes(title_text="成交量", row=2, col=1)
            
            return fig
        except Exception as e:
            logger.error(f"生成成交量图表失败: {e}")
            return None
    
    @staticmethod
    def save_chart(fig: go.Figure, filename: str = "chart.html"):
        """保存图表为HTML文件"""
        if fig:
            fig.write_html(filename)
            logger.info(f"图表已保存: {filename}")
