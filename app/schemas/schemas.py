from pydantic import BaseModel, ConfigDict, EmailStr

class Base(BaseModel):
    pass

# ---------------------------------------------------------------------------------------
#
# ### AUTH ###
#
# ---------------------------------------------------------------------------------------

class TokenPayload(BaseModel):
    sub: int
    role: str

# ---------------------------------------------------------------------------------------
#
# ### LOGIN ###
#
# ---------------------------------------------------------------------------------------

class LoginCreate(Base):
    email: EmailStr
    senha: str

class LoginResponse(Base):
    username: str
    token: str

# ---------------------------------------------------------------------------------------
#
# ### USUÁRIOS ###
#
# ---------------------------------------------------------------------------------------

class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    role: str

class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: str

    model_config = ConfigDict(from_attributes=True)

# ---------------------------------------------------------------------------------------
#
# ### PEDIDOS ###
#
# ---------------------------------------------------------------------------------------

class PedidoCreate(Base):
    drink: str
    cliente_nome: str

class PedidoResponse(Base):
    id: int
    drink: str
    cliente_nome: str
    status: str

    model_config = ConfigDict(from_attributes=True)