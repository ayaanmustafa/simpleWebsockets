import asyncio
import os
import websockets

clients = {}  # websocket -> username


async def process_request(path, headers):
    # allows Render HTTP health checks
    if path == "/":
        return (200, [("Content-Type", "text/plain")], b"WebSocket chat server\n")


async def broadcast(message, sender=None):
    tasks = []
    for ws in clients:
        if ws != sender:
            tasks.append(ws.send(message))

    if tasks:
        await asyncio.gather(*tasks, return_exceptions=True)


async def handler(ws):
    username = await ws.recv()
    clients[ws] = username

    await broadcast(f"* {username} joined")

    try:
        async for msg in ws:

            if msg.lower() == "exit":
                break

            await broadcast(f"{username}: {msg}", sender=ws)

    finally:
        name = clients.pop(ws, None)

        if name:
            await broadcast(f"* {name} left")


PORT = int(os.environ.get("PORT", 8765))


async def main():
    async with websockets.serve(
        handler,
        "0.0.0.0",
        PORT,
        process_request=process_request
    ):
        print("Server running on port", PORT)
        await asyncio.Future()


asyncio.run(main())
