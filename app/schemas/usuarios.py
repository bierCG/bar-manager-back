from pydantic import ConfigDict
from app.schemas import Base

class CreateRequest(Base):
    nome: str
    usuario: str
    senha: str
    role: str

class CreateResponse(Base):
    id: int
    nome: str
    usuario: str

    model_config = ConfigDict(from_attributes=True)