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
- 🔮 AI-powered price forecasting (ARIMA & Linear Regression)
- 📈 Interactive charts and historical data visualization
- 🧮 Built-in calculator with currency conversion support
- 🔔 Automated price alerts and notifications

**Key Innovation:** 100% button-based interface — no manual typing required! Get conversions in just 2-3 clicks.

### 🚀 User Experience

**Complete button-based workflow:**

1. **Quick Convert** → Select FROM currency (button) → Select TO currency (button) → Choose amount (preset buttons: 10/50/100/500/1000/5000) → **Instant result!**

2. **Compare Rates** → Select crypto (button) → Get live prices from 5+ exchanges with spread analysis

3. **Rate Forecast** → Select crypto (button) → Get AI-powered 7-day prediction with trend visualization

4. **Charts** → Select crypto (button) → Get 30-day historical chart with statistics

**No typing. No copy-paste. Just buttons!** 🎯

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

### 🛠️ Tech Stack

- **Language:** Python 3.11+
- **Bot Framework:** `python-telegram-bot` ^22.5 (latest async API)
- **Financial Data:** `yfinance` ^0.2 (Yahoo Finance API)
- **HTTP Client:** `requests` ^2.32 (exchange API connections)
- **Data Visualization:** `matplotlib` ^3.9 (chart generation)
- **Machine Learning:** 
  - `statsmodels` ^0.14 (ARIMA forecasting)
  - `scikit-learn` ^1.5 (Linear Regression)
  - `numpy` ^2.0 (numerical computations)
- **Task Scheduling:** `apscheduler` ^3.10 (background jobs)
- **Configuration:** `python-dotenv` ^1.0 (environment variables)
- **Exchange Integration:** `bestchange-api` ^3.1 (BestChange rates)
- **Data Storage:** `shelve` (built-in, persistent alerts storage)
- **Dependency Management:** `poetry` (modern Python packaging)

### ⚙️ Installation & Usage

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

### 🚀 Пользовательский опыт

**Полностью кнопочный workflow:**

1. **Быстрая конвертация** → Выбор валюты ОТ (кнопка) → Выбор валюты В (кнопка) → Выбор суммы (пресеты: 10/50/100/500/1000/5000) → **Мгновенный результат!**

2. **Сравнение курсов** → Выбор крипты (кнопка) → Получение актуальных цен с 5+ бирж с анализом спреда

3. **Прогноз курса** → Выбор крипты (кнопка) → Получение ИИ-прогноза на 7 дней с визуализацией тренда

4. **Графики** → Выбор крипты (кнопка) → Получение графика за 30 дней со статистикой

**Никакого набора текста. Никакого копипаста. Только кнопки!** 🎯

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

### ⚙️ Установка и запуск

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
   poetry run python coinflow.py
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
python coinflow.py
```

---

## ⚠️ Отказ от ответственности

Этот бот является сложным технологическим демонстрационным проектом. Данные о курсах предоставляются для ознакомительных целей. Функция прогнозирования использует упрощенную математическую модель и **не является финансовым советом или торговой рекомендацией**. Всегда проводите собственное исследование перед принятием финансовых решений.

## 📄 Лицензия

Проект распространяется под лицензией MIT. Вы можете свободно использовать и изменять код.