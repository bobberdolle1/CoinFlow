#!/usr/bin/env python3
"""
CoinFlow Bot: The Ultimate Edition
Полнофункциональный бот-агрегатор курсов с интерактивным интерфейсом
"""

import os
import re
import io
import shelve
import requests
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.arima.model import ARIMA
from typing import Dict, Optional, List, Tuple
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from apscheduler.schedulers.background import BackgroundScheduler
from bestchange_api import BestChange
import warnings
warnings.filterwarnings('ignore')

# --- Localization (i18n) System ---
LOCALIZATION = {
    'en': {
        'welcome_new': '👋 *Welcome to CoinFlow Bot!*\n\nYour personal financial assistant for currency conversion, cryptocurrency analysis, and rate forecasting.\n\n🌍 Choose your language:',
        'welcome_back': '👋 *Welcome back!*\n\nI\'m ready to help you with currency conversions and cryptocurrency analysis.\n\n💡 Use the menu below to get started:',
        'language_set': '✅ Language set to English!',
        'main_menu': '📊 *Main Menu*\n\nChoose an action:',
        'quick_convert': '⚡ Quick Convert',
        'full_conversion': '💱 Full Conversion',
        'simple_conversion': '🔄 Simple Convert',
        'crypto_rates': '📈 Crypto Rates',
        'rate_charts': '📊 Rate Charts',
        'rate_prediction': '🔮 Rate Forecast',
        'compare_rates': '⚖️ Compare Rates',
        'calculator': '🧮 Calculator',
        'notifications': '🔔 Notifications',
        'favorites': '⭐ Favorites',
        'settings': '⚙️ Settings',
        'about_btn': 'ℹ️ About',
        'back': '◀️ Back',
        'select_from_currency': '💰 *Select source currency:*\n\nChoose the currency you want to convert FROM:',
        'select_to_currency': '💵 *Select target currency:*\n\nChoose the currency you want to convert TO:',
        'enter_amount': '💵 Enter amount to convert:',
        'conversion_result': '💱 *Conversion Result*\n\n{amount} {from_curr} = *{result} {to_curr}*\n\n📊 Rate: 1 {from_curr} = {rate} {to_curr}\n⏰ Updated: {time}',
        'popular': '⭐ Popular',
        'fiat': '💵 Fiat',
        'crypto': '🪙 Crypto',
        'search': '🔍 Search',
        'error': '❌ Error: {msg}',
        'rate_unavailable': 'Rate is currently unavailable. Please try again later.',
        'invalid_amount': 'Invalid amount. Please enter a valid number.',
        'comparing_rates': '⚖️ *Comparing rates for {symbol}*\n\nFetching data from exchanges...',
        'compare_result': '⚖️ *Price comparison for {symbol}/USDT:*\n\n{rates}\n\n📊 Average price: *${avg}*\n📈 Highest: ${high} ({high_ex})\n📉 Lowest: ${low} ({low_ex})\n📊 Spread: {spread}%',
        'chart_generating': '📊 Generating chart for {pair}...\n\nPlease wait...',
        'chart_ready': '📊 *Chart for {pair}*\n\n📈 Period: {period} days\n💰 Current price: ${current}\n📊 Average: ${avg}\n📈 High: ${high}\n📉 Low: ${low}',
        'prediction_generating': '🔮 Creating forecast for {pair}...\n\nThis may take up to a minute. Analyzing {days} days of data...',
        'prediction_ready': '🔮 *Forecast for {pair}*\n\n📊 Model: {model}\n📈 Trend: {trend}\n💰 Current: ${current}\n🎯 7-day forecast: ${forecast}\n\n⚠️ *DISCLAIMER:*\nThis is NOT financial advice. The forecast is based on mathematical models and does not account for market news or other factors.',
        'alert_set': '✅ *Alert set!*\n\n{pair}: {condition} ${target}\n\nI will notify you when the price reaches your target.',
        'alert_triggered': '🔔 *PRICE ALERT!*\n\n{pair} {condition} ${target}\n\nCurrent price: ${current}',
        'no_alerts': 'You have no active alerts.',
        'alerts_list': '🔔 *Your Alerts:*\n\n{alerts}',
        'calculator_mode': '🧮 *Calculator Mode*\n\nEnter an expression to calculate (e.g., `100 + 50 * 2`)\n\nOr use currency conversion: `100 USD to EUR`',
        'calc_result': '🧮 *Result:* {result}',
        'settings_menu': '⚙️ *Settings*',
        'prediction_model_btn': '🔮 Prediction Model: {model}',
        'rub_source_btn': '🇷🇺 RUB Source: {source}',
        'data_sources_btn': '📊 Data Sources',
        'language_btn': '🌍 Language',
        'model_changed': '✅ Prediction model changed to: {model}',
        'rub_source_changed': '✅ RUB source changed to: {source}',
        'about_text': 'ℹ️ *About CoinFlow Bot*\n\n🪙 CoinFlow is your ultimate financial assistant that aggregates data from multiple exchanges and sources to provide you with the most accurate currency rates and cryptocurrency analysis.\n\n*Features:*\n• 💱 Currency conversion with 100+ currencies\n• 📊 Real-time crypto rates from 5+ exchanges\n• ⚖️ Price comparison across exchanges\n• 📈 Historical charts and analysis\n• 🔮 AI-powered price forecasting\n• 🔔 Price alerts and notifications\n• 🧮 Built-in calculator\n\n*Data Sources:*\n• Binance, Bybit, HTX, KuCoin, Gate.io\n• Central Bank of Russia (CBR)\n• Yahoo Finance\n• BestChange\n\n📖 [Source Code](https://github.com/bobberdolle1/CoinFlow)\n\n⚠️ Not financial advice!',
    },
    'ru': {
        'welcome_new': '👋 *Добро пожаловать в CoinFlow Bot!*\n\nВаш персональный финансовый ассистент для конвертации валют, анализа криптовалют и прогнозирования курсов.\n\n🌍 Выберите язык:',
        'welcome_back': '👋 *С возвращением!*\n\nЯ готов помочь вам с конвертацией валют и анализом криптовалют.\n\n💡 Используйте меню ниже для начала работы:',
        'language_set': '✅ Язык установлен: Русский!',
        'main_menu': '📊 *Главное меню*\n\nВыберите действие:',
        'quick_convert': '⚡ Быстрая конвертация',
        'full_conversion': '💱 Полная конвертация',
        'simple_conversion': '🔄 Простая конвертация',
        'crypto_rates': '📈 Курсы крипты',
        'rate_charts': '📊 Графики курсов',
        'rate_prediction': '🔮 Прогноз курса',
        'compare_rates': '⚖️ Сравнить курсы',
        'calculator': '🧮 Калькулятор',
        'notifications': '🔔 Уведомления',
        'favorites': '⭐ Избранное',
        'settings': '⚙️ Настройки',
        'about_btn': 'ℹ️ О боте',
        'back': '◀️ Назад',
        'select_from_currency': '💰 *Выберите исходную валюту:*\n\nВыберите валюту, которую хотите конвертировать:',
        'select_to_currency': '💵 *Выберите целевую валюту:*\n\nВыберите валюту, в которую хотите конвертировать:',
        'enter_amount': '💵 Введите сумму для конвертации:',
        'conversion_result': '💱 *Результат конвертации*\n\n{amount} {from_curr} = *{result} {to_curr}*\n\n📊 Курс: 1 {from_curr} = {rate} {to_curr}\n⏰ Обновлено: {time}',
        'popular': '⭐ Популярные',
        'fiat': '💵 Фиат',
        'crypto': '🪙 Крипта',
        'search': '🔍 Поиск',
        'error': '❌ Ошибка: {msg}',
        'rate_unavailable': 'Курс временно недоступен. Попробуйте позже.',
        'invalid_amount': 'Неверная сумма. Введите корректное число.',
        'comparing_rates': '⚖️ *Сравниваю курсы для {symbol}*\n\nПолучаю данные с бирж...',
        'compare_result': '⚖️ *Сравнение цен для {symbol}/USDT:*\n\n{rates}\n\n📊 Средняя цена: *${avg}*\n📈 Максимум: ${high} ({high_ex})\n📉 Минимум: ${low} ({low_ex})\n📊 Спред: {spread}%',
        'chart_generating': '📊 Создаю график для {pair}...\n\nПожалуйста, подождите...',
        'chart_ready': '📊 *График для {pair}*\n\n📈 Период: {period} дней\n💰 Текущая цена: ${current}\n📊 Среднее: ${avg}\n📈 Максимум: ${high}\n📉 Минимум: ${low}',
        'prediction_generating': '🔮 Создаю прогноз для {pair}...\n\nЭто может занять до минуты. Анализирую данные за {days} дней...',
        'prediction_ready': '🔮 *Прогноз для {pair}*\n\n📊 Модель: {model}\n📈 Тренд: {trend}\n💰 Текущая: ${current}\n🎯 Прогноз на 7 дней: ${forecast}\n\n⚠️ *ОТКАЗ ОТ ОТВЕТСТВЕННОСТИ:*\nЭто НЕ финансовый совет. Прогноз основан на математических моделях и не учитывает рыночные новости и другие факторы.',
        'alert_set': '✅ *Уведомление установлено!*\n\n{pair}: {condition} ${target}\n\nЯ уведомлю вас, когда цена достигнет цели.',
        'alert_triggered': '🔔 *ЦЕНОВОЕ ОПОВЕЩЕНИЕ!*\n\n{pair} {condition} ${target}\n\nТекущая цена: ${current}',
        'no_alerts': 'У вас нет активных уведомлений.',
        'alerts_list': '🔔 *Ваши уведомления:*\n\n{alerts}',
        'calculator_mode': '🧮 *Режим калькулятора*\n\nВведите выражение для вычисления (например, `100 + 50 * 2`)\n\nИли используйте конвертацию валют: `100 USD to EUR`',
        'calc_result': '🧮 *Результат:* {result}',
        'settings_menu': '⚙️ *Настройки*',
        'prediction_model_btn': '🔮 Модель прогноза: {model}',
        'rub_source_btn': '🇷🇺 Источник RUB: {source}',
        'data_sources_btn': '📊 Источники данных',
        'language_btn': '🌍 Язык',
        'model_changed': '✅ Модель прогноза изменена на: {model}',
        'rub_source_changed': '✅ Источник RUB изменен на: {source}',
        'about_text': 'ℹ️ *О боте CoinFlow*\n\n🪙 CoinFlow — это ваш финансовый ассистент, который агрегирует данные с множества бирж и источников, чтобы предоставить вам наиболее точные курсы валют и анализ криптовалют.\n\n*Возможности:*\n• 💱 Конвертация валют (100+ валют)\n• 📊 Курсы крипты в реальном времени с 5+ бирж\n• ⚖️ Сравнение цен на биржах\n• 📈 Исторические графики и анализ\n• 🔮 ИИ-прогнозирование цен\n• 🔔 Ценовые уведомления\n• 🧮 Встроенный калькулятор\n\n*Источники данных:*\n• Binance, Bybit, HTX, KuCoin, Gate.io\n• Центральный Банк России (ЦБ РФ)\n• Yahoo Finance\n• BestChange\n\n📖 [Исходный код](https://github.com/bobberdolle1/CoinFlow)\n\n⚠️ Не является финансовым советом!',
    }
}

