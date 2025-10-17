# 🔄 Migration Guide: v1.0 → v2.0

**Languages:** [English](#english) | [Русский](#russian)

---

<a name="english"></a>
## 📖 English Version

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

v2.0 introduces full Docker support for easy containerized deployment.

### Prerequisites

**Install Docker:**
- **Windows**: [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/)
- **Mac**: [Docker Desktop for Mac](https://docs.docker.com/desktop/install/mac-install/)
- **Linux**: 
  ```bash
  # Ubuntu/Debian
  curl -fsSL https://get.docker.com -o get-docker.sh
  sudo sh get-docker.sh
  sudo usermod -aG docker $USER
  newgrp docker
  ```

**Install docker-compose** (if not included with Docker Desktop):
```bash
# Linux
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verify installation
docker --version
docker-compose --version
```

### Migration Steps

#### 1. Prepare Environment

```bash
# Clone or navigate to project
cd CoinFlow

# Create .env file
cp .env.example .env
nano .env  # Add your TELEGRAM_BOT_TOKEN
```

**Required .env configuration:**
```env
TELEGRAM_BOT_TOKEN='your_bot_token_here'

# Optional configurations
DATABASE_URL='sqlite:///data/coinflow.db'
CACHE_TTL_SECONDS=60
ALERT_CHECK_INTERVAL=5
LOG_LEVEL=INFO
```

#### 2. Build and Run Container

**Option A: Using helper script (recommended)**
```bash
# Linux/Mac
chmod +x docker-run.sh
./docker-run.sh
# Select: 1. Build and start containers

# Windows
docker-run.bat
# Select: 1. Build and start containers
```

**Option B: Manual docker-compose**
```bash
# Build and start in detached mode
docker-compose up -d --build

# View real-time logs
docker-compose logs -f

# View logs for specific service
docker-compose logs -f coinflow
```

#### 3. Verify Deployment

```bash
# Check container status
docker ps

# Expected output:
# CONTAINER ID   IMAGE              STATUS         PORTS
# abc123def456   coinflow_coinflow  Up 2 minutes   

# Check logs for successful start
docker-compose logs | grep "Bot started"

# Test bot in Telegram
# Send /start to your bot
```

### Container Management

#### Starting/Stopping
```bash
# Start containers
docker-compose start

# Stop containers (keeps data)
docker-compose stop

# Restart containers
docker-compose restart

# Stop and remove containers (data persists in volumes)
docker-compose down
```

#### Viewing Logs
```bash
# All logs
docker-compose logs

# Last 100 lines
docker-compose logs --tail=100

# Follow logs in real-time
docker-compose logs -f

# Logs with timestamps
docker-compose logs -t
```

#### Accessing Container Shell
```bash
# Open bash in running container
docker-compose exec coinflow /bin/bash

# Or use docker directly
docker exec -it coinflow-bot bash

# Inside container, you can:
python --version
ls -la /app
cat logs/coinflow.log
```

### Data Migration to Docker

If migrating from non-Docker v1.0 installation:

#### Option 1: Copy existing database
```bash
# Stop old bot
ctrl+c  # or kill process

# Copy database to Docker data directory
mkdir -p data
cp /path/to/old/coinflow.db data/
cp /path/to/old/alerts.db data/  # if exists

# Start Docker bot
docker-compose up -d
```

#### Option 2: Fresh start (recommended)
```bash
# Start with clean database
# Docker will create new database automatically
docker-compose up -d

# Users will need to:
# 1. Send /start again
# 2. Recreate alerts
# 3. Set language preference
```

### Updating to Latest Version

```bash
# Method 1: Pull latest code and rebuild
git pull origin main
docker-compose down
docker-compose up -d --build

# Method 2: Using helper script
./docker-run.sh  # Select option 4: Pull and rebuild

# Method 3: Just rebuild without pulling
docker-compose up -d --build
```

### Production Deployment

For production, use optimized configuration:

**Create docker-compose.prod.yml:**
```yaml
version: '3.8'

services:
  coinflow:
    build: .
    container_name: coinflow-bot
    restart: unless-stopped
    env_file: .env
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
    healthcheck:
      test: ["CMD", "python", "-c", "import sys; sys.exit(0)"]
      interval: 30s
      timeout: 10s
      retries: 3
```

**Run production:**
```bash
docker-compose -f docker-compose.prod.yml up -d --build
```

### Backup and Restore

#### Backup
```bash
# Backup data directory
tar -czf coinflow-backup-$(date +%Y%m%d).tar.gz data/ logs/

# Or copy database only
cp data/coinflow.db backups/coinflow-$(date +%Y%m%d).db
```

#### Restore
```bash
# Stop containers
docker-compose down

# Restore from backup
tar -xzf coinflow-backup-20241017.tar.gz

# Or restore database only
cp backups/coinflow-20241017.db data/coinflow.db

# Start containers
docker-compose up -d
```

### Troubleshooting Docker

#### Container won't start
```bash
# Check logs
docker-compose logs

# Rebuild from scratch
docker-compose down -v  # WARNING: Removes volumes
docker-compose up -d --build

# Check .env file
cat .env | grep TELEGRAM_BOT_TOKEN
```

#### Port conflicts
```bash
# If you see "port already in use"
# Find process using port
sudo lsof -i :8080
sudo netstat -tulpn | grep :8080

# Kill process or change port in docker-compose.yml
```

#### Permission errors (Linux)
```bash
# Fix ownership
sudo chown -R $USER:$USER data logs
chmod -R 755 data logs
```

#### Out of space
```bash
# Clean up Docker resources
docker system prune -a

# Remove unused volumes
docker volume prune

# Check disk usage
df -h
```

### Migrating from systemd to Docker

If you have bot running as systemd service:

```bash
# 1. Stop systemd service
sudo systemctl stop coinflow
sudo systemctl disable coinflow

# 2. Backup data
cp ~/CoinFlow/data/coinflow.db ~/coinflow-backup.db

# 3. Navigate to project
cd ~/CoinFlow

# 4. Copy database to data directory
mkdir -p data
cp ~/coinflow-backup.db data/coinflow.db

# 5. Start Docker
docker-compose up -d --build

# 6. Verify
docker-compose logs -f

# 7. Optional: Remove systemd service file
sudo rm /etc/systemd/system/coinflow.service
sudo systemctl daemon-reload
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

---
---

<a name="russian"></a>
## 📖 Русская версия

# 🔄 Руководство по миграции: v1.0 → v2.0

## Обзор

CoinFlow v2.0 представляет крупную архитектурную модернизацию с модульной структурой, постоянной базой данных и расширенными функциями. Это руководство поможет вам мигрировать с v1.0 на v2.0.

## 🆕 Что изменилось

### Архитектура
- **Старая**: Монолитный `coinflow.py` (1000+ строк)
- **Новая**: Модульная структура с отдельными пакетами для базы данных, сервисов, обработчиков и утилит

### База данных
- **Старая**: `shelve` только для алертов, `user_states` в памяти (теряется при перезапуске)
- **Новая**: SQLAlchemy с SQLite для постоянного хранения пользователей, алертов, истории и избранного

### Точка входа
- **Старая**: `coinflow.py`
- **Новая**: `main.py` (coinflow.py всё ещё работает, но устарел)

## 📋 Шаги миграции

### Шаг 1: Резервное копирование текущих данных

```bash
# Резервная копия .env файла
cp .env .env.backup

# Резервная копия базы данных алертов (если существует)
cp alerts.db alerts.db.backup
```

### Шаг 2: Установка новых зависимостей

```bash
# Обновление зависимостей
poetry install

# Или добавить новые зависимости вручную
poetry add sqlalchemy aiohttp
```

### Шаг 3: Обновление переменных окружения

Новый `.env` имеет больше опций конфигурации:

```bash
# Скопировать новый пример
cp .env.example .env

# Добавить токен бота
TELEGRAM_BOT_TOKEN='ВАШ_ТОКЕН_ЗДЕСЬ'

# Опционально: Настроить другие параметры
DATABASE_URL='sqlite:///coinflow.db'
CACHE_TTL_SECONDS=60
ALERT_CHECK_INTERVAL=5
LOG_LEVEL=INFO
```

### Шаг 4: Запуск новой версии

```bash
# Запуск с Poetry
poetry run python main.py

# Или активировать venv сначала
poetry shell
python main.py
```

## 🔧 Изменения конфигурации

### Новые переменные окружения

| Переменная | По умолчанию | Описание |
|------------|--------------|----------|
| `DATABASE_URL` | `sqlite:///coinflow.db` | Строка подключения к БД |
| `CACHE_TTL_SECONDS` | `60` | Длительность кеша курсов |
| `ALERT_CHECK_INTERVAL` | `5` | Минуты между проверками алертов |
| `CHART_DPI` | `150` | Качество изображения графиков |
| `LOG_LEVEL` | `INFO` | Уровень логирования |
| `LOG_FILE` | `coinflow.log` | Путь к файлу логов |

## 📊 Миграция данных

### Данные пользователей
- **Пользователям нужно будет снова выполнить `/start`** для инициализации в новой БД
- Языковые предпочтения теряются (пользователи выбирают снова при первом запуске)
- Настройки пользователей можно переконфигурировать через `/settings`

### Алерты
- **Старые алерты из `alerts.db` НЕ мигрируются автоматически**
- Пользователям нужно пересоздать свои алерты
- Рассмотрите скрипт ручной миграции при необходимости:

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

## 🐳 Миграция Docker

v2.0 вводит полную поддержку Docker для простого контейнеризованного развертывания.

### Требования

**Установите Docker:**
- **Windows**: [Docker Desktop для Windows](https://docs.docker.com/desktop/install/windows-install/)
- **Mac**: [Docker Desktop для Mac](https://docs.docker.com/desktop/install/mac-install/)
- **Linux**: 
  ```bash
  # Ubuntu/Debian
  curl -fsSL https://get.docker.com -o get-docker.sh
  sudo sh get-docker.sh
  sudo usermod -aG docker $USER
  newgrp docker
  ```

**Установите docker-compose** (если не включен в Docker Desktop):
```bash
# Linux
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Проверка установки
docker --version
docker-compose --version
```

### Шаги миграции

#### 1. Подготовка окружения

```bash
# Клонировать или перейти в проект
cd CoinFlow

# Создать .env файл
cp .env.example .env
nano .env  # Добавьте ваш TELEGRAM_BOT_TOKEN
```

**Необходимая конфигурация .env:**
```env
TELEGRAM_BOT_TOKEN='ваш_токен_бота_здесь'

# Опциональные настройки
DATABASE_URL='sqlite:///data/coinflow.db'
CACHE_TTL_SECONDS=60
ALERT_CHECK_INTERVAL=5
LOG_LEVEL=INFO
```

#### 2. Сборка и запуск контейнера

**Вариант A: Использование вспомогательного скрипта (рекомендуется)**
```bash
# Linux/Mac
chmod +x docker-run.sh
./docker-run.sh
# Выберите: 1. Build and start containers

# Windows
docker-run.bat
# Выберите: 1. Build and start containers
```

**Вариант B: Ручной docker-compose**
```bash
# Собрать и запустить в фоновом режиме
docker-compose up -d --build

# Просмотр логов в реальном времени
docker-compose logs -f

# Просмотр логов конкретного сервиса
docker-compose logs -f coinflow
```

#### 3. Проверка развертывания

```bash
# Проверить статус контейнера
docker ps

# Ожидаемый вывод:
# CONTAINER ID   IMAGE              STATUS         PORTS
# abc123def456   coinflow_coinflow  Up 2 minutes   

# Проверить логи на успешный запуск
docker-compose logs | grep "Bot started"

# Протестировать бота в Telegram
# Отправьте /start вашему боту
```

### Управление контейнером

```bash
# Запустить контейнеры
docker-compose start

# Остановить контейнеры (данные сохраняются)
docker-compose stop

# Перезапустить контейнеры
docker-compose restart

# Остановить и удалить контейнеры (данные сохраняются в томах)
docker-compose down

# Просмотр логов
docker-compose logs -f

# Доступ к оболочке контейнера
docker-compose exec coinflow /bin/bash
```

### Обновление до последней версии

```bash
# Получить последний код и пересобрать
git pull origin main
docker-compose down
docker-compose up -d --build
```

### Резервное копирование и восстановление

```bash
# Резервное копирование
tar -czf coinflow-backup-$(date +%Y%m%d).tar.gz data/ logs/

# Восстановление
docker-compose down
tar -xzf coinflow-backup-20241017.tar.gz
docker-compose up -d
```

### Устранение неполадок Docker

```bash
# Контейнер не запускается
docker-compose logs
docker-compose down -v  # ВНИМАНИЕ: Удаляет тома
docker-compose up -d --build

# Ошибки прав доступа (Linux)
sudo chown -R $USER:$USER data logs
chmod -R 755 data logs

# Очистка Docker ресурсов
docker system prune -a
docker volume prune
```

### Миграция с systemd на Docker

```bash
# 1. Остановить systemd сервис
sudo systemctl stop coinflow
sudo systemctl disable coinflow

# 2. Резервная копия данных
cp ~/CoinFlow/data/coinflow.db ~/coinflow-backup.db

# 3. Копировать БД в data директорию
cd ~/CoinFlow
mkdir -p data
cp ~/coinflow-backup.db data/coinflow.db

# 4. Запустить Docker
docker-compose up -d --build

# 5. Проверить
docker-compose logs -f

# 6. Удалить systemd сервис (опционально)
sudo rm /etc/systemd/system/coinflow.service
sudo systemctl daemon-reload
```

Подробнее см. [Руководство по Docker](./DOCKER_GUIDE.md)

## 🆕 Новые функции для информирования пользователей

### 1. Команда History
```
Пользователи теперь могут набрать /history чтобы увидеть последние 10 конвертаций
```

### 2. Система избранного
```
Пользователи могут добавлять валюты в избранное для быстрого доступа
Используйте кнопку ⭐ при выборе валюты
```

### 3. Inline режим
```
Пользователи могут конвертировать без открытия бота:
@your_bot_username 100 USD to EUR
```

### 4. Статистика
```
Пользователи могут набрать /stats чтобы увидеть свою статистику использования
```

### 5. Настраиваемые периоды графиков
```
При генерации графиков пользователи могут выбрать:
7 дней / 30 дней / 90 дней / 1 год
```

## ⚠️ Критические изменения

### 1. Старая точка входа устарела
- `coinflow.py` всё ещё существует, но перенаправляет на `main.py`
- Обновите systemd сервисы или cron задачи для использования `main.py`

### 2. Сброс состояний пользователей
- Все состояния пользователей в памяти теряются
- Пользователям нужно перезапустить разговоры

### 3. Изменения импорта
```python
# Старый (v1.0)
from coinflow import TelegramBot

# Новый (v2.0)
from coinflow.bot import CoinFlowBot
```

## 🔍 Устранение неполадок

### Ошибки "Module not found"
```bash
# Переустановить зависимости
poetry install
```

### Ошибки базы данных
```bash
# Удалить старую БД и начать заново
rm coinflow.db
python main.py
```

### Ошибки прав доступа
```bash
# Убедиться, что директория data существует и доступна для записи
mkdir -p data logs
chmod 755 data logs
```

### Конфликты со старым alerts.db
```bash
# Переименовать старую базу данных
mv alerts.db alerts.db.old
```

## 📝 Контрольный список

- [ ] Резервное копирование `.env` и `alerts.db`
- [ ] Установить новые зависимости (`poetry install`)
- [ ] Обновить `.env` новыми переменными
- [ ] Протестировать бота с `python main.py`
- [ ] Объявить пользователям о новых функциях
- [ ] Информировать пользователей о необходимости `/start` снова
- [ ] Информировать пользователей о пересоздании алертов
- [ ] Обновить скрипты развертывания (если есть)
- [ ] Мониторить логи на наличие ошибок

## 🚀 План отката

Если что-то пойдёт не так:

```bash
# 1. Остановить новую версию
# Нажать Ctrl+C или:
docker-compose down

# 2. Восстановить старые файлы
git checkout v1.0  # или восстановить из резервной копии

# 3. Восстановить .env
cp .env.backup .env

# 4. Запустить старую версию
python coinflow.py
```

## 📞 Поддержка

Если возникли проблемы во время миграции:
1. Проверьте логи: `tail -f coinflow.log`
2. Просмотрите GitHub issues
3. Откройте новый issue с деталями ошибки

## 🎉 После миграции

После успешной миграции:

1. **Протестируйте все функции**:
   - Конвертация валют
   - Генерация графиков
   - Прогнозы
   - Алерты
   - Калькулятор
   - История
   - Избранное

2. **Мониторинг производительности**:
   - Проверьте показатели попаданий в кеш
   - Мониторьте размер базы данных
   - Проверяйте файлы логов

3. **Объявите новую версию** пользователям со списком функций

4. **Очистите старые файлы** (опционально):
   ```bash
   # После подтверждения, что всё работает
   rm alerts.db.backup
   rm .env.backup
   ```

---

**Готовы к миграции? Следуйте шагам выше и наслаждайтесь CoinFlow v2.0! 🚀**
