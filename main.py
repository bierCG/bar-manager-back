import os
import json
from typing import List, Dict

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema de Pedidos - API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PedidoCreate(BaseModel):
    drink: str
    cliente_nome: str


db_pedidos: List[Dict] = []


class ConnectionManager:

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

        print(
            f"Cliente conectado! "
            f"Total de conexões ativas: {len(self.active_connections)}"
        )

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

            print(
                f"Cliente desconectado. "
                f"Total de conexões ativas: {len(self.active_connections)}"
            )

    async def broadcast(self, message: dict):
        for connection in list(self.active_connections):
            try:
                await connection.send_json(message)

            except Exception as e:
                print(f"Erro ao transmitir mensagem: {e}")
                self.disconnect(connection)


manager = ConnectionManager()


@app.get("/")
async def health_check():
    return {
        "status": "ok",
        "message": "API do Bar rodando com sucesso!"
    }


@app.post("/pedidos")
async def criar_pedido(pedido: PedidoCreate):

    novo_pedido = {
        "id": len(db_pedidos) + 1,
        "drink": pedido.drink,
        "cliente_nome": pedido.cliente_nome,
        "status": "ABERTO"
    }

    db_pedidos.append(novo_pedido)

    await manager.broadcast({
        "event": "NOVO_PEDIDO",
        "pedido": novo_pedido
    })

    return {
        "message": "Pedido criado com sucesso!",
        "pedido": novo_pedido
    }


@app.websocket("/ws/bar")
async def websocket_bar(websocket: WebSocket):

    await manager.connect(websocket)

    # Envia os pedidos existentes para quem acabou de conectar
    for pedido in db_pedidos:

        await websocket.send_json({
            "event": "NOVO_PEDIDO",
            "pedido": pedido
        })

    try:

        while True:

            data = await websocket.receive_text()

            payload = json.loads(data)

            if payload.get("event") == "ATUALIZAR_STATUS":

                pedido_id = payload.get("pedido_id")
                novo_status = payload.get("status")

                for pedido in db_pedidos:

                    if pedido["id"] == pedido_id:

                        pedido["status"] = novo_status

                        await manager.broadcast({
                            "event": "STATUS_ATUALIZADO",
                            "pedido": pedido
                        })

                        break

    except WebSocketDisconnect:

        manager.disconnect(websocket)

    except Exception as e:

        print(f"Erro inesperado na conexão WebSocket: {e}")
        manager.disconnect(websocket)


# INICIALIZAÇÃO PARA AMBIENTES DE NUVEM (RENDER)

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 8000))

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False
    )