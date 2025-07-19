#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram Bot для управления ПК
Главный файл запуска
"""

from bot import bot
import logging

if __name__ == "__main__":
    print("🤖 Запуск Telegram бота для управления ПК...")
    print("📝 Убедитесь, что вы настроили TOKEN и ADMIN_ID в файле bot.py")
    print("🔒 Бот запущен. Для остановки нажмите Ctrl+C")
    
    try:
        bot.polling(none_stop=True)
    except KeyboardInterrupt:
        print("\n⏹️ Бот остановлен пользователем")
    except Exception as e:
        print(f"❌ Ошибка в работе бота: {e}")
        logging.error(f"Критическая ошибка: {e}")