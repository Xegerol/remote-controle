# Пример файла конфигурации
# Скопируйте этот файл как config.py и настройте под себя

# Telegram Bot Token - получите у @BotFather
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

# Ваш Telegram ID - получите у @userinfobot  
ADMIN_ID = 123456789

# Настройки безопасности
ENABLE_SHUTDOWN_COMMANDS = True  # Разрешить команды выключения/перезагрузки
SHUTDOWN_DELAY = 30              # Задержка перед выключением (секунды)

# Настройки логирования
LOG_LEVEL = "INFO"               # DEBUG, INFO, WARNING, ERROR
LOG_TO_FILE = True              # Сохранять логи в файл

# Настройки скриншотов
SCREENSHOT_QUALITY = 95          # Качество JPEG (1-100)
DELETE_SCREENSHOTS = True       # Удалять временные файлы скриншотов

# Настройки файловой системы
MAX_FILES_IN_LIST = 20          # Максимум файлов в списке
ALLOWED_EXTENSIONS = [          # Разрешенные расширения для открытия
    '.txt', '.pdf', '.doc', '.docx', 
    '.jpg', '.png', '.gif', '.mp4', 
    '.mp3', '.avi', '.exe'
]