# --- Helper Classes ---

class AlertManager:
    """Менеджер ценовых уведомлений"""
    def __init__(self):
        self.db_path = 'alerts_db'
        
    def add_alert(self, user_id: int, pair: str, condition: str, target: float):
        """Добавить новое уведомление"""
        with shelve.open(self.db_path) as db:
            if str(user_id) not in db:
                db[str(user_id)] = []
            alerts = db[str(user_id)]
            alert = {
                'pair': pair.upper(),
                'condition': condition,
                'target': target,
                'created': datetime.now().isoformat()
            }
            alerts.append(alert)
            db[str(user_id)] = alerts
            
    def get_alerts(self, user_id: int) -> List[Dict]:
        """Получить все уведомления пользователя"""
        with shelve.open(self.db_path) as db:
            return db.get(str(user_id), [])
            
    def remove_alert(self, user_id: int, index: int):
        """Удалить уведомление"""
        with shelve.open(self.db_path) as db:
            if str(user_id) in db:
                alerts = db[str(user_id)]
                if 0 <= index < len(alerts):
                    alerts.pop(index)
                    db[str(user_id)] = alerts
                    
    def check_alerts(self, user_id: int, pair: str, current_price: float) -> List[Dict]:
        """Проверить уведомления и вернуть сработавшие"""
        triggered = []
        with shelve.open(self.db_path) as db:
            if str(user_id) in db:
                alerts = db[str(user_id)]
                remaining = []
                for alert in alerts:
                    if alert['pair'] == pair.upper():
                        should_trigger = False
                        if alert['condition'] == 'above' and current_price >= alert['target']:
                            should_trigger = True
                        elif alert['condition'] == 'below' and current_price <= alert['target']:
                            should_trigger = True
                        
                        if should_trigger:
                            triggered.append(alert)
                        else:
                            remaining.append(alert)
                    else:
                        remaining.append(alert)
                db[str(user_id)] = remaining
        return triggered

