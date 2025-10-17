#!/bin/bash

# CoinFlow Bot - Docker Runner for Linux/Mac
# This script helps you run CoinFlow bot using Docker

set -e

echo "========================================"
echo "  CoinFlow Bot v2.0 - Docker Runner"
echo "========================================"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "[ERROR] Docker is not installed"
    echo "Please install Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "[ERROR] docker-compose is not installed"
    echo "Please install docker-compose: https://docs.docker.com/compose/install/"
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "[WARNING] .env file not found!"
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo ""
    echo "[ACTION REQUIRED] Please edit .env and add your TELEGRAM_BOT_TOKEN"
    echo "Then run this script again."
    exit 1
fi

# Function to display menu
show_menu() {
    echo ""
    echo "What would you like to do?"
    echo ""
    echo "1. Build and start the bot"
    echo "2. Stop the bot"
    echo "3. View logs"
    echo "4. Restart the bot"
    echo "5. Remove containers and images"
    echo "6. Exit"
    echo ""
    read -p "Enter your choice (1-6): " choice
    echo ""
}

# Function to build and start
build_start() {
    echo "Building and starting CoinFlow bot..."
    docker-compose up -d --build
    if [ $? -eq 0 ]; then
        echo ""
        echo "[SUCCESS] Bot is now running!"
        echo "Use 'docker-compose logs -f' to view logs"
    else
        echo "[ERROR] Failed to start the bot"
        exit 1
    fi
}

# Function to stop
stop_bot() {
    echo "Stopping CoinFlow bot..."
    docker-compose down
    echo "[SUCCESS] Bot stopped"
}

# Function to view logs
view_logs() {
    echo "Showing logs (Press Ctrl+C to exit)..."
    docker-compose logs -f
}

# Function to restart
restart_bot() {
    echo "Restarting CoinFlow bot..."
    docker-compose restart
    echo "[SUCCESS] Bot restarted"
}

# Function to clean
clean_all() {
    echo "[WARNING] This will remove all containers and images!"
    read -p "Are you sure? (y/n): " confirm
    if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
        docker-compose down --rmi all --volumes
        echo "[SUCCESS] Cleanup complete"
    else
        echo "Cleanup cancelled"
    fi
}

# Main loop
while true; do
    show_menu
    case $choice in
        1)
            build_start
            break
            ;;
        2)
            stop_bot
            break
            ;;
        3)
            view_logs
            break
            ;;
        4)
            restart_bot
            break
            ;;
        5)
            clean_all
            break
            ;;
        6)
            echo "Goodbye!"
            exit 0
            ;;
        *)
            echo "Invalid choice! Please enter 1-6"
            ;;
    esac
done
