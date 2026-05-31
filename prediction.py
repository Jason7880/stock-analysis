import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
import warnings
warnings.filterwarnings('ignore')

class PredictionModel:
    def __init__(self, data):
        self.data = data.copy()
        self.scaler = MinMaxScaler()
        self.model = None
    
    def prepare_data(self, lookback=60):
        """准备训练数据"""
        prices = self.data['Close'].values.reshape(-1, 1)
        scaled_prices = self.scaler.fit_transform(prices)
        
        X, y = [], []
        for i in range(lookback, len(scaled_prices)):
            X.append(scaled_prices[i-lookback:i, 0])
            y.append(scaled_prices[i, 0])
        
        return np.array(X), np.array(y)
    
    def train_linear_model(self):
        """训练线性回归模型"""
        X, y = self.prepare_data()
        self.model = LinearRegression()
        self.model.fit(X, y)
        return self.model
    
    def exponential_smoothing(self, alpha=0.3):
        """指数平滑预测"""
        prices = self.data['Close'].values
        forecast = [prices[0]]
        
        for i in range(1, len(prices)):
            forecast.append(alpha * prices[i] + (1 - alpha) * forecast[i-1])
        
        return forecast
    
    def predict(self, days=30):
        """预测未来价格"""
        try:
            self.train_linear_model()
            
            # 使用最后60天的数据进行预测
            lookback = 60
            last_data = self.data['Close'].values[-lookback:].reshape(-1, 1)
            scaled_last = self.scaler.transform(last_data)
            
            predictions = []
            current_sequence = scaled_last.flatten().copy()
            
            for _ in range(days):
                next_pred = self.model.predict([current_sequence])[0]
                predictions.append(next_pred)
                current_sequence = np.append(current_sequence[1:], next_pred)
            
            # 反向缩放
            predictions = np.array(predictions).reshape(-1, 1)
            predictions = self.scaler.inverse_transform(predictions)
            
            # 创建结果 DataFrame
            future_dates = pd.date_range(
                start=self.data.index[-1],
                periods=days+1,
                freq='D'
            )[1:]
            
            result = pd.DataFrame({
                '日期': future_dates,
                '预测价格': predictions.flatten()
            })
            
            return result
        
        except Exception as e:
            print(f"预测失败: {str(e)}")
            return None