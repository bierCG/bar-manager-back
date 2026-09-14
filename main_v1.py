from fastapi import FastAPI, WebSocket

app = FastAPI()

@app.get('/')
def hello_world():
    return {'mssage':'Hello Fucking World'}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Cliente conectado!")
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Recebido do Flutter: {data}")

            await websocket.send_text(f"Servidor recebeu: {data}")
    except:
        print("Cliente desconectou")