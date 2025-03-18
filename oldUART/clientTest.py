import asyncio
import websockets
import json

async def test_client():
    uri = "ws://172.16.15.68:5001"
    async with websockets.connect(uri) as websocket:
        # Sende 4 Zahlen als kommagetrennte Werte
        await websocket.send("100,150,200,250")
        response = await websocket.recv()
        data = json.loads(response)
        print("Empfangenes Array:", data)

asyncio.run(test_client())
