# 📦 Полное руководство по установке CoinFlow Bot

Подробная пошаговая инструкция по установке CoinFlow Bot с нуля для всех операционных систем.

[English](#english) | [Русский](#русский)

---

<a name="english"></a>

## 🇬🇧 English

### 📋 Table of Contents

- [Prerequisites Installation](#prerequisites-installation)
- [Bot Installation](#bot-installation)
- [Configuration](#configuration)
- [Running the Bot](#running-the-bot)
- [Troubleshooting](#troubleshooting)

---

## 🔧 Prerequisites Installation

### 1. Installing Python 3.11+

#### Windows

**Option 1: Official Installer (Recommended)**
1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Download Python 3.11+ installer
3. Run installer, **check "Add Python to PATH"**
4. Verify: `python --version`

**Option 2: Microsoft Store**
1. Open Microsoft Store
2. Search "Python 3.11"
3. Install

**Option 3: Winget**
```powershell
winget install Python.Python.3.11
```

#### macOS

**Using Homebrew:**
```bash
brew install python@3.11
```

**Or download from** [python.org/downloads/macos](https://www.python.org/downloads/macos/)

#### Linux

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip
```

**Fedora/RHEL:**
```bash
sudo dnf install python3.11 python3-pip
```

**Verify:**
```bash
python3.11 --version
```

---

### 2. Installing Poetry

#### Windows
```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

Add to PATH: `%APPDATA%\Python\Scripts`

Or via pip:
```powershell
pip install poetry
```

#### macOS/Linux
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Add to PATH in `~/.bashrc` or `~/.zshrc`:
```bash
export PATH="$HOME/.local/bin:$PATH"
```

Or via pip:
```bash
pip3 install poetry
```

**Verify:**
```bash
poetry --version
```

---

### 3. Installing Docker (Optional)

#### Windows
1. Download [Docker Desktop](https://www.docker.com/products/docker-desktop)
2. Run installer, restart if needed
3. Start Docker Desktop
4. Verify: `docker --version`

#### macOS
1. Download [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop)
2. Install and launch
3. Verify: `docker --version`

#### Linux (Ubuntu/Debian)
```bash
# Install Docker
sudo apt update
sudo apt install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Add user to docker group
sudo usermod -aG docker $USER

# Start Docker
sudo systemctl start docker
sudo systemctl enable docker
```

---

### 4. Getting Telegram Bot Token

1. Open Telegram, find [@BotFather](https://t.me/BotFather)
2. Send `/newbot` command
3. Follow instructions:
   - Enter bot name: "My CoinFlow Bot"
   - Enter username: "my_coinflow_bot" (must end with "bot")
4. **Save your token**: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`
5. Optional: Set description `/setdescription`, photo `/setuserpic`, enable inline `/setinline`

⚠️ **Keep token secret!**

---

## 📦 Bot Installation

### Method 1: Standard Installation (Poetry)

#### Step 1: Clone Repository

```bash
git clone https://github.com/bobberdolle1/CoinFlow.git
cd CoinFlow
```

Or download ZIP from GitHub and extract.

#### Step 2: Install Dependencies

```bash
poetry install
```

Takes 2-5 minutes.

#### Step 3: Configure Environment

**Windows:**
```powershell
Copy-Item .env.example .env
notepad .env
```

**macOS/Linux:**
```bash
cp .env.example .env
nano .env
```

Edit `.env` file:

```env
TELEGRAM_BOT_TOKEN='YOUR_TOKEN_HERE'
DATABASE_URL='sqlite:///coinflow.db'
CACHE_TTL_SECONDS=60
ALERT_CHECK_INTERVAL=5
CHART_DPI=150
LOG_LEVEL=INFO
```

#### Step 4: Run the Bot

```bash
poetry run python main.py
```

Or activate virtual environment:
```bash
poetry shell
python main.py
```

✅ **Success!** Bot is running!

---

### Method 2: Docker Installation

#### Step 1: Clone Repository

```bash
git clone https://github.com/bobberdolle1/CoinFlow.git
cd CoinFlow
```

#### Step 2: Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and add your token.

#### Step 3: Run with Docker

**Using docker-compose:**
```bash
docker-compose up -d
```

**Or use helper script:**

Windows:
```cmd
docker-run.bat
```

Linux/macOS:
```bash
chmod +x docker-run.sh
./docker-run.sh
```

#### Step 4: View Logs

```bash
docker-compose logs -f
```

✅ **Success!** Bot is running in Docker!

---

## ⚙️ Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `TELEGRAM_BOT_TOKEN` | ✅ | - | Bot token from @BotFather |
| `DATABASE_URL` | ❌ | `sqlite:///coinflow.db` | Database connection |
| `CACHE_TTL_SECONDS` | ❌ | `60` | Cache duration |
| `ALERT_CHECK_INTERVAL` | ❌ | `5` | Alert check (minutes) |
| `CHART_DPI` | ❌ | `150` | Chart quality |
| `LOG_LEVEL` | ❌ | `INFO` | Log level |

---

## 🚀 Running the Bot

### Standard (Poetry)

**Foreground:**
```bash
poetry run python main.py
```

**Background (Linux/macOS):**
```bash
nohup poetry run python main.py &
```

### Docker

**Start:**
```bash
docker-compose up -d
```

**Stop:**
```bash
docker-compose down
```

**Restart:**
```bash
docker-compose restart
```

**Logs:**
```bash
docker-compose logs -f
```

---

## ✅ Verification

### Test Your Bot

1. Open Telegram, find your bot
2. Send `/start`
3. Select language
4. Main menu appears with buttons
5. Try "⚡ Quick Convert":
   - Select USD → EUR
   - Choose amount: 100
   - See result

### Check Logs

**Standard:**
```bash
tail -f coinflow.log
```

**Docker:**
```bash
docker-compose logs -f
```

---

## 🔍 Troubleshooting

### Module Not Found
```bash
poetry install --no-cache
```

### Invalid Token
- Check `.env` file
- No extra spaces/quotes
- Format: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`

### Permission Denied (Linux)
```bash
chmod +x main.py
```

### Docker Build Fails
```bash
docker builder prune -a
docker-compose build --no-cache
```

### Poetry Not Found

**Windows:** Add to PATH: `%APPDATA%\Python\Scripts`

**Linux/macOS:**
```bash
export PATH="$HOME/.local/bin:$PATH"
```

### Database Locked
```bash
# Stop bot
pkill -f main.py

# Restart
poetry run python main.py
```

---

<a name="русский"></a>

## 🇷🇺 Русский

### 📋 Содержание

- [Установка зависимостей](#установка-зависимостей-1)
- [Установка бота](#установка-бота-1)
- [Настройка](#настройка-1)
- [Запуск бота](#запуск-бота-1)
- [Решение проблем](#решение-проблем-1)

---

## 🔧 Установка зависимостей

### 1. Установка Python 3.11+

#### Windows

**Вариант 1: Официальный установщик (рекомендуется)**
1. Перейдите на [python.org/downloads](https://www.python.org/downloads/)
2. Скачайте установщик Python 3.11+
3. Запустите, **отметьте "Add Python to PATH"**
4. Проверка: `python --version`

**Вариант 2: Microsoft Store**
1. Откройте Microsoft Store
2. Найдите "Python 3.11"
3. Установите

**Вариант 3: Winget**
```powershell
winget install Python.Python.3.11
```

#### macOS

**Через Homebrew:**
```bash
brew install python@3.11
```

**Или скачайте с** [python.org/downloads/macos](https://www.python.org/downloads/macos/)

#### Linux

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip
```

**Fedora/RHEL:**
```bash
sudo dnf install python3.11 python3-pip
```

**Проверка:**
```bash
python3.11 --version
```

---

### 2. Установка Poetry

#### Windows
```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

Добавьте в PATH: `%APPDATA%\Python\Scripts`

Или через pip:
```powershell
pip install poetry
```

#### macOS/Linux
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Добавьте в PATH в `~/.bashrc` или `~/.zshrc`:
```bash
export PATH="$HOME/.local/bin:$PATH"
```

Или через pip:
```bash
pip3 install poetry
```

**Проверка:**
```bash
poetry --version
```

---

### 3. Установка Docker (опционально)

#### Windows
1. Скачайте [Docker Desktop](https://www.docker.com/products/docker-desktop)
2. Запустите установщик, перезагрузитесь при необходимости
3. Запустите Docker Desktop
4. Проверка: `docker --version`

#### macOS
1. Скачайте [Docker Desktop для Mac](https://www.docker.com/products/docker-desktop)
2. Установите и запустите
3. Проверка: `docker --version`

#### Linux (Ubuntu/Debian)
```bash
# Установка Docker
sudo apt update
sudo apt install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Добавить пользователя в группу docker
sudo usermod -aG docker $USER

# Запустить Docker
sudo systemctl start docker
sudo systemctl enable docker
```

---

### 4. Получение токена Telegram-бота

1. Откройте Telegram, найдите [@BotFather](https://t.me/BotFather)
2. Отправьте команду `/newbot`
3. Следуйте инструкциям:
   - Введите имя бота: "My CoinFlow Bot"
   - Введите username: "my_coinflow_bot" (должен заканчиваться на "bot")
4. **Сохраните токен**: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`
5. Опционально: установите описание `/setdescription`, фото `/setuserpic`, включите inline-режим `/setinline`

⚠️ **Храните токен в секрете!**

---

## 📦 Установка бота

### Метод 1: Стандартная установка (Poetry)

#### Шаг 1: Клонирование репозитория

```bash
git clone https://github.com/bobberdolle1/CoinFlow.git
cd CoinFlow
```

Или скачайте ZIP с GitHub и распакуйте.

#### Шаг 2: Установка зависимостей

```bash
poetry install
```

Займет 2-5 минут.

#### Шаг 3: Настройка окружения

**Windows:**
```powershell
Copy-Item .env.example .env
notepad .env
```

**macOS/Linux:**
```bash
cp .env.example .env
nano .env
```

Отредактируйте файл `.env`:

```env
TELEGRAM_BOT_TOKEN='ВАШ_ТОКЕН_ЗДЕСЬ'
DATABASE_URL='sqlite:///coinflow.db'
CACHE_TTL_SECONDS=60
ALERT_CHECK_INTERVAL=5
CHART_DPI=150
LOG_LEVEL=INFO
```

#### Шаг 4: Запуск бота

```bash
poetry run python main.py
```

Или активируйте виртуальное окружение:
```bash
poetry shell
python main.py
```

✅ **Успех!** Бот запущен!

---

### Метод 2: Установка через Docker

#### Шаг 1: Клонирование репозитория

```bash
git clone https://github.com/bobberdolle1/CoinFlow.git
cd CoinFlow
```

#### Шаг 2: Настройка окружения

```bash
cp .env.example .env
```

Отредактируйте `.env` и добавьте токен.

#### Шаг 3: Запуск с Docker

**Используя docker-compose:**
```bash
docker-compose up -d
```

**Или используйте скрипт-помощник:**

Windows:
```cmd
docker-run.bat
```

Linux/macOS:
```bash
chmod +x docker-run.sh
./docker-run.sh
```

#### Шаг 4: Просмотр логов

```bash
docker-compose logs -f
```

✅ **Успех!** Бот работает в Docker!

---

## ⚙️ Настройка

### Переменные окружения

| Переменная | Обязательна | По умолчанию | Описание |
|----------|----------|---------|-------------|
| `TELEGRAM_BOT_TOKEN` | ✅ | - | Токен от @BotFather |
| `DATABASE_URL` | ❌ | `sqlite:///coinflow.db` | Подключение к БД |
| `CACHE_TTL_SECONDS` | ❌ | `60` | Длительность кэша |
| `ALERT_CHECK_INTERVAL` | ❌ | `5` | Проверка алертов (мин) |
| `CHART_DPI` | ❌ | `150` | Качество графиков |
| `LOG_LEVEL` | ❌ | `INFO` | Уровень логирования |

---

## 🚀 Запуск бота

### Стандартный (Poetry)

**На переднем плане:**
```bash
poetry run python main.py
```

**В фоне (Linux/macOS):**
```bash
nohup poetry run python main.py &
```

### Docker

**Запуск:**
```bash
docker-compose up -d
```

**Остановка:**
```bash
docker-compose down
```

**Перезапуск:**
```bash
docker-compose restart
```

**Логи:**
```bash
docker-compose logs -f
```

---

## ✅ Проверка работы

### Тестирование бота

1. Откройте Telegram, найдите своего бота
2. Отправьте `/start`
3. Выберите язык
4. Появится главное меню с кнопками
5. Попробуйте "⚡ Быстрая конвертация":
   - Выберите USD → EUR
   - Выберите сумму: 100
   - Посмотрите результат

### Проверка логов

**Стандартный:**
```bash
tail -f coinflow.log
```

**Docker:**
```bash
docker-compose logs -f
```

---

## 🔍 Решение проблем

### Модуль не найден
```bash
poetry install --no-cache
```

### Неверный токен
- Проверьте файл `.env`
- Убедитесь в отсутствии лишних пробелов/кавычек
- Формат: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`

### Ошибка доступа (Linux)
```bash
chmod +x main.py
```

### Сборка Docker не удалась
```bash
docker builder prune -a
docker-compose build --no-cache
```

### Poetry не найден

**Windows:** Добавьте в PATH: `%APPDATA%\Python\Scripts`

**Linux/macOS:**
```bash
export PATH="$HOME/.local/bin:$PATH"
```

### База данных заблокирована
```bash
# Остановите бота
pkill -f main.py

# Перезапустите
poetry run python main.py
```

---

## 📚 Дополнительная информация

### Документация

- 📖 [Главная документация](../README.md)
- 🚀 [Краткое руководство](QUICK_START.md)
- 🐳 [Руководство по Docker](DOCKER_GUIDE.md)
- 🚀 [Руководство по развертыванию](DEPLOYMENT.md)
- 🔧 [Решение проблем](TROUBLESHOOTING.md)

### Поддержка

- 🐛 Сообщить об ошибке: [GitHub Issues](https://github.com/bobberdolle1/CoinFlow/issues)
- 💬 Вопросы: [GitHub Discussions](https://github.com/bobberdolle1/CoinFlow/discussions)

---

## 📄 Лицензия

MIT License - свободно используйте и изменяйте.

**Успешной установки! 🪙✨**
