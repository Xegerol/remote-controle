#!/usr/bin/env python3
"""
Главный файл для запуска Telegram PC Controller
Можно запустить как обычный бот или как приложение системного трея
"""

import sys
import os
import argparse

def main():
    parser = argparse.ArgumentParser(description='Telegram PC Controller')
    parser.add_argument('--tray', action='store_true', help='Запустить с системным треем')
    parser.add_argument('--console', action='store_true', help='Запустить в консольном режиме')
    args = parser.parse_args()

    # Проверяем наличие config.py
    if not os.path.exists('config.py'):
        print("❌ Ошибка: Файл config.py не найден!")
        print("📋 Инструкция по настройке:")
        print("1. Скопируйте config_example.py в config.py")
        print("2. Отредактируйте config.py, указав ваш BOT_TOKEN и ADMIN_CHAT_ID")
        print("3. Запустите программу снова")
        input("Нажмите Enter для выхода...")
        return

    if args.tray or (not args.console and len(sys.argv) == 1):
        # Запуск с системным треем (по умолчанию)
        try:
            from tray_app import TrayApp
            app = TrayApp()
            app.run()
        except ImportError as e:
            print(f"❌ Ошибка импорта для системного трея: {e}")
            print("� Установите недостающие зависимости: pip install pystray")
            # Fallback к консольному режиму
            run_console_mode()
    else:
        # Консольный режим
        run_console_mode()

def run_console_mode():
    """Запуск в консольном режиме"""
    try:
        from config import BOT_TOKEN, ADMIN_CHAT_ID
        from bot import TelegramBot
        import time
        
        bot_instance = TelegramBot(BOT_TOKEN, ADMIN_CHAT_ID)
        print("🤖 Telegram PC Controller запущен в консольном режиме...")
        print("Нажмите Ctrl+C для остановки")
        
        bot_instance.start()
        
        try:
            while bot_instance.is_running():
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Остановка бота...")
            bot_instance.stop()
            print("✅ Бот остановлен")
            
    except ImportError:
        print("❌ Ошибка: Не удалось загрузить конфигурацию из config.py")
    except Exception as e:
        print(f"❌ Ошибка запуска бота: {e}")

if __name__ == "__main__":
    main()
