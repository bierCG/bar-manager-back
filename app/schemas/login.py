from app.schemas import Base

class LoginRequest(Base):
    usuario: str
    senha: str

class LoginResponse(Base):
    token: str