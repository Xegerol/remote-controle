#!/usr/bin/env python3
"""
Утилита для управления автозагрузкой Telegram PC Controller
"""

import os
import sys
import winreg
import argparse

def get_script_path():
    """Получить путь к основному скрипту"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, "main.py")

def is_autostart_enabled():
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

def enable_autostart():
    """Включение автозагрузки"""
    try:
        script_path = get_script_path()
        python_exe = sys.executable
        
        # Команда запуска с параметром --tray
        command = f'"{python_exe}" "{script_path}" --tray'
        
        # Добавляем в реестр
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_SET_VALUE
        )
        winreg.SetValueEx(key, "TelegramPCController", 0, winreg.REG_SZ, command)
        winreg.CloseKey(key)
        
        print("✅ Автозагрузка включена")
        print(f"📁 Команда: {command}")
        return True
    except Exception as e:
        print(f"❌ Ошибка включения автозагрузки: {e}")
        return False

def disable_autostart():
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
        
        print("✅ Автозагрузка отключена")
        return True
    except Exception as e:
        print(f"❌ Ошибка отключения автозагрузки: {e}")
        return False

def check_status():
    """Проверка статуса автозагрузки"""
    enabled = is_autostart_enabled()
    status = "включена" if enabled else "отключена"
    print(f"🔄 Автозагрузка: {status}")
    return enabled

def main():
    parser = argparse.ArgumentParser(description='Управление автозагрузкой Telegram PC Controller')
    parser.add_argument('--enable', action='store_true', help='Включить автозагрузку')
    parser.add_argument('--disable', action='store_true', help='Отключить автозагрузку')
    parser.add_argument('--status', action='store_true', help='Проверить статус')
    parser.add_argument('--toggle', action='store_true', help='Переключить автозагрузку')
    
    args = parser.parse_args()
    
    if args.enable:
        enable_autostart()
    elif args.disable:
        disable_autostart()
    elif args.status:
        check_status()
    elif args.toggle:
        if is_autostart_enabled():
            disable_autostart()
        else:
            enable_autostart()
    else:
        # Интерактивное меню
        print("🤖 Управление автозагрузкой Telegram PC Controller")
        print("=" * 50)
        
        current_status = check_status()
        print()
        
        if current_status:
            print("1. Отключить автозагрузку")
            print("2. Проверить статус")
            print("0. Выход")
            
            choice = input("\nВыберите действие (0-2): ").strip()
            
            if choice == "1":
                disable_autostart()
            elif choice == "2":
                check_status()
        else:
            print("1. Включить автозагрузку")
            print("2. Проверить статус") 
            print("0. Выход")
            
            choice = input("\nВыберите действие (0-2): ").strip()
            
            if choice == "1":
                enable_autostart()
            elif choice == "2":
                check_status()

if __name__ == "__main__":
    main()
