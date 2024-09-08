import socket
import threading

# Параметры сервера
HOST = '0.0.0.0'  # Сервер принимает подключения на всех сетевых интерфейсах
PORT = 55000  # Порт, на котором сервер слушает входящие соединения

clients = []  # Список подключенных клиентов

# Обработка сообщений от клиента
def handle_client(client_socket):
    while True:
        try:
            # Получение сообщения от клиента
            message = client_socket.recv(2048).decode('utf-8')
            if message:
                print(f"Сообщение от клиента: {message}")
                # Отправка сообщения всем остальным клиентам
                broadcast(message, client_socket)
            else:
                # Если сообщение пустое, удаляем клиента из списка
                remove_client(client_socket)
                break
        except:
            # В случае ошибки продолжаем цикл, чтобы избежать зависаний
            continue

# Рассылка сообщения всем клиентам, кроме отправителя
def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                # Отправка сообщения каждому подключенному клиенту
                client.send(message.encode('utf-8'))
            except:
                # Если не удается отправить сообщение, удаляем клиента
                remove_client(client)

# Удаление клиента из списка подключений
def remove_client(client_socket):
    if client_socket in clients:
        clients.remove(client_socket)

# Основной цикл работы сервера
def main():
    # Создание сокета
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Привязка сокета к хосту и порту
    server.bind((HOST, PORT))
    # Прослушивание до 5 подключений в очереди
    server.listen(5)
    print(f"Сервер запущен на {HOST}:{PORT}")

    while True:
        # Принятие нового подключения
        client_socket, client_address = server.accept()
        print(f"Подключен клиент: {client_address}")
        # Добавление нового клиента в список
        clients.append(client_socket)
        
        # Создаем поток для обработки нового клиента
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

# Запуск сервера
if __name__ == '__main__':
    main()
