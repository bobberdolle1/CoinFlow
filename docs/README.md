# 📚 CoinFlow Bot Documentation

**Languages:** [English](#english) | [Русский](#russian)

Complete documentation for deploying and managing CoinFlow Bot.

---

<a name="english"></a>
## 📖 English Version

## 📖 Documentation Index

### Getting Started
- [Quick Start Guide](../QUICK_START.md) - Get up and running in 5 minutes
- [Migration Guide](../MIGRATION_GUIDE.md) - Upgrade from v1.0 to v2.0

### Deployment
- [🐳 Docker Guide](./DOCKER_GUIDE.md) - Deploy using Docker (recommended)
- [🚀 Deployment Guide](./DEPLOYMENT.md) - VPS, systemd, production setup ([Русский](./DEPLOYMENT.md#russian))
- [🔧 Troubleshooting](./TROUBLESHOOTING.md) - Common issues and solutions ([Русский](./TROUBLESHOOTING.md#russian))

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

---
---

<a name="russian"></a>
## 📖 Русская версия

# 📚 Документация CoinFlow Bot

Полная документация по развертыванию и управлению ботом CoinFlow.

## 📖 Содержание документации

### Начало работы
- [Краткое руководство](../QUICK_START.md) - Запустите бота за 5 минут
- [Руководство по миграции](../MIGRATION_GUIDE.md) - Обновление с v1.0 до v2.0

### Развертывание
- [🐳 Руководство по Docker](./DOCKER_GUIDE.md) - Развертывание с использованием Docker (рекомендуется)
- [🚀 Руководство по развертыванию](./DEPLOYMENT.md#russian) - VPS, systemd, настройка продакшена
- [🔧 Решение проблем](./TROUBLESHOOTING.md#russian) - Типичные проблемы и решения

### Быстрые ссылки
- [Основной README](../README.md) - Обзор проекта и функции
- [История изменений](../CHANGELOG.md) - История версий
- [Репозиторий GitHub](https://github.com/bobberdolle1/CoinFlow)

---

## 🚀 Быстрое развертывание

### Docker (Рекомендуется)

**Windows:**
```cmd
docker-run.bat
```

**Linux/Mac:**
```bash
chmod +x docker-run.sh
./docker-run.sh
```

### Вручную

```bash
# Клонировать и установить
git clone https://github.com/bobberdolle1/CoinFlow.git
cd CoinFlow
poetry install

# Настроить
cp .env.example .env
# Отредактировать .env и добавить TELEGRAM_BOT_TOKEN

# Запустить
poetry run python main.py
```

---

## 📋 Краткое описание документации

### Руководство по Docker
Полное руководство по развертыванию Docker включает:
- Необходимые условия для установки
- Использование вспомогательных скриптов (docker-run.bat/sh)
- Ручные команды Docker
- Параметры конфигурации
- Решение проблем

### Руководство по развертыванию
Развертывание в продакшене охватывает:
- Настройка VPS/облачного сервера
- Конфигурация сервиса Systemd
- Практики безопасности
- Мониторинг и обслуживание
- Процедуры обновления

### Решение проблем
Быстрые решения для:
- Проблемы установки
- Ошибки выполнения
- Проблемы с базой данных
- Проблемы API/сети
- Проблемы Docker

---

## 🆘 Нужна помощь?

1. Проверьте [Руководство по решению проблем](./TROUBLESHOOTING.md#russian)
2. Просмотрите [Руководство по Docker](./DOCKER_GUIDE.md) для проблем с Docker
3. См. [Руководство по развертыванию](./DEPLOYMENT.md#russian) для настройки сервера
4. Откройте issue на [GitHub](https://github.com/bobberdolle1/CoinFlow/issues)

---

**Сделано с ❤️ для сообщества**
