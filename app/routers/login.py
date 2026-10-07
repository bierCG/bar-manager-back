from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.schemas import LoginCreate, LoginResponse
from app.services.login import LoginService
from app.database.connection import get_db

router = APIRouter(prefix="/login", tags=["Login"])

# ------------------------------------------------------------------------------------------
#
# ### GET ###
#
# ------------------------------------------------------------------------------------------

def get_service(session: Session = Depends(get_db)) -> LoginService:
    return LoginService(session)

# ------------------------------------------------------------------------------------------
#
# ### POST ###
#
# ------------------------------------------------------------------------------------------

@router.post("/", response_model=LoginResponse)
def login(
    login: LoginCreate,
    service: LoginService = Depends(get_service)
):
    return service.logar(email=login.email, senha=login.senha)