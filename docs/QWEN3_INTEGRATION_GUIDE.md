# Руководство по интеграции Qwen3 Cloud Models в CoinFlow Bot

## Обзор изменений

CoinFlow Bot v3.1+ теперь использует облачные модели **Qwen3** через Ollama для расширенного ИИ-функционала:

- **qwen3-coder:480b-cloud** - для текстовых запросов, управления ботом и генерации прогнозов
- **qwen3-vl:235b-cloud** - для визуального анализа графиков цен

### Ключевые улучшения

1. **Визуальный анализ прогнозов**: График цен анализируется ИИ-моделью с компьютерным зрением
2. **Поддержка акций**: ИИ-ассистент теперь понимает запросы об акциях (AAPL, TSLA, SBER.ME и т.д.)
3. **Унифицированная структура**: ЦБ РФ интегрирован как альтернативный источник данных для фиата
4. **Расширенный контекст**: 32K токенов для более сложных диалогов

---

## Установка и настройка

### Шаг 1: Установка Ollama

```bash
# Скачайте и установите Ollama с официального сайта
# https://ollama.ai

# Проверьте установку
ollama --version
```

### Шаг 2: Загрузка моделей

⚠️ **ВНИМАНИЕ**: Эти модели очень большие (~480GB и ~235GB) и требуют мощного железа!

```bash
# Загрузить текстовую модель (может занять несколько часов)
ollama pull qwen3-coder:480b-cloud

# Загрузить визуальную модель
ollama pull qwen3-vl:235b-cloud
```

**Альтернатива для тестирования** (меньшие модели):
```bash
# Используйте меньшие модели для локальной разработки
ollama pull qwen3:8b
ollama pull llava:7b
```

### Шаг 3: Конфигурация бота

Обновите `.env` файл:

```env
# Ollama AI settings
OLLAMA_URL=http://localhost:11434
OLLAMA_TEXT_MODEL=qwen3-coder:480b-cloud
OLLAMA_VISION_MODEL=qwen3-vl:235b-cloud

# Для локального тестирования используйте меньшие модели:
# OLLAMA_TEXT_MODEL=qwen3:8b
# OLLAMA_VISION_MODEL=llava:7b
```

### Шаг 4: Запуск бота

```bash
# Убедитесь, что Ollama запущен
# Ollama работает автоматически после установки

# Запустите бота
python main.py
```

---

## Архитектура

### Компоненты системы

```
┌─────────────────────────────────────────────────────┐
│                 CoinFlow Bot                         │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌───────────────┐      ┌────────────────────┐    │
│  │  AI Service   │◄─────┤  Prediction Gen.   │    │
│  │ (2 models)    │      │  (with vision)     │    │
│  └───────┬───────┘      └────────────────────┘    │
│          │                                          │
│  ┌───────▼────────────────────────────────┐       │
│  │        Ollama API Server                │       │
│  │  ┌──────────────┐  ┌──────────────┐   │       │
│  │  │ qwen3-coder  │  │  qwen3-vl    │   │       │
│  │  │ 480b-cloud   │  │  235b-cloud  │   │       │
│  │  └──────────────┘  └──────────────┘   │       │
│  └─────────────────────────────────────────┘       │
│                                                      │
└─────────────────────────────────────────────────────┘
```

### Новые методы в AI Service

#### `get_text_response(prompt, system_prompt, temperature, max_tokens)`
Получение текстового ответа от qwen3-coder.

```python
response = await ai_service.get_text_response(
    prompt="Что такое Bitcoin?",
    system_prompt="Ты финансовый ассистент",
    temperature=0.7,
    max_tokens=1000
)
```

#### `get_vision_analysis(image_path, prompt, temperature)`
Анализ изображения с помощью qwen3-vl.

```python
analysis = await ai_service.get_vision_analysis(
    image_path="/tmp/chart.png",
    prompt="Проанализируй этот график цен BTC",
    temperature=0.7
)
```

### Улучшенный прогноз с визуальным анализом

```python
# В prediction_generator теперь доступен метод:
chart_bytes, stats, vision_analysis = await prediction_generator.generate_prediction_with_vision_analysis(
    symbol='BTC-USD',
    asset_type='crypto',
    model_type='arima',
    days=90,
    forecast_days=7
)

# Результат включает:
# - chart_bytes: изображение графика
# - stats: числовые статистики (ARIMA/LinReg)
# - vision_analysis: текстовый анализ от qwen3-vl
```

---

## Использование

### 1. Прогнозы с визуальным анализом

```python
# Пример использования в handler
async def handle_forecast(update, context):
    symbol = 'AAPL'  # Можно использовать криптовалюты или акции
    
    # Генерируем прогноз с AI-анализом
    chart, stats, ai_analysis = await bot.prediction_generator.generate_prediction_with_vision_analysis(
        symbol=symbol,
        asset_type='stock',
        model_type='arima'
    )
    
    # Формируем сообщение
    message = f"""
📊 **Прогноз для {symbol}**

📈 Текущая цена: ${stats['current']:.2f}
🔮 Прогноз (7 дней): ${stats['predicted']:.2f}
📊 Изменение: {stats['change']:+.2f}%
🎯 Модель: {stats['model']}

🤖 **AI-анализ графика:**
{ai_analysis}

⚠️ Это не финансовая рекомендация.
"""
    
    await update.message.reply_photo(photo=chart, caption=message)
```

