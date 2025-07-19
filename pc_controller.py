import os
import sys
import subprocess
import psutil
import platform
import time
import tempfile
from datetime import datetime
try:
    from PIL import ImageGrab
except ImportError:
    ImageGrab = None

class PCController:
    """Класс для управления компьютером через Telegram бота"""
    
    def __init__(self):
        self.system = platform.system()
    
    def get_system_info(self):
        """Получение информации о системе"""
        try:
            # Основная информация
            system = platform.system()
            release = platform.release()
            version = platform.version()
            machine = platform.machine()
            processor = platform.processor()
            
            # Время работы системы
            boot_time = psutil.boot_time()
            uptime = datetime.now() - datetime.fromtimestamp(boot_time)
            
            info = f"""
*Система:* {system} {release}
*Версия:* {version}
*Архитектура:* {machine}
*Процессор:* {processor}
*Время работы:* {str(uptime).split('.')[0]}
*Время загрузки:* {datetime.fromtimestamp(boot_time).strftime('%Y-%m-%d %H:%M:%S')}
            """
            return info.strip()
        except Exception as e:
            return f"Ошибка получения информации о системе: {str(e)}"
    
    def get_cpu_usage(self):
        """Получение загрузки процессора"""
        try:
            return psutil.cpu_percent(interval=1)
        except Exception as e:
            raise Exception(f"Ошибка получения загрузки CPU: {str(e)}")
    
    def get_memory_usage(self):
        """Получение информации об использовании памяти"""
        try:
            memory = psutil.virtual_memory()
            total = self._bytes_to_gb(memory.total)
            used = self._bytes_to_gb(memory.used)
            free = self._bytes_to_gb(memory.available)
            percent = memory.percent
            
            return f"""
*Общий объем:* {total:.2f} GB
*Используется:* {used:.2f} GB ({percent:.1f}%)
*Доступно:* {free:.2f} GB
            """.strip()
        except Exception as e:
            raise Exception(f"Ошибка получения данных о памяти: {str(e)}")
    
    def get_disk_usage(self):
        """Получение информации об использовании диска"""
        try:
            disk_info = ""
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    total = self._bytes_to_gb(usage.total)
                    used = self._bytes_to_gb(usage.used)
                    free = self._bytes_to_gb(usage.free)
                    percent = (used / total) * 100 if total > 0 else 0
                    
                    disk_info += f"""
*Диск {partition.device}*
Общий объем: {total:.2f} GB
Используется: {used:.2f} GB ({percent:.1f}%)
Свободно: {free:.2f} GB

"""
                except PermissionError:
                    continue
            
            return disk_info.strip()
        except Exception as e:
            raise Exception(f"Ошибка получения данных о диске: {str(e)}")
    
    def _bytes_to_gb(self, bytes_value):
        """Конвертация байтов в гигабайты"""
        return bytes_value / (1024 ** 3)
    
    def shutdown(self, delay=30):
        """Выключение компьютера"""
        try:
            if self.system == "Windows":
                subprocess.run(f"shutdown /s /t {delay}", shell=True, check=True)
            elif self.system == "Linux" or self.system == "Darwin":
                subprocess.run(f"sudo shutdown -h +{delay//60}", shell=True, check=True)
        except Exception as e:
            raise Exception(f"Ошибка выключения системы: {str(e)}")
    
    def restart(self, delay=30):
        """Перезагрузка компьютера"""
        try:
            if self.system == "Windows":
                subprocess.run(f"shutdown /r /t {delay}", shell=True, check=True)
            elif self.system == "Linux" or self.system == "Darwin":
                subprocess.run(f"sudo shutdown -r +{delay//60}", shell=True, check=True)
        except Exception as e:
            raise Exception(f"Ошибка перезагрузки системы: {str(e)}")
    
    def sleep(self):
        """Перевод в спящий режим"""
        try:
            if self.system == "Windows":
                subprocess.run("rundll32.exe powrprof.dll,SetSuspendState 0,1,0", shell=True, check=True)
            elif self.system == "Linux":
                subprocess.run("systemctl suspend", shell=True, check=True)
            elif self.system == "Darwin":
                subprocess.run("pmset sleepnow", shell=True, check=True)
        except Exception as e:
            raise Exception(f"Ошибка перевода в спящий режим: {str(e)}")
    
    def lock_screen(self):
        """Блокировка экрана"""
        try:
            if self.system == "Windows":
                subprocess.run("rundll32.exe user32.dll,LockWorkStation", shell=True, check=True)
            elif self.system == "Linux":
                subprocess.run("gnome-screensaver-command -l", shell=True, check=True)
            elif self.system == "Darwin":
                subprocess.run("pmset displaysleepnow", shell=True, check=True)
        except Exception as e:
            raise Exception(f"Ошибка блокировки экрана: {str(e)}")
    
    def take_screenshot(self):
        """Создание скриншота"""
        try:
            if ImageGrab is None:
                raise Exception("Pillow не установлен. Установите: pip install Pillow")
            
            # Создаем временный файл
            temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
            temp_file.close()
            
            # Делаем скриншот
            screenshot = ImageGrab.grab()
            screenshot.save(temp_file.name, 'PNG')
            
            return temp_file.name
        except Exception as e:
            raise Exception(f"Ошибка создания скриншота: {str(e)}")
    
    def volume_up(self, step=10):
        """Увеличение громкости"""
        try:
            if self.system == "Windows":
                # Используем nircmd для Windows (нужно скачать отдельно)
                # Альтернативно можно использовать pycaw
                subprocess.run("nircmd.exe changesysvolume 6553", shell=True, check=True)
            elif self.system == "Linux":
                subprocess.run(f"amixer -D pulse sset Master {step}%+", shell=True, check=True)
            elif self.system == "Darwin":
                subprocess.run(f"osascript -e 'set volume output volume (output volume of (get volume settings) + {step})'", shell=True, check=True)
        except Exception as e:
            # Если команды не работают, используем альтернативный метод для Windows
            if self.system == "Windows":
                try:
                    import pycaw
                    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
                    devices = AudioUtilities.GetSpeakers()
                    interface = devices.Activate(IAudioEndpointVolume._iid_, None, None)
                    volume = interface.QueryInterface(IAudioEndpointVolume)
                    current_volume = volume.GetMasterScalarVolume()
                    new_volume = min(1.0, current_volume + 0.1)
                    volume.SetMasterScalarVolume(new_volume, None)
                except:
                    raise Exception(f"Ошибка увеличения громкости: {str(e)}")
            else:
                raise Exception(f"Ошибка увеличения громкости: {str(e)}")
    
    def volume_down(self, step=10):
        """Уменьшение громкости"""
        try:
            if self.system == "Windows":
                subprocess.run("nircmd.exe changesysvolume -6553", shell=True, check=True)
            elif self.system == "Linux":
                subprocess.run(f"amixer -D pulse sset Master {step}%-", shell=True, check=True)
            elif self.system == "Darwin":
                subprocess.run(f"osascript -e 'set volume output volume (output volume of (get volume settings) - {step})'", shell=True, check=True)
        except Exception as e:
            if self.system == "Windows":
                try:
                    import pycaw
                    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
                    devices = AudioUtilities.GetSpeakers()
                    interface = devices.Activate(IAudioEndpointVolume._iid_, None, None)
                    volume = interface.QueryInterface(IAudioEndpointVolume)
                    current_volume = volume.GetMasterScalarVolume()
                    new_volume = max(0.0, current_volume - 0.1)
                    volume.SetMasterScalarVolume(new_volume, None)
                except:
                    raise Exception(f"Ошибка уменьшения громкости: {str(e)}")
            else:
                raise Exception(f"Ошибка уменьшения громкости: {str(e)}")
    
    def mute_toggle(self):
        """Переключение звука (вкл/выкл)"""
        try:
            if self.system == "Windows":
                subprocess.run("nircmd.exe mutesysvolume 2", shell=True, check=True)
            elif self.system == "Linux":
                subprocess.run("amixer -D pulse sset Master toggle", shell=True, check=True)
            elif self.system == "Darwin":
                subprocess.run("osascript -e 'set volume with output muted'", shell=True, check=True)
        except Exception as e:
            raise Exception(f"Ошибка переключения звука: {str(e)}")
    
    def media_play_pause(self):
        """Воспроизведение/пауза медиа"""
        try:
            if self.system == "Windows":
                subprocess.run("nircmd.exe sendkeypress media_play_pause", shell=True, check=True)
            elif self.system == "Linux":
                subprocess.run("playerctl play-pause", shell=True, check=True)
            elif self.system == "Darwin":
                subprocess.run("osascript -e 'tell application \"Music\" to playpause'", shell=True, check=True)
        except Exception as e:
            raise Exception(f"Ошибка управления воспроизведением: {str(e)}")
    
    def media_next(self):
        """Следующий трек"""
        try:
            if self.system == "Windows":
                subprocess.run("nircmd.exe sendkeypress media_next", shell=True, check=True)
            elif self.system == "Linux":
                subprocess.run("playerctl next", shell=True, check=True)
            elif self.system == "Darwin":
                subprocess.run("osascript -e 'tell application \"Music\" to next track'", shell=True, check=True)
        except Exception as e:
            raise Exception(f"Ошибка переключения трека: {str(e)}")
    
    def media_previous(self):
        """Предыдущий трек"""
        try:
            if self.system == "Windows":
                subprocess.run("nircmd.exe sendkeypress media_prev", shell=True, check=True)
            elif self.system == "Linux":
                subprocess.run("playerctl previous", shell=True, check=True)
            elif self.system == "Darwin":
                subprocess.run("osascript -e 'tell application \"Music\" to previous track'", shell=True, check=True)
        except Exception as e:
            raise Exception(f"Ошибка переключения трека: {str(e)}")
    
    def open_file(self, file_path):
        """Открытие файла"""
        try:
            if not os.path.exists(file_path):
                raise Exception("Файл не найден")
            
            if self.system == "Windows":
                os.startfile(file_path)
            elif self.system == "Linux":
                subprocess.run(f"xdg-open '{file_path}'", shell=True, check=True)
            elif self.system == "Darwin":
                subprocess.run(f"open '{file_path}'", shell=True, check=True)
        except Exception as e:
            raise Exception(f"Ошибка открытия файла: {str(e)}")
    
    def list_files(self, directory):
        """Получение списка файлов в директории"""
        try:
            if not os.path.exists(directory):
                raise Exception("Директория не найдена")
            
            if not os.path.isdir(directory):
                raise Exception("Указанный путь не является директорией")
            
            files = []
            for item in os.listdir(directory):
                item_path = os.path.join(directory, item)
                if os.path.isdir(item_path):
                    files.append(f"📁 {item}/")
                else:
                    files.append(f"📄 {item}")
            
            return sorted(files)
        except Exception as e:
            raise Exception(f"Ошибка получения списка файлов: {str(e)}")
    
    def get_network_info(self):
        """Получение информации о сети"""
        try:
            network_info = ""
            for interface_name, interface_addresses in psutil.net_if_addrs().items():
                for address in interface_addresses:
                    if str(address.family) == 'AddressFamily.AF_INET':
                        network_info += f"Interface: {interface_name}\n"
                        network_info += f"IP Address: {address.address}\n"
                        network_info += f"Netmask: {address.netmask}\n\n"
            return network_info
        except Exception as e:
            raise Exception(f"Ошибка получения сетевой информации: {str(e)}")
    
    def run_command(self, command):
        """Выполнение произвольной команды (ОСТОРОЖНО!)"""
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
            return f"Код возврата: {result.returncode}\nВывод:\n{result.stdout}\nОшибки:\n{result.stderr}"
        except subprocess.TimeoutExpired:
            return "Команда превысила лимит времени выполнения (30 секунд)"
        except Exception as e:
            raise Exception(f"Ошибка выполнения команды: {str(e)}")
