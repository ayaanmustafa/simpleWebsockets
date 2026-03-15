import asyncio
import websockets
import sys

URI = "wss://simplewebsockets.onrender.com/ws"

async def send(ws):
    loop = asyncio.get_event_loop()

    while True:
        msg = await loop.run_in_executor(None, lambda: input("you: "))
        await ws.send(msg)

async def receive(ws, username):
    async for msg in ws:
        if not msg.startswith(username + ":"):
            # move to new clean line
            sys.stdout.write("\r")
            sys.stdout.flush()

            print(msg)

            # redraw prompt
            sys.stdout.write("you: ")
            sys.stdout.flush()

async def main():
    username = input("Enter username: ")

    async with websockets.connect(URI) as ws:
        await ws.send(username)

        await asyncio.gather(
            send(ws),
            receive(ws, username)
        )

asyncio.run(main())