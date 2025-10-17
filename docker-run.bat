@echo off
REM CoinFlow Bot - Docker Runner for Windows
REM This script helps you run CoinFlow bot using Docker

echo ========================================
echo   CoinFlow Bot v2.0 - Docker Runner
echo ========================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not installed or not in PATH
    echo Please install Docker Desktop: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist ".env" (
    echo [WARNING] .env file not found!
    echo Creating .env from .env.example...
    copy .env.example .env
    echo.
    echo [ACTION REQUIRED] Please edit .env and add your TELEGRAM_BOT_TOKEN
    echo Then run this script again.
    pause
    exit /b 1
)

echo What would you like to do?
echo.
echo 1. Build and start the bot
echo 2. Stop the bot
echo 3. View logs
echo 4. Restart the bot
echo 5. Remove containers and images
echo 6. Exit
echo.
set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" goto build
if "%choice%"=="2" goto stop
if "%choice%"=="3" goto logs
if "%choice%"=="4" goto restart
if "%choice%"=="5" goto clean
if "%choice%"=="6" goto end

echo Invalid choice!
pause
exit /b 1

:build
echo.
echo Building and starting CoinFlow bot...
docker-compose up -d --build
if errorlevel 1 (
    echo [ERROR] Failed to start the bot
    pause
    exit /b 1
)
echo.
echo [SUCCESS] Bot is now running!
echo Use 'docker-compose logs -f' to view logs
goto end

:stop
echo.
echo Stopping CoinFlow bot...
docker-compose down
echo [SUCCESS] Bot stopped
goto end

:logs
echo.
echo Showing logs (Press Ctrl+C to exit)...
docker-compose logs -f
goto end

:restart
echo.
echo Restarting CoinFlow bot...
docker-compose restart
echo [SUCCESS] Bot restarted
goto end

:clean
echo.
echo [WARNING] This will remove all containers and images!
set /p confirm="Are you sure? (y/n): "
if /i "%confirm%"=="y" (
    docker-compose down --rmi all --volumes
    echo [SUCCESS] Cleanup complete
) else (
    echo Cleanup cancelled
)
goto end

:end
echo.
pause
