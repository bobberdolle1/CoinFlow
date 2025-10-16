# 🚀 Quick Start Guide - CoinFlow v2.0

Get your CoinFlow bot running in 5 minutes!

## Prerequisites

- Python 3.11+
- Poetry installed
- Telegram Bot Token

## Installation

### 1. Clone & Install

```bash
git clone https://github.com/bobberdolle1/CoinFlow.git
cd CoinFlow
poetry install
```

### 2. Configure

```bash
cp .env.example .env
```

Edit `.env` and add your bot token:
```env
TELEGRAM_BOT_TOKEN='your_token_from_botfather'
```

### 3. Run

```bash
poetry run python main.py
```

That's it! Your bot is now running! 🎉

## Docker (Alternative)

Prefer Docker? Even easier:

```bash
# 1. Clone
git clone https://github.com/bobberdolle1/CoinFlow.git
cd CoinFlow

# 2. Configure
cp .env.example .env
# Edit .env with your token

# 3. Run
docker-compose up -d
```

## First Steps

1. **Start the bot** in Telegram: `/start`
2. **Select your language**: English or Русский
3. **Try a conversion**: Click "⚡ Quick Convert"
4. **Explore features**:
   - 📊 Rate Charts
   - 🔮 Rate Forecast
   - ⚖️ Compare Rates
   - 🧮 Calculator
   - And more!

## Common Commands

| Command | Description |
|---------|-------------|
| `/start` | Initialize/restart bot |
| `/help` | Show help |
| `/stats` | Your usage statistics |
| `/history` | Conversion history |
| `/favorites` | Manage favorites |

## Inline Mode

Type in any chat:
```
@your_bot_username 100 USD to EUR
```
Get instant results!

## Troubleshooting

### Module not found
```bash
poetry install
```

### Bot not responding
- Check bot token in `.env`
- Verify internet connection
- Check logs: `tail -f coinflow.log`

### Permission errors
```bash
chmod +x main.py
```

## Configuration

Customize in `.env`:

```env
# Cache duration (seconds)
CACHE_TTL_SECONDS=60

# Alert check interval (minutes)  
ALERT_CHECK_INTERVAL=5

# Chart quality
CHART_DPI=150

# Logging
LOG_LEVEL=INFO
```

## Next Steps

- Read [README_V2.md](README_V2.md) for full documentation
- Check [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) if upgrading from v1.0
- Explore the modular codebase in `coinflow/` directory

## Need Help?

- 📖 Full docs: [README_V2.md](README_V2.md)
- 🐛 Issues: [GitHub Issues](https://github.com/bobberdolle1/CoinFlow/issues)
- 💬 Questions: Open a discussion

---

**Enjoy CoinFlow v2.0! 🪙✨**
