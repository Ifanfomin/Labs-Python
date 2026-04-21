### Задача 1

# Реализовать чат без графического интерфейса, который позволит обмениваться сообщениями только между клиентом и сервером. 
# Сервер (и клиент) помимо обычных сообщений от клиента (сервера) должен принимать специальные команды (зарезервированные слова), например:
# - на отключение сервера, при этом клиент также должен выключиться автоматически
# - перевод сервера в спящий режим на некоторое время

# Клиент и сервер можно запустить одновременно в различных окнах терминала

from typing import List, Tuple
import threading
import argparse
import socket
import shutil
import time
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--server-ip", default="127.0.0.1")
parser.add_argument("--client-ip", default="127.0.0.1")
parser.add_argument("--server-port", type=int, default=5000)
parser.add_argument("--client-port", type=int, default=5000)
parser.add_argument("--name", default="anon")
args = parser.parse_args()

SERVER_IP = args.server_ip
CLIENT_IP = args.client_ip
SERVER_PORT = args.server_port
CLIENT_PORT = args.client_port
USER_NAME = args.name
TERMINAL_SIZE = shutil.get_terminal_size()
CENTER_TEXT = "Ifanfomin chat"
TERMINAL_HEADER =  " " * int((TERMINAL_SIZE[0] - len(CENTER_TEXT)) / 2) + CENTER_TEXT

running = True
sleeping = False
chat_history: List[Tuple[str, str]] = []


def server():
    global running, sleeping
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((SERVER_IP, SERVER_PORT))
    sock.listen(10)

    print('Server is running')

    conn, addr = sock.accept()

    try:
        while True:
            data = conn.recv(1024)

            data = data.decode().split("||", 1)
            user, text = data if len(data) == 2 else ("", "/exit")

            if text == "/exit":
                print_message("SYSTEM", "Собеседник вышел из чата")
                print_message("SYSTEM", "Введите Enter для выхода")
                running = False
                break
            elif text.startswith("/sleep"):
                sleeping = True
                sleep_time = int(text.split()[1])
                print_message("SYSTEM", f"Собеседник собеседник отправил вас в сон на {sleep_time} секунд")
                time.sleep(sleep_time)
                sleeping = False
                print_message("SYSTEM", f"Вы вышли из сна")
            else:
                print_message(user, text)
    finally:
        conn.close()


def client():
    global running, sleeping
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((CLIENT_IP, CLIENT_PORT))
            break
        except ConnectionRefusedError:
            print("Подключение не удалось, пробую снова...")
            time.sleep(1)
    
    print_message("", "")

    while running:
        try:
            text = input()
            if sleeping:
                print_message("SYSTEM", f"Вы не можете отправлять сообщения пока спите")
            elif text == "/exit":
                    break
            elif text.startswith("/sleep"):
                sleep_time = text.split()[1]
                if sleep_time.isdecimal():
                    print_message("SYSTEM", f"Вы отправили собеседника в сон на {sleep_time} секунд")
                    sock.send(f"{USER_NAME}||{text}".encode())
                else:
                    print_message("SYSTEM", "Проверьте что правильно указали время сна (число). Например: '/sleep 5'")
            else:
                print_message(USER_NAME, text)
                sock.send(f"{USER_NAME}||{text}".encode())

        except (BrokenPipeError, ConnectionResetError):
            print("Соединение потеряно")
            break

    sock.close()


def print_message(user, message):
    if user != "" and message.strip() != "":
        chat_history.append((user, message))
        if len(chat_history) > TERMINAL_SIZE[1] - 2:
            chat_history.pop(0)
    
    sys.stdout.write("\033[2J\033[H")
    print(TERMINAL_HEADER)
    if len(chat_history) < TERMINAL_SIZE[1] - 2:
        sys.stdout.write("\n" * (TERMINAL_SIZE[1] - len(chat_history) - 2))

    for h_user, h_message in chat_history:
        print(h_user + ": " + h_message)
    print(">>> ", end = "")
    sys.stdout.flush()


sys.stdout.write("\033[?1049h")

try:
    server_thread = threading.Thread(target=server, daemon=True)
    client_thread = threading.Thread(target=client)

    server_thread.start()
    client_thread.start()

    client_thread.join()

finally:
    sys.stdout.write("\033[?1049l")