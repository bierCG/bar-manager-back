from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base

class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    cliente_nome = Column(String(30), nullable=False)
    drink = Column(String(50), nullable=False)    
    status = Column(String(30), nullable=False)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())