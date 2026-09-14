import os
import json
from typing import List, Dict
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="Sistema de Pedidos - API")

# 1. LIBERAÇÃO DE CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. MODELOS E BANCO EM MEMÓRIA
class PedidoCreate(BaseModel):
    cliente_id: str
    drink: str
    mesa: int

db_pedidos: List[Dict] = []


# 3. GERENCIADOR DE CONEXÕES WEBSOCKET
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"Cliente conectado! Total de conexões ativas: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            print(f"Cliente desconectado. Total de conexões ativas: {len(self.active_connections)}")

    async def broadcast(self, message: dict):
        """Transmite mensagens para todos os clientes conectados de forma segura."""
        for connection in list(self.active_connections):
            try:
                await connection.send_json(message)
            except Exception as e:
                print(f"Erro ao transmitir mensagem: {e}")
                self.disconnect(connection)

manager = ConnectionManager()


# 4. ENDPOINTS HTTP
@app.get("/")
async def health_check():
    return {"status": "ok", "message": "API do Bar rodando com sucesso!"}

@app.post("/pedidos")
async def criar_pedido(pedido: PedidoCreate):
    novo_pedido = {
        "id": len(db_pedidos) + 1,
        "cliente_id": pedido.cliente_id,
        "drink": pedido.drink,
        "mesa": int(pedido.mesa),
        "status": "PENDENTE"
    }
    
    db_pedidos.append(novo_pedido)

    # Notifica todas as telas conectadas
    await manager.broadcast({
        "event": "NOVO_PEDIDO",
        "pedido": novo_pedido
    })

    return {"message": "Pedido criado com sucesso!", "pedido": novo_pedido}


# 5. ENDPOINT WEBSOCKET
@app.websocket("/ws/bar")
async def websocket_bar(websocket: WebSocket):
    await manager.connect(websocket)
    
    # Envia os pedidos já existentes para a tela que acabou de conectar
    for p in db_pedidos:
        await websocket.send_json({
            "event": "NOVO_PEDIDO",
            "pedido": p
        })

    try:
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)

            if payload.get("event") == "ATUALIZAR_STATUS":
                pedido_id = payload.get("pedido_id")
                novo_status = payload.get("status")

                for p in db_pedidos:
                    if p["id"] == pedido_id:
                        p["status"] = novo_status
                        
                        await manager.broadcast({
                            "event": "STATUS_ATUALIZADO",
                            "pedido": p
                        })
                        break

    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"Erro inesperado na conexão WebSocket: {e}")
        manager.disconnect(websocket)


# 6. INICIALIZAÇÃO PARA AMBIENTES DE NUVEM (RENDER)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)