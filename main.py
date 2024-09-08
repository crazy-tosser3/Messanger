import dearpygui.dearpygui as dpg  # Импорт библиотеки DearPyGui для создания графического интерфейса
import ctypes  # Импорт библиотеки ctypes для взаимодействия с системными вызовами Windows
import os  # Импорт модуля os для работы с файловой системой
from gui import GraphicalUserInterface  # Импорт всех функций и классов из модуля gui
from func import get_info   # Импорт всех функций и классов из модуля func

# Установка режима DPI-awareness для приложения на Windows (чтобы интерфейс корректно отображался на экранах с высокой плотностью пикселей)
ctypes.windll.shcore.SetProcessDpiAwareness(True)

# Определение пути к файлу настроек
SETTING_PATH = os.path.join("JSON", "setting.json")

# Загрузка настроек из файла
SETTING = get_info(SETTING_PATH)

# Извлечение настроек подключения (порт и хост) из загруженных настроек
connect = SETTING['Connect']
PORT = connect['Port']
HOST = connect['Host']
BYTE = connect['Bytes']
KEY = connect['Key']
# Определение пути к иконке приложения
ICON = os.path.join((os.path.join("sprites", "icons")), "icon.ico")

# Определение пути к шрифту и установка его размера
FONT = os.path.join("Font", "founder.otf")
FONT_SIZE = 14

big_let_start = 0x00C0  # Большая букава А кирилицы
big_let_end = 0x00DF  # Большая букава Я кирилицы
small_let_end = 0x00FF  # Маленькая букава я кирилицы
remap_big_let = 0x0410  # Начальное число для ремапинга кирилицы
alph_len = big_let_end - big_let_start + 1  # переход от больших букв к маленьким
alph_shift = remap_big_let - big_let_start  # от переназначенных до не-переназначенных

# Извлечение языка интерфейса из настроек
LANG = SETTING['LANG']
LANG_DICT = LANG['lang_dict']

# Создание экземпляра класса GraphicalUserInterface с параметрами языка, порта, хоста и настроек
GUI = GraphicalUserInterface(
    LANG , PORT , HOST ,
    SETTING_PATH , SETTING,BYTE , 
    KEY , LANG_DICT
    )

# Основная часть программы, выполняемая при запуске скрипта
if __name__ == '__main__':
    # Создание контекста DearPyGui
    dpg.create_context()

    # Регистрация шрифта в DearPyGui
with dpg.font_registry():
    with dpg.font(FONT, FONT_SIZE,tag="FONT") as default_font:
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
        biglet = remap_big_let  # Стартовое число для переназначения кирилицы
        for i1 in range(big_let_start, big_let_end + 1):  # Цикл захватывающий большие буквы из кириллици
            dpg.add_char_remap(i1, biglet)  # Переназначение больших букв кирилици
            dpg.add_char_remap(i1 + alph_len, biglet + alph_len)  # Переназначение маленьких букв
            biglet += 1  # Следующая буква

    # Привязка шрифта для использования в интерфейсе
    dpg.bind_font("FONT")

    # Создание основного окна приложения
    with dpg.window(tag="main window"):
        dpg.bind_font("FONT")  # Привязка шрифта к основному окну
        GUI.menu_bar()  # Добавление меню в окно
        GUI.main_menu()  # Добавление основного меню
        GUI.configurate()

    # Создание окна приложения с заданными параметрами (заголовок, размеры, иконка и возможность изменения размера)
    dpg.create_viewport(title='messenger', width=335, height=300, small_icon=ICON, large_icon=ICON, resizable=False)

    # Настройка DearPyGui
    dpg.setup_dearpygui()

    # Установка основного окна приложения
    dpg.set_primary_window("main window", True)

    # Отображение окна приложения
    dpg.show_viewport()

    # Запуск основного цикла обработки событий DearPyGui
    dpg.start_dearpygui()

    # Уничтожение контекста DearPyGui после завершения работы
    dpg.destroy_context()