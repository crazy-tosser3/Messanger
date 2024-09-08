import json  # Импорт модуля для работы с JSON
from tkinter.messagebox import showerror  # Импорт функции для отображения ошибок в графическом интерфейсе
import socket  # Импорт модуля для работы с сокетами
import threading  # Импорт модуля для работы с потоками
from cryptography.fernet import Fernet  # Импорт библиотеки для шифрования данных
import dearpygui.dearpygui as dpg  # Импорт библиотеки DearPyGui для создания графического интерфейса

# Глобальные переменные для сокета и шифрования
fernet = None
client_socket = None

# Декоратор для обработки ошибок в функциях
def Error(func):
    def wrap(*args, **kwargs):
        try:
            return func(*args, **kwargs)  # Выполняем функцию и возвращаем результат

        except ValueError:
            # Обработка ошибки, если введены неверные данные для порта или хоста
            showerror(title="Ошибка!", message="Убедитесь в том что вы правильно заполнили поля ПОРТ и ХОСТ!")
            client_socket.close()  # Закрытие сокета при ошибке

        except ConnectionRefusedError:
            # Обработка ошибки, если не удалось подключиться к серверу
            showerror(title="Ошибка!", message="Не удалось подключиться к серверу!")
            client_socket.close()  # Закрытие сокета при ошибке
        
        except FileNotFoundError as error:
            # Обработка ошибки при отсутствии указанного файла
            showerror(title="Ошибка!", message=f"Не удалось найти файл: {error}")

        except Exception as error:
            # Обработка всех остальных исключений
            showerror(title="Ошибка!", message=str(error))
            client_socket.close()  # Закрытие сокета при ошибке

    return wrap  # Возвращаем обертку функции

# Функция для получения информации из файла настроек
@Error
def get_info(path):
    with open(path, 'r', encoding='utf-8') as file:  # Открытие файла в режиме чтения
        return json.load(file)  # Возвращаем данные в формате JSON

# Функция для сохранения настроек в файл
def save_json(path, settings, p, h, b):
    with open(path, "w") as file:  # Открытие файла в режиме записи
        # Обновляем значения порта, хоста и размера пакетов в настройках
        settings["Connect"]["Port"] = p
        settings["Connect"]["Host"] = h
        settings["Connect"]["Bytes"] = b
        json.dump(settings, file, indent=4)  # Записываем обновленные настройки в файл

# Функция для обработки сообщений от сервера
@Error
def message_handler(byte, chat):
    global client_socket, fernet  # Используем глобальные переменные сокета и шифрования
    while True:
        # Получаем текущее значение чата и новое сообщение от сервера
        chat_box = dpg.get_value(chat)
        message = str(client_socket.recv(byte), encoding='utf-8')  # Получаем сообщение
        dec_message = fernet.decrypt(bytes(message, encoding='utf-8'))  # Расшифровываем сообщение
        print(f"Новое сообщение: {str(dec_message, encoding='utf-8')}")  # Выводим расшифрованное сообщение

        # Обновляем поле чата новым сообщением
        new_message = chat_box + str(dec_message, encoding='utf-8') + '\n'
        dpg.set_value(item=chat, value=new_message)

# Функция для отправки сообщения на сервер
@Error
def send_message(message):
    global client_socket  # Используем глобальную переменную сокета
    
    # Шифруем сообщение перед отправкой
    enc_message = fernet.encrypt(bytes(message, encoding='utf-8'))
    client_socket.send(enc_message)  # Отправляем зашифрованное сообщение

# Основная функция для подключения к серверу
@Error
def main(adress, byte, chat, key):
    global client_socket, fernet  # Используем глобальные переменные сокета и шифрования

    # Инициализируем шифрование с использованием ключа
    fernet = Fernet(key)

    # Создаем сокет и подключаемся к серверу
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(adress)

    print(f"Подключено к серверу: {adress}")  # Выводим сообщение о подключении
    dpg.set_value(item=chat, value=f"Подключено к серверу: {adress}\n")  # Обновляем поле чата

    # Создаем поток для получения сообщений от сервера
    recive_threading = threading.Thread(target=message_handler, args=(byte, chat,))
    recive_threading.start()  # Запуск потока
