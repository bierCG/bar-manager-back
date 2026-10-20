from app.schemas import Base

class Auth(Base):
    sub: int
    role: str