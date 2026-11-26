import os
from pathlib import Path

def launch_by_name(app_name):
    # Папки, где Windows хранит все ярлыки меню "Пуск"
    start_menu_dirs = [
        Path(os.environ["PROGRAMDATA"]) / "Microsoft/Windows/Start Menu/Programs",
        Path(os.environ["APPDATA"]) / "Microsoft/Windows/Start Menu/Programs",
    ]
    
    app_name = app_name.lower()
    
    for folder in start_menu_dirs:
        # Ищем все ярлыки (.lnk) во всех подпапках
        for shortcut in folder.rglob("*.lnk"):
            if app_name in shortcut.stem.lower():
                print(f"Запускаю: {shortcut.stem}")
                os.startfile(shortcut)
                return True
                
    print(f"Программа '{app_name}' не найдена в меню Пуск.")
    return False

# Примеры использования (достаточно части названия):
launch_by_name("discord")

