from sqlalchemy.orm import Session
from app.core.database.models import Usuario

class LoginRepository():
    def __init__(self, session: Session):
        self.session = session

    def get_by_username(self, username: str) -> Usuario | None:
        return (
            self.session.query(Usuario)
            .filter(Usuario.usuario == username)
            .first()
        )
