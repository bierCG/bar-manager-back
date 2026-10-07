from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session

from app.security.password import validar_senha
from app.security.auth import create_token

from app.repositories.login import LoginRepository
from app.exceptions.exceptions import LoginInvalido

class LoginService():
    def __init__(self, session: Session) -> dict:
        self.session = session
        self.repo = LoginRepository(session)


    def logar(self, email: str, senha: str) -> dict[str, str]:
        usuario = self.repo.get_user(email)

        if not usuario or not validar_senha(senha, usuario.senha):
            raise LoginInvalido()

        payload = {
            "sub": str(usuario.id),
            "role": usuario.role,
            "exp": datetime.now(timezone.utc) + timedelta(hours=12),
        }

        token = create_token(payload)

        return {"token": token, "username": usuario.nome}