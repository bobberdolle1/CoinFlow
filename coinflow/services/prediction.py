"""Price prediction service using AI models."""

import io
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.arima.model import ARIMA
from typing import Optional, Tuple, Dict
from ..utils.logger import setup_logger
import warnings
warnings.filterwarnings('ignore')

logger = setup_logger('prediction')


class PredictionGenerator:
    """Генератор прогнозов курсов."""
    
    def __init__(self, dpi: int = 150):
        self.dpi = dpi
    
    def generate_prediction(self, pair: str, model_type: str = 'arima', 
                          days: int = 90, forecast_days: int = 7) -> Tuple[Optional[bytes], Dict]:
        """
        Создать прогноз для пары валют.
        
        Args:
            pair: Trading pair (e.g., "BTC-USD")
            model_type: 'arima' or 'linear'
            days: Historical days to analyze
            forecast_days: Days to forecast ahead
        
        Returns:
            Tuple of (image bytes, statistics dict)
        """
        try:
            logger.info(f"Generating prediction for {pair}, model: {model_type}, days: {days}")
            
            # Загрузка данных
            ticker = yf.Ticker(pair)
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            df = ticker.history(start=start_date, end=end_date)
            
            if df.empty or len(df) < 30:
                logger.warning(f"Insufficient data for {pair}")
                return None, {}
            
            prices = df['Close'].values
            current_price = prices[-1]
            
            # Прогнозирование
            forecast = None
            if model_type == 'arima':
                try:
                    model = ARIMA(prices, order=(5, 1, 0))
                    model_fit = model.fit()
                    forecast = model_fit.forecast(steps=forecast_days)
                    logger.info(f"ARIMA forecast completed for {pair}")
                except Exception as e:
                    logger.warning(f"ARIMA failed for {pair}, falling back to linear: {e}")
                    model_type = 'linear'
            
            if model_type == 'linear' or forecast is None:
                X = np.arange(len(prices)).reshape(-1, 1)
                y = prices
                model = LinearRegression()
                model.fit(X, y)
                future_X = np.arange(len(prices), len(prices) + forecast_days).reshape(-1, 1)
                forecast = model.predict(future_X)
                logger.info(f"Linear regression forecast completed for {pair}")
            
            forecast_price = forecast[-1]
            trend = 'up' if forecast_price > current_price else 'down'
            
            # Статистика
            stats = {
                'model': model_type.upper(),
                'current': round(current_price, 2),
                'forecast': round(forecast_price, 2),
                'trend': '📈 Upward' if trend == 'up' else '📉 Downward',
                'days': days
            }
            
            # Создание графика
            plt.figure(figsize=(12, 6))
            
            # Исторические данные
            dates = np.arange(len(prices))
            plt.plot(dates, prices, label='Historical Data', linewidth=2, color='#2196F3')
            
            # Прогноз
            forecast_dates = np.arange(len(prices), len(prices) + forecast_days)
            plt.plot(forecast_dates, forecast, label='Forecast', linewidth=2, 
                    color='#FF5722', linestyle='--')
            
            # Тренд
            all_dates = np.concatenate([dates, forecast_dates])
            all_prices = np.concatenate([prices, forecast])
            z = np.polyfit(all_dates, all_prices, 1)
            p = np.poly1d(z)
            plt.plot(all_dates, p(all_dates), 'g--', alpha=0.5, label='Trend Line')
            
            plt.title(f'{pair} - {forecast_days} Day Forecast ({model_type.upper()})', 
                     fontsize=16, fontweight='bold')
            plt.xlabel('Days', fontsize=12)
            plt.ylabel('Price ($)', fontsize=12)
            plt.legend()
            plt.grid(True, alpha=0.3)
            plt.axvline(x=len(prices)-1, color='red', linestyle=':', alpha=0.5)
            plt.tight_layout()
            
            # Сохранение в буфер
            buf = io.BytesIO()
            plt.savefig(buf, format='png', dpi=self.dpi)
            buf.seek(0)
            plt.close()
            
            logger.info(f"Prediction generated successfully for {pair}")
            return buf.getvalue(), stats
            
        except Exception as e:
            logger.error(f"Prediction generation error for {pair}: {e}")
            return None, {}
