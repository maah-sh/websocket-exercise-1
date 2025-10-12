import asyncio
import websockets

CONNECTIONS = set()

async def echo(websocket):
    if websocket not in CONNECTIONS:
        CONNECTIONS.add(websocket)
    async for message in websocket:
        await asyncio.gather(*[c.send(message) for c in CONNECTIONS if c != websocket])


async def main():
    async with websockets.serve(echo, 'localhost', 8765) as server:
        print('WebSocket server running at ws://127.0.0.1:8765')
        await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(main())




