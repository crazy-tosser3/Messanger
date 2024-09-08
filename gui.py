import dearpygui.dearpygui as dpg  # Импорт библиотеки DearPyGui для создания графического интерфейса
from func import *  # Импорт всех функций из модуля func
from cryptography.fernet import Fernet  # Импорт библиотеки для шифрования данных
import pyperclip  # Импорт библиотеки для работы с буфером обмена

chat = None  # Переменная для хранения окна чата

# Класс, представляющий графический интерфейс пользователя
class GraphicalUserInterface:
    def __init__(self, lang, port, host, path_setting, setting, byte, key, lang_dict):
        # Инициализация переменных класса
        self.language = lang  # Словарь с текстами на разных языках
        self.port = port  # Порт для подключения
        self.host = host  # Хост для подключения
        self.path_sett = path_setting  # Путь к файлу настроек
        self.setting = setting  # Настройки приложения
        self.bytes = byte  # Размер передаваемой информации в байтах
        self.key = key  # Ключ для шифрования/дешифрования сообщений
        self.lang_dict = lang_dict  # Список поддерживаемых языков

    # Метод для переключения языка интерфейса
    def switch_lang(self):
        language = dpg.get_value("lang sw")  # Получение текущего языка
        if language in self.language:
            labels = self.language[language]  # Получение текстовых меток для выбранного языка
            dpg.configure_item('message input', hint=labels[0])
            dpg.configure_item('send', label=labels[1])
            dpg.configure_item('connect', label=labels[2])
            dpg.configure_item('connections', label=labels[3])
            dpg.configure_item('host', hint=labels[4])
            dpg.configure_item('port', hint=labels[5])
            dpg.configure_item('bytes', hint=labels[6])
            dpg.configure_item('lang', label=labels[7])
            dpg.configure_item("socket", label=labels[8])
            dpg.configure_item("key", hint=labels[9])
            dpg.configure_item(item='get key', label=labels[11])
            dpg.configure_item(item='gen', label=labels[12])

    # Метод для создания главного меню интерфейса
    def main_menu(self):
        global chat
        with dpg.group(horizontal=False):  # Создание вертикальной группы элементов
            # Поле для отображения сообщений (только для чтения)
            chat = dpg.add_input_text(width=298, height=110, multiline=True, readonly=True, tag="Chat")
            # Поле для ввода сообщения пользователем
            dpg.add_input_text(width=298, height=30, hint="Write anything:", tag="message input")

            # Создание горизонтальной группы для кнопок "SEND" и "CONNECT"
            with dpg.group(horizontal=True):
                # Кнопка отправки сообщения с вызовом метода send_callback
                dpg.add_button(label="SEND", width=147, height=40, tag='send', callback=lambda: self.send_callback())
                # Кнопка для подключения с вызовом метода connect
                dpg.add_button(label="CONNECT", width=143, height=40, tag='connect', callback=lambda: self.connect())

    # Метод для генерации нового ключа шифрования и копирования его в буфер обмена
    def get_key(self):
        key = Fernet.generate_key()  # Генерация ключа шифрования
        dpg.set_value(item='key', value=str(key, encoding='utf-8'))  # Установка значения ключа в поле интерфейса
        pyperclip.copy(str(key, encoding='utf-8'))  # Копирование ключа в буфер обмена

    # Метод для создания меню в верхней части окна
    def menu_bar(self):
        with dpg.menu_bar():  # Создание строки меню
            with dpg.menu(label="Socket", tag='socket'):  # Меню "Socket"
                # Подменю "Connections" для ввода данных подключения
                with dpg.menu(label="Connections", tag='connections'):
                    with dpg.group(horizontal=False):
                        # Поле ввода для хоста
                        dpg.add_input_text(hint="HOST:", tag='host', default_value='')
                        # Поле ввода для порта
                        dpg.add_input_text(hint="PORT:", tag='port', default_value='')
                        # Поле ввода для количества байтов
                        dpg.add_input_text(hint="BYTES:", tag='bytes', default_value='')
                        # Поле ввода для секретного ключа
                        dpg.add_input_text(hint="Secret Key: ", tag='key')

            # Меню для выбора языка интерфейса
            with dpg.menu(label="Language", tag='lang'):
                # Выбор языка с переключением через callback на switch_lang
                dpg.add_combo(items=self.lang_dict, default_value=self.lang_dict[0], tag='lang sw', callback=lambda: self.switch_lang())

            # Меню для генерации нового ключа шифрования
            with dpg.menu(label="Get Key", tag='get key'):
                dpg.add_button(label="Generate Key", tag='gen', callback=lambda: self.get_key())

    # Метод для подключения по указанным параметрам (хост, порт, байты, ключ)
    def connect(self):
        global chat
        # Получение значений порта, хоста, количества байтов и ключа из полей ввода
        p = int(dpg.get_value('port'))
        h = dpg.get_value('host')
        b = int(dpg.get_value('bytes'))
        k = bytes(dpg.get_value('key'), encoding='utf-8')
        # Сохранение настроек подключения в файл
        save_json(self.path_sett, self.setting, p, h, b)
        # Подключение к серверу с указанными параметрами
        main(adress=(h, p), byte=b, key=k, chat=chat)

    # Метод для отправки сообщения
    def send_callback(self):
        language = dpg.get_value('lang sw')  # Получение текущего языка
        if language in self.language:
            labels = self.language[language]  # Получение текстовых меток для выбранного языка
            message = dpg.get_value('message input')  # Получение введенного сообщения
            send_message(message=message)  # Отправка сообщения
            dpg.configure_item('message input', default_value='')  # Очистка поля ввода после отправки
            chat_box = dpg.get_value(chat)  # Получение текущего содержимого чата
            new_chat_box = chat_box + f"[{labels[10]}]: {message}" + '\n'  # Формирование нового сообщения в чате
            dpg.set_value(item=chat, value=new_chat_box)  # Обновление поля чата с новым сообщением

    # Метод для конфигурации интерфейса с установкой значений по умолчанию для хоста, порта, количества байтов и ключа
    def configurate(self):
        dpg.configure_item(item='host', default_value=self.host)  # Установка хоста по умолчанию
        dpg.configure_item(item='port', default_value=self.port)  # Установка порта по умолчанию
        dpg.configure_item(item='bytes', default_value=self.bytes)  # Установка значения байтов по умолчанию
        dpg.configure_item(item='key', default_value=self.key)  # Установка ключа по умолчанию