class ChartGenerator:
    """Генератор графиков курсов"""
    def generate_chart(self, pair: str, period: int = 30) -> Tuple[Optional[bytes], Dict]:
        """Создать график для пары валют"""
        try:
            # Загрузка данных
            ticker = yf.Ticker(pair)
            end_date = datetime.now()
            start_date = end_date - timedelta(days=period)
            df = ticker.history(start=start_date, end=end_date)
            
            if df.empty:
                return None, {}
            
            # Статистика
            stats = {
                'current': round(df['Close'].iloc[-1], 2),
                'avg': round(df['Close'].mean(), 2),
                'high': round(df['High'].max(), 2),
                'low': round(df['Low'].min(), 2),
                'period': period
            }
            
            # Создание графика
            plt.figure(figsize=(12, 6))
            plt.plot(df.index, df['Close'], label='Close Price', linewidth=2, color='#2196F3')
            plt.fill_between(df.index, df['Low'], df['High'], alpha=0.2, color='#2196F3')
            plt.title(f'{pair} - Last {period} Days', fontsize=16, fontweight='bold')
            plt.xlabel('Date', fontsize=12)
            plt.ylabel('Price ($)', fontsize=12)
            plt.legend()
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            
            # Сохранение в буфер
            buf = io.BytesIO()
            plt.savefig(buf, format='png', dpi=150)
            buf.seek(0)
            plt.close()
            
            return buf.getvalue(), stats
        except Exception as e:
            print(f"Chart generation error: {e}")
            return None, {}

class PredictionGenerator:
    """Генератор прогнозов курсов"""
    def generate_prediction(self, pair: str, model_type: str = 'arima', days: int = 90) -> Tuple[Optional[bytes], Dict]:
        """Создать прогноз для пары валют"""
        try:
            # Загрузка данных
            ticker = yf.Ticker(pair)
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            df = ticker.history(start=start_date, end=end_date)
            
            if df.empty or len(df) < 30:
                return None, {}
            
            prices = df['Close'].values
            current_price = prices[-1]
            
            # Прогнозирование
            forecast_days = 7
            if model_type == 'arima':
                try:
                    model = ARIMA(prices, order=(5, 1, 0))
                    model_fit = model.fit()
                    forecast = model_fit.forecast(steps=forecast_days)
                except:
                    # Fallback to linear regression
                    model_type = 'linear'
            
            if model_type == 'linear':
                X = np.arange(len(prices)).reshape(-1, 1)
                y = prices
                model = LinearRegression()
                model.fit(X, y)
                future_X = np.arange(len(prices), len(prices) + forecast_days).reshape(-1, 1)
                forecast = model.predict(future_X)
            
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
            plt.plot(forecast_dates, forecast, label='Forecast', linewidth=2, color='#FF5722', linestyle='--')
            
            # Тренд
            all_dates = np.concatenate([dates, forecast_dates])
            all_prices = np.concatenate([prices, forecast])
            z = np.polyfit(all_dates, all_prices, 1)
            p = np.poly1d(z)
            plt.plot(all_dates, p(all_dates), 'g--', alpha=0.5, label='Trend Line')
            
            plt.title(f'{pair} - {forecast_days} Day Forecast ({model_type.upper()})', fontsize=16, fontweight='bold')
            plt.xlabel('Days', fontsize=12)
            plt.ylabel('Price ($)', fontsize=12)
            plt.legend()
            plt.grid(True, alpha=0.3)
            plt.axvline(x=len(prices)-1, color='red', linestyle=':', alpha=0.5, label='Today')
            plt.tight_layout()
            
            # Сохранение в буфер
            buf = io.BytesIO()
            plt.savefig(buf, format='png', dpi=150)
            buf.seek(0)
            plt.close()
            
            return buf.getvalue(), stats
        except Exception as e:
            print(f"Prediction generation error: {e}")
            return None, {}

