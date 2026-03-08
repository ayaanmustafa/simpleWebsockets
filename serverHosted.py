import asyncio
import websockets
import os

clients = {}

async def process_request(path, headers):
    return (200, [], b"Chat server running\n")

async def handler(ws):
    username = await ws.recv()
    clients[ws] = username

    try:
        async for msg in ws:

            if msg.lower() == "exit":
                await ws.close()
                break

            message = f"{username}: {msg}"

            await asyncio.gather(
                *(c.send(message) for c in clients if c != ws),
                return_exceptions=True
            )

    finally:
        if ws in clients:
            name = clients.pop(ws)

            await asyncio.gather(
                *(c.send(f"* {name} left") for c in clients),
                return_exceptions=True
            )

PORT = int(os.environ.get("PORT", 8765))

async def main():
    async with websockets.serve(
        handler,
        "0.0.0.0",
        PORT,
        process_request=process_request
    ):
        print(f"Server running on port {PORT}")
        await asyncio.Future()

asyncio.run(main())
