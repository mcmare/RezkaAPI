from datetime import datetime, timezone, timedelta
import jwt
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Boolean, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, sessionmaker
import os

load_dotenv()

SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)


class Base(DeclarativeBase): pass


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)
    admin = Column(Boolean, default=False)
    token = Column(String, )


Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autoflush=False, bind=engine)
db = SessionLocal()


def create_user(username, password):
    token = create_access_token({
        "username": username,
        "password": str(password)
    })
    sql = Users(username=username, password=password, token=token)
    db.add(sql)
    db.commit()


def get_auth_data():
    return {"secret_key": os.getenv("SECRET_KEY"), "algorithm": os.getenv("ALGORITHM")}


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({"exp": expire})
    auth_data = get_auth_data()
    encode_jwt = jwt.encode(to_encode, auth_data['secret_key'], algorithm=auth_data['algorithm'])
    return encode_jwt

