"""A股数据获取模块
支持从 AKShare 获取实时和历史行情数据
"""

import akshare as ak
import pandas as pd
from typing import Optional, List
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StockDataFetcher:
    """A股数据获取类"""
    
    def __init__(self):
        self.cache = {}
    
    def get_stock_list(self) -> pd.DataFrame:
        """
        获取A股全部股票列表
        Returns: DataFrame 包含股票代码和名称
        """
        try:
            logger.info("正在获取A股股票列表...")
            df = ak.stock_info_a_sina()
            logger.info(f"成功获取 {len(df)} 只A股股票")
            return df
        except Exception as e:
            logger.error(f"获取股票列表失败: {e}")
            return pd.DataFrame()
    
    def get_daily_data(
        self, 
        symbol: str, 
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        adjust: str = "qfq"  # qfq=前复权, hfq=后复权
    ) -> pd.DataFrame:
        """
        获取股票日线数据
        
        Args:
            symbol: 股票代码 (e.g., "000001" for 平安银行)
            start_date: 开始日期 (YYYY-MM-DD)
            end_date: 结束日期 (YYYY-MM-DD)
            adjust: 复权方式
            
        Returns: DataFrame 包含OHLCV数据
        """
        try:
            if start_date is None:
                start_date = (datetime.now() - timedelta(days=365)).strftime("%Y%m%d")
            else:
                start_date = start_date.replace("-", "")
            
            if end_date is None:
                end_date = datetime.now().strftime("%Y%m%d")
            else:
                end_date = end_date.replace("-", "")
            
            logger.info(f"正在获取 {symbol} 从 {start_date} 到 {end_date} 的日线数据...")
            
            df = ak.stock_zh_a_hist(
                symbol=symbol,
                period="daily",
                start_date=start_date,
                end_date=end_date,
                adjust=adjust
            )
            
            # 数据清洗
            df['日期'] = pd.to_datetime(df['日期'])
            df = df.sort_values('日期').reset_index(drop=True)
            
            logger.info(f"成功获取 {len(df)} 条数据")
            return df
            
        except Exception as e:
            logger.error(f"获取日线数据失败: {e}")
            return pd.DataFrame()
    
    def get_realtime_quote(self, symbols: List[str]) -> pd.DataFrame:
        """
        获取实时行情数据
        
        Args:
            symbols: 股票代码列表
            
        Returns: DataFrame 包含实时行情
        """
        try:
            logger.info(f"正在获取实时行情: {symbols}")
            df = ak.stock_zh_a_spot()
            df = df[df['代码'].isin(symbols)]
            logger.info(f"成功获取 {len(df)} 只股票的实时行情")
            return df
        except Exception as e:
            logger.error(f"获取实时行情失败: {e}")
            return pd.DataFrame()
    
    def get_stock_fundamentals(self, symbol: str) -> dict:
        """
        获取股票基本面数据
        
        Args:
            symbol: 股票代码
            
        Returns: dict 包含市盈率、市净率等指标
        """
        try:
            logger.info(f"正在获取 {symbol} 的基本面数据...")
            
            # 获取实时行情数据
            df = ak.stock_zh_a_spot()
            stock_info = df[df['代码'] == symbol]
            
            if stock_info.empty:
                logger.warning(f"未找到股票 {symbol}")
                return {}
            
            fundamentals = {
                '代码': symbol,
                '名称': stock_info['名称'].values[0],
                '最新价': stock_info['最新价'].values[0],
                '市盈率': stock_info['市盈率'].values[0],
                '市净率': stock_info['市净率'].values[0],
                '总市值': stock_info['总市值'].values[0],
                '流通市值': stock_info['流通市值'].values[0],
                '成交量': stock_info['成交量'].values[0],
                '成交额': stock_info['成交额'].values[0],
            }
            
            return fundamentals
            
        except Exception as e:
            logger.error(f"获取基本面数据失败: {e}")
            return {}


if __name__ == "__main__":
    fetcher = StockDataFetcher()
    
    # 示例1: 获取平安银行的日线数据
    df = fetcher.get_daily_data("000001", start_date="2024-01-01")
    print("\n平安银行日线数据示例:")
    print(df.head())
    
    # 示例2: 获取基本面数据
    info = fetcher.get_stock_fundamentals("000001")
    print("\n平安银行基本面数据:")
    print(info)