class Calculator:
    """Калькулятор с поддержкой конвертации валют"""
    def __init__(self, converter):
        self.converter = converter
        
    def calculate(self, expression: str, user_id: int = None) -> Optional[str]:
        """Вычислить выражение или конвертировать валюту"""
        try:
            # Проверка на конвертацию валют
            match = re.match(r'([\d.]+)\s*([A-Z]{3})\s*(?:to|in|->)\s*([A-Z]{3})', expression, re.IGNORECASE)
            if match:
                amount = float(match.group(1))
                from_curr = match.group(2).upper()
                to_curr = match.group(3).upper()
                result = self.converter.convert(amount, from_curr, to_curr, user_id)
                if result:
                    return f"{amount} {from_curr} = {result:.2f} {to_curr}"
                return None
            
            # Обычное вычисление
            # Безопасное вычисление только разрешенных операций
            allowed_chars = set('0123456789+-*/(). ')
            if not all(c in allowed_chars for c in expression):
                return None
            
            result = eval(expression, {"__builtins__": {}}, {})
            return f"{expression} = {result}"
        except:
            return None

class CurrencyConverter:
    """Агрегатор курсов валют с разных площадок."""
    def __init__(self, bot_instance=None):
        self.bot = bot_instance
        self.exchange_rate_api = "https://api.exchangerate-api.com/v4/latest"
        self.cbr_api_url = "https://www.cbr-xml-daily.ru/daily_json.js"
        self.crypto_symbols = ['BTC', 'ETH', 'USDT', 'BNB', 'SOL', 'XRP', 'ADA', 'DOGE', 'DOT', 'MATIC', 
                               'SHIB', 'AVAX', 'TRX', 'LINK', 'UNI', 'ATOM', 'LTC', 'XLM', 'BCH', 'ALGO']
        self.crypto_providers = [
            {'name': 'BestChange', 'method': self.get_bestchange_rate},
            {'name': 'Binance', 'method': self.get_binance_ticker},
            {'name': 'Bybit', 'method': self.get_bybit_ticker},
            {'name': 'HTX', 'method': self.get_htx_ticker},
            {'name': 'KuCoin', 'method': self.get_kucoin_ticker},
            {'name': 'Gate.io', 'method': self.get_gateio_ticker},
        ]
        self.bestchange = BestChange()
        self.bestchange_ids = {
            'BTC': 93,
            'USDT': 115,
            'ETH': 139,
            'RUB': 643,
        }
    
    def get_binance_ticker(self, from_symbol: str, to_symbol: str) -> Optional[float]:
        """Получить курс с Binance"""
        try:
            pair = f"{from_symbol}{to_symbol}"
            url = f"https://api.binance.com/api/v3/ticker/price?symbol={pair}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return float(data['price'])
        except:
            pass
        return None
    
    def get_bybit_ticker(self, from_symbol: str, to_symbol: str) -> Optional[float]:
        """Получить курс с Bybit"""
        try:
            pair = f"{from_symbol}{to_symbol}"
            url = f"https://api.bybit.com/v5/market/tickers?category=spot&symbol={pair}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data['retCode'] == 0 and data['result']['list']:
                    return float(data['result']['list'][0]['lastPrice'])
        except:
            pass
        return None
    
    def get_htx_ticker(self, from_symbol: str, to_symbol: str) -> Optional[float]:
        """Получить курс с HTX (Huobi)"""
        try:
            pair = f"{from_symbol.lower()}{to_symbol.lower()}"
            url = f"https://api.huobi.pro/market/detail/merged?symbol={pair}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data['status'] == 'ok':
                    return float(data['tick']['close'])
        except:
            pass
        return None
    
    def get_kucoin_ticker(self, from_symbol: str, to_symbol: str) -> Optional[float]:
        """Получить курс с KuCoin"""
        try:
            pair = f"{from_symbol}-{to_symbol}"
            url = f"https://api.kucoin.com/api/v1/market/orderbook/level1?symbol={pair}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data['code'] == '200000':
                    return float(data['data']['price'])
        except:
            pass
        return None
    
    def get_gateio_ticker(self, from_symbol: str, to_symbol: str) -> Optional[float]:
        """Получить курс с Gate.io"""
        try:
            pair = f"{from_symbol}_{to_symbol}"
            url = f"https://api.gateio.ws/api/v4/spot/tickers?currency_pair={pair}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data:
                    return float(data[0]['last'])
        except:
            pass
        return None
    
    def get_bestchange_rate(self, from_symbol: str, to_symbol: str) -> Optional[float]:
        """Получить курс с BestChange"""
        try:
            if from_symbol in self.bestchange_ids and to_symbol in self.bestchange_ids:
                from_id = self.bestchange_ids[from_symbol]
                to_id = self.bestchange_ids[to_symbol]
                rate = self.bestchange.get_rate(from_id, to_id)
                if rate:
                    return float(rate)
        except:
            pass
        return None
    
    def get_fiat_rate(self, from_currency: str, to_currency: str) -> Optional[float]:
        """Получить курс фиатных валют"""
        try:
            url = f"{self.exchange_rate_api}/{from_currency}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if to_currency in data['rates']:
                    return float(data['rates'][to_currency])
        except:
            pass
        return None

    def get_active_providers(self, user_id: int) -> List[Dict]:
        if not self.bot: return self.crypto_providers
        provider_settings = self.bot.user_states.get(user_id, {}).get('providers', {})
        return [p for p in self.crypto_providers if provider_settings.get(p['name'], True)]

    def get_cbrf_rate(self, from_currency: str, to_currency: str) -> Optional[float]:
        """Получить официальный курс ЦБ РФ"""
        try:
            response = requests.get(self.cbr_api_url, timeout=10).json()
            rates = response.get('Valute', {})
            
            if from_currency == 'RUB':
                if to_currency in rates:
                    return 1 / (rates[to_currency]['Value'] / rates[to_currency]['Nominal'])
            elif to_currency == 'RUB':
                if from_currency in rates:
                    return rates[from_currency]['Value'] / rates[from_currency]['Nominal']
            return None
        except Exception: return None

    def get_crypto_rate_aggregated(self, from_symbol: str, to_symbol: str, user_id: int) -> Optional[float]:
        for provider in self.get_active_providers(user_id):
            rate = provider['method'](from_symbol, to_symbol)
            if rate is not None: return rate
        return None

    def get_all_crypto_rates(self, from_symbol: str, to_symbol: str, user_id: int) -> List[Tuple[str, float]]:
        rates = []
        for provider in self.get_active_providers(user_id):
            rate = provider['method'](from_symbol, to_symbol)
            if rate is not None: rates.append((provider['name'], rate))
        return rates

    def get_rate(self, from_currency: str, to_currency: str, user_id: int = None) -> Optional[float]:
        from_currency, to_currency = from_currency.upper(), to_currency.upper()
        if from_currency == to_currency: return 1.0

        if user_id and self.bot:
            rub_source = self.bot.user_states.get(user_id, {}).get('rub_source', 'aggregator')
            if rub_source == 'cbrf' and ('RUB' in [from_currency, to_currency]):
                return self.get_cbrf_rate(from_currency, to_currency)

        is_from_crypto = from_currency in self.crypto_symbols
        is_to_crypto = to_currency in self.crypto_symbols

        if is_from_crypto and not is_to_crypto:
            rate_crypto_usd = self.get_crypto_rate_aggregated(from_currency, 'USDT', user_id)
            rate_usd_fiat = self.get_fiat_rate('USD', to_currency)
            return rate_crypto_usd * rate_usd_fiat if rate_crypto_usd and rate_usd_fiat else None
        if not is_from_crypto and is_to_crypto:
            rate_fiat_usd = self.get_fiat_rate(from_currency, 'USD')
            rate_crypto_usd = self.get_crypto_rate_aggregated(to_currency, 'USDT', user_id)
            return (rate_fiat_usd / rate_crypto_usd) if rate_fiat_usd and rate_crypto_usd else None
        if is_from_crypto and is_to_crypto:
            return self.get_crypto_rate_aggregated(from_currency, to_currency, user_id)
        return self.get_fiat_rate(from_currency, to_currency)

    def convert(self, amount: float, from_currency: str, to_currency: str, user_id: int = None) -> Optional[float]:
        rate = self.get_rate(from_currency, to_currency, user_id)
        return amount * rate if rate else None

