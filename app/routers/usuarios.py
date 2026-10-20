from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.usuarios import CreateRequest, CreateResponse
from app.services.usuarios import UsuarioService
from app.core.security.auth import requer_roles
from app.core.database.connection import get_db

router = APIRouter(prefix="/usuarios", tags=["Usuários"])

def get_service(session: Session = Depends(get_db)) -> UsuarioService:
    return UsuarioService(session)

# ------------------------------------------------------------------------------------------
#
# ### POST ###
#
# ------------------------------------------------------------------------------------------

@router.post(
    "/",
    dependencies=[Depends(requer_roles('admin'))],
    response_model=CreateResponse
)
def cadastrar_usuario(
    cadastro: CreateRequest,
    service: UsuarioService = Depends(get_service)
):
    return service.cadastrar_usuario(cadastro)