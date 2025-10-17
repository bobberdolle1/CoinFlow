# 🚀 Deployment Guide

**Languages:** [English](#english) | [Русский](#russian)

Complete guide for deploying CoinFlow Bot to production environments.

---

<a name="english"></a>
## 📖 English Version

## 📋 Table of Contents

- [Deployment Options](#deployment-options)
- [Local Server](#local-server)
- [VPS/Cloud Server](#vpscloud-server)
- [Docker Container](#docker-container)
- [Systemd Service](#systemd-service)
- [Environment Configuration](#environment-configuration)
- [Security Best Practices](#security-best-practices)

---

## 🎯 Deployment Options

### 1. Local Machine (Development)
- **Pros**: Easy setup, full control
- **Cons**: Not always online, not suitable for production
- **Best for**: Testing, development

### 2. VPS/Cloud Server (Production)
- **Pros**: 24/7 uptime, reliable
- **Cons**: Monthly cost
- **Best for**: Production bots
- **Providers**: DigitalOcean, Linode, AWS, Hetzner, Vultr

### 3. Docker Container
- **Pros**: Easy deployment, isolated environment
- **Cons**: Requires Docker knowledge
- **Best for**: Production with Docker

### 4. Raspberry Pi (Home Server)
- **Pros**: Low power consumption, cheap
- **Cons**: Limited resources
- **Best for**: Small-scale personal use

---

## 💻 Local Server Deployment

### Prerequisites
- Python 3.11+
- Poetry
- Git

### Steps

```bash
# 1. Clone repository
git clone https://github.com/bobberdolle1/CoinFlow.git
cd CoinFlow

# 2. Install dependencies
poetry install

# 3. Configure environment
cp .env.example .env
nano .env  # Add your TELEGRAM_BOT_TOKEN

# 4. Run bot
poetry run python main.py
```

### Keep Running with Screen/tmux

**Using screen:**
```bash
# Start screen session
screen -S coinflow

# Run bot
poetry run python main.py

# Detach: Press Ctrl+A, then D
# Reattach: screen -r coinflow
```

**Using tmux:**
```bash
# Start tmux session
tmux new -s coinflow

# Run bot
poetry run python main.py

# Detach: Press Ctrl+B, then D
# Reattach: tmux attach -t coinflow
```

---

## ☁️ VPS/Cloud Server Deployment

### 1. Choose a Provider

**Recommended Providers:**
- **DigitalOcean**: $5-10/month, easy to use
- **Hetzner**: €3-5/month, good EU servers
- **Vultr**: $2.50-5/month, global locations
- **Linode**: $5-10/month, reliable

**Minimum Specs:**
- 1 vCPU
- 1GB RAM
- 20GB SSD
- Ubuntu 22.04 LTS

### 2. Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.11
sudo apt install python3.11 python3.11-venv python3-pip git -y

# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### 3. Deploy Bot

```bash
# Clone repository
cd ~
git clone https://github.com/bobberdolle1/CoinFlow.git
cd CoinFlow

# Install dependencies
poetry install

# Configure
cp .env.example .env
nano .env  # Add TELEGRAM_BOT_TOKEN

# Test run
poetry run python main.py
```

### 4. Setup Systemd Service (Auto-start)

See [Systemd Service](#systemd-service) section below.

---

## 🐳 Docker Deployment

### Prerequisites
- Docker installed
- docker-compose installed

### Quick Deploy

```bash
# 1. Clone repository
git clone https://github.com/bobberdolle1/CoinFlow.git
cd CoinFlow

# 2. Configure environment
cp .env.example .env
nano .env  # Add TELEGRAM_BOT_TOKEN

# 3. Run with helper script
chmod +x docker-run.sh
./docker-run.sh
# Select option 1: Build and start

# OR manually:
docker-compose up -d --build
```

### Production Docker Setup

**docker-compose.prod.yml:**
```yaml
version: '3.8'

services:
  coinflow:
    build: .
    container_name: coinflow-bot
    env_file: .env
    restart: unless-stopped
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
```

Run:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

---

## ⚙️ Systemd Service (Linux)

Create a systemd service for auto-start on boot.

### 1. Create Service File

```bash
sudo nano /etc/systemd/system/coinflow.service
```

### 2. Service Configuration

```ini
[Unit]
Description=CoinFlow Telegram Bot
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/home/YOUR_USERNAME/CoinFlow
Environment="PATH=/home/YOUR_USERNAME/.local/bin:/usr/bin"
ExecStart=/home/YOUR_USERNAME/.local/bin/poetry run python main.py
Restart=always
RestartSec=10
StandardOutput=append:/var/log/coinflow/bot.log
StandardError=append:/var/log/coinflow/error.log

[Install]
WantedBy=multi-user.target
```

**Replace:**
- `YOUR_USERNAME` with your actual username

### 3. Create Log Directory

```bash
sudo mkdir -p /var/log/coinflow
sudo chown YOUR_USERNAME:YOUR_USERNAME /var/log/coinflow
```

### 4. Enable and Start

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service (start on boot)
sudo systemctl enable coinflow

# Start service
sudo systemctl start coinflow

# Check status
sudo systemctl status coinflow

# View logs
sudo journalctl -u coinflow -f
```

### 5. Manage Service

```bash
# Start
sudo systemctl start coinflow

# Stop
sudo systemctl stop coinflow

# Restart
sudo systemctl restart coinflow

# Status
sudo systemctl status coinflow

# Disable auto-start
sudo systemctl disable coinflow

# View logs
sudo journalctl -u coinflow -n 100
sudo journalctl -u coinflow -f  # follow logs
```

---

## 🔐 Environment Configuration

### Production .env

```env
# Bot Token (REQUIRED)
TELEGRAM_BOT_TOKEN='your_production_token'

# Database (SQLite - default)
DATABASE_URL='sqlite:///data/coinflow.db'

# Cache
CACHE_TTL_SECONDS=60

# Alerts
ALERT_CHECK_INTERVAL=5

# Charts
CHART_DPI=150
DEFAULT_CHART_PERIOD=30

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/coinflow.log
```

### PostgreSQL (Optional)

For production, consider PostgreSQL:

```env
DATABASE_URL='postgresql://user:password@localhost:5432/coinflow'
```

Install dependencies:
```bash
poetry add psycopg2-binary
```

---

## 🛡️ Security Best Practices

### 1. Bot Token Security

```bash
# Never commit .env to git
echo ".env" >> .gitignore

# Secure .env permissions
chmod 600 .env

# Use environment variables
export TELEGRAM_BOT_TOKEN='your_token'
```

### 2. Server Security

```bash
# Update system regularly
sudo apt update && sudo apt upgrade -y

# Setup firewall
sudo ufw allow 22/tcp  # SSH
sudo ufw enable

# Create non-root user
sudo adduser botuser
sudo usermod -aG sudo botuser

# Disable root SSH
sudo nano /etc/ssh/sshd_config
# Set: PermitRootLogin no
sudo systemctl restart sshd

# Setup fail2ban (protection against brute force)
sudo apt install fail2ban
sudo systemctl enable fail2ban
```

### 3. Monitoring

```bash
# Monitor bot process
ps aux | grep python

# Check memory usage
free -h

# Check disk space
df -h

# View system logs
journalctl -xe
```

### 4. Backup Strategy

```bash
# Backup database daily
0 2 * * * /usr/bin/cp /home/user/CoinFlow/data/coinflow.db /home/user/backups/coinflow-$(date +\%Y\%m\%d).db

# Keep last 7 days
0 3 * * * find /home/user/backups -name "coinflow-*.db" -mtime +7 -delete
```

---

## 🔄 Updates

### Manual Update

```bash
# Pull latest code
cd ~/CoinFlow
git pull origin main

# Update dependencies
poetry install

# Restart bot
# If using systemd:
sudo systemctl restart coinflow

# If using Docker:
docker-compose up -d --build

# If using screen/tmux:
# Kill old process and start new one
```

### Automated Updates (Optional)

Create update script:
```bash
#!/bin/bash
cd ~/CoinFlow
git pull origin main
poetry install
sudo systemctl restart coinflow
```

---

## 📊 Monitoring & Maintenance

### Health Checks

```bash
# Check if bot is running
systemctl status coinflow

# Check logs for errors
journalctl -u coinflow | grep ERROR

# Check resource usage
htop
```

### Log Rotation

Setup logrotate:
```bash
sudo nano /etc/logrotate.d/coinflow
```

```
/var/log/coinflow/*.log {
    daily
    rotate 7
    compress
    missingok
    notifempty
}
```

---

## 🆘 Troubleshooting

### Bot Not Starting

```bash
# Check service status
sudo systemctl status coinflow

# View detailed logs
sudo journalctl -u coinflow -n 100

# Check .env file
cat .env | grep TELEGRAM_BOT_TOKEN
```

### Permission Errors

```bash
# Fix ownership
sudo chown -R YOUR_USERNAME:YOUR_USERNAME ~/CoinFlow

# Fix permissions
chmod -R 755 ~/CoinFlow
chmod 600 ~/CoinFlow/.env
```

### Database Locked

```bash
# Stop bot
sudo systemctl stop coinflow

# Remove lock
rm ~/CoinFlow/data/coinflow.db-lock

# Start bot
sudo systemctl start coinflow
```

---

## 📚 Additional Resources

- [Docker Guide](./DOCKER_GUIDE.md)
- [Troubleshooting](./TROUBLESHOOTING.md)
- [DigitalOcean Tutorials](https://www.digitalocean.com/community/tutorials)
- [Systemd Documentation](https://www.freedesktop.org/software/systemd/man/)

---
---

<a name="russian"></a>
## 📖 Русская версия

# 🚀 Руководство по развертыванию

Полное руководство по развертыванию бота CoinFlow в продакшн среде.

## 📋 Содержание

- [Варианты развертывания](#варианты-развертывания)
- [Локальный сервер](#локальный-сервер)
- [VPS/Облачный сервер](#vpsоблачный-сервер)
- [Docker контейнер](#docker-контейнер)
- [Systemd сервис](#systemd-сервис)
- [Настройка окружения](#настройка-окружения)
- [Практики безопасности](#практики-безопасности)

---

## 🎯 Варианты развертывания

### 1. Локальная машина (Разработка)
- **Плюсы**: Простая настройка, полный контроль
- **Минусы**: Не всегда онлайн, не подходит для продакшена
- **Подходит для**: Тестирование, разработка

### 2. VPS/Облачный сервер (Продакшен)
- **Плюсы**: Работа 24/7, надежность
- **Минусы**: Ежемесячная плата
- **Подходит для**: Продакшн боты
- **Провайдеры**: DigitalOcean, Linode, AWS, Hetzner, Vultr

### 3. Docker контейнер
- **Плюсы**: Простое развертывание, изолированная среда
- **Минусы**: Требуется знание Docker
- **Подходит для**: Продакшен с Docker

### 4. Raspberry Pi (Домашний сервер)
- **Плюсы**: Низкое энергопотребление, дешево
- **Минусы**: Ограниченные ресурсы
- **Подходит для**: Небольшое личное использование

---

## 💻 Развертывание на локальном сервере

### Требования
- Python 3.11+
- Poetry
- Git

### Шаги

```bash
# 1. Клонировать репозиторий
git clone https://github.com/bobberdolle1/CoinFlow.git
cd CoinFlow

# 2. Установить зависимости
poetry install

# 3. Настроить окружение
cp .env.example .env
nano .env  # Добавьте ваш TELEGRAM_BOT_TOKEN

# 4. Запустить бота
poetry run python main.py
```

### Поддержание работы с Screen/tmux

**Использование screen:**
```bash
# Запустить screen сессию
screen -S coinflow

# Запустить бота
poetry run python main.py

# Отключиться: Нажмите Ctrl+A, затем D
# Подключиться обратно: screen -r coinflow
```

**Использование tmux:**
```bash
# Запустить tmux сессию
tmux new -s coinflow

# Запустить бота
poetry run python main.py

# Отключиться: Нажмите Ctrl+B, затем D
# Подключиться обратно: tmux attach -t coinflow
```

---

## ☁️ Развертывание на VPS/Облачном сервере

### 1. Выбрать провайдера

**Рекомендуемые провайдеры:**
- **DigitalOcean**: $5-10/месяц, простой в использовании
- **Hetzner**: €3-5/месяц, хорошие серверы в ЕС
- **Vultr**: $2.50-5/месяц, глобальные локации
- **Linode**: $5-10/месяц, надежный

**Минимальные характеристики:**
- 1 vCPU
- 1GB RAM
- 20GB SSD
- Ubuntu 22.04 LTS

### 2. Настройка сервера

```bash
# Обновить систему
sudo apt update && sudo apt upgrade -y

# Установить Python 3.11
sudo apt install python3.11 python3.11-venv python3-pip git -y

# Установить Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Добавить Poetry в PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### 3. Развернуть бота

```bash
# Клонировать репозиторий
cd ~
git clone https://github.com/bobberdolle1/CoinFlow.git
cd CoinFlow

# Установить зависимости
poetry install

# Настроить
cp .env.example .env
nano .env  # Добавить TELEGRAM_BOT_TOKEN

# Тестовый запуск
poetry run python main.py
```

### 4. Настроить Systemd сервис (Автозапуск)

См. раздел [Systemd сервис](#systemd-сервис) ниже.

---

## 🐳 Развертывание Docker

### Требования
- Установленный Docker
- Установленный docker-compose

### Быстрое развертывание

```bash
# 1. Клонировать репозиторий
git clone https://github.com/bobberdolle1/CoinFlow.git
cd CoinFlow

# 2. Настроить окружение
cp .env.example .env
nano .env  # Добавить TELEGRAM_BOT_TOKEN

# 3. Запустить со вспомогательным скриптом
chmod +x docker-run.sh
./docker-run.sh
# Выберите опцию 1: Собрать и запустить

# ИЛИ вручную:
docker-compose up -d --build
```

### Продакшн настройка Docker

**docker-compose.prod.yml:**
```yaml
version: '3.8'

services:
  coinflow:
    build: .
    container_name: coinflow-bot
    env_file: .env
    restart: unless-stopped
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
```

Запуск:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

---

## ⚙️ Systemd сервис (Linux)

Создание systemd сервиса для автозапуска при загрузке.

### 1. Создать файл сервиса

```bash
sudo nano /etc/systemd/system/coinflow.service
```

### 2. Конфигурация сервиса

```ini
[Unit]
Description=CoinFlow Telegram Bot
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/home/YOUR_USERNAME/CoinFlow
Environment="PATH=/home/YOUR_USERNAME/.local/bin:/usr/bin"
ExecStart=/home/YOUR_USERNAME/.local/bin/poetry run python main.py
Restart=always
RestartSec=10
StandardOutput=append:/var/log/coinflow/bot.log
StandardError=append:/var/log/coinflow/error.log

[Install]
WantedBy=multi-user.target
```

**Замените:**
- `YOUR_USERNAME` на ваше фактическое имя пользователя

### 3. Создать директорию для логов

```bash
sudo mkdir -p /var/log/coinflow
sudo chown YOUR_USERNAME:YOUR_USERNAME /var/log/coinflow
```

### 4. Включить и запустить

```bash
# Перезагрузить systemd
sudo systemctl daemon-reload

# Включить сервис (запуск при загрузке)
sudo systemctl enable coinflow

# Запустить сервис
sudo systemctl start coinflow

# Проверить статус
sudo systemctl status coinflow

# Просмотр логов
sudo journalctl -u coinflow -f
```

### 5. Управление сервисом

```bash
# Запустить
sudo systemctl start coinflow

# Остановить
sudo systemctl stop coinflow

# Перезапустить
sudo systemctl restart coinflow

# Статус
sudo systemctl status coinflow

# Отключить автозапуск
sudo systemctl disable coinflow

# Просмотр логов
sudo journalctl -u coinflow -n 100
sudo journalctl -u coinflow -f  # следить за логами
```

---

## 🔐 Настройка окружения

### Продакшн .env

```env
# Bot Token (ОБЯЗАТЕЛЬНО)
TELEGRAM_BOT_TOKEN='your_production_token'

# База данных (SQLite - по умолчанию)
DATABASE_URL='sqlite:///data/coinflow.db'

# Кеш
CACHE_TTL_SECONDS=60

# Оповещения
ALERT_CHECK_INTERVAL=5

# Графики
CHART_DPI=150
DEFAULT_CHART_PERIOD=30

# Логирование
LOG_LEVEL=INFO
LOG_FILE=logs/coinflow.log
```

### PostgreSQL (Опционально)

Для продакшена рассмотрите PostgreSQL:

```env
DATABASE_URL='postgresql://user:password@localhost:5432/coinflow'
```

Установка зависимостей:
```bash
poetry add psycopg2-binary
```

---

## 🛡️ Практики безопасности

### 1. Безопасность токена бота

```bash
# Никогда не коммитьте .env в git
echo ".env" >> .gitignore

# Защитите права доступа к .env
chmod 600 .env

# Используйте переменные окружения
export TELEGRAM_BOT_TOKEN='your_token'
```

### 2. Безопасность сервера

```bash
# Регулярно обновляйте систему
sudo apt update && sudo apt upgrade -y

# Настройте файрвол
sudo ufw allow 22/tcp  # SSH
sudo ufw enable

# Создайте пользователя без root прав
sudo adduser botuser
sudo usermod -aG sudo botuser

# Отключите root SSH
sudo nano /etc/ssh/sshd_config
# Установите: PermitRootLogin no
sudo systemctl restart sshd

# Установите fail2ban (защита от брутфорса)
sudo apt install fail2ban
sudo systemctl enable fail2ban
```

### 3. Мониторинг

```bash
# Мониторинг процесса бота
ps aux | grep python

# Проверка использования памяти
free -h

# Проверка дискового пространства
df -h

# Просмотр системных логов
journalctl -xe
```

### 4. Стратегия резервного копирования

```bash
# Ежедневное резервное копирование базы данных
0 2 * * * /usr/bin/cp /home/user/CoinFlow/data/coinflow.db /home/user/backups/coinflow-$(date +\%Y\%m\%d).db

# Хранить последние 7 дней
0 3 * * * find /home/user/backups -name "coinflow-*.db" -mtime +7 -delete
```

---

## 🔄 Обновления

### Ручное обновление

```bash
# Получить последний код
cd ~/CoinFlow
git pull origin main

# Обновить зависимости
poetry install

# Перезапустить бота
# Если используется systemd:
sudo systemctl restart coinflow

# Если используется Docker:
docker-compose up -d --build

# Если используется screen/tmux:
# Завершите старый процесс и запустите новый
```

### Автоматические обновления (Опционально)

Создайте скрипт обновления:
```bash
#!/bin/bash
cd ~/CoinFlow
git pull origin main
poetry install
sudo systemctl restart coinflow
```

---

## 📊 Мониторинг и обслуживание

### Проверки работоспособности

```bash
# Проверить работает ли бот
systemctl status coinflow

# Проверить логи на наличие ошибок
journalctl -u coinflow | grep ERROR

# Проверить использование ресурсов
htop
```

### Ротация логов

Настройка logrotate:
```bash
sudo nano /etc/logrotate.d/coinflow
```

```
/var/log/coinflow/*.log {
    daily
    rotate 7
    compress
    missingok
    notifempty
}
```

---

## 🆘 Решение проблем

### Бот не запускается

```bash
# Проверить статус сервиса
sudo systemctl status coinflow

# Просмотреть подробные логи
sudo journalctl -u coinflow -n 100

# Проверить файл .env
cat .env | grep TELEGRAM_BOT_TOKEN
```

### Ошибки прав доступа

```bash
# Исправить владельца
sudo chown -R YOUR_USERNAME:YOUR_USERNAME ~/CoinFlow

# Исправить права
chmod -R 755 ~/CoinFlow
chmod 600 ~/CoinFlow/.env
```

### База данных заблокирована

```bash
# Остановить бота
sudo systemctl stop coinflow

# Удалить блокировку
rm ~/CoinFlow/data/coinflow.db-lock

# Запустить бота
sudo systemctl start coinflow
```

---

## 📚 Дополнительные ресурсы

- [Руководство по Docker](./DOCKER_GUIDE.md)
- [Решение проблем](./TROUBLESHOOTING.md)
- [Уроки DigitalOcean](https://www.digitalocean.com/community/tutorials)
- [Документация Systemd](https://www.freedesktop.org/software/systemd/man/)
