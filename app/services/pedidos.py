from datetime import datetime, time, timedelta, date
from sqlalchemy.orm import Session

from app.schemas.schemas import PedidoCreate
from app.repositories.pedidos import PedidoRepository
from app.exceptions.exceptions import (
    PedidoNaoEncontrado,
    CancelamentoInvalido,
    PedidoNaoPodeSerFinalizado
)

class PedidosService():
    def __init__(self, session: Session):
        self.session = session
        self.repo = PedidoRepository(session)


    def _get_intervalo(self) -> dict:
        data = date.today()

        inicio = datetime.combine(data, time(7))
        fim = datetime.combine(data + timedelta(days=1), time(6))

        return inicio, fim


    def listar_ultimos_pedidos(self):
        inicio, fim = self._get_intervalo()
        return self.repo.get_ultimos_pedidos(inicio, fim)


    def listar_pedidos_bartender(self, user_id: int):
        inicio, fim = self._get_intervalo()
        return self.repo.get_bartender_ultimos_pedidos(user_id, inicio, fim)


    def criar_pedido(self, dados_pedido: PedidoCreate, usuario_id: int):
        dados = dados_pedido.model_dump(mode="json")
        status = "ABERTO"
        return self.repo.create(dados, usuario_id, status)


    def atualiza_status_pedido(self, pedido_id: int, status: str):
        return self.repo.update_status_pedido(pedido_id, status)


    def cancelar_pedido(self, pedido_id: int):
        pedido = self.repo.get_pedido(pedido_id)

        if not pedido:
            raise PedidoNaoEncontrado

        if pedido.status not in ["ABERTO", "PRONTO"]:
            raise CancelamentoInvalido

        return self.repo.update_status_pedido(pedido_id, "CANCELADO")


    def finalizar_pedido(self, pedido_id: int):
        pedido = self.repo.get_pedido(pedido_id)

        if not pedido:
            raise PedidoNaoEncontrado

        if not pedido.status == "ABERTO":
            raise PedidoNaoPodeSerFinalizado

        return self.repo.update_status_pedido(pedido_id, "PRONTO")

    def entregar_pedido(self, pedido_id: int):
        pedido = self.repo.get_pedido(pedido_id)

        if not pedido:
            raise PedidoNaoEncontrado

        if not pedido.status == "PRONTO":
            raise PedidoNaoPodeSerFinalizado

        return self.repo.update_status_pedido(pedido_id, "ENTREGUE")