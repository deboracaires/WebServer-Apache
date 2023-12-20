import asyncio
import websockets

async def chat_server(websocket, path):
    async for message in websocket:
        await websocket.send(f"Received: {message}")

if __name__ == "__main__":
    start_server = websockets.serve(chat_server, "localhost", 8765)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
