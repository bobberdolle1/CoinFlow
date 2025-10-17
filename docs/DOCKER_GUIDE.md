# 🐳 Docker Deployment Guide

Complete guide for deploying CoinFlow Bot using Docker.

[English](#english) | [Русский](#русский)

---

<a name="english"></a>

## 🇬🇧 English

### 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Using Helper Scripts](#using-helper-scripts)
- [Manual Docker Commands](#manual-docker-commands)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)

---

## 🔧 Prerequisites

### 1. Install Docker

**Windows:**
- Download [Docker Desktop](https://www.docker.com/products/docker-desktop)
- Run installer and follow instructions
- Restart your computer if required

**Mac:**
- Download [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop)
- Install and start Docker Desktop

**Linux:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install docker.io docker-compose

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Add your user to docker group (to run without sudo)
sudo usermod -aG docker $USER
# Log out and back in for this to take effect
```

### 2. Get Bot Token

1. Open Telegram and find [@BotFather](https://t.me/BotFather)
2. Send `/newbot` command
3. Follow instructions to create your bot
4. Copy the token (e.g., `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

---

## ⚡ Quick Start

### Method 1: Using Helper Scripts (Recommended)

**Windows:**
```cmd
# Double-click docker-run.bat or run in CMD:
docker-run.bat
```

**Linux/Mac:**
```bash
# Make script executable
chmod +x docker-run.sh

# Run script
./docker-run.sh
```

The script will:
1. Check if Docker is installed
2. Create `.env` file from `.env.example` if needed
3. Show menu with options to build, start, stop, view logs, etc.

### Method 2: Using docker-compose

```bash
# 1. Create .env file
cp .env.example .env

# 2. Edit .env and add your token
nano .env  # or use any text editor

# 3. Build and start
docker-compose up -d

# 4. View logs
docker-compose logs -f

# 5. Stop
docker-compose down
```

---

## 🎮 Using Helper Scripts

### Windows (docker-run.bat)

**Option 1: Build and Start**
- Builds Docker image
- Creates and starts container
- Bot runs in background

**Option 2: Stop**
- Stops the running bot
- Removes containers

**Option 3: View Logs**
- Shows real-time logs
- Press Ctrl+C to exit

**Option 4: Restart**
- Restarts the bot without rebuilding

**Option 5: Clean**
- Removes containers, images, and volumes
- Use when you want to start fresh

### Linux/Mac (docker-run.sh)

Same options as Windows, but with bash script.

```bash
# First time setup
chmod +x docker-run.sh
./docker-run.sh

# Select option 1 to build and start
# Select option 3 to view logs
```

---

## 🔨 Manual Docker Commands

### Build Image

```bash
# Build with tag
docker build -t coinflow:latest .

# Build with no cache (fresh build)
docker build --no-cache -t coinflow:latest .
```

### Run Container

```bash
# Run in detached mode
docker run -d \
  --name coinflow-bot \
  --env-file .env \
  --restart unless-stopped \
  coinflow:latest

# Run with interactive logs
docker run -it --env-file .env coinflow:latest
```

### Manage Container

```bash
# View logs
docker logs coinflow-bot
docker logs -f coinflow-bot  # follow logs

# Stop container
docker stop coinflow-bot

# Start stopped container
docker start coinflow-bot

# Restart container
docker restart coinflow-bot

# Remove container
docker rm coinflow-bot

# Remove image
docker rmi coinflow:latest
```

### Docker Compose Commands

```bash
# Build and start
docker-compose up -d --build

# Start (without building)
docker-compose up -d

# Stop
docker-compose down

# View logs
docker-compose logs
docker-compose logs -f  # follow logs
docker-compose logs -f --tail=100  # last 100 lines

# Restart
docker-compose restart

# Rebuild specific service
docker-compose build coinflow

# Remove everything (containers, volumes, images)
docker-compose down --rmi all --volumes
```

---

## ⚙️ Configuration

### Environment Variables (.env)

Required:
```env
TELEGRAM_BOT_TOKEN='your_token_here'
```

Optional:
```env
# Database
DATABASE_URL='sqlite:///coinflow.db'

# Cache
CACHE_TTL_SECONDS=60

# Alerts
ALERT_CHECK_INTERVAL=5

# Charts
CHART_DPI=150
DEFAULT_CHART_PERIOD=30

# Logging
LOG_LEVEL=INFO
LOG_FILE=coinflow.log
```

### Docker Compose Configuration

Edit `docker-compose.yml` to customize:

```yaml
version: '3.8'

services:
  coinflow:
    build: .
    container_name: coinflow-bot
    env_file: .env
    restart: unless-stopped
    volumes:
      - ./data:/app/data  # Persistent data
      - ./logs:/app/logs  # Logs
```

**Restart Policies:**
- `no`: Never restart (default)
- `always`: Always restart
- `unless-stopped`: Restart unless manually stopped
- `on-failure`: Restart only on failure

---

## 🔍 Troubleshooting

### Container Won't Start

```bash
# Check container status
docker ps -a

# View container logs
docker logs coinflow-bot

# Check if port is already in use
docker port coinflow-bot
```

### Permission Errors (Linux)

```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Log out and back in, or run:
newgrp docker
```

### Image Build Fails

```bash
# Clean build cache
docker builder prune

# Build with no cache
docker-compose build --no-cache
```

### Bot Database Issues

```bash
# Stop container
docker-compose down

# Remove volumes (this deletes data!)
docker-compose down --volumes

# Start fresh
docker-compose up -d
```

### View Container Details

```bash
# Inspect container
docker inspect coinflow-bot

# Check resource usage
docker stats coinflow-bot

# Access container shell
docker exec -it coinflow-bot /bin/bash
```

### Update Bot

```bash
# Pull latest code
git pull origin main

# Rebuild and restart
docker-compose up -d --build

# Or with helper script
./docker-run.sh  # select option 1
```

---

## 📊 Monitoring

### View Logs in Real-Time

```bash
# All logs
docker-compose logs -f

# Last 100 lines
docker-compose logs -f --tail=100

# Grep for errors
docker-compose logs | grep ERROR
```

### Check Container Health

```bash
# Container status
docker ps

# Resource usage
docker stats coinflow-bot

# Container processes
docker top coinflow-bot
```

---

## 🚀 Production Tips

1. **Use restart policy**: Set to `unless-stopped` in docker-compose.yml
2. **Mount volumes**: Keep data persistent across restarts
3. **Monitor logs**: Set up log rotation or use logging service
4. **Backup data**: Regularly backup `./data` directory
5. **Update regularly**: Pull updates and rebuild image
6. **Security**: Never commit `.env` file to git

---

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [CoinFlow GitHub](https://github.com/bobberdolle1/CoinFlow)
- [Troubleshooting Guide](./TROUBLESHOOTING.md)
- [Deployment Guide](./DEPLOYMENT.md)
