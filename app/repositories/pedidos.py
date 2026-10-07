from sqlalchemy import update
from sqlalchemy.orm import Session
from app.database.models import Pedido

class PedidoRepository():
    def __init__(self, session: Session):
        self.session = session

    def get_pedido(self, pedido_id: int):
        return self.session.query(Pedido).filter(Pedido.id == pedido_id).first()

    def get_ultimos_pedidos(self, inicio, fim):
        pedidos = (
            self.session.query(Pedido)
                .filter(Pedido.criado_em.between(inicio, fim))
                .all()
        )
        return pedidos

    def get_bartender_ultimos_pedidos(self, usuario_id: int, inicio, fim):
        pedidos = (
            self.session.query(Pedido)
                .filter(
                    Pedido.vendedor_id == usuario_id,
                    Pedido.criado_em.between(inicio, fim)
                )
                .all()
        )
        return pedidos

    def create(self, dados: dict, usuario_id: int, status: str):
        pedido = Pedido(
            **dados,
            vendedor_id = usuario_id,
            status=status
        )

        self.session.add(pedido)
        self.session.commit()
        self.session.refresh(pedido)

        return pedido

    def update_status_pedido(self, pedido_id: int, status: str):
        stmt = (
            update(Pedido)
            .where(Pedido.id == pedido_id)
            .values(status = status)
            .returning(Pedido)
        )

        pedido = self.session.execute(stmt).scalar_one_or_none()
        self.session.commit()

        return pedido