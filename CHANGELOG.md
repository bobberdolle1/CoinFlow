# Changelog

All notable changes to CoinFlow Bot will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-10-16

### 🎉 Major Release - Complete Rewrite

### Added
- 🏗️ **Modular Architecture**: Separated into services, handlers, database, and utilities packages
- 💾 **SQLAlchemy Database**: Persistent storage with User, Alert, ConversionHistory, and Favorite models
- ⭐ **Favorites System**: Save frequently used currencies for quick access
- 📜 **Conversion History**: Track all conversions with timestamps and statistics
- 💬 **Inline Mode**: Quick conversions in any chat (`@bot 100 USD to EUR`)
- 📅 **Custom Chart Periods**: Choose from 7/30/90/365 days for historical charts
- 📊 **User Statistics**: View personal usage stats and popular currency pairs
- ⚡ **Smart Caching**: 60-second TTL cache for exchange rates
- 🚀 **Async Support**: Asynchronous exchange rate fetching
- 📝 **Professional Logging**: Rotating file logs with configurable levels
- 📊 **Metrics System**: Track bot usage with comprehensive statistics
- 🐳 **Docker Support**: Full containerization with docker-compose
- 🔧 **New Commands**: `/stats`, `/history`, `/favorites`, `/help`, `/cancel`
- 🔘 **Button-based Menu**: All functions accessible via buttons (no typing)

### Changed
- 🔒 **Security**: Replaced `eval()` with AST-based safe calculator
- 📁 **Project Structure**: From monolithic `coinflow.py` to modular package
- 🗄️ **Data Storage**: From `shelve` to SQLAlchemy with SQLite
- 🎯 **Entry Point**: Changed from `coinflow.py` to `main.py`
- ⚙️ **Configuration**: Enhanced `.env` with more options
- 📖 **Documentation**: Comprehensive README with migration guide

### Improved
- ⚡ **Performance**: Caching and async operations reduce API calls
- 🔄 **Reliability**: Auto-reconnect and error handling
- 🎨 **User Experience**: Streamlined button-based interface
- 📊 **Data Persistence**: User states and history survive restarts
- 🌍 **Localization**: Better EN/RU translations

### Technical
- **Dependencies**: Added `sqlalchemy ^2.0` and `aiohttp ^3.9`
- **Python**: Requires Python 3.11+
- **Database Schema**: 4 tables (Users, Alerts, ConversionHistory, Favorites)
- **API**: python-telegram-bot ^22.5 with async support

### Migration Notes
- Users must restart bot with `/start`
- Old alerts from v1.0 need to be recreated
- Favorites must be added again
- See `MIGRATION_GUIDE.md` for details

## [1.0.0] - 2025-10-15

### Initial Release
- Basic currency conversion
- Cryptocurrency analysis
- Price charts (30 days)
- AI predictions (ARIMA, Linear Regression)
- Price alerts
- Calculator with conversion
- Exchange rate comparison (5+ exchanges)
- Inline button interface
- EN/RU localization
- Background alert monitoring
