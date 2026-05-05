import asyncio
from asyncio import StreamReader, StreamWriter

clients: set[StreamWriter] = set()

async def broadcast(message: str, clients: set[StreamWriter], sender: StreamWriter | None = None):
    for client in clients:
        if client != sender:
            client.write((message).encode())
            await client.drain()

async def handle_client(reader: StreamReader, writer: StreamWriter):
    addr = writer.get_extra_info('peername')
    print(f"Подключен: {addr}")

    clients.add(writer)

    try:
        while True:
            data = await reader.read(1024)

            if not data:
                break

            user, message = data.decode().strip().split(": ", 1)

            if message == "/hello":
                await broadcast(f"К чату присоединился {user}", clients, writer)

            elif message == "/exit":
                await broadcast(f"Из чата вышел {user}", clients)
                break
            else:
                await broadcast(f"{user}: {message}", clients, writer)

    finally:
        print(f"Отключен: {addr}")
        clients.remove(writer)
        writer.close()
        await writer.wait_closed()


async def main():
    server = await asyncio.start_server(handle_client, "127.0.0.1", 5000)

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())