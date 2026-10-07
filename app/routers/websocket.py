import json

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from app.core.logger import logger

from app.security.auth import autenticar_ws
from app.schemas.schemas import TokenPayload
from app.websocket.manager import manager

router = APIRouter(prefix="/ws", tags=["WebSocket"])

# ------------------------------------------------------------------------------------------
#
# ### POST ###
#
# ------------------------------------------------------------------------------------------

@router.websocket("/bar")
async def estabelecer_conexao(
    websocket: WebSocket,
    usuario: TokenPayload = Depends(autenticar_ws),
):
    await manager.connect(websocket, usuario)
        
    try:
        while True:
            mensagem = await websocket.receive_text()

            payload = json.loads(mensagem)

            if payload["event"] == "PING":
                await websocket.send_json({
                    "event": "PONG"
                })
                continue

    except WebSocketDisconnect as e:
        logger.info(f"WebSocket desconectado: {e}")
    finally:
        await manager.disconnect(websocket, usuario.sub, usuario.role)