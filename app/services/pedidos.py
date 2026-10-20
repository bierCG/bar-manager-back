from datetime import datetime, time, timedelta, date
from sqlalchemy.orm import Session

from app.core.database.models import Pedido
from app.schemas.pedidos import CreateRequest
from app.repositories.pedidos import PedidoRepository
from app.core.exceptions.exceptions import (
    PedidoNaoEncontrado,
    CancelamentoInvalido,
    PedidoNaoPodeSerFinalizado
)

class PedidosService():
    def __init__(self, session: Session):
        self.repo = PedidoRepository(session)

    def _get_intervalo(self) -> dict:
        data = date.today()

        inicio = datetime.combine(data, time(7))
        fim = datetime.combine(data + timedelta(days=1), time(6))

        return inicio, fim

    def criar_pedido(self, dados: CreateRequest, usuario_id: int) -> Pedido:
        pedido = Pedido(
            **dados.model_dump(),
            status="ABERTO",
            usuario_id=usuario_id
        )
        return self.repo.create(pedido)

    def atualiza_status_pedido(self, pedido_id: int, status: str) -> Pedido:
        pedido = self.repo.get_by_id(pedido_id)
        if not pedido:
            raise PedidoNaoEncontrado()
        
        if status == "PRONTO":
            if not pedido.status == "ABERTO":
                raise PedidoNaoPodeSerFinalizado

        if status == "ENTREGUE":
            if not pedido.status == "PRONTO":
                raise PedidoNaoPodeSerFinalizado

        pedido.status = status
        
        return self.repo.update(pedido)

    def listar_ultimos_pedidos(self):
        inicio, fim = self._get_intervalo()
        return self.repo.get_ultimos_pedidos(inicio, fim)

    def listar_pedidos_bartender(self, usuario_id: int):
        inicio, fim = self._get_intervalo()
        return self.repo.get_bartender_ultimos_pedidos(usuario_id, inicio, fim)