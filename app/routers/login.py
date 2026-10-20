from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.login import LoginRequest, LoginResponse
from app.services.login import LoginService
from app.core.database.connection import get_db

router = APIRouter(prefix="/login", tags=["Login"])

def get_service(session: Session = Depends(get_db)) -> LoginService:
    return LoginService(session)

# ------------------------------------------------------------------------------------------
#
# ### POST ###
#
# ------------------------------------------------------------------------------------------

@router.post("/", response_model=LoginResponse)
def login(
    login: LoginRequest,
    service: LoginService = Depends(get_service)
):
    return service.logar(login)