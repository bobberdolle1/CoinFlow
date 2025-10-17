# 📚 CoinFlow Bot Documentation

Complete documentation for deploying and managing CoinFlow Bot.

## 📖 Documentation Index

### Getting Started
- [Quick Start Guide](../QUICK_START.md) - Get up and running in 5 minutes
- [Migration Guide](../MIGRATION_GUIDE.md) - Upgrade from v1.0 to v2.0

### Deployment
- [🐳 Docker Guide](./DOCKER_GUIDE.md) - Deploy using Docker (recommended)
- [🚀 Deployment Guide](./DEPLOYMENT.md) - VPS, systemd, production setup
- [🔧 Troubleshooting](./TROUBLESHOOTING.md) - Common issues and solutions

### Quick Links
- [Main README](../README.md) - Project overview and features
- [Changelog](../CHANGELOG.md) - Version history
- [GitHub Repository](https://github.com/bobberdolle1/CoinFlow)

---

## 🚀 Quick Deploy

### Docker (Recommended)

**Windows:**
```cmd
docker-run.bat
```

**Linux/Mac:**
```bash
chmod +x docker-run.sh
./docker-run.sh
```

### Manual

```bash
# Clone and install
git clone https://github.com/bobberdolle1/CoinFlow.git
cd CoinFlow
poetry install

# Configure
cp .env.example .env
# Edit .env and add TELEGRAM_BOT_TOKEN

# Run
poetry run python main.py
```

---

## 📋 Documentation Summary

### Docker Guide
Complete guide for Docker deployment including:
- Installation prerequisites
- Using helper scripts (docker-run.bat/sh)
- Manual Docker commands
- Configuration options
- Troubleshooting

### Deployment Guide
Production deployment covering:
- VPS/Cloud server setup
- Systemd service configuration
- Security best practices
- Monitoring and maintenance
- Update procedures

### Troubleshooting
Quick solutions for:
- Installation issues
- Runtime errors
- Database problems
- API/Network issues
- Docker problems

---

## 🆘 Need Help?

1. Check [Troubleshooting Guide](./TROUBLESHOOTING.md)
2. Review [Docker Guide](./DOCKER_GUIDE.md) for Docker issues
3. See [Deployment Guide](./DEPLOYMENT.md) for server setup
4. Open issue on [GitHub](https://github.com/bobberdolle1/CoinFlow/issues)

---

**Made with ❤️ for the community**
