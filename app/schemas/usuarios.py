from enum import Enum
from pydantic import ConfigDict

from app.schemas import Base

class UserRole(str, Enum):
    COZINHA = "COZINHA"
    EXPOSITOR = "EXPOSITOR"
    BARTENDER = "BARTENDER"
    ADMIN = "ADMIN"

class CadastroUsuarioRequest(Base):
    nome: str
    usuario: str
    senha: str
    role: UserRole

class CadastroUsuarioResponse(Base):
    id: int
    nome: str
    usuario: str

    model_config = ConfigDict(from_attributes=True)