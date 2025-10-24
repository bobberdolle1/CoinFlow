# Интеграция акций в CoinFlow Bot

## Обзор

CoinFlow Bot v3.1+ теперь полностью поддерживает работу с акциями (stocks) наравне с криптовалютами и фиатными валютами. Акции интегрированы во все ключевые функции бота.

---

## Поддерживаемые акции

### Глобальные акции (US Market)

| Тикер | Компания | Биржа |
|-------|----------|-------|
| AAPL | Apple Inc. | NASDAQ |
| MSFT | Microsoft | NASDAQ |
| GOOGL | Alphabet (Google) | NASDAQ |
| AMZN | Amazon | NASDAQ |
| NVDA | NVIDIA | NASDAQ |
| TSLA | Tesla | NASDAQ |
| META | Meta (Facebook) | NASDAQ |
| V | Visa | NYSE |
| JPM | JPMorgan Chase | NYSE |
| ... | +15 других | - |

### Российские акции (MOEX)

| Тикер | Компания | Биржа |
|-------|----------|-------|
| SBER.ME | Сбербанк | MOEX |
| GAZP.ME | Газпром | MOEX |
| LKOH.ME | Лукойл | MOEX |
| GMKN.ME | Норникель | MOEX |
| YNDX.ME | Яндекс | MOEX |
| ROSN.ME | Роснефть | MOEX |
| NVTK.ME | Новатэк | MOEX |
| ... | +10 других | - |

---

## Функционал

### 1. Просмотр информации об акциях

```
📊 Stocks → Global Stocks → AAPL
```

Отображается:
- Текущая цена
- Изменение за 24 часа (%)
- Рыночная капитализация
- Объём торгов
- Кнопка для просмотра графика

### 2. Графики акций

```
📊 Stocks → Global Stocks → AAPL → Show Chart
```

Доступные периоды:
- 7 дней
- 30 дней (по умолчанию)
- 90 дней
- 365 дней

Данные из **Yahoo Finance** (для глобальных) и **MOEX API** (для российских).

### 3. Прогнозы цен акций

Теперь прогнозы работают не только для крипты, но и для акций:

```python
# Пример прогноза для акций
chart, stats, ai_analysis = await prediction_generator.generate_prediction_with_vision_analysis(
    symbol='AAPL',
    asset_type='stock',
    model_type='arima',
    days=90,
    forecast_days=7
)
```

Доступные модели:
- **ARIMA** - для акций с выраженным трендом
- **Linear Regression** - для стабильных акций
- **Prophet** (опционально) - для сложных паттернов

### 4. ИИ-ассистент с поддержкой акций

Бот понимает естественные запросы:

**Примеры запросов:**
- "Покажи график Apple" → Отображает график AAPL
- "Прогноз для Tesla" → Генерирует прогноз TSLA
- "Сколько стоит Сбербанк?" → Показывает текущую цену SBER.ME
- "Сравни Microsoft и Google" → (планируется)

**Поддерживаемые альтернативные названия:**
- Apple → AAPL
- Tesla → TSLA
- Microsoft → MSFT
- Сбер, Сбербанк → SBER.ME
- Газпром → GAZP.ME

### 5. Портфолио с акциями

Добавьте акции в свой портфель:

```
💼 Portfolio → Add Asset → Stock → AAPL → Quantity: 10
```

Функции:
- Отслеживание стоимости портфеля в реальном времени
- Автоматический расчёт P&L (прибыль/убыток)
- Диверсификация по типам активов (crypto/stock/fiat)
- Экспорт в CSV, JSON, Google Sheets

### 6. Уведомления по ценам

```
🔔 Notifications → Add Alert → Stock → TSLA → Above $300
```

Типы алертов:
- Цена выше порога
- Цена ниже порога
- Изменение на X%

---

## API и источники данных

### Yahoo Finance (yfinance)

Используется для:
- Глобальные акции (NASDAQ, NYSE, etc.)
- Исторические данные
- Прогнозирование

```python
import yfinance as yf

stock = yf.Ticker('AAPL')
data = stock.history(period='1mo')
```

### MOEX API

Используется для:
- Российские акции
- Реальное время (без задержки)

```python
url = f'https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities/{ticker}.json'
```

### Кэширование

Данные кэшируются на **5 минут** для оптимизации:
- Снижение нагрузки на API
- Быстрый отклик
- Актуальность данных

---

## Архитектура

```
┌─────────────────────────────────────────────┐
│            StockService                      │
├─────────────────────────────────────────────┤
│                                              │
│  get_global_stock(ticker) ──► Yahoo Finance │
│  get_russian_stock(ticker) ──► MOEX API     │
│  get_cbr_rate(currency) ────► CBR API       │
│                                              │
└───────┬─────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────┐
│         StocksHandler                        │
├─────────────────────────────────────────────┤
│  show_stocks_menu()                          │
│  show_global_stocks()                        │
│  show_russian_stocks()                       │
│  show_stock_chart()                          │
└─────────────────────────────────────────────┘
```

