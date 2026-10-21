import os

from sqladmin import Admin

from .auth import AdminAuth
from .views import UsuarioAdmin

from app.core.database.connection import engine
from app.core.config import SQLADMIN_SESSION_SECRET_KEY

def setup_admin(app) -> Admin:
    admin = Admin(
        app,
        engine,
        authentication_backend=AdminAuth(secret_key=SQLADMIN_SESSION_SECRET_KEY),
    )
    admin.add_view(UsuarioAdmin)
    return admin