from typing import List, Tuple
import threading
import argparse
import socket
import time
import curses
import locale

locale.setlocale(locale.LC_ALL, '')

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

running = True
sleeping = False
chat_history: List[Tuple[str, str]] = []
input_buffer = ""
lock = threading.Lock()


def add_message(user, msg):
    with lock:
        chat_history.append((user, msg))
        if len(chat_history) > 200:
            chat_history.pop(0)


def server():
    global running, sleeping

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((SERVER_IP, SERVER_PORT))
    sock.listen(1)

    conn, _ = sock.accept()

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break

            user, text = data.decode().split("||", 1)

            if text == "/exit":
                add_message("SYSTEM", "Собеседник вышел из чата")
                running = False
                break

            elif text.startswith("/sleep"):
                sleeping = True
                t = int(text.split()[1])
                add_message("SYSTEM", f"Вас усыпили на {t} сек")
                time.sleep(t)
                sleeping = False
                add_message("SYSTEM", "Вы проснулись")

            else:
                add_message(user, text)

    finally:
        conn.close()


def client(stdscr):
    global running, sleeping, input_buffer

    # подключение
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((CLIENT_IP, CLIENT_PORT))
            break
        except ConnectionRefusedError:
            time.sleep(1)

    stdscr.nodelay(True)
    curses.curs_set(1)

    while running:
        draw(stdscr)

        try:
            key = stdscr.get_wch()
        except curses.error:
            time.sleep(0.05)
            continue

        # Enter
        if key in ("\n", "\r"):
            text = input_buffer

            if sleeping:
                add_message("SYSTEM", "Вы спите")

            elif text == "/exit":
                sock.send(f"{USER_NAME}||{text}".encode())
                running = False

            elif text.startswith("/sleep"):
                parts = text.split()
                if len(parts) == 2 and parts[1].isdigit():
                    add_message("SYSTEM", f"Вы усыпили на {parts[1]} сек")
                    sock.send(f"{USER_NAME}||{text}".encode())
                else:
                    add_message("SYSTEM", "Ошибка команды")

            else:
                add_message(USER_NAME, text)
                sock.send(f"{USER_NAME}||{text}".encode())

            input_buffer = ""

        # Backspace
        elif key in (curses.KEY_BACKSPACE, '\b', '\x7f'):
            input_buffer = input_buffer[:-1]

        # Обычные символы (включая кириллицу)
        elif isinstance(key, str):
            input_buffer += key

    sock.close()


def draw(stdscr):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    # заголовок
    title = "Ifanfomin chat"
    stdscr.addstr(0, max(0, (w - len(title)) // 2), title)

    max_messages = h - 2
    visible = chat_history[-max_messages:]

    # сообщения снизу вверх
    for i, (u, m) in enumerate(reversed(visible)):
        y = h - 2 - i
        if y <= 0:
            break

        line = f"{u}: {m}"[:w - 1]
        try:
            stdscr.addstr(y, 0, line)
        except:
            pass

    # строка ввода
    prompt = ">>> " + input_buffer
    stdscr.addstr(h - 1, 0, prompt[:w - 1])

    stdscr.refresh()


def main(stdscr):
    server_thread = threading.Thread(target=server, daemon=True)
    client_thread = threading.Thread(target=client, args=(stdscr,))

    server_thread.start()
    client_thread.start()

    client_thread.join()


if __name__ == "__main__":
    curses.wrapper(main)