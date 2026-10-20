from pydantic import ConfigDict
from enum import Enum
from app.schemas import Base

class StatusPedido(str, Enum):
    ABERTO = "ABERTO"
    PRONTO = "PRONTO"
    ENTREGUE = "ENTREGUE"

class CreateRequest(Base):
    drink: str
    cliente_nome: str

class CreateResponse(Base):
    id: int
    drink: str
    cliente_nome: str
    status: str

    model_config = ConfigDict(from_attributes=True)

class UpdateStatusRequest(Base):
    status: StatusPedido

class UpdateStatusResponse(Base):
    id: int
    status: StatusPedido
    drink: str
    cliente_nome: str

    model_config = ConfigDict(from_attributes=True)

class ReadResponse(Base):
    id: int
    drink: str
    cliente_nome: str
    status: str

    model_config = ConfigDict(from_attributes=True)