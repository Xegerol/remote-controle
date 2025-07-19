import telebot
import logging
from pc_controller import PCController
import os
from functools import wraps

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен бота (замените на свой)
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

# ID администратора (замените на свой Telegram ID)
ADMIN_ID = 123456789  # Ваш Telegram ID

bot = telebot.TeleBot(BOT_TOKEN)
pc_controller = PCController()

# Декоратор для проверки прав администратора
def admin_required(func):
    @wraps(func)
    def wrapper(message):
        if message.from_user.id != ADMIN_ID:
            bot.reply_to(message, "❌ У вас нет прав для выполнения этой команды!")
            return
        return func(message)
    return wrapper

# Команда /start
@bot.message_handler(commands=['start'])
def start_command(message):
    welcome_text = """
🤖 Добро пожаловать в бота управления ПК!

📋 Доступные команды:

🖥️ *Управление системой:*
/shutdown - Выключить ПК
/restart - Перезагрузить ПК
/sleep - Перевести в спящий режим
/lock - Заблокировать экран

📊 *Информация о системе:*
/sysinfo - Информация о системе
/cpu - Загрузка процессора
/memory - Использование памяти
/disk - Использование диска

🔊 *Управление звуком:*
/volume_up - Увеличить громкость
/volume_down - Уменьшить громкость
/mute - Отключить/включить звук

📷 *Скриншот:*
/screenshot - Сделать скриншот экрана

📁 *Файловая система:*
/open_file - Открыть файл
/list_files - Список файлов в директории

🎵 *Медиа:*
/play_pause - Воспроизведение/пауза
/next_track - Следующий трек
/prev_track - Предыдущий трек

⚠️ *Внимание:* Некоторые команды доступны только администратору!
    """
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

# Информация о системе
@bot.message_handler(commands=['sysinfo'])
@admin_required
def system_info(message):
    try:
        info = pc_controller.get_system_info()
        bot.reply_to(message, f"🖥️ *Информация о системе:*\n\n{info}", parse_mode='Markdown')
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка получения информации: {str(e)}")

# Загрузка процессора
@bot.message_handler(commands=['cpu'])
@admin_required
def cpu_usage(message):
    try:
        cpu = pc_controller.get_cpu_usage()
        bot.reply_to(message, f"🔥 *Загрузка процессора:* {cpu}%", parse_mode='Markdown')
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка получения данных о CPU: {str(e)}")

# Использование памяти
@bot.message_handler(commands=['memory'])
@admin_required
def memory_usage(message):
    try:
        memory = pc_controller.get_memory_usage()
        bot.reply_to(message, f"🧠 *Использование памяти:*\n{memory}", parse_mode='Markdown')
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка получения данных о памяти: {str(e)}")

# Использование диска
@bot.message_handler(commands=['disk'])
@admin_required
def disk_usage(message):
    try:
        disk = pc_controller.get_disk_usage()
        bot.reply_to(message, f"💾 *Использование диска:*\n{disk}", parse_mode='Markdown')
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка получения данных о диске: {str(e)}")

# Выключение ПК
@bot.message_handler(commands=['shutdown'])
@admin_required
def shutdown_pc(message):
    try:
        pc_controller.shutdown()
        bot.reply_to(message, "🔌 ПК будет выключен через 30 секунд...")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка выключения: {str(e)}")

# Перезагрузка ПК
@bot.message_handler(commands=['restart'])
@admin_required
def restart_pc(message):
    try:
        pc_controller.restart()
        bot.reply_to(message, "🔄 ПК будет перезагружен через 30 секунд...")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка перезагрузки: {str(e)}")

# Спящий режим
@bot.message_handler(commands=['sleep'])
@admin_required
def sleep_pc(message):
    try:
        pc_controller.sleep()
        bot.reply_to(message, "😴 ПК переведен в спящий режим")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка перевода в спящий режим: {str(e)}")

# Блокировка экрана
@bot.message_handler(commands=['lock'])
@admin_required
def lock_screen(message):
    try:
        pc_controller.lock_screen()
        bot.reply_to(message, "🔒 Экран заблокирован")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка блокировки экрана: {str(e)}")

# Скриншот
@bot.message_handler(commands=['screenshot'])
@admin_required
def take_screenshot(message):
    try:
        screenshot_path = pc_controller.take_screenshot()
        with open(screenshot_path, 'rb') as photo:
            bot.send_photo(message.chat.id, photo, caption="📷 Скриншот экрана")
        os.remove(screenshot_path)  # Удаляем временный файл
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка создания скриншота: {str(e)}")

# Управление громкостью
@bot.message_handler(commands=['volume_up'])
@admin_required
def volume_up(message):
    try:
        pc_controller.volume_up()
        bot.reply_to(message, "🔊 Громкость увеличена")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка увеличения громкости: {str(e)}")

@bot.message_handler(commands=['volume_down'])
@admin_required
def volume_down(message):
    try:
        pc_controller.volume_down()
        bot.reply_to(message, "🔉 Громкость уменьшена")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка уменьшения громкости: {str(e)}")

@bot.message_handler(commands=['mute'])
@admin_required
def mute_toggle(message):
    try:
        pc_controller.mute_toggle()
        bot.reply_to(message, "🔇 Звук переключен")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка переключения звука: {str(e)}")

# Управление медиа
@bot.message_handler(commands=['play_pause'])
@admin_required
def play_pause(message):
    try:
        pc_controller.media_play_pause()
        bot.reply_to(message, "⏯️ Воспроизведение/пауза")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка управления воспроизведением: {str(e)}")

@bot.message_handler(commands=['next_track'])
@admin_required
def next_track(message):
    try:
        pc_controller.media_next()
        bot.reply_to(message, "⏭️ Следующий трек")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка переключения трека: {str(e)}")

@bot.message_handler(commands=['prev_track'])
@admin_required
def prev_track(message):
    try:
        pc_controller.media_previous()
        bot.reply_to(message, "⏮️ Предыдущий трек")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка переключения трека: {str(e)}")

# Открытие файла
@bot.message_handler(commands=['open_file'])
@admin_required
def open_file_command(message):
    msg = bot.reply_to(message, "📁 Введите путь к файлу для открытия:")
    bot.register_next_step_handler(msg, process_open_file)

def process_open_file(message):
    try:
        file_path = message.text.strip()
        pc_controller.open_file(file_path)
        bot.reply_to(message, f"✅ Файл открыт: {file_path}")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка открытия файла: {str(e)}")

# Список файлов
@bot.message_handler(commands=['list_files'])
@admin_required
def list_files_command(message):
    msg = bot.reply_to(message, "📁 Введите путь к директории:")
    bot.register_next_step_handler(msg, process_list_files)

def process_list_files(message):
    try:
        directory = message.text.strip()
        files = pc_controller.list_files(directory)
        if files:
            file_list = "\n".join(files[:20])  # Показываем только первые 20 файлов
            if len(files) > 20:
                file_list += f"\n... и еще {len(files) - 20} файлов"
            bot.reply_to(message, f"📁 *Файлы в {directory}:*\n\n`{file_list}`", parse_mode='Markdown')
        else:
            bot.reply_to(message, "📂 Директория пуста или недоступна")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка получения списка файлов: {str(e)}")

# Обработчик всех остальных сообщений
@bot.message_handler(func=lambda message: True)
def unknown_command(message):
    bot.reply_to(message, "❓ Неизвестная команда. Используйте /start для просмотра доступных команд.")

if __name__ == "__main__":
    print("🤖 Бот запущен...")
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logger.error(f"Ошибка в работе бота: {e}")
