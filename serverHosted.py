import asyncio
import websockets
import os

clients = {}

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
                *(c.send(message) for c in clients if c != ws)
            )

    finally:
        if ws in clients:
            name = clients[ws]
            del clients[ws]

            await asyncio.gather(
                *(c.send(f"* {name} left") for c in clients)
            )

PORT = int(os.environ.get("PORT", 8765))

async def main():
    async with websockets.serve(handler, "0.0.0.0", PORT):
        print(f"Server running on port {PORT}")
        await asyncio.Future()

asyncio.run(main())