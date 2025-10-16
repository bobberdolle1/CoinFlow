"""Chart generation service."""

import io
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from typing import Optional, Tuple, Dict
from ..utils.logger import setup_logger

logger = setup_logger('charts')


class ChartGenerator:
    """Генератор графиков курсов."""
    
    def __init__(self, dpi: int = 150):
        self.dpi = dpi
    
    def generate_chart(self, pair: str, period: int = 30, theme: str = 'light') -> Tuple[Optional[bytes], Dict]:
        """
        Создать график для пары валют.
        
        Args:
            pair: Trading pair (e.g., "BTC-USD")
            period: Number of days to show
            theme: 'light' or 'dark'
        
        Returns:
            Tuple of (image bytes, statistics dict)
        """
        try:
            logger.info(f"Generating chart for {pair}, period: {period} days")
            
            # Загрузка данных
            ticker = yf.Ticker(pair)
            end_date = datetime.now()
            start_date = end_date - timedelta(days=period)
            df = ticker.history(start=start_date, end=end_date)
            
            if df.empty:
                logger.warning(f"No data available for {pair}")
                return None, {}
            
            # Статистика
            stats = {
                'current': round(df['Close'].iloc[-1], 2),
                'avg': round(df['Close'].mean(), 2),
                'high': round(df['High'].max(), 2),
                'low': round(df['Low'].min(), 2),
                'period': period
            }
            
            # Применение темы
            if theme == 'dark':
                plt.style.use('dark_background')
                line_color = '#00D9FF'
                fill_color = '#00D9FF'
            else:
                plt.style.use('default')
                line_color = '#2196F3'
                fill_color = '#2196F3'
            
            # Создание графика
            plt.figure(figsize=(12, 6))
            plt.plot(df.index, df['Close'], label='Close Price', linewidth=2, color=line_color)
            plt.fill_between(df.index, df['Low'], df['High'], alpha=0.2, color=fill_color)
            plt.title(f'{pair} - Last {period} Days', fontsize=16, fontweight='bold')
            plt.xlabel('Date', fontsize=12)
            plt.ylabel('Price ($)', fontsize=12)
            plt.legend()
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            
            # Сохранение в буфер
            buf = io.BytesIO()
            plt.savefig(buf, format='png', dpi=self.dpi)
            buf.seek(0)
            plt.close()
            
            logger.info(f"Chart generated successfully for {pair}")
            return buf.getvalue(), stats
            
        except Exception as e:
            logger.error(f"Chart generation error for {pair}: {e}")
            return None, {}