### 2. ИИ-ассистент с поддержкой акций

Теперь бот понимает запросы типа:
- "Покажи график Apple"
- "Прогноз для Сбербанка"
- "Сколько стоит Tesla?"
- "Сравни BTC и AAPL"

```python
# Пример обработки запроса
result = await ai_service.interpret_user_message(
    message="Покажи график Tesla",
    user_lang='ru'
)

if result['type'] == 'command':
    action = result['action']  # 'CHART'
    symbol = result['params']['symbol']  # 'TSLA'
    # Выполнить команду...
```

### 3. Интеграция акций

Акции теперь являются первоклассными активами в боте:

```python
# В StockService уже интегрированы:
GLOBAL_STOCKS = {
    'AAPL': 'Apple Inc.',
    'MSFT': 'Microsoft',
    'TSLA': 'Tesla',
    # ... и 20+ других
}

RUSSIAN_STOCKS = {
    'SBER': 'Сбербанк',
    'GAZP': 'Газпром',
    'LKOH': 'Лукойл',
    # ... и 15+ других
}
```

---

## Производительность и стоимость

### Требования к железу

**Для облачных моделей (480B/235B):**
- GPU: 8x NVIDIA A100 (80GB) или аналог
- RAM: 512GB+
- Диск: 1TB+ SSD

**Для локальных моделей (8B/7B):**
- GPU: NVIDIA RTX 3090 (24GB) или аналог
- RAM: 32GB
- Диск: 50GB SSD

### Время обработки

| Операция | Cloud Model | Local Model |
|----------|-------------|-------------|
| Текстовый ответ | 2-5 сек | <1 сек |
| Визуальный анализ | 5-15 сек | 2-5 сек |
| Прогноз с vision | 15-30 сек | 5-10 сек |

### Стоимость (примерная)

**Cloud hosting:**
- ~$3-5 за GPU-час (AWS/GCP)
- ~$100-200/день при активном использовании

**Локальный запуск:**
- Стоимость электричества (~300W GPU)
- Амортизация железа

⚠️ **Рекомендация**: Используйте меньшие модели для разработки и тестирования!

---

## Troubleshooting

### Проблема: Модели не загружаются

```bash
# Проверьте статус Ollama
ollama list

# Попробуйте загрузить модель вручную
ollama pull qwen3-coder:480b-cloud

# Проверьте логи
journalctl -u ollama -f
```

### Проблема: Vision анализ не работает

Проверьте, что модель доступна:
```python
if bot.ai_service.vision_available:
    print("Vision model OK")
else:
    print("Vision model not available")
```

### Проблема: Медленная генерация

1. Проверьте GPU утилизацию: `nvidia-smi`
2. Используйте меньшие модели для тестирования
3. Настройте `max_tokens` и `temperature`

### Проблема: Out of Memory

Уменьшите размер модели:
```env
OLLAMA_TEXT_MODEL=qwen3:8b
OLLAMA_VISION_MODEL=llava:7b
```

---

## Migration Guide

### Обновление с v3.0

1. Обновите зависимости:
```bash
poetry install
```

2. Обновите `.env`:
```bash
cp .env .env.backup
cat .env.example >> .env
# Отредактируйте новые переменные
```

3. Загрузите модели (см. Шаг 2)

4. Перезапустите бота

### Обратная совместимость

Бот полностью работает без AI-моделей:
- Стандартные прогнозы (ARIMA/LinReg) работают
- Конвертация валют работает
- Графики генерируются

Только визуальный анализ требует qwen3-vl.

---

## API Reference

### AIService

```python
class AIService:
    def __init__(self, ollama_url: str, 
                 text_model: str, 
                 vision_model: str)
    
    async def check_availability(self, auto_pull: bool = False) -> bool
    async def get_text_response(self, prompt: str, ...) -> str
    async def get_vision_analysis(self, image_path: str, ...) -> str
    async def interpret_user_message(self, message: str, ...) -> Dict
```

### PredictionGenerator

```python
class PredictionGenerator:
    def __init__(self, dpi: int, db, ai_service)
    
    async def generate_prediction_with_vision_analysis(
        self, 
        symbol: str,
        asset_type: str = 'crypto',
        model_type: str = 'arima',
        days: int = 90,
        forecast_days: int = 7
    ) -> Tuple[bytes, Dict, str]
```

---

## Дальнейшее развитие

### Планируемые улучшения

- [ ] Кэширование AI-ответов для популярных запросов
- [ ] Batch-обработка множественных прогнозов
- [ ] Fine-tuning моделей на финансовых данных
- [ ] Интеграция с реальными торговыми сигналами
- [ ] Мультиязычный анализ новостей

### Экспериментальные функции

- Sentiment analysis из новостей
- Portfolio optimization с помощью AI
- Автоматические торговые стратегии
- Real-time market commentary

---

## Поддержка

При возникновении проблем:

1. Проверьте логи: `tail -f coinflow.log`
2. Проверьте статус Ollama: `ollama list`
3. Откройте issue на GitHub
4. Консультируйтесь с документацией Ollama: https://ollama.ai/docs

---

## Лицензия

CoinFlow Bot - MIT License
Qwen3 Models - см. лицензию на https://qwenlm.github.io/

---

**Версия документа**: 1.0  
**Дата**: 2025-10-24  
**Совместимость**: CoinFlow Bot v3.1+
