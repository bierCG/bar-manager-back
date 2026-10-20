from sqlalchemy import update
from sqlalchemy.orm import Session
from app.core.database.models import Pedido

class PedidoRepository():
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, pedido_id: int):
        return (
            self.session.query(Pedido)
            .filter(
                Pedido.id == pedido_id
            )
            .first()
        )

    def get_ultimos_pedidos(self, inicio, fim):
        return (
            self.session.query(Pedido)
                .filter(Pedido.criado_em.between(inicio, fim))
                .all()
        )

    def get_bartender_ultimos_pedidos(self, usuario_id: int, inicio, fim):
        return (
            self.session.query(Pedido)
                .filter(
                    Pedido.usuario_id == usuario_id,
                    Pedido.criado_em.between(inicio, fim)
                )
                .all()
        )

    def create(self, pedido: Pedido) -> Pedido:
        self.session.add(pedido)
        self.session.commit()
        self.session.refresh(pedido)
        return pedido

    def update(self, pedido: Pedido):
        self.session.commit()
        self.session.refresh(pedido)
        return pedido