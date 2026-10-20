from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session

from app.core.security.password import validar_senha
from app.core.security.auth import create_token

from app.schemas.login import LoginRequest

from app.repositories.usuarios import UsuarioRepository
from app.core.exceptions.exceptions import LoginInvalido

class LoginService():
    def __init__(self, session: Session) -> dict:
        self.repo = UsuarioRepository(session)

    def logar(self, login: LoginRequest) -> dict[str, str]:
        usuario = self.repo.get_by_username(login.usuario)

        if not usuario or not validar_senha(login.senha, usuario.senha):
            raise LoginInvalido()

        token = create_token({
            "sub": str(usuario.id),
            "role": usuario.role,
            "exp": datetime.now(timezone.utc) + timedelta(hours=12),
        })

        return {"token": token}