---

## Удаление отдельного раздела ЦБ РФ

### Что изменилось?

**Раньше:**
```
📊 Stocks
  ├─ Global Stocks
  ├─ Russian Stocks
  └─ 💱 CBR Rates (отдельный раздел)
```

**Теперь:**
```
📊 Stocks
  ├─ Global Stocks
  └─ Russian Stocks

💱 Converter (встроено)
  ├─ Market rate (default)
  └─ CBR rate (опция для RUB)
```

### Как это работает?

Курсы ЦБ РФ теперь используются как **альтернативный источник данных** для конвертации с участием рубля:

```python
# При конвертации USD → RUB
rate = converter.get_rate('USD', 'RUB', source='cbr')  # Официальный курс ЦБ
rate = converter.get_rate('USD', 'RUB', source='market')  # Рыночный курс (default)
```

**Преимущества:**
- Унифицированный интерфейс
- Меньше навигации для пользователя
- Акции стали первоклассными активами
- ЦБ РФ остаётся доступным там, где нужен

---

## Примеры использования

### Пример 1: Мониторинг портфеля акций

```python
# Пользователь добавляет акции в портфель
portfolio.add_item(user_id, 'AAPL', quantity=10, asset_type='stock')
portfolio.add_item(user_id, 'TSLA', quantity=5, asset_type='stock')
portfolio.add_item(user_id, 'SBER.ME', quantity=100, asset_type='stock')

# Получение сводки
summary = portfolio.get_summary(user_id)
# {
#   'total_value_usd': 12450.50,
#   'by_type': {
#     'stock': {'total_value_usd': 12450.50, 'count': 3}
#   }
# }
```

### Пример 2: Прогноз с AI-анализом

```python
# Пользователь запрашивает прогноз для Tesla
chart, stats, analysis = await bot.prediction_generator.generate_prediction_with_vision_analysis(
    symbol='TSLA',
    asset_type='stock',
    model_type='arima',
    days=90,
    forecast_days=7
)

# Отправка пользователю
message = f"""
📊 Прогноз TSLA на 7 дней

💰 Текущая цена: ${stats['current']:.2f}
🔮 Прогноз: ${stats['predicted']:.2f}
📈 Изменение: {stats['change']:+.2f}%
🎯 Модель: {stats['model']}

🤖 AI-анализ:
{analysis}
"""

await update.message.reply_photo(photo=chart, caption=message)
```

### Пример 3: Голосовой запрос

```
🎤 "Покажи мне график Apple за последние три месяца"

↓ (Voice → Text via Whisper)

↓ (Text → AI interpretation)

↓ {
    "command": "CHART",
    "symbol": "AAPL",
    "days": 90,
    "type": "stock"
  }

↓ (Execute command)

📊 [График AAPL 90 дней]
```

---

## Ограничения

### 1. Рыночные часы

Акции торгуются только в определённые часы:
- **US Market**: 16:30 - 23:00 МСК (пн-пт)
- **MOEX**: 10:00 - 18:40 МСК (пн-пт)

Вне торговых часов данные не обновляются.

### 2. API Limits

- **Yahoo Finance**: без жестких лимитов, но есть rate limiting
- **MOEX API**: 100 запросов/минуту

Кэширование помогает избежать превышения лимитов.

### 3. Задержка данных

- Yahoo Finance: задержка ~15 минут для free tier
- MOEX API: real-time для российских акций

---

## FAQ

**Q: Можно ли добавить другие акции?**  
A: Да, добавьте тикеры в `stock_service.py` → `GLOBAL_STOCKS` или `RUSSIAN_STOCKS`.

**Q: Почему нет прогнозов для мелких акций?**  
A: Недостаточно исторических данных. Требуется минимум 30 дней торговли.

**Q: Как работает визуальный анализ для акций?**  
A: График отправляется в qwen3-vl модель, которая анализирует паттерны и тренды.

**Q: Можно ли использовать реальные торговые сигналы?**  
A: Да, но это не финансовые советы. Используйте на свой риск.

**Q: Поддерживаются ли ETF и индексы?**  
A: Частично. Можно добавить тикеры ETF (SPY, QQQ, etc.) в список акций.

---

## Roadmap

### v3.2 (Q4 2025)
- [ ] Сравнение акций side-by-side
- [ ] Индикаторы (RSI, MACD, Bollinger Bands)
- [ ] Скринер акций по критериям

### v3.3 (Q1 2026)
- [ ] ETF и индексы
- [ ] Dividends tracking
- [ ] Corporate events (splits, earnings)

### v4.0 (Q2 2026)
- [ ] Реальные торговые интеграции (API брокеров)
- [ ] Paper trading (демо-торговля)
- [ ] Backtest стратегий

---

**Версия документа**: 1.0  
**Дата**: 2025-10-24  
**Совместимость**: CoinFlow Bot v3.1+
