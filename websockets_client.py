import asyncio
import json
import websockets


async def send_message(websocket, client_name):
    asyncio_loop = asyncio.get_running_loop()
    message_text = await asyncio_loop.run_in_executor(None, input, '')
    message = {'client': client_name, 'text': message_text}
    await websocket.send(json.dumps(message))


async def receive_message(websocket):
    message = await websocket.recv()
    message_parsed = json.loads(message)
    print(message_parsed['client'] +': ' + message_parsed['text'])


async def handle_messages(websocket, client_name):
    async def send_loop():
        while True:
            await send_message(websocket, client_name)

    async def receive_loop():
        while True:
            await receive_message(websocket)

    await asyncio.gather(send_loop(), receive_loop())

async def main():
    client_name = input('Enter your name: ')
    async with websockets.connect('ws://localhost:8765') as websocket:
        print('Chat started: ')
        await handle_messages(websocket, client_name)


if __name__ == "__main__":
    asyncio.run(main())