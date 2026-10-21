import os
from dotenv import load_dotenv

load_dotenv()

SQLADMIN_SESSION_SECRET_KEY = os.getenv("SQLADMIN_SESSION_SECRET_KEY")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
DATABASE_URL = os.getenv("DATABASE_URL")