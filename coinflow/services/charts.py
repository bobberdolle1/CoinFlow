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
    
    def generate_portfolio_pie_chart(self, portfolio_summary: Dict, theme: str = 'light') -> Optional[bytes]:
        """
        Generate pie chart for portfolio distribution.
        
        Args:
            portfolio_summary: Portfolio summary with by_type distribution
            theme: 'light' or 'dark'
        
        Returns:
            Image bytes or None
        """
        try:
            by_type = portfolio_summary.get('by_type', {})
            
            if not by_type:
                logger.warning("No portfolio data for pie chart")
                return None
            
            # Prepare data
            labels = []
            sizes = []
            colors_map = {
                'crypto': '#F7931A',  # Bitcoin orange
                'stock': '#2196F3',   # Blue
                'fiat': '#4CAF50',    # Green
                'cs2': '#FF6B6B'      # Red
            }
            colors = []
            
            for asset_type, data in by_type.items():
                labels.append(f"{asset_type.title()} ({data['count']})")
                sizes.append(data['total_value_usd'])
                colors.append(colors_map.get(asset_type, '#9E9E9E'))
            
            # Apply theme
            if theme == 'dark':
                plt.style.use('dark_background')
                text_color = 'white'
            else:
                plt.style.use('default')
                text_color = 'black'
            
            # Create pie chart
            fig, ax = plt.subplots(figsize=(10, 8))
            
            wedges, texts, autotexts = ax.pie(
                sizes,
                labels=labels,
                colors=colors,
                autopct='%1.1f%%',
                startangle=90,
                textprops={'color': text_color, 'fontsize': 11}
            )
            
            # Make percentage text bold
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
            
            ax.set_title(
                f'Portfolio Distribution\nTotal: ${portfolio_summary["total_value_usd"]:.2f}',
                fontsize=14,
                fontweight='bold',
                color=text_color,
                pad=20
            )
            
            plt.tight_layout()
            
            # Save to buffer
            buf = io.BytesIO()
            plt.savefig(buf, format='png', dpi=self.dpi, bbox_inches='tight')
            buf.seek(0)
            plt.close()
            
            logger.info("Portfolio pie chart generated successfully")
            return buf.getvalue()
        
        except Exception as e:
            logger.error(f"Error generating portfolio pie chart: {e}")
            return None
