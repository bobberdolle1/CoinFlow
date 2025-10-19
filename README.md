# 🪙 CoinFlow Bot v2.0 - Ultimate Edition

![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg) ![License](https://img.shields.io/badge/License-MIT-green.svg) ![Status](https://img.shields.io/badge/Status-Production%20Ready-success.svg) ![Version](https://img.shields.io/badge/Version-2.0-orange.svg)

**Advanced Telegram bot for currency conversion and cryptocurrency analysis with professional architecture**

[English](#english) | [Русский](#русский)

---

<a name="english"></a>

## 🇬🇧 English

**CoinFlow** is your ultimate Telegram-based financial assistant that combines:
- 💱 Advanced multi-source currency converter (60+ currencies)
- 📊 Real-time cryptocurrency analysis from 5+ exchanges
- 📈 Global & Russian stock market analytics (35+ stocks)
- 🎮 CS2 item price comparison across marketplaces
- 🔮 AI-powered price forecasting (ARIMA & Linear Regression)
- 📈 Interactive charts and historical data visualization
- 🧮 Built-in calculator with currency conversion support
- 🔔 Automated price alerts and notifications

**Key Innovation:** 100% button-based interface — no manual typing required! Get conversions in just 2-3 clicks.

### 🚀 User Experience (v2.0)

**Complete button-based workflow:**

1. **Quick Convert** → Select FROM currency → Select TO currency → Choose amount (presets: 10/50/100/500/1000/5000) → **Instant result!**

2. **Rate Charts** → Select crypto → Select period (7/30/90/365 days) → **See price chart for 1 unit** (e.g., 1 BTC = $67,234)

3. **Rate Forecast** → Select crypto → **Get AI prediction for 1 unit** (7-day forecast with trend)

4. **Compare Rates** → Select crypto → **See prices for 1 unit across 5+ exchanges** with best price recommendation

5. **Price Alerts** → Set target price → Get instant notifications when reached

6. **History & Stats** → View conversion history, favorites, personal statistics

**No typing. No copy-paste. Just buttons!** 🎯

**New in v2.0:** Charts, forecasts, and comparisons now display **price for 1 unit** by default (industry standard UX), making it easy to compare assets like on CoinGecko or TradingView.

### ✨ Key Features

#### 🎯 **User-Friendly Interface**
- **100% Button-Based:** No manual input required — everything via inline buttons
- **Categorized Currency Selection:** Popular (9), Fiat (30+), Crypto (30+)
- **Preset Amounts:** Quick selection of common amounts (10, 50, 100, 500, 1000, 5000)
- **2-3 Click Conversions:** Fastest conversion experience possible

#### 💱 **Advanced Currency Conversion**
- **60+ Currencies:** 30+ fiat currencies (USD, EUR, RUB, CNY, GBP, JPY, etc.)
- **30+ Cryptocurrencies:** BTC, ETH, BNB, SOL, ADA, DOGE, DOT, MATIC, and more
- **Multi-Source Aggregation:** Data from 5+ exchanges for maximum accuracy
- **Automatic Fallback:** If one source fails, seamlessly switches to the next

#### 📊 **Real-Time Market Data**
- **5+ Exchange Integration:** Binance, Bybit, HTX (Huobi), KuCoin, Gate.io, BestChange
- **Live Price Comparison:** Compare spot prices across all exchanges instantly
- **Spread Analysis:** See highest, lowest, average prices and spread percentage
- **ЦБ РФ Integration:** Optional official Central Bank of Russia rates for RUB

#### 🔮 **AI-Powered Forecasting**
- **Dual Models:** ARIMA (statistical) and Linear Regression (trend-based)
- **7-Day Predictions:** Forward-looking price forecasts with trend visualization
- **90-Day Analysis:** Historical data analysis for accurate predictions
- **Visual Charts:** Beautiful matplotlib-generated graphs with trend lines

#### 📈 **Data Visualization**
- **30-Day Historical Charts:** Price movement with high/low/average statistics
- **HD Graphics:** 150 DPI publication-quality charts
- **Interactive Statistics:** Current price, averages, extremes

#### 🔔 **Smart Notifications**
- **Price Alerts:** Set target prices with above/below conditions
- **Background Monitoring:** Automatic checks every 5 minutes
- **Instant Notifications:** Real-time alerts when targets are hit
- **Persistent Storage:** Alerts saved in local database

#### 🧮 **Built-in Calculator**
- **Mathematical Expressions:** Standard calculations (100 + 50 * 2)
- **Currency Conversion:** Direct format (100 USD to EUR)
- **Safe Evaluation:** Secure calculation engine

#### 🌍 **Multilingual**
- **English 🇬🇧:** Full translation
- **Russian 🇷🇺:** Полный перевод
- **Easy Language Switch:** Change anytime in settings

### 🆕 What's New in v2.0

**Major Architectural Improvements:**
- 🏗️ **Modular Structure**: Separated into `services/`, `handlers/`, `database/`, `utils/` packages
- 💾 **SQLAlchemy Database**: Persistent storage for users, alerts, history, and favorites (replaces shelve)
- ⚡ **Smart Caching**: 60-second TTL cache for exchange rates reduces API calls
- 🔒 **Enhanced Security**: Replaced `eval()` with AST-based safe calculator
- 📊 **Advanced Metrics**: Comprehensive bot usage tracking and analytics
- 🚀 **Async Support**: Asynchronous exchange rate fetching for better performance
- 🐳 **Docker Ready**: Full containerization with `docker-compose.yml`
- 📝 **Professional Logging**: Rotating file logs with configurable levels

**New Features:**
- ⭐ **Favorites System**: Save frequently used currencies for quick access
- 📜 **Conversion History**: Track all conversions with timestamps (last 10 visible)
- 💬 **Inline Mode**: Quick conversions without opening bot (`@bot 100 USD to EUR`)
- 📅 **Custom Chart Periods**: Choose from 7/30/90/365 days
- 📊 **User Statistics**: View usage stats, popular pairs, total conversions
- 🔘 **Button-based Commands**: All functions accessible via buttons (History, Stats, Favorites)
- 🔄 **Auto-reconnect**: Improved reliability with automatic recovery

**UX Improvements:**
- 📊 **Price for 1 Unit**: Charts, forecasts, and comparisons now show price per 1 unit (e.g., 1 BTC)
- 🎯 **Streamlined Flow**: No amount input for charts/forecasts (only for conversions)
- 📱 **Industry Standard**: Follows UX patterns from CoinGecko, TradingView, Binance

**Market Expansion:**
- 📈 **Stock Market Integration**: Global stocks (Yahoo Finance), Russian stocks (MOEX), CBR official rates
- 🎮 **Gaming Market**: CS2 item prices from Steam Community Market and Skinport
- 🌍 **Universal Coverage**: Crypto + Stocks + Gaming = All-in-one analytics tool

### 📈 Stock Market Features (NEW!)

#### 🌍 Global Stocks (20+ tickers)
- **Popular stocks**: AAPL, MSFT, GOOGL, AMZN, NVDA, TSLA, META, JPM, and more
- **Real-time data**: Current price, 24h change ($ and %), market cap, volume
- **Charts**: 30-day price history with interactive statistics
- **API**: Yahoo Finance (yfinance library)

#### 🇷🇺 Russian Stocks (15+ tickers)
- **Major stocks**: Сбербанк (SBER), Газпром (GAZP), Лукойл (LKOH), Норникель (GMKN), Яндекс (YNDX)
- **MOEX integration**: Real-time prices from Moscow Exchange
- **Ruble pricing**: All prices in RUB with daily change tracking

#### 💱 CBR Exchange Rates (8 currencies)
- **Official rates**: USD, EUR, CNY, GBP, JPY, TRY, KZT, BYN
- **Daily updates**: Central Bank of Russia official exchange rates
- **Unified menu**: Russian stocks and CBR rates in one convenient interface

### 🎮 CS2 Market Features (NEW!)

#### Item Categories (30+ items)
- **🔪 Knives**: Karambit, M9 Bayonet, Butterfly Knife, Talon Knife
- **🧤 Gloves**: Sport Gloves, Specialist Gloves, Driver Gloves
- **🔫 Rifles**: AK-47, M4A4, M4A1-S skins (Redline, Vulcan, Asiimov, etc.)
- **🎯 Snipers**: AWP skins (Dragon Lore, Asiimov, Hyper Beast, etc.)
- **🔫 Pistols**: Desert Eagle, Glock, USP-S premium skins
- **⚡ SMGs**: P90, MAC-10, Five-SeveN skins

#### Price Comparison
- **Multi-marketplace**: Steam Community Market + Skinport
- **Smart analysis**: Average, min, max prices with spread calculation
- **Best deal finder**: Automatic recommendation for best buying price
- **Real-time updates**: 5-minute cache for fresh pricing data

### 🛠️ Tech Stack

**Core:**
- Python 3.11+
- `python-telegram-bot` ^22.5 (async API)
- `sqlalchemy` ^2.0 (ORM for database)
- `aiohttp` ^3.9 (async HTTP client)

**Data & Analytics:**
- `yfinance` ^0.2 (market data)
- `matplotlib` ^3.9 (charts)
- `statsmodels` ^0.14 (ARIMA)
- `scikit-learn` ^1.5 (ML)
- `numpy` ^2.0 (computations)

**Infrastructure:**
- `apscheduler` ^3.10 (background tasks)
- `python-dotenv` ^1.0 (config)
- `bestchange-api` ^3.1 (exchange rates)
- `requests` ^2.32 (HTTP)
- Docker & docker-compose

**Dependency Management:** Poetry

### 🎮 Bot Commands & Features

**Main Menu Buttons:**
- ⚡ **Quick Convert**: Currency conversion with amount presets
- 📊 **Rate Charts**: Historical price charts (7/30/90/365 days) for 1 unit
- 🔮 **Rate Forecast**: AI price predictions for 1 unit (7-day ahead)
- ⚖️ **Compare Rates**: Cross-exchange price comparison for 1 unit
- 📈 **Stocks**: Global stocks, Russian stocks (MOEX), CBR exchange rates
- 🎮 **CS2 Skins**: CS2 item prices across Steam & Skinport marketplaces
- 🧮 **Calculator**: Math expressions with currency conversion
- 🔔 **Notifications**: Manage price alerts
- ⭐ **Favorites**: Quick access to saved currencies
- 📜 **History**: View last 10 conversions
- 📊 **Statistics**: Personal usage stats and popular pairs
- ⚙️ **Settings**: Bot configuration and language

**Slash Commands (also available as buttons):**
- `/start` - Start/restart the bot
- `/help` - Show help message
- `/stats` - View your statistics
- `/history` - Conversion history
- `/favorites` - Manage favorites
- `/cancel` - Cancel current operation

**Inline Mode:**
```
@your_bot_username 100 USD to EUR
```
Get instant conversion in any chat!

### 📚 Documentation

Complete guides for deployment and troubleshooting:

- [📚 Documentation Index](./docs/README.md) - All documentation ([Russian version](./docs/README.md#russian))
- [📦 Installation Guide](./docs/INSTALLATION.md) - Complete installation from scratch ([Russian version](./docs/INSTALLATION.md#русский))
- [🚀 Quick Start Guide](./docs/QUICK_START.md) - Get started in 5 minutes
- [🐳 Docker Guide](./docs/DOCKER_GUIDE.md) - Deploy with Docker
- [🚀 Deployment Guide](./docs/DEPLOYMENT.md) - Production setup ([Russian version](./docs/DEPLOYMENT.md#russian))
- [🔧 Troubleshooting](./docs/TROUBLESHOOTING.md) - Common issues ([Russian version](./docs/TROUBLESHOOTING.md#russian))

---

### ⚙️ Installation & Usage

> 📦 **New to setup?** Check our [Complete Installation Guide](./docs/INSTALLATION.md) for step-by-step instructions including Python, Poetry, and Docker installation from scratch!

#### **Prerequisites**
- Python 3.11 or higher
- Poetry (Python dependency manager)
- Telegram Bot Token from [@BotFather](https://t.me/BotFather)

#### **Quick Start**

1. **Clone the repository:**
   ```bash
   git clone https://github.com/bobberdolle1/CoinFlow.git
   cd CoinFlow
   ```

2. **Install Poetry** (if not already installed):
   ```bash
   # Linux/macOS/WSL
   curl -sSL https://install.python-poetry.org | python3 -
   
   # Windows (PowerShell)
   (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
   ```

3. **Configure environment:**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your bot token:
   ```env
   TELEGRAM_BOT_TOKEN='YOUR_ACTUAL_BOT_TOKEN_HERE'
   ```

4. **Install dependencies:**
   ```bash
   poetry install
   ```

5. **Run the bot:**
   ```bash
   poetry run python main.py
   ```

6. **Start chatting with your bot in Telegram!**

#### **Update Dependencies**

To update to the latest versions:
```bash
poetry update
```

#### **Development**

Activate virtual environment:
```bash
poetry shell
python main.py
```

---

<a name="русский"></a>

## 🇷🇺 Русский

**CoinFlow** — ваш персональный финансовый ассистент в Telegram, который объединяет:
- 💱 Продвинутый конвертер валют с множественными источниками (60+ валют)
- 📊 Анализ криптовалют в реальном времени с 5+ бирж
- 🔮 ИИ-прогнозирование цен (ARIMA и Линейная Регрессия)
- 📈 Интерактивные графики и визуализация исторических данных
- 🧮 Встроенный калькулятор с конвертацией валют
- 🔔 Автоматические уведомления о ценах

**Главная инновация:** 100% кнопочный интерфейс — никакого ручного ввода! Конвертация за 2-3 клика.

### 🚀 Пользовательский опыт (v2.0)

**Полностью кнопочный workflow:**

1. **Быстрая конвертация** → Выбор валюты ОТ → Выбор валюты В → Выбор суммы (пресеты: 10/50/100/500/1000/5000) → **Мгновенный результат!**

2. **Графики курсов** → Выбор крипты → Выбор периода (7/30/90/365 дней) → **График цены 1 единицы** (например, 1 BTC = $67,234)

3. **Прогноз курса** → Выбор крипты → **ИИ-прогноз для 1 единицы** (на 7 дней с трендом)

4. **Сравнение курсов** → Выбор крипты → **Цены 1 единицы на 5+ биржах** с рекомендацией лучшей цены

5. **Ценовые уведомления** → Установка целевой цены → Мгновенные уведомления при достижении

6. **История и статистика** → История конвертаций, избранное, личная статистика

**Никакого набора текста. Никакого копипаста. Только кнопки!** 🎯

**Новое в v2.0:** Графики, прогнозы и сравнения теперь показывают **цену за 1 единицу** по умолчанию (стандарт индустрии), что упрощает сравнение активов как на CoinGecko или TradingView.

### ✨ Ключевые особенности

#### 🎯 **Удобный интерфейс**
- **100% на кнопках:** Не требуется ручной ввод — всё через inline-кнопки
- **Категоризованный выбор валют:** Популярные (9), Фиат (30+), Крипта (30+)
- **Пресеты сумм:** Быстрый выбор популярных сумм (10, 50, 100, 500, 1000, 5000)
- **Конвертация за 2-3 клика:** Максимально быстрый опыт конвертации

#### 💱 **Продвинутая конвертация валют**
- **60+ валют:** 30+ фиатных валют (USD, EUR, RUB, CNY, GBP, JPY и др.)
- **30+ криптовалют:** BTC, ETH, BNB, SOL, ADA, DOGE, DOT, MATIC и другие
- **Агрегация из множества источников:** Данные с 5+ бирж для максимальной точности
- **Автоматический резерв:** Если один источник недоступен, плавное переключение на следующий

#### 📊 **Рыночные данные в реальном времени**
- **Интеграция с 5+ биржами:** Binance, Bybit, HTX (Huobi), KuCoin, Gate.io, BestChange
- **Сравнение цен в реальном времени:** Мгновенное сравнение спотовых цен на всех биржах
- **Анализ спреда:** Максимальная, минимальная, средняя цены и процент спреда
- **Интеграция с ЦБ РФ:** Опциональные официальные курсы Центрального Банка России для RUB

#### 🔮 **ИИ-прогнозирование**
- **Две модели:** ARIMA (статистическая) и Линейная Регрессия (на основе тренда)
- **7-дневные прогнозы:** Перспективные прогнозы цен с визуализацией тренда
- **Анализ 90 дней:** Анализ исторических данных для точных прогнозов
- **Визуальные графики:** Красивые графики matplotlib с линиями тренда

#### 📈 **Визуализация данных**
- **30-дневные исторические графики:** Движение цен со статистикой максимумов/минимумов/средних
- **HD-графика:** Графики публикационного качества 150 DPI
- **Интерактивная статистика:** Текущая цена, средние, экстремумы

#### 🔔 **Умные уведомления**
- **Ценовые алерты:** Установка целевых цен с условиями выше/ниже
- **Фоновый мониторинг:** Автоматические проверки каждые 5 минут
- **Мгновенные уведомления:** Уведомления в реальном времени при достижении целей
- **Постоянное хранилище:** Алерты сохраняются в локальной базе данных

#### 🧮 **Встроенный калькулятор**
- **Математические выражения:** Стандартные вычисления (100 + 50 * 2)
- **Конвертация валют:** Прямой формат (100 USD to EUR)
- **Безопасное вычисление:** Защищённый движок расчётов

#### 🌍 **Мультиязычность**
- **English 🇬🇧:** Полный перевод
- **Русский 🇷🇺:** Полный перевод
- **Лёгкая смена языка:** Изменение в любое время в настройках

### 🛠️ Стек технологий

- **Язык:** Python 3.11+
- **Фреймворк бота:** `python-telegram-bot` ^22.5 (последний async API)
- **Финансовые данные:** `yfinance` ^0.2 (Yahoo Finance API)
- **HTTP-клиент:** `requests` ^2.32 (подключения к API бирж)
- **Визуализация данных:** `matplotlib` ^3.9 (генерация графиков)
- **Машинное обучение:** 
  - `statsmodels` ^0.14 (ARIMA прогнозирование)
  - `scikit-learn` ^1.5 (Линейная Регрессия)
  - `numpy` ^2.0 (численные вычисления)
- **Планировщик задач:** `apscheduler` ^3.10 (фоновые задачи)
- **Конфигурация:** `python-dotenv` ^1.0 (переменные окружения)
- **Интеграция с биржами:** `bestchange-api` ^3.1 (курсы BestChange)
- **Хранение данных:** `shelve` (встроенное, постоянное хранение алертов)
- **Управление зависимостями:** `poetry` (современная упаковка Python)

### 📚 Документация

Полные руководства по развертыванию и решению проблем:

- [📚 Содержание документации](./docs/README.md#russian) - Вся документация
- [📦 Руководство по установке](./docs/INSTALLATION.md#русский) - Полная установка с нуля
- [🚀 Краткое руководство](./docs/QUICK_START.md) - Запустите бота за 5 минут
- [🐳 Руководство по Docker](./docs/DOCKER_GUIDE.md) - Развертывание с Docker
- [🚀 Руководство по развертыванию](./docs/DEPLOYMENT.md#russian) - Настройка продакшена
- [🔧 Решение проблем](./docs/TROUBLESHOOTING.md#russian) - Типичные проблемы

---

### ⚙️ Установка и запуск

> 📦 **Впервые устанавливаете?** Смотрите [Полное руководство по установке](./docs/INSTALLATION.md#русский) с пошаговыми инструкциями, включая установку Python, Poetry и Docker с нуля!

#### **Требования**
- Python 3.11 или выше
- Poetry (менеджер зависимостей Python)
- Токен Telegram-бота от [@BotFather](https://t.me/BotFather)

#### **Быстрый старт**

1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/bobberdolle1/CoinFlow.git
   cd CoinFlow
   ```

2. **Установите Poetry** (если ещё не установлен):
   ```bash
   # Linux/macOS/WSL
   curl -sSL https://install.python-poetry.org | python3 -
   
   # Windows (PowerShell)
   (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
   ```

3. **Настройте окружение:**
   ```bash
   cp .env.example .env
   ```
   
   Отредактируйте `.env` и добавьте токен вашего бота:
   ```env
   TELEGRAM_BOT_TOKEN='ВАШ_РЕАЛЬНЫЙ_ТОКЕН_БОТА_ЗДЕСЬ'
   ```

4. **Установите зависимости:**
   ```bash
   poetry install
   ```

5. **Запустите бота:**
   ```bash
   poetry run python main.py
   ```

6. **Начните общаться с ботом в Telegram!**

#### **Обновление зависимостей**

Для обновления до последних версий:
```bash
poetry update
```

#### **Разработка**

Активация виртуального окружения:
```bash
poetry shell
python main.py
```

---

## ⚠️ Отказ от ответственности

Этот бот является сложным технологическим демонстрационным проектом. Данные о курсах предоставляются для ознакомительных целей. Функция прогнозирования использует упрощенную математическую модель и **не является финансовым советом или торговой рекомендацией**. Всегда проводите собственное исследование перед принятием финансовых решений.

## 📄 Лицензия

Проект распространяется под лицензией MIT. Вы можете свободно использовать и изменять код.