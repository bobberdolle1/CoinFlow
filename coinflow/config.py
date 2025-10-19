"""Configuration management for CoinFlow bot."""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration."""
    
    # Telegram Bot
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///coinflow.db")
    
    # Cache settings
    CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", "60"))
    
    # Alert check interval (minutes)
    ALERT_CHECK_INTERVAL = int(os.getenv('ALERT_CHECK_INTERVAL', '5'))
    
    # Web App URL
    WEBAPP_URL = os.getenv('WEBAPP_URL', 'http://localhost:8000')
    
    # Ollama AI settings
    OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://localhost:11434')
    OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'llama3.2:3b')
    
    # Chart settings
    CHART_DPI = int(os.getenv("CHART_DPI", "150"))
    DEFAULT_CHART_PERIOD = int(os.getenv("DEFAULT_CHART_PERIOD", "30"))
    
    # Prediction settings
    DEFAULT_PREDICTION_DAYS = int(os.getenv("DEFAULT_PREDICTION_DAYS", "90"))
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "coinflow.log")
    LOG_MAX_BYTES = int(os.getenv("LOG_MAX_BYTES", "10485760"))  # 10MB
    LOG_BACKUP_COUNT = int(os.getenv("LOG_BACKUP_COUNT", "5"))


config = Config()
