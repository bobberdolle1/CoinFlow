# 🔧 Troubleshooting Guide

Common issues and solutions for CoinFlow Bot.

## 🔨 Installation Issues

### ModuleNotFoundError: No module named 'sqlalchemy'

**Solution:**
```bash
poetry install
```

### Poetry not found

**Solution:**
```bash
curl -sSL https://install.python-poetry.org | python3 -
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Python version mismatch (3.11+ required)

**Solution:**
```bash
python3 --version  # Check version
sudo apt install python3.11  # Ubuntu
```

---

## ⚡ Runtime Errors

### Bot not responding to commands

**Check 1: Token configured?**
```bash
cat .env | grep TELEGRAM_BOT_TOKEN
```

**Check 2: Bot running?**
```bash
ps aux | grep python
```

### ImportError: cannot import name 'engine'

**Solution:** Update to latest version:
```bash
git pull origin main
poetry install
```

---

## 💾 Database Issues

### Database locked

**Solution:**
```bash
# Stop bot
sudo systemctl stop coinflow  # or kill process

# Remove lock
rm data/coinflow.db-lock

# Restart
sudo systemctl start coinflow
```

### Database corrupted

**Solution:**
```bash
# Backup old DB
mv data/coinflow.db data/coinflow.db.backup

# Bot will create new DB on start
poetry run python main.py
```

---

## 🌐 API & Network Issues

### Rate limit exceeded

**Problem:** Too many requests to exchange APIs.

**Solution:** Wait 1-2 minutes, bot has 60-second cache.

### Connection timeout

**Solution:**
```bash
# Check internet connection
ping google.com

# Check DNS
nslookup api.binance.com
```

---

## 🐳 Docker Issues

### Container won't start

**Solution:**
```bash
# Check logs
docker-compose logs

# Rebuild
docker-compose up -d --build
```

### Permission denied

**Linux solution:**
```bash
sudo usermod -aG docker $USER
newgrp docker
```

### Port already in use

**Solution:**
```bash
# Find process
sudo lsof -i :8080

# Kill process
sudo kill -9 <PID>
```

---

## 🚀 Performance Issues

### High memory usage

**Solution:**
```bash
# Check usage
docker stats coinflow-bot

# Restart bot
docker-compose restart
```

### Slow responses

**Possible causes:**
- API rate limits
- Network issues
- High load

**Solution:** Check logs for errors:
```bash
docker-compose logs | grep ERROR
```

---

## 📝 Common Commands

### Check bot status
```bash
# Systemd
sudo systemctl status coinflow

# Docker
docker ps | grep coinflow
```

### View logs
```bash
# Systemd
sudo journalctl -u coinflow -f

# Docker
docker-compose logs -f
```

### Restart bot
```bash
# Systemd
sudo systemctl restart coinflow

# Docker
docker-compose restart
```

---

## 🆘 Still Having Issues?

1. Check full logs for error details
2. Verify .env configuration
3. Ensure all dependencies installed
4. Try fresh install in clean directory
5. Open issue on [GitHub](https://github.com/bobberdolle1/CoinFlow/issues)

---

## 📚 See Also

- [Docker Guide](./DOCKER_GUIDE.md)
- [Deployment Guide](./DEPLOYMENT.md)
- [Quick Start](../QUICK_START.md)
