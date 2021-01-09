import asyncio
import websockets


async def hello(websocket, path):
    r = await websocket.recv()
    print(r)
    await websocket.send("pong")


if __name__ == "__main__":
    start_server = websockets.serve(hello, "localhost", 5000)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
