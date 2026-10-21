from pwdlib.exceptions import UnknownHashError
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from ..core.database.connection import SessionLocal 
from ..core.database.models import Usuario               
from ..core.security.password import validar_senha       

ADMIN_ROLE = "ADMIN"


def _verificar(senha: str, hash_: str) -> bool:
    try:
        return validar_senha(senha, hash_)
    except UnknownHashError:
        return False


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form.get("username"), form.get("password")
        if not username or not password:
            return False

        with SessionLocal() as db:
            user = db.query(Usuario).filter(Usuario.usuario == username).first()
            if user and user.role == ADMIN_ROLE and _verificar(password, user.senha):
                request.session.update({"admin_id": user.id})
                return True
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        admin_id = request.session.get("admin_id")
        if not admin_id:
            return False
        with SessionLocal() as db:
            user = db.get(Usuario, admin_id)
            return bool(user and user.role == ADMIN_ROLE)