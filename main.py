import os
import json
from typing import List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
import uvicorn

from database import engine, Base, get_db, SessionLocal
import models

# Cria as tabelas no Neon se ainda não existirem
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

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"Cliente conectado! Conexões ativas: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            print(f"Cliente desconectado. Conexões ativas: {len(self.active_connections)}")

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
    return {"status": "ok", "message": "API do Bar rodando com sucesso!"}

# --- ROTA POST PERMUTADA PARA O NEON ---
@app.post("/pedidos")
async def criar_pedido(pedido: PedidoCreate, db: Session = Depends(get_db)):
    # 1. Instancia o objeto para a tabela
    novo_pedido = models.Pedido(
        drink=pedido.drink,
        cliente_nome=pedido.cliente_nome,
        status="ABERTO"
    )

    # 2. Persiste no banco de dados
    db.add(novo_pedido)
    db.commit()
    db.refresh(novo_pedido)

    # 3. Prepara o dicionário para a transmissão WebSocket
    pedido_dict = {
        "id": novo_pedido.id,
        "drink": novo_pedido.drink,
        "cliente_nome": novo_pedido.cliente_nome,
        "status": novo_pedido.status
    }

    await manager.broadcast({
        "event": "NOVO_PEDIDO",
        "pedido": pedido_dict
    })

    return {
        "message": "Pedido criado com sucesso!",
        "pedido": pedido_dict
    }

# --- WEBSOCKET ATUALIZADO PARA CONSULTAR O NEON ---
@app.websocket("/ws/bar")
async def websocket_bar(websocket: WebSocket):
    await manager.connect(websocket)

    # Abre sessão do banco para carregar histórico inicial no socket
    db = SessionLocal()
    try:
        pedidos_db = db.query(models.Pedido).all()
        for pedido in pedidos_db:
            await websocket.send_json({
                "event": "NOVO_PEDIDO",
                "pedido": {
                    "id": pedido.id,
                    "drink": pedido.drink,
                    "cliente_nome": pedido.cliente_nome,
                    "status": pedido.status
                }
            })
    finally:
        db.close()

    try:
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)

            if payload.get("event") == "ATUALIZAR_STATUS":
                pedido_id = payload.get("pedido_id")
                novo_status = payload.get("status")

                # Atualiza no PostgreSQL (Neon)
                db_session = SessionLocal()
                try:
                    pedido = db_session.query(models.Pedido).filter(models.Pedido.id == pedido_id).first()
                    if pedido:
                        pedido.status = novo_status
                        db_session.commit()
                        db_session.refresh(pedido)

                        await manager.broadcast({
                            "event": "STATUS_ATUALIZADO",
                            "pedido": {
                                "id": pedido.id,
                                "drink": pedido.drink,
                                "cliente_nome": pedido.cliente_nome,
                                "status": pedido.status
                            }
                        })
                finally:
                    db_session.close()

    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"Erro no WebSocket: {e}")
        manager.disconnect(websocket)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)