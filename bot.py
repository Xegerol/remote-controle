import telebot
import logging
from pc_controller import PCController
import os
from functools import wraps
import threading
import time

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TelegramBot:
    """Класс для управления Telegram ботом"""
    
    def __init__(self, bot_token, admin_id):
        self.bot_token = bot_token
        self.admin_id = admin_id
        self.bot = telebot.TeleBot(bot_token)
        self.pc_controller = PCController()
        self.running = False
        self.polling_thread = None
        
        # Регистрируем обработчики команд
        self._register_handlers()
    
    def _register_handlers(self):
        """Регистрация обработчиков команд"""
        
        # Декоратор для проверки прав администратора
        def admin_required(func):
            @wraps(func)
            def wrapper(message):
                if message.from_user.id != self.admin_id:
                    self.bot.reply_to(message, "❌ У вас нет прав для выполнения этой команды!")
                    return
                return func(message)
            return wrapper

        # Команда /start
        @self.bot.message_handler(commands=['start'])
        def start_command(message):
            welcome_text = """🤖 Добро пожаловать в бота управления ПК!

📋 Доступные команды:

🖥️ Управление системой:
/shutdown - Выключить ПК
/restart - Перезагрузить ПК
/sleep - Перевести в спящий режим
/lock - Заблокировать экран

📊 Информация о системе:
/sysinfo - Информация о системе
/cpu - Загрузка процессора
/memory - Использование памяти
/disk - Использование диска

🔊 Управление звуком:
/volume_up - Увеличить громкость
/volume_down - Уменьшить громкость
/mute - Выключить/включить звук

🎵 Управление медиа:
/play_pause - Воспроизведение/пауза
/next - Следующий трек
/previous - Предыдущий трек

📷 Скриншоты:
/screenshot - Сделать скриншот

📁 Файлы:
/files <путь> - Список файлов в папке
/open <путь> - Открыть файл

🌐 Сеть:
/network - Информация о сети

⚠️ Только для администратора!"""
            self.bot.reply_to(message, welcome_text)

        # Команда /sysinfo
        @self.bot.message_handler(commands=['sysinfo'])
        @admin_required
        def system_info_command(message):
            try:
                info = self.pc_controller.get_system_info()
                self.bot.reply_to(message, f"🖥️ Информация о системе:\n\n{info}")
            except Exception as e:
                self.bot.reply_to(message, f"❌ Ошибка получения информации: {str(e)}")

        # Команда /cpu
        @self.bot.message_handler(commands=['cpu'])
        @admin_required
        def cpu_command(message):
            try:
                cpu = self.pc_controller.get_cpu_usage()
                self.bot.reply_to(message, f"🔥 Загрузка процессора: {cpu}%")
            except Exception as e:
                self.bot.reply_to(message, f"❌ Ошибка получения данных о CPU: {str(e)}")

        # Команда /memory
        @self.bot.message_handler(commands=['memory'])
        @admin_required
        def memory_command(message):
            try:
                memory = self.pc_controller.get_memory_usage()
                self.bot.reply_to(message, f"🧠 Использование памяти:\n{memory}")
            except Exception as e:
                self.bot.reply_to(message, f"❌ Ошибка получения данных о памяти: {str(e)}")

        # Команда /disk
        @self.bot.message_handler(commands=['disk'])
        @admin_required
        def disk_command(message):
            try:
                disk = self.pc_controller.get_disk_usage()
                self.bot.reply_to(message, f"💾 Использование диска:\n{disk}")
            except Exception as e:
                self.bot.reply_to(message, f"❌ Ошибка получения данных о диске: {str(e)}")

        # Команда /shutdown
        @self.bot.message_handler(commands=['shutdown'])
        @admin_required
        def shutdown_command(message):
            try:
                self.pc_controller.shutdown()
                self.bot.reply_to(message, "🔴 Компьютер будет выключен через 30 секунд!")
            except Exception as e:
                self.bot.reply_to(message, f"❌ Ошибка выключения: {str(e)}")

        # Команда /restart
        @self.bot.message_handler(commands=['restart'])
        @admin_required
        def restart_command(message):
            try:
                self.pc_controller.restart()
                self.bot.reply_to(message, "🔄 Компьютер будет перезагружен через 30 секунд!")
            except Exception as e:
                self.bot.reply_to(message, f"❌ Ошибка перезагрузки: {str(e)}")

        # Команда /sleep
        @self.bot.message_handler(commands=['sleep'])
        @admin_required
        def sleep_command(message):
            try:
                self.pc_controller.sleep()
                self.bot.reply_to(message, "😴 Компьютер переводится в спящий режим...")
            except Exception as e:
                self.bot.reply_to(message, f"❌ Ошибка перевода в спящий режим: {str(e)}")

        # Команда /lock
        @self.bot.message_handler(commands=['lock'])
        @admin_required
        def lock_command(message):
            try:
                self.pc_controller.lock_screen()
                self.bot.reply_to(message, "🔒 Экран заблокирован!")
            except Exception as e:
                self.bot.reply_to(message, f"❌ Ошибка блокировки экрана: {str(e)}")

        # Команда /screenshot
        @self.bot.message_handler(commands=['screenshot'])
        @admin_required
        def screenshot_command(message):
            try:
                screenshot_path = self.pc_controller.take_screenshot()
                with open(screenshot_path, 'rb') as photo:
                    self.bot.send_photo(message.chat.id, photo)
                os.remove(screenshot_path)
            except Exception as e:
                self.bot.reply_to(message, f"❌ Ошибка создания скриншота: {str(e)}")

        # Команды управления звуком
        @self.bot.message_handler(commands=['volume_up'])
        @admin_required
        def volume_up_command(message):
            try:
                self.pc_controller.volume_up()
                self.bot.reply_to(message, "🔊 Громкость увеличена!")
            except Exception as e:
                self.bot.reply_to(message, f"❌ Ошибка увеличения громкости: {str(e)}")

        @self.bot.message_handler(commands=['volume_down'])
        @admin_required
        def volume_down_command(message):
            try:
                self.pc_controller.volume_down()
                self.bot.reply_to(message, "🔉 Громкость уменьшена!")
            except Exception as e:
                self.bot.reply_to(message, f"❌ Ошибка уменьшения громкости: {str(e)}")

        @self.bot.message_handler(commands=['mute'])
        @admin_required
        def mute_command(message):
            try:
                self.pc_controller.mute_toggle()
                self.bot.reply_to(message, "🔇 Звук переключен!")
            except Exception as e:
                self.bot.reply_to(message, f"❌ Ошибка переключения звука: {str(e)}")

        # Команды управления медиа
        @self.bot.message_handler(commands=['play_pause'])
        @admin_required
        def play_pause_command(message):
            try:
                self.pc_controller.media_play_pause()
                self.bot.reply_to(message, "⏯️ Воспроизведение переключено!")
            except Exception as e:
                self.bot.reply_to(message, f"❌ Ошибка управления воспроизведением: {str(e)}")

        @self.bot.message_handler(commands=['next'])
        @admin_required
        def next_command(message):
            try:
                self.pc_controller.media_next()
                self.bot.reply_to(message, "⏭️ Следующий трек!")
            except Exception as e:
                self.bot.reply_to(message, f"❌ Ошибка переключения трека: {str(e)}")

        @self.bot.message_handler(commands=['previous'])
        @admin_required
        def previous_command(message):
            try:
                self.pc_controller.media_previous()
                self.bot.reply_to(message, "⏮️ Предыдущий трек!")
            except Exception as e:
                self.bot.reply_to(message, f"❌ Ошибка переключения трека: {str(e)}")

        # Команда /network
        @self.bot.message_handler(commands=['network'])
        @admin_required
        def network_command(message):
            try:
                network = self.pc_controller.get_network_info()
                self.bot.reply_to(message, f"🌐 Сетевая информация:\n{network}")
            except Exception as e:
                self.bot.reply_to(message, f"❌ Ошибка получения сетевой информации: {str(e)}")

        # Команда /files
        @self.bot.message_handler(commands=['files'])
        @admin_required
        def files_command(message):
            try:
                # Получаем путь из сообщения
                text = message.text.split(' ', 1)
                if len(text) < 2:
                    self.bot.reply_to(message, "📁 Укажите путь к папке. Пример: /files C:\\")
                    return
                
                directory = text[1].strip()
                files = self.pc_controller.list_files(directory)
                
                if files:
                    files_text = "\n".join(files[:20])  # Показываем первые 20 файлов
                    if len(files) > 20:
                        files_text += f"\n... и еще {len(files) - 20} файлов"
                    self.bot.reply_to(message, f"📂 Содержимое папки {directory}:\n\n{files_text}")
                else:
                    self.bot.reply_to(message, "📂 Директория пуста или недоступна")
            except Exception as e:
                self.bot.reply_to(message, f"❌ Ошибка получения списка файлов: {str(e)}")

        # Команда /open
        @self.bot.message_handler(commands=['open'])
        @admin_required
        def open_command(message):
            try:
                # Получаем путь из сообщения
                text = message.text.split(' ', 1)
                if len(text) < 2:
                    self.bot.reply_to(message, "📁 Укажите путь к файлу. Пример: /open C:\\file.txt")
                    return
                
                file_path = text[1].strip()
                self.pc_controller.open_file(file_path)
                self.bot.reply_to(message, f"📂 Файл {file_path} открыт!")
            except Exception as e:
                self.bot.reply_to(message, f"❌ Ошибка открытия файла: {str(e)}")

        # Обработчик всех остальных сообщений
        @self.bot.message_handler(func=lambda message: True)
        def unknown_command(message):
            self.bot.reply_to(message, "❓ Неизвестная команда. Используйте /start для просмотра доступных команд.")

    def start(self):
        """Запуск бота"""
        if self.running:
            logger.warning("Бот уже запущен")
            return
            
        self.running = True
        logger.info("Telegram бот запускается...")
        
        def polling_worker():
            try:
                self.bot.polling(none_stop=True, interval=1, timeout=20)
            except Exception as e:
                logger.error(f"Ошибка в работе бота: {e}")
                self.running = False
        
        self.polling_thread = threading.Thread(target=polling_worker, daemon=True)
        self.polling_thread.start()
        logger.info("Telegram бот успешно запущен!")

    def stop(self):
        """Остановка бота"""
        if not self.running:
            logger.warning("Бот не запущен")
            return
            
        self.running = False
        try:
            self.bot.stop_polling()
            logger.info("Telegram бот остановлен")
        except Exception as e:
            logger.error(f"Ошибка остановки бота: {e}")

    def is_running(self):
        """Проверка статуса бота"""
        return self.running

# Для обратной совместимости - если файл запускается напрямую
if __name__ == "__main__":
    # Попытка загрузить конфигурацию
    try:
        from config import BOT_TOKEN, ADMIN_CHAT_ID
        
        bot_instance = TelegramBot(BOT_TOKEN, ADMIN_CHAT_ID)
        print("🤖 Бот запущен...")
        bot_instance.start()
        
        # Держим главный поток активным
        try:
            while bot_instance.is_running():
                time.sleep(1)
        except KeyboardInterrupt:
            print("Остановка бота...")
            bot_instance.stop()
            
    except ImportError:
        print("❌ Ошибка: Файл config.py не найден!")
        print("Создайте файл config.py на основе config_example.py")
    except Exception as e:
        print(f"❌ Ошибка запуска: {e}")
