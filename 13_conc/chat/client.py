from typing import List, Tuple
import asyncio
from asyncio import StreamReader, StreamWriter
import argparse
import shutil
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--server-ip", default="127.0.0.1")
parser.add_argument("--server-port", type=int, default=5000)
parser.add_argument("--name", default="anon")
args = parser.parse_args()

SERVER_IP = args.server_ip
SERVER_PORT = args.server_port
USER_NAME = args.name

TERMINAL_SIZE = shutil.get_terminal_size()
CENTER_TEXT = "Ifanfomin Async Chat"
TERMINAL_HEADER = " " * int((TERMINAL_SIZE[0] - len(CENTER_TEXT)) / 2) + CENTER_TEXT

chat_history: List[Tuple[str, str]] = []
running = True


def print_message(user: str, message: str):
    if user != "" and message.strip() != "":
        chat_history.append((user, message))
        if len(chat_history) > TERMINAL_SIZE[1] - 2:
            chat_history.pop(0)

    sys.stdout.write("\033[2J\033[H")
    print(TERMINAL_HEADER)

    if len(chat_history) < TERMINAL_SIZE[1] - 2:
        sys.stdout.write("\n" * (TERMINAL_SIZE[1] - len(chat_history) - 2))

    for h_user, h_message in chat_history:
        print(f"{h_user}: {h_message}")

    print(">>> ", end="")
    sys.stdout.flush()


async def send_messages(writer: StreamWriter):
    global running

    template = "{0}: {1}"

    writer.write(template.format(USER_NAME, "/hello").encode())
    await writer.drain()

    while running:
        message = await asyncio.to_thread(input)

        if message == "/exit":
            writer.write(template.format(USER_NAME, message).encode())
            await writer.drain()
            running = False
            break

        print_message(USER_NAME, message)

        writer.write(template.format(USER_NAME, message).encode())
        await writer.drain()


async def receive_messages(reader: StreamReader):
    global running

    while running:
        data = await reader.read(1024)

        if not data:
            running = False
            break

        decoded = data.decode()

        if ": " in decoded:
            user, msg = decoded.split(": ", 1)
        else:
            user, msg = "SYSTEM", decoded

        print_message(user, msg)


async def main():
    global running

    try:
        reader, writer = await asyncio.open_connection(SERVER_IP, SERVER_PORT)
    except ConnectionRefusedError:
        print("Не удалось подключиться к серверу")
        return

    print_message("", "")

    await asyncio.gather(
        send_messages(writer),
        receive_messages(reader)
    )

    writer.close()
    await writer.wait_closed()


sys.stdout.write("\033[?1049h")

try:
    asyncio.run(main())
finally:
    sys.stdout.write("\033[?1049l")