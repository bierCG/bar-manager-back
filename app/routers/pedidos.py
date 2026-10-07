from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.security.auth import requer_roles
from app.schemas.schemas import TokenPayload, PedidoCreate, PedidoResponse
from app.services.pedidos import PedidosService
from app.database.connection import get_db
from app.websocket.notify import notificar_cozinha, notificar_pedido, notificar_pv

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

def get_service(session: Session = Depends(get_db)) -> PedidosService:
    return PedidosService(session)

# ------------------------------------------------------------------------------------------
#
# ### GET ###
#
# ------------------------------------------------------------------------------------------

@router.get("/", response_model=list[PedidoResponse])
def listar_ultimos_pedidos(
    _usuario: TokenPayload = Depends(requer_roles('cozinha', 'pv')),
    service: PedidosService = Depends(get_service)
):
    return service.listar_ultimos_pedidos()

@router.get("/bartender", response_model=list[PedidoResponse])
def listar_pedidos_bartender(
    usuario: TokenPayload = Depends(requer_roles('bartender')),
    service: PedidosService = Depends(get_service),
):
    return service.listar_pedidos_bartender(usuario.sub)

# ------------------------------------------------------------------------------------------
#
# ### POST ###
#
# ------------------------------------------------------------------------------------------

@router.post("/", response_model=PedidoResponse)
async def criar_pedido(
    dados: PedidoCreate,
    usuario: TokenPayload = Depends(requer_roles('bartender')),
    service: PedidosService = Depends(get_service),
):
    pedido = service.criar_pedido(dados_pedido=dados, usuario_id=usuario.sub)

    response_ws = PedidoResponse.model_validate(pedido).model_dump(mode="json")

    await notificar_cozinha("pedido.created", response_ws)
    await notificar_pv("pedido.created", response_ws)

    return pedido

# ------------------------------------------------------------------------------------------
#
# ### PATCH ###
#
# ------------------------------------------------------------------------------------------

@router.patch("/{pedido_id}/cancel", status_code=200, response_model=PedidoResponse)
async def cancelar_pedido(
    pedido_id: int,
    _usuario: TokenPayload = Depends(requer_roles('cozinha')),
    service: PedidosService = Depends(get_service),
):
    pedido = service.cancelar_pedido(pedido_id)

    response_ws = PedidoResponse.model_validate(pedido).model_dump(mode="json")

    await notificar_pedido("pedido.updated", response_ws, pedido.vendedor_id)
    await notificar_cozinha("pedido.updated", response_ws)
    await notificar_pv("pedido.updated", response_ws)

    return pedido

@router.patch("/{pedido_id}/finish", status_code=200, response_model=PedidoResponse)
async def finalizar_pedido(
    pedido_id: int,
    _usuario: TokenPayload = Depends(requer_roles('cozinha')),
    service: PedidosService = Depends(get_service),
):
    pedido = service.finalizar_pedido(pedido_id)

    response_ws = PedidoResponse.model_validate(pedido).model_dump(mode="json")

    await notificar_pedido("pedido.updated", response_ws, pedido.vendedor_id)
    await notificar_cozinha("pedido.updated", response_ws)
    await notificar_pv("pedido.updated", response_ws)

    return pedido