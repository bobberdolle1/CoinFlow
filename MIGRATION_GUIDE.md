# 🔄 Migration Guide: v1.0 → v2.0

## Overview

CoinFlow v2.0 introduces a major architectural overhaul with modular structure, persistent database, and enhanced features. This guide will help you migrate from v1.0 to v2.0.

## 🆕 What Changed

### Architecture
- **Old**: Monolithic `coinflow.py` (1000+ lines)
- **New**: Modular structure with separate packages for database, services, handlers, and utilities

### Database
- **Old**: `shelve` for alerts only, `user_states` in memory (lost on restart)
- **New**: SQLAlchemy with SQLite for persistent storage of users, alerts, history, and favorites

### Entry Point
- **Old**: `coinflow.py`
- **New**: `main.py` (coinflow.py still works but deprecated)

## 📋 Migration Steps

### Step 1: Backup Current Data

```bash
# Backup your current .env file
cp .env .env.backup

# Backup alert database (if exists)
cp alerts.db alerts.db.backup
```

### Step 2: Install New Dependencies

```bash
# Update dependencies
poetry install

# Or manually add new dependencies
poetry add sqlalchemy aiohttp
```

### Step 3: Update Environment Variables

The new `.env` has more configuration options:

```bash
# Copy new example
cp .env.example .env

# Add your bot token
TELEGRAM_BOT_TOKEN='YOUR_TOKEN_HERE'

# Optional: Customize other settings
DATABASE_URL='sqlite:///coinflow.db'
CACHE_TTL_SECONDS=60
ALERT_CHECK_INTERVAL=5
LOG_LEVEL=INFO
```

### Step 4: Run the New Version

```bash
# Run with Poetry
poetry run python main.py

# Or activate venv first
poetry shell
python main.py
```

## 🔧 Configuration Changes

### New Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `sqlite:///coinflow.db` | Database connection string |
| `CACHE_TTL_SECONDS` | `60` | Cache duration for rates |
| `ALERT_CHECK_INTERVAL` | `5` | Minutes between alert checks |
| `CHART_DPI` | `150` | Chart image quality |
| `LOG_LEVEL` | `INFO` | Logging level |
| `LOG_FILE` | `coinflow.log` | Log file path |

## 📊 Data Migration

### User Data
- **Users will need to `/start` again** to initialize in the new database
- Language preferences are lost (users select again on first start)
- User settings can be reconfigured via `/settings`

### Alerts
- **Old alerts from `alerts.db` are NOT automatically migrated**
- Users need to recreate their alerts
- Consider manual migration script if needed:

```python
# migration_script.py
import shelve
from coinflow.database import DatabaseRepository

old_db = shelve.open('alerts.db.backup')
new_db = DatabaseRepository('sqlite:///coinflow.db')

for user_id_str, alerts in old_db.items():
    user_id = int(user_id_str)
    for alert in alerts:
        new_db.add_alert(
            user_id=user_id,
            pair=alert['pair'],
            condition=alert['condition'],
            target=alert['target']
        )
old_db.close()
```

## 🐳 Docker Migration

### Old Deployment
```bash
# No docker support in v1.0
```

### New Deployment
```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Update
docker-compose pull
docker-compose up -d
```

## 🆕 New Features to Tell Users

### 1. History Command
```
Users can now type /history to see their last 10 conversions
```

### 2. Favorites System
```
Users can favorite currencies for quick access
Use the ⭐ button in currency selection
```

### 3. Inline Mode
```
Users can convert without opening bot:
@your_bot_username 100 USD to EUR
```

### 4. Statistics
```
Users can type /stats to see their usage statistics
```

### 5. Custom Chart Periods
```
When generating charts, users can select:
7 days / 30 days / 90 days / 1 year
```

## ⚠️ Breaking Changes

### 1. Old Entry Point Deprecated
- `coinflow.py` still exists but redirects to `main.py`
- Update systemd services or cron jobs to use `main.py`

### 2. User States Reset
- All in-memory user states are lost
- Users need to restart conversations

### 3. Import Changes
```python
# Old (v1.0)
from coinflow import TelegramBot

# New (v2.0)
from coinflow.bot import CoinFlowBot
```

## 🔍 Troubleshooting

### "Module not found" errors
```bash
# Reinstall dependencies
poetry install
```

### Database errors
```bash
# Delete old database and start fresh
rm coinflow.db
python main.py
```

### Permission errors
```bash
# Ensure data directory exists and is writable
mkdir -p data logs
chmod 755 data logs
```

### Old alerts.db conflicts
```bash
# Rename old database
mv alerts.db alerts.db.old
```

## 📝 Checklist

- [ ] Backup `.env` and `alerts.db`
- [ ] Install new dependencies (`poetry install`)
- [ ] Update `.env` with new variables
- [ ] Test bot with `python main.py`
- [ ] Announce to users about new features
- [ ] Inform users to `/start` again
- [ ] Inform users to recreate alerts
- [ ] Update deployment scripts (if any)
- [ ] Monitor logs for errors

## 🚀 Rollback Plan

If something goes wrong:

```bash
# 1. Stop new version
# Press Ctrl+C or:
docker-compose down

# 2. Restore old files
git checkout v1.0  # or restore from backup

# 3. Restore .env
cp .env.backup .env

# 4. Run old version
python coinflow.py
```

## 📞 Support

If you encounter issues during migration:
1. Check logs: `tail -f coinflow.log`
2. Review GitHub issues
3. Open a new issue with error details

## 🎉 Post-Migration

After successful migration:

1. **Test all features**:
   - Currency conversion
   - Charts generation
   - Predictions
   - Alerts
   - Calculator
   - History
   - Favorites

2. **Monitor performance**:
   - Check cache hit rates
   - Monitor database size
   - Review log files

3. **Announce new version** to users with feature list

4. **Clean up old files** (optional):
   ```bash
   # After confirming everything works
   rm alerts.db.backup
   rm .env.backup
   ```

---

**Ready to migrate? Follow the steps above and enjoy CoinFlow v2.0! 🚀**
