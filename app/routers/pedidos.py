from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security.auth import requer_roles
from app.schemas.auth import Auth
from app.schemas.pedidos import (
    CreateRequest,
    CreateResponse,
    UpdateStatusRequest,
    UpdateStatusResponse,
    ReadResponse
)
from app.services.pedidos import PedidosService
from app.core.database.connection import get_db
from app.websocket.notify import notificar_cozinha, notificar_pedido, notificar_expositor

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

def get_service(session: Session = Depends(get_db)) -> PedidosService:
    return PedidosService(session)

# ------------------------------------------------------------------------------------------
#
# ### GET ###
#
# ------------------------------------------------------------------------------------------

@router.get(
    "/",
    dependencies=[Depends(requer_roles('COZINHA', 'EXPOSITOR'))],
    response_model=list[ReadResponse])
def listar_ultimos_pedidos(
    service: PedidosService = Depends(get_service)
):
    return service.listar_ultimos_pedidos()

@router.get(
    "/bartender",
    response_model=list[ReadResponse]
)
def listar_pedidos_bartender(
    userAuth: Auth = Depends(requer_roles('BARTENDER')),
    service: PedidosService = Depends(get_service),
):
    return service.listar_pedidos_bartender(userAuth.sub)

# ------------------------------------------------------------------------------------------
#
# ### POST ###
#
# ------------------------------------------------------------------------------------------

@router.post("/", response_model=CreateResponse)
async def criar_pedido(
    dados_pedido: CreateRequest,
    userAuth: Auth = Depends(requer_roles('BARTENDER')),
    service: PedidosService = Depends(get_service),
):
    pedido = service.criar_pedido(dados_pedido, userAuth.sub)

    response_ws = CreateResponse.model_validate(pedido).model_dump(mode="json")

    await notificar_cozinha("pedido.created", response_ws)
    await notificar_expositor("pedido.created", response_ws)

    return pedido

# ------------------------------------------------------------------------------------------
#
# ### PATCH ###
#
# ------------------------------------------------------------------------------------------

@router.patch(
    "/{pedido_id}/status",
    dependencies=[Depends(requer_roles('COZINHA'))],
    response_model=UpdateStatusResponse
)
async def atualizar_status_pedido(
    pedido_id: int,
    dados: UpdateStatusRequest,
    service: PedidosService = Depends(get_service)
):
    pedido = service.atualiza_status_pedido(pedido_id, dados.status)
    
    response_ws = UpdateStatusResponse.model_validate(pedido).model_dump(mode="json")

    await notificar_pedido("pedido.updated", response_ws, pedido.usuario_id)
    await notificar_cozinha("pedido.updated", response_ws)
    await notificar_expositor("pedido.updated", response_ws)

    return pedido