# --- Main Bot Class & Execution ---
class TelegramBot:
    """Полнофункциональный бот с интерактивным интерфейсом на кнопках"""
    def __init__(self, converter: 'CurrencyConverter', calculator: 'Calculator', chart_generator: 'ChartGenerator', prediction_generator: 'PredictionGenerator', alert_manager: 'AlertManager', app: Application):
        self.converter = converter
        self.calculator = calculator
        self.chart_generator = chart_generator
        self.prediction_generator = prediction_generator
        self.alert_manager = alert_manager
        self.app = app
        load_dotenv()
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.user_states = {}
        
        # Расширенный список популярных валют
        self.popular_currencies = ['USD', 'EUR', 'RUB', 'CNY', 'GBP', 'JPY', 'BTC', 'ETH', 'USDT']
        
        # Фиатные валюты
        self.fiat_currencies = [
            'USD', 'EUR', 'RUB', 'CNY', 'GBP', 'JPY', 'CAD', 'AUD', 'CHF', 'KRW',
            'INR', 'BRL', 'MXN', 'TRY', 'SEK', 'NOK', 'DKK', 'PLN', 'THB', 'IDR',
            'HUF', 'CZK', 'ILS', 'CLP', 'PHP', 'AED', 'SAR', 'MYR', 'RON', 'SGD'
        ]
        
        # Криптовалюты
        self.crypto_currencies = [
            'BTC', 'ETH', 'USDT', 'BNB', 'SOL', 'XRP', 'ADA', 'DOGE', 'DOT', 'MATIC',
            'SHIB', 'AVAX', 'TRX', 'LINK', 'UNI', 'ATOM', 'LTC', 'XLM', 'BCH', 'ALGO',
            'VET', 'FIL', 'HBAR', 'APE', 'NEAR', 'QNT', 'AAVE', 'GRT', 'XTZ', 'SAND'
        ]

    def _t(self, user_id: int, key: str, **kwargs) -> str:
        """Получить перевод текста для пользователя"""
        lang = self.user_states.get(user_id, {}).get('lang', 'en')
        return LOCALIZATION.get(lang, LOCALIZATION['en']).get(key, key).format(**kwargs)

    def get_main_menu_keyboard(self, user_id: int) -> ReplyKeyboardMarkup:
        """Создать главное меню с кнопками"""
        return ReplyKeyboardMarkup([
            [self._t(user_id, 'quick_convert')],
            [self._t(user_id, 'rate_charts'), self._t(user_id, 'rate_prediction')],
            [self._t(user_id, 'compare_rates'), self._t(user_id, 'calculator')],
            [self._t(user_id, 'notifications'), self._t(user_id, 'settings')],
            [self._t(user_id, 'about_btn')]
        ], resize_keyboard=True)
    
    def get_currency_selection_keyboard(self, user_id: int, selection_type: str = 'all') -> InlineKeyboardMarkup:
        """Создать inline-клавиатуру для выбора валюты"""
        keyboard = []
        
        # Добавляем категории
        keyboard.append([
            InlineKeyboardButton(self._t(user_id, 'popular'), callback_data='cat_popular'),
            InlineKeyboardButton(self._t(user_id, 'fiat'), callback_data='cat_fiat'),
            InlineKeyboardButton(self._t(user_id, 'crypto'), callback_data='cat_crypto')
        ])
        
        # Показываем валюты в зависимости от категории
        currencies = []
        if selection_type == 'popular':
            currencies = self.popular_currencies
        elif selection_type == 'fiat':
            currencies = self.fiat_currencies[:20]  # Первые 20
        elif selection_type == 'crypto':
            currencies = self.crypto_currencies[:20]  # Первые 20
        else:
            currencies = self.popular_currencies
        
        # Разбиваем валюты по 3 в строке
        row = []
        for curr in currencies:
            row.append(InlineKeyboardButton(curr, callback_data=f'curr_{curr}'))
            if len(row) == 3:
                keyboard.append(row)
                row = []
        if row:
            keyboard.append(row)
        
        # Добавляем кнопку "Назад"
        keyboard.append([InlineKeyboardButton(self._t(user_id, 'back'), callback_data='back_main')])
        
        return InlineKeyboardMarkup(keyboard)
    
    def get_amount_presets_keyboard(self, user_id: int) -> InlineKeyboardMarkup:
        """Создать клавиатуру с пресетами сумм"""
        keyboard = [
            [InlineKeyboardButton('10', callback_data='amt_10'),
             InlineKeyboardButton('50', callback_data='amt_50'),
             InlineKeyboardButton('100', callback_data='amt_100')],
            [InlineKeyboardButton('500', callback_data='amt_500'),
             InlineKeyboardButton('1000', callback_data='amt_1000'),
             InlineKeyboardButton('5000', callback_data='amt_5000')],
            [InlineKeyboardButton('💬 Custom', callback_data='amt_custom'),
             InlineKeyboardButton(self._t(user_id, 'back'), callback_data='back_main')]
        ]
        return InlineKeyboardMarkup(keyboard)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        user_id = update.effective_user.id
        if not self.user_states.get(user_id, {}).get('lang'):
            self.user_states[user_id] = {
                'state': 'language_select', 
                'prediction_model': 'arima',
                'rub_source': 'aggregator',
                'providers': {p['name']: True for p in self.converter.crypto_providers}
            }
            keyboard = ReplyKeyboardMarkup([['English 🇬🇧', 'Русский 🇷🇺']], resize_keyboard=True)
            await update.message.reply_text(LOCALIZATION['en']['welcome_new'], reply_markup=keyboard, parse_mode='Markdown')
        else:
            self.user_states[user_id]['state'] = 'main_menu'
            await update.message.reply_text(self._t(user_id, 'welcome_back'), reply_markup=self.get_main_menu_keyboard(user_id), parse_mode='Markdown')

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Основной обработчик текстовых сообщений"""
        user_id = update.effective_user.id
        text = update.message.text
        
        if user_id not in self.user_states:
            await self.start(update, context)
            return
        
        state = self.user_states[user_id].get('state', 'main_menu')
        
        # Выбор языка
        if state == 'language_select':
            if 'English' in text:
                self.user_states[user_id]['lang'] = 'en'
            elif 'Русский' in text:
                self.user_states[user_id]['lang'] = 'ru'
            self.user_states[user_id]['state'] = 'main_menu'
            await update.message.reply_text(
                self._t(user_id, 'language_set'),
                reply_markup=self.get_main_menu_keyboard(user_id),
                parse_mode='Markdown'
            )
            return
        
        # Главное меню
        if text == self._t(user_id, 'quick_convert'):
            self.user_states[user_id]['state'] = 'select_from_currency'
            await update.message.reply_text(
                self._t(user_id, 'select_from_currency'),
                reply_markup=self.get_currency_selection_keyboard(user_id, 'popular'),
                parse_mode='Markdown'
            )
        elif text == self._t(user_id, 'rate_charts'):
            self.user_states[user_id]['state'] = 'select_chart_pair'
            await update.message.reply_text(
                self._t(user_id, 'select_from_currency'),
                reply_markup=self.get_currency_selection_keyboard(user_id, 'crypto'),
                parse_mode='Markdown'
            )
        elif text == self._t(user_id, 'rate_prediction'):
            self.user_states[user_id]['state'] = 'select_prediction_pair'
            await update.message.reply_text(
                self._t(user_id, 'select_from_currency'),
                reply_markup=self.get_currency_selection_keyboard(user_id, 'crypto'),
                parse_mode='Markdown'
            )
        elif text == self._t(user_id, 'compare_rates'):
            self.user_states[user_id]['state'] = 'select_compare_symbol'
            await update.message.reply_text(
                self._t(user_id, 'select_from_currency'),
                reply_markup=self.get_currency_selection_keyboard(user_id, 'crypto'),
                parse_mode='Markdown'
            )
        elif text == self._t(user_id, 'calculator'):
            self.user_states[user_id]['state'] = 'calculator'
            await update.message.reply_text(
                self._t(user_id, 'calculator_mode'),
                parse_mode='Markdown'
            )
        elif text == self._t(user_id, 'notifications'):
            await self.show_alerts(update, context)
        elif text == self._t(user_id, 'settings'):
            await self.show_settings(update, context)
        elif text == self._t(user_id, 'about_btn'):
            await update.message.reply_text(
                self._t(user_id, 'about_text'),
                parse_mode='Markdown',
                disable_web_page_preview=True
            )
        elif state == 'calculator':
            result = self.calculator.calculate(text, user_id)
            if result:
                await update.message.reply_text(self._t(user_id, 'calc_result', result=result))
            else:
                await update.message.reply_text(self._t(user_id, 'error', msg='Invalid expression'))
        elif state == 'enter_amount':
            try:
                amount = float(text.replace(',', '.'))
                await self.perform_conversion(update, context, amount)
            except:
                await update.message.reply_text(self._t(user_id, 'invalid_amount'))

    async def handle_callback_query(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик inline-кнопок"""
        query = update.callback_query
        await query.answer()
        user_id = query.from_user.id
        data = query.data
        
        if user_id not in self.user_states:
            self.user_states[user_id] = {'state': 'main_menu', 'lang': 'en'}
        
        # Выбор категории валют
        if data.startswith('cat_'):
            category = data.split('_')[1]
            await query.edit_message_reply_markup(
                reply_markup=self.get_currency_selection_keyboard(user_id, category)
            )
        
        # Выбор валюты
        elif data.startswith('curr_'):
            currency = data.split('_')[1]
            state = self.user_states[user_id].get('state')
            
            if state == 'select_from_currency':
                self.user_states[user_id]['from_currency'] = currency
                self.user_states[user_id]['state'] = 'select_to_currency'
                await query.edit_message_text(
                    self._t(user_id, 'select_to_currency'),
                    reply_markup=self.get_currency_selection_keyboard(user_id, 'popular'),
                    parse_mode='Markdown'
                )
            elif state == 'select_to_currency':
                self.user_states[user_id]['to_currency'] = currency
                self.user_states[user_id]['state'] = 'select_amount'
                await query.edit_message_text(
                    self._t(user_id, 'enter_amount'),
                    reply_markup=self.get_amount_presets_keyboard(user_id),
                    parse_mode='Markdown'
                )
            elif state == 'select_chart_pair':
                await self.generate_chart(query, user_id, currency)
            elif state == 'select_prediction_pair':
                await self.generate_prediction(query, user_id, currency)
            elif state == 'select_compare_symbol':
                await self.compare_rates(query, user_id, currency)
        
        # Выбор суммы
        elif data.startswith('amt_'):
            if data == 'amt_custom':
                self.user_states[user_id]['state'] = 'enter_amount'
                await query.edit_message_text(
                    self._t(user_id, 'enter_amount'),
                    parse_mode='Markdown'
                )
            else:
                amount = float(data.split('_')[1])
                await self.perform_conversion_callback(query, user_id, amount)
        
        # Назад в главное меню
        elif data == 'back_main':
            self.user_states[user_id]['state'] = 'main_menu'
            await query.message.reply_text(
                self._t(user_id, 'main_menu'),
                reply_markup=self.get_main_menu_keyboard(user_id),
                parse_mode='Markdown'
            )

    async def perform_conversion(self, update: Update, context: ContextTypes.DEFAULT_TYPE, amount: float):
        """Выполнить конвертацию валюты"""
        user_id = update.effective_user.id
        from_curr = self.user_states[user_id].get('from_currency')
        to_curr = self.user_states[user_id].get('to_currency')
        
        result = self.converter.convert(amount, from_curr, to_curr, user_id)
        
        if result:
            rate = self.converter.get_rate(from_curr, to_curr, user_id)
            await update.message.reply_text(
                self._t(user_id, 'conversion_result',
                       amount=amount,
                       from_curr=from_curr,
                       result=f"{result:.2f}",
                       to_curr=to_curr,
                       rate=f"{rate:.6f}",
                       time=datetime.now().strftime('%H:%M')),
                parse_mode='Markdown',
                reply_markup=self.get_main_menu_keyboard(user_id)
            )
        else:
            await update.message.reply_text(
                self._t(user_id, 'rate_unavailable'),
                reply_markup=self.get_main_menu_keyboard(user_id)
            )
        
        self.user_states[user_id]['state'] = 'main_menu'

    async def perform_conversion_callback(self, query, user_id: int, amount: float):
        """Выполнить конвертацию из callback"""
        from_curr = self.user_states[user_id].get('from_currency')
        to_curr = self.user_states[user_id].get('to_currency')
        
        result = self.converter.convert(amount, from_curr, to_curr, user_id)
        
        if result:
            rate = self.converter.get_rate(from_curr, to_curr, user_id)
            await query.edit_message_text(
                self._t(user_id, 'conversion_result',
                       amount=amount,
                       from_curr=from_curr,
                       result=f"{result:.2f}",
                       to_curr=to_curr,
                       rate=f"{rate:.6f}",
                       time=datetime.now().strftime('%H:%M')),
                parse_mode='Markdown'
            )
        else:
            await query.edit_message_text(self._t(user_id, 'rate_unavailable'))
        
        self.user_states[user_id]['state'] = 'main_menu'

    async def generate_chart(self, query, user_id: int, pair: str):
        """Генерация графика"""
        await query.edit_message_text(self._t(user_id, 'chart_generating', pair=pair))
        
        chart_data, stats = self.chart_generator.generate_chart(f"{pair}-USD", 30)
        
        if chart_data and stats:
            await query.message.reply_photo(
                photo=chart_data,
                caption=self._t(user_id, 'chart_ready',
                               pair=pair,
                               period=stats['period'],
                               current=stats['current'],
                               avg=stats['avg'],
                               high=stats['high'],
                               low=stats['low']),
                parse_mode='Markdown'
            )
        else:
            await query.edit_message_text(self._t(user_id, 'error', msg='Chart generation failed'))
        
        self.user_states[user_id]['state'] = 'main_menu'

    async def generate_prediction(self, query, user_id: int, pair: str):
        """Генерация прогноза"""
        model = self.user_states[user_id].get('prediction_model', 'arima')
        await query.edit_message_text(self._t(user_id, 'prediction_generating', pair=pair, days=90))
        
        pred_data, stats = self.prediction_generator.generate_prediction(f"{pair}-USD", model, 90)
        
        if pred_data and stats:
            await query.message.reply_photo(
                photo=pred_data,
                caption=self._t(user_id, 'prediction_ready',
                               pair=pair,
                               model=stats['model'],
                               trend=stats['trend'],
                               current=stats['current'],
                               forecast=stats['forecast']),
                parse_mode='Markdown'
            )
        else:
            await query.edit_message_text(self._t(user_id, 'error', msg='Prediction failed'))
        
        self.user_states[user_id]['state'] = 'main_menu'

    async def compare_rates(self, query, user_id: int, symbol: str):
        """Сравнение курсов на биржах"""
        await query.edit_message_text(self._t(user_id, 'comparing_rates', symbol=symbol))
        
        rates = self.converter.get_all_crypto_rates(symbol, 'USDT', user_id)
        
        if rates:
            rate_text = '\n'.join([f"• **{ex}:** ${rate:.2f}" for ex, rate in rates])
            prices = [r[1] for r in rates]
            avg = sum(prices) / len(prices)
            high = max(prices)
            low = min(prices)
            high_ex = [ex for ex, rate in rates if rate == high][0]
            low_ex = [ex for ex, rate in rates if rate == low][0]
            spread = ((high - low) / avg) * 100
            
            await query.edit_message_text(
                self._t(user_id, 'compare_result',
                       symbol=symbol,
                       rates=rate_text,
                       avg=f"{avg:.2f}",
                       high=f"{high:.2f}",
                       high_ex=high_ex,
                       low=f"{low:.2f}",
                       low_ex=low_ex,
                       spread=f"{spread:.2f}"),
                parse_mode='Markdown'
            )
        else:
            await query.edit_message_text(self._t(user_id, 'error', msg='No data available'))
        
        self.user_states[user_id]['state'] = 'main_menu'

    async def show_alerts(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать уведомления"""
        user_id = update.effective_user.id
        alerts = self.alert_manager.get_alerts(user_id)
        
        if alerts:
            alert_text = '\n'.join([f"{i+1}. {a['pair']} {a['condition']} ${a['target']}" 
                                   for i, a in enumerate(alerts)])
            await update.message.reply_text(
                self._t(user_id, 'alerts_list', alerts=alert_text),
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text(self._t(user_id, 'no_alerts'))

    async def show_settings(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать настройки"""
        user_id = update.effective_user.id
        await update.message.reply_text(
            self._t(user_id, 'settings_menu'),
            parse_mode='Markdown'
        )

# --- Background Tasks ---
def check_alerts(context, bot_instance: TelegramBot):
    """Фоновая функция для проверки ценовых уведомлений"""
    try:
        # Получаем всех пользователей с активными уведомлениями
        alert_manager = bot_instance.alert_manager
        converter = bot_instance.converter
        
        # Проверяем популярные пары
        pairs_to_check = ['BTC-USD', 'ETH-USD', 'BNB-USD', 'SOL-USD']
        
        for user_id_str in list(bot_instance.user_states.keys()):
            user_id = int(user_id_str) if isinstance(user_id_str, str) else user_id_str
            alerts = alert_manager.get_alerts(user_id)
            
            for alert in alerts:
                pair = alert['pair']
                # Получаем текущую цену
                try:
                    if pair in ['BTC', 'ETH', 'BNB', 'SOL', 'XRP']:
                        current_price = converter.get_crypto_rate_aggregated(pair, 'USDT', user_id)
                        if current_price:
                            triggered = alert_manager.check_alerts(user_id, pair, current_price)
                            
                            # Отправляем уведомления
                            for t_alert in triggered:
                                try:
                                    context.bot.send_message(
                                        chat_id=user_id,
                                        text=bot_instance._t(user_id, 'alert_triggered',
                                                           pair=t_alert['pair'],
                                                           condition=t_alert['condition'],
                                                           target=t_alert['target'],
                                                           current=current_price),
                                        parse_mode='Markdown'
                                    )
                                except:
                                    pass
                except:
                    continue
    except Exception as e:
        print(f"Alert check error: {e}")

def main():
    """Main function to setup and run the bot and scheduler."""
    app = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
    alert_manager = AlertManager()
    # Pass the bot instance to the converter for accessing user states
    bot_for_converter = TelegramBot(None, None, None, None, alert_manager, app)
    converter = CurrencyConverter(bot_for_converter)
    
    calculator = Calculator(converter)
    chart_generator = ChartGenerator()
    prediction_generator = PredictionGenerator()
    
    # Create the final bot instance with all components
    bot = TelegramBot(converter, calculator, chart_generator, prediction_generator, alert_manager, app)
    bot_for_converter.bot = bot # Fix circular reference

    scheduler = BackgroundScheduler()
    scheduler.add_job(check_alerts, 'interval', minutes=5, kwargs={'context': app, 'bot_instance': bot})
    scheduler.start()

    app.add_handler(CommandHandler("start", bot.start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_message))
    app.add_handler(CallbackQueryHandler(bot.handle_callback_query))

    print("🤖 Bot CoinFlow Ultimate is running...")
    app.run_polling()

if __name__ == "__main__":
    main()