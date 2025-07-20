import sys
import os
import threading
import winreg
import tkinter as tk
from tkinter import messagebox
import pystray
from PIL import Image, ImageDraw
import subprocess
from bot import TelegramBot
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('telegram_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TrayApp:
    """Приложение системного трея для Telegram бота"""
    
    def __init__(self):
        self.bot_thread = None
        self.bot_instance = None
        self.is_running = False
        self.icon = None
        
    def create_image(self, color="blue"):
        """Создание иконки для трея"""
        # Создаем простую иконку 64x64
        image = Image.new('RGB', (64, 64), color=(255, 255, 255))
        draw = ImageDraw.Draw(image)
        
        if color == "blue":
            # Синяя иконка - бот запущен
            draw.ellipse([8, 8, 56, 56], fill=(0, 123, 255))
            draw.text((20, 25), "TG", fill=(255, 255, 255))
        else:
            # Красная иконка - бот остановлен
            draw.ellipse([8, 8, 56, 56], fill=(220, 53, 69))
            draw.text((20, 25), "TG", fill=(255, 255, 255))
            
        return image
    
    def start_bot(self):
        """Запуск бота в отдельном потоке"""
        if self.is_running:
            messagebox.showinfo("Информация", "Бот уже запущен!")
            return
            
        try:
            # Проверяем наличие config.py
            if not os.path.exists('config.py'):
                messagebox.showerror(
                    "Ошибка", 
                    "Файл config.py не найден!\nСоздайте файл config.py на основе config_example.py"
                )
                return
            
            def run_bot():
                try:
                    from config import BOT_TOKEN, ADMIN_CHAT_ID
                    self.bot_instance = TelegramBot(BOT_TOKEN, ADMIN_CHAT_ID)
                    self.is_running = True
                    self.update_icon()
                    logger.info("Telegram бот запущен через системный трей")
                    self.bot_instance.start()
                except Exception as e:
                    logger.error(f"Ошибка запуска бота: {e}")
                    self.is_running = False
                    self.update_icon()
                    messagebox.showerror("Ошибка", f"Не удалось запустить бота:\n{str(e)}")
            
            self.bot_thread = threading.Thread(target=run_bot, daemon=True)
            self.bot_thread.start()
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка запуска: {str(e)}")
    
    def stop_bot(self):
        """Остановка бота"""
        if not self.is_running:
            messagebox.showinfo("Информация", "Бот не запущен!")
            return
            
        try:
            if self.bot_instance:
                self.bot_instance.stop()
            self.is_running = False
            self.update_icon()
            logger.info("Telegram бот остановлен")
            messagebox.showinfo("Успех", "Бот остановлен!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка остановки бота: {str(e)}")
    
    def update_icon(self):
        """Обновление иконки в зависимости от состояния бота"""
        if self.icon:
            color = "blue" if self.is_running else "red"
            self.icon.icon = self.create_image(color)
            
            # Обновляем tooltip
            status = "Запущен" if self.is_running else "Остановлен"
            self.icon.title = f"Telegram PC Controller - {status}"
    
    def show_status(self):
        """Показать статус бота"""
        status = "Запущен" if self.is_running else "Остановлен"
        messagebox.showinfo("Статус бота", f"Telegram PC Controller\nСтатус: {status}")
    
    def open_config(self):
        """Открыть папку с конфигурацией"""
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            os.startfile(current_dir)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось открыть папку: {str(e)}")
    
    def open_logs(self):
        """Открыть файл логов"""
        try:
            log_file = "telegram_bot.log"
            if os.path.exists(log_file):
                os.startfile(log_file)
            else:
                messagebox.showinfo("Информация", "Файл логов не найден")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось открыть логи: {str(e)}")
    
    def toggle_autostart(self):
        """Переключение автозагрузки"""
        if self.is_autostart_enabled():
            self.disable_autostart()
            messagebox.showinfo("Автозагрузка", "Автозагрузка отключена")
        else:
            self.enable_autostart()
            messagebox.showinfo("Автозагрузка", "Автозагрузка включена")
    
    def is_autostart_enabled(self):
        """Проверка включена ли автозагрузка"""
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_READ
            )
            try:
                winreg.QueryValueEx(key, "TelegramPCController")
                winreg.CloseKey(key)
                return True
            except FileNotFoundError:
                winreg.CloseKey(key)
                return False
        except Exception:
            return False
    
    def enable_autostart(self):
        """Включение автозагрузки"""
        try:
            # Путь к текущему скрипту
            script_path = os.path.abspath(__file__)
            python_exe = sys.executable
            
            # Команда запуска (скрытый запуск)
            command = f'"{python_exe}" "{script_path}" --autostart'
            
            # Добавляем в реестр
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_SET_VALUE
            )
            winreg.SetValueEx(key, "TelegramPCController", 0, winreg.REG_SZ, command)
            winreg.CloseKey(key)
            
            logger.info("Автозагрузка включена")
        except Exception as e:
            logger.error(f"Ошибка включения автозагрузки: {e}")
            messagebox.showerror("Ошибка", f"Не удалось включить автозагрузку: {str(e)}")
    
    def disable_autostart(self):
        """Отключение автозагрузки"""
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_SET_VALUE
            )
            winreg.DeleteValue(key, "TelegramPCController")
            winreg.CloseKey(key)
            
            logger.info("Автозагрузка отключена")
        except Exception as e:
            logger.error(f"Ошибка отключения автозагрузки: {e}")
            messagebox.showerror("Ошибка", f"Не удалось отключить автозагрузку: {str(e)}")
    
    def quit_app(self):
        """Выход из приложения"""
        if self.is_running:
            response = messagebox.askyesno(
                "Подтверждение", 
                "Бот сейчас запущен. Вы уверены, что хотите выйти?"
            )
            if not response:
                return
                
        try:
            if self.bot_instance:
                self.bot_instance.stop()
            self.is_running = False
            logger.info("Приложение завершено")
            if self.icon:
                self.icon.stop()
        except Exception as e:
            logger.error(f"Ошибка при завершении: {e}")
    
    def create_menu(self):
        """Создание контекстного меню трея"""
        autostart_text = "✓ Автозагрузка" if self.is_autostart_enabled() else "Автозагрузка"
        
        return pystray.Menu(
            pystray.MenuItem("Статус", self.show_status),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Запустить бота", self.start_bot),
            pystray.MenuItem("Остановить бота", self.stop_bot),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(autostart_text, self.toggle_autostart),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Открыть папку", self.open_config),
            pystray.MenuItem("Показать логи", self.open_logs),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Выход", self.quit_app)
        )
    
    def run(self, autostart=False):
        """Запуск приложения трея"""
        try:
            # Создаем иконку
            image = self.create_image("red")  # Начинаем с красной (остановлен)
            self.icon = pystray.Icon(
                "telegram_pc_controller",
                image,
                "Telegram PC Controller - Остановлен",
                self.create_menu()
            )
            
            # Если запуск с автозагрузкой, сразу запускаем бота
            if autostart and os.path.exists('config.py'):
                threading.Timer(2.0, self.start_bot).start()
            
            logger.info("Системный трей запущен")
            self.icon.run()
            
        except Exception as e:
            logger.error(f"Ошибка запуска трея: {e}")
            messagebox.showerror("Ошибка", f"Не удалось запустить системный трей: {str(e)}")

def main():
    """Главная функция"""
    # Проверяем аргументы командной строки
    autostart = "--autostart" in sys.argv
    
    # Создаем и запускаем приложение
    app = TrayApp()
    app.run(autostart=autostart)

if __name__ == "__main__":
    main()
