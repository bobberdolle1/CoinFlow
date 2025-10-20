# 🐳 CoinFlow Bot - Docker Deployment Guide

Complete guide for deploying CoinFlow Bot v3.0 with Qwen3-8B using Docker.

---

## 📋 Prerequisites

- **Docker** 20.10+
- **Docker Compose** 2.0+
- **16 GB RAM** minimum (32 GB recommended)
- **20 GB** free disk space

### Install Docker

**Windows:**
- Download Docker Desktop: https://www.docker.com/products/docker-desktop

**Linux:**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
sudo usermod -aG docker $USER
```

**macOS:**
- Download Docker Desktop: https://www.docker.com/products/docker-desktop

---

## 🚀 Quick Start (Automated)

### Linux/macOS:
```bash
# Make script executable
chmod +x docker-init.sh

# Run setup
./docker-init.sh
```

### Windows (PowerShell):
```powershell
# Use docker-run.bat or manual steps below
.\docker-run.bat
```

---

## 📝 Manual Setup

### 1. Configure Environment

```bash
# Copy example config
cp .env.example .env

# Edit .env and set your bot token
nano .env  # or use any text editor
```

**Required settings in `.env`:**
```bash
TELEGRAM_BOT_TOKEN=your_token_here
ADMIN_IDS=your_telegram_id
```

### 2. Create Directories

```bash
mkdir -p data logs
```

### 3. Build and Start

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d
```

### 4. Download Qwen3-8B Model

```bash
# Wait for Ollama to be ready (20-30 seconds)
sleep 30

# Pull the model (5-10 minutes)
docker exec coinflow-ollama ollama pull qwen3:8b
```

### 5. Verify

```bash
# Check logs
docker-compose logs -f coinflow-bot

# Should see:
# ✅ Model qwen3:8b is available
# ✅ AI service (Qwen3-8B) is ready!
# 🤖 CoinFlow Bot v2.7 is running...
```

---

## 📊 Service Management

### View Logs
```bash
# All services
docker-compose logs -f

# Only bot
docker-compose logs -f coinflow-bot

# Only Ollama
docker-compose logs -f ollama
```

### Stop Services
```bash
docker-compose stop
```

### Restart Services
```bash
docker-compose restart
```

### Stop and Remove
```bash
docker-compose down

# Remove volumes too (deletes data)
docker-compose down -v
```

### Update
```bash
# Pull latest code
git pull

# Rebuild
docker-compose build

# Restart
docker-compose up -d
```

---

## 🔧 Architecture

```
┌─────────────────────────────────────┐
│     Docker Compose Stack            │
├─────────────────────────────────────┤
│                                     │
│  ┌──────────────────────────────┐  │
│  │  Ollama Container            │  │
│  │  - Qwen3-8B Model            │  │
│  │  - Port: 11434               │  │
│  │  - GPU Support (optional)    │  │
│  └──────────────────────────────┘  │
│               ▲                     │
│               │ HTTP API            │
│               │                     │
│  ┌──────────────────────────────┐  │
│  │  CoinFlow Bot Container      │  │
│  │  - Python 3.11               │  │
│  │  - Telegram Bot              │  │
│  │  - AI Service                │  │
│  │  - All Features              │  │
│  └──────────────────────────────┘  │
│                                     │
└─────────────────────────────────────┘
         │
         ▼
   Host Volumes:
   - ./data (database)
   - ./logs (logs)
```

---

## 🐛 Troubleshooting

### Ollama not starting

**Check logs:**
```bash
docker-compose logs ollama
```

**Restart Ollama:**
```bash
docker-compose restart ollama
```

### Model not downloading

**Check Ollama is running:**
```bash
docker exec coinflow-ollama ollama list
```

**Manually pull:**
```bash
docker exec coinflow-ollama ollama pull qwen3:8b
```

### Bot can't connect to Ollama

**Check network:**
```bash
docker exec coinflow-bot ping ollama
```

**Check Ollama URL in logs:**
```bash
docker-compose logs coinflow-bot | grep OLLAMA
```

### Out of memory

**Check Docker resources:**
```bash
docker stats
```

**Increase Docker memory:**
- Docker Desktop → Settings → Resources → Memory
- Set to at least 16 GB

**Or use smaller model:**
```bash
# In .env
OLLAMA_MODEL=qwen3:3b
```

### Permission errors

```bash
# Fix data directory permissions
sudo chown -R $USER:$USER data logs

# Or run with sudo
sudo docker-compose up -d
```

---

## 🎮 GPU Support (Optional)

For faster AI responses with NVIDIA GPU:

### 1. Install NVIDIA Container Toolkit

**Linux:**
```bash
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker
```

### 2. Update docker-compose.yml

Add to `ollama` service:
```yaml
ollama:
  deploy:
    resources:
      reservations:
        devices:
          - driver: nvidia
            count: 1
            capabilities: [gpu]
```

### 3. Restart

```bash
docker-compose down
docker-compose up -d
```

### 4. Verify GPU

```bash
docker exec coinflow-ollama nvidia-smi
```

---

## 📈 Performance

| Configuration | Response Time |
|--------------|---------------|
| CPU only (4 cores, 16GB RAM) | 15-30 sec |
| CPU (8 cores, 32GB RAM) | 5-15 sec |
| GPU (NVIDIA 8GB VRAM) | 2-5 sec |

---

## 🔒 Security

**Firewall:**
```bash
# Only expose Telegram bot port if needed
# Ollama port (11434) is NOT exposed to internet by default
```

**Environment variables:**
```bash
# Never commit .env to Git
# .env is already in .gitignore
```

**Updates:**
```bash
# Regularly update base images
docker-compose pull
docker-compose up -d
```

---

## 📦 Backup

### Backup Data
```bash
# Backup database and logs
tar -czf coinflow-backup-$(date +%Y%m%d).tar.gz data logs .env

# Backup Ollama models (optional, can be re-downloaded)
docker run --rm -v coinflow_ollama-data:/data -v $(pwd):/backup alpine tar -czf /backup/ollama-models.tar.gz -C /data .
```

### Restore
```bash
# Restore data
tar -xzf coinflow-backup-YYYYMMDD.tar.gz

# Restart services
docker-compose restart
```

---

## 🆘 Support

**Logs location:**
- Bot logs: `./logs/coinflow.log`
- Docker logs: `docker-compose logs`

**Common commands:**
```bash
# Check container status
docker-compose ps

# Check resource usage
docker stats

# Enter container shell
docker exec -it coinflow-bot bash

# Check Ollama models
docker exec coinflow-ollama ollama list

# Test Ollama API
docker exec coinflow-bot curl http://ollama:11434/api/tags
```

---

## ✅ Production Checklist

- [ ] Docker and Docker Compose installed
- [ ] `.env` configured with bot token
- [ ] Firewall configured (block 11434 from internet)
- [ ] 16+ GB RAM available
- [ ] 20+ GB disk space
- [ ] Qwen3-8B model downloaded
- [ ] Bot starts without errors
- [ ] Telegram commands work
- [ ] AI responses work
- [ ] Voice messages work (if enabled)
- [ ] Backups configured

---

**Version:** 3.0.0  
**Last updated:** 2025-10-20  
**Author:** bobberdolle1
