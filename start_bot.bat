@echo off
echo Запуск Telegram PC Controller...

REM Переходим в папку с ботом
cd /d "%~dp0"

REM Активируем виртуальное окружение, если оно есть
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

REM Запускаем системный трей
python tray_app.py --autostart

pause
