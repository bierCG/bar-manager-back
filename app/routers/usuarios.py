from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.schemas import TokenPayload, UsuarioCreate, UsuarioResponse
from app.services.usuarios import UsuarioService
from app.security.auth import requer_roles
from app.database.connection import get_db

router = APIRouter(prefix="/usuarios", tags=["Usuários"])

def get_service(session: Session = Depends(get_db)) -> UsuarioService:
    return UsuarioService(session)

# ------------------------------------------------------------------------------------------
#
# ### GET ###
#
# ------------------------------------------------------------------------------------------

@router.get("/",  response_model=list[UsuarioResponse])
def listar_usuarios(
    _usuario: TokenPayload = Depends(requer_roles('admin')),
    service: UsuarioService = Depends(get_service)
):
    return service.listar_usuarios()

# ------------------------------------------------------------------------------------------
#
# ### POST ###
#
# ------------------------------------------------------------------------------------------

@router.post("/", response_model=UsuarioResponse)
def criar_usuario(
    dados: UsuarioCreate,
    _usuario: TokenPayload = Depends(requer_roles('admin')),
    service: UsuarioService = Depends(get_service)
):
    return service.criar_usuario(dados)