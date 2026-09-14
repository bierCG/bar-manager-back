import json
from typing import List, Dict
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Libera o acesso para qualquer origem (ótimo para desenvolvimento)
    allow_credentials=True,
    allow_methods=["*"],  # Libera todos os métodos (GET, POST, etc)
    allow_headers=["*"],  # Libera todos os cabeçalhos
)

# 1. MODELOS DE DADOS
# O Pydantic valida automaticamente o JSON que chega na requisição HTTP
class PedidoCreate(BaseModel):
    cliente_id: str
    drink: str
    mesa: int

# Banco de dados temporário em memória (para aprendizado)
db_pedidos: List[Dict] = []


# 2. GERENCIADOR DE CONEXÕES WEBSOCKET
class ConnectionManager:
    def __init__(self):
        # Lista para guardar todas as telas/dispositivos conectados
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print("Novo cliente conectado via WebSocket!")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            print("Cliente desconectado do WebSocket.")

    async def broadcast(self, message: dict):
        """Envia uma mensagem em JSON para TODOS os conectados."""
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()


# 3. ENDPOINT HTTP: Criar Pedido
@app.post("/pedidos")
async def criar_pedido(pedido: PedidoCreate):
    # Montamos o objeto do novo pedido
    novo_pedido = {
        "id": len(db_pedidos) + 1,  # Gera um ID simples (1, 2, 3...)
        "cliente_id": pedido.cliente_id,
        "drink": pedido.drink,
        "mesa": pedido.mesa,
        "status": "PENDENTE"
    }
    
    # Salva na memória
    db_pedidos.append(novo_pedido)

    # AVISO INSTANTÂNEO: Transmite o novo pedido para todos via WebSocket
    await manager.broadcast({
        "event": "NOVO_PEDIDO",
        "pedido": novo_pedido
    })

    return {"message": "Pedido criado com sucesso!", "pedido": novo_pedido}


# 4. ENDPOINT WEBSOCKET: Conexão e Atualizações
@app.websocket("/ws/bar")
async def websocket_bar(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Fica escutando mensagens enviadas pelo Flutter através do WebSocket
            data = await websocket.receive_text()
            payload = json.loads(data) # Transforma o texto recebido em Dicionário

            # Se o Flutter enviar um comando de atualizar status:
            if payload.get("event") == "ATUALIZAR_STATUS":
                pedido_id = payload.get("pedido_id")
                novo_status = payload.get("status")

                # Procura o pedido pelo ID e atualiza
                for p in db_pedidos:
                    if p["id"] == pedido_id:
                        p["status"] = novo_status
                        
                        # Avisa todo mundo conectado que o status mudou
                        await manager.broadcast({
                            "event": "STATUS_ATUALIZADO",
                            "pedido": p
                        })
                        break

    except WebSocketDisconnect:
        manager.disconnect(websocket)