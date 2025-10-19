# API Documentation for CoinFlow Bot

This document describes all external APIs used by CoinFlow Bot for fetching market data.

## Table of Contents
- [Cryptocurrency APIs](#cryptocurrency-apis)
- [Stock Market APIs](#stock-market-apis)
- [CS2 Market APIs](#cs2-market-apis)
- [Rate Limiting & Caching](#rate-limiting--caching)

---

## Cryptocurrency APIs

### 1. Multiple Exchange APIs (Existing)
Used for fetching real-time cryptocurrency prices and comparing rates across exchanges.

**Exchanges:**
- Binance
- Coinbase
- Kraken
- KuCoin
- Bybit

**Endpoint Examples:**
- Binance: `https://api.binance.com/api/v3/ticker/price`
- Coinbase: `https://api.coinbase.com/v2/exchange-rates`

**Rate Limits:** Varies by exchange (typically 1200 requests/minute for Binance)

---

## Stock Market APIs

### 1. Yahoo Finance (yfinance)
**Purpose:** Fetch global stock prices and historical data

**Library:** `yfinance` (Python wrapper for Yahoo Finance API)

**Usage:**
```python
import yfinance as yf
stock = yf.Ticker("AAPL")
info = stock.info
history = stock.history(period="30d")
```

**Features:**
- Real-time stock prices
- Historical data (daily, weekly, monthly)
- Company information (market cap, volume, etc.)
- Support for 50,000+ global stocks

**Supported Markets:**
- NYSE, NASDAQ (US stocks)
- LSE (London Stock Exchange)
- HKEX (Hong Kong Exchange)
- And many more

**Rate Limits:** 
- Free tier: 2,000 requests/hour per IP
- No official rate limit, but recommended to cache for 5+ minutes

**Covered Stocks (20+):**
- AAPL (Apple), MSFT (Microsoft), GOOGL (Alphabet)
- AMZN (Amazon), NVDA (NVIDIA), TSLA (Tesla)
- META (Meta/Facebook), JPM (JPMorgan Chase)
- And 16 more popular stocks

---

### 2. MOEX API (Moscow Exchange)
**Purpose:** Fetch Russian stock prices from Moscow Exchange

**Base URL:** `https://iss.moex.com/iss/`

**Endpoint Example:**
```
GET https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities/SBER.json
```

**Parameters:**
- `iss.meta=off` - Disable metadata
- `iss.only=securities,marketdata` - Only fetch specific data

**Response Format:** JSON

**Features:**
- Real-time prices for Russian stocks
- Trading volume data
- Previous close prices
- No authentication required

**Covered Stocks (15+):**
- SBER (Сбербанк), GAZP (Газпром), LKOH (Лукойл)
- GMKN (Норникель), YNDX (Яндекс), ROSN (Роснефть)
- And 9 more major Russian stocks

**Rate Limits:** 
- 60 requests/minute
- Recommended caching: 5 minutes

**Documentation:** https://www.moex.com/a2193

---

### 3. Central Bank of Russia (CBR) API
**Purpose:** Official exchange rates from the Russian Central Bank

**Base URL:** `https://www.cbr-xml-daily.ru/`

**Endpoint:**
```
GET https://www.cbr-xml-daily.ru/daily_json.js
```

**Response Format:** JSON

**Features:**
- Official daily exchange rates
- Updated once per day (around 15:00 Moscow time)
- Rates for 40+ currencies
- Historical rate changes

**Example Response:**
```json
{
  "Date": "2025-10-19T11:30:00+03:00",
  "Valute": {
    "USD": {
      "Value": 92.5432,
      "Previous": 92.1234,
      "Nominal": 1
    }
  }
}
```

**Covered Currencies (8):**
- USD (US Dollar), EUR (Euro), CNY (Chinese Yuan)
- GBP (British Pound), JPY (Japanese Yen), TRY (Turkish Lira)
- KZT (Kazakhstan Tenge), BYN (Belarusian Ruble)

**Rate Limits:** No official limit, updates once daily

**Caching:** Should be cached for at least 1 hour

**Documentation:** https://www.cbr-xml-daily.ru/

---

## CS2 Market APIs

### 1. Steam Community Market API
**Purpose:** Fetch CS2 (Counter-Strike 2) item prices from Steam

**Base URL:** `https://steamcommunity.com/market/`

**Endpoint:**
```
GET https://steamcommunity.com/market/priceoverview/
```

**Parameters:**
- `appid=730` - CS2/CSGO app ID
- `currency=1` - USD (1), EUR (3), RUB (5), etc.
- `market_hash_name` - Full item name (e.g., "AK-47 | Redline (Field-Tested)")

**Example Request:**
```
https://steamcommunity.com/market/priceoverview/?appid=730&currency=1&market_hash_name=AK-47%20%7C%20Redline%20(Field-Tested)
```

**Example Response:**
```json
{
  "success": true,
  "lowest_price": "$12.34",
  "median_price": "$13.45",
  "volume": "1,234"
}
```

**Rate Limits:**
- 20 requests/minute per IP
- **Important:** Very strict rate limiting
- Recommended: 5-minute cache minimum

**Covered Items (30+):**
- Knives: Karambit, M9 Bayonet, Butterfly Knife
- Gloves: Sport Gloves, Specialist Gloves, Driver Gloves
- Rifles: AK-47, M4A4, M4A1-S skins
- Snipers: AWP skins
- Pistols: Desert Eagle, Glock, USP-S skins

---

### 2. Skinport API
**Purpose:** Alternative CS2 item marketplace with public API

**Base URL:** `https://api.skinport.com/v1/`

**Endpoint:**
```
GET https://api.skinport.com/v1/items
```

**Parameters:**
- `app_id=730` - CS2
- `currency=USD`

**Features:**
- Returns all items with current prices
- Minimum price, suggested price
- No authentication required for basic queries

**Rate Limits:**
- 100 requests/hour for unauthenticated
- 1000 requests/hour with API key (free)

**Documentation:** https://docs.skinport.com/

---

### 3. CS.Money API (Note)
**Status:** No stable public API available

**Note:** CS.Money does not provide an official public API. Web scraping is not recommended due to:
- Terms of Service violations
- Unstable HTML structure
- IP blocking risk

**Alternative:** Use Steam Community Market and Skinport as primary sources.

---

## Rate Limiting & Caching

### Caching Strategy

All external API calls are cached to minimize requests and improve performance:

| API | Cache TTL | Reason |
|-----|-----------|--------|
| Yahoo Finance | 5 minutes | Stock prices update frequently during trading hours |
| MOEX API | 5 minutes | Real-time trading data |
| CBR Rates | 60 minutes | Updated once daily by CBR |
| Steam Market | 5 minutes | Strict rate limits |
| Skinport | 5 minutes | Moderate rate limits |
| Crypto Exchanges | 1-2 minutes | High volatility |

### Implementation

Caching is implemented using the `Cache` utility class:

```python
from coinflow.utils.cache import Cache

cache = Cache(ttl=300)  # 5 minutes
cache.set(key, data)
cached_data = cache.get(key)
```

### Best Practices

1. **Always cache API responses** - Reduces load and respects rate limits
2. **Use appropriate TTL** - Balance between freshness and performance
3. **Handle rate limit errors** - Implement exponential backoff
4. **Monitor API usage** - Track requests to avoid hitting limits
5. **Fallback mechanisms** - Use cached data if API fails

---

## Error Handling

All services implement comprehensive error handling:

```python
try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.RequestException as e:
    logger.error(f"API error: {e}")
    return None
```

**Common Error Scenarios:**
- Network timeouts (10 second timeout)
- Rate limit exceeded (429 status)
- Invalid data (404 status)
- API downtime (5xx status)

---

## Data Sources Summary

| Feature | Primary API | Backup API | Update Frequency |
|---------|-------------|------------|------------------|
| Global Stocks | Yahoo Finance | - | Real-time |
| Russian Stocks | MOEX | - | Real-time |
| CBR Rates | CBR XML Daily | - | Daily |
| CS2 Items | Steam Market | Skinport | Real-time |
| Cryptocurrencies | Binance + Others | CoinGecko | Real-time |

---

## API Keys & Authentication

**Current Status:** All APIs used are **free and public** with no authentication required.

**Future Considerations:**
- Yahoo Finance: Consider paid tier for higher limits
- Skinport: Free API key for 10x rate limit
- Premium crypto exchange APIs for additional features

---

## Compliance & Terms of Service

All APIs are used in compliance with their respective Terms of Service:

✅ **Yahoo Finance** - Free for non-commercial use  
✅ **MOEX** - Public data, free access  
✅ **CBR** - Open government data  
✅ **Steam** - Public market data (respect rate limits)  
✅ **Skinport** - Public API, free tier available  

**Disclaimer:** This bot is for informational purposes only and does not constitute financial advice.

---

## Additional Resources

- [Yahoo Finance Python Docs](https://pypi.org/project/yfinance/)
- [MOEX API Documentation](https://www.moex.com/a2193)
- [CBR XML Daily](https://www.cbr-xml-daily.ru/)
- [Skinport API Docs](https://docs.skinport.com/)
- [Steam Web API](https://steamcommunity.com/dev)

---

**Last Updated:** 2025-10-19  
**Version:** 2.0.0
