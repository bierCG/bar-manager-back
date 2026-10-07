from sqlalchemy.orm import Session
from app.database.models import Usuario

class LoginRepository():
    def __init__(self, session: Session):
        self.session = session

    def get_user(self, email: str):
        return (
            self.session.query(Usuario)
            .filter(Usuario.email == email)
            .first()
        )
