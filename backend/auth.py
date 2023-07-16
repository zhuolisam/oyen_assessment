from jose import jwt, JWTError, ExpiredSignatureError
from fastapi import HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()


class AuthHandler:
    # JWT token
    security = HTTPBearer()
    secret = os.getenv("JWT_SECRET_KEY")
    algorithm = "HS256"
    access_token_expire_minutes = 30

    # Password Hashing
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def hash_password(cls, password: str):
        return cls.pwd_context.hash(password)

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str):
        return cls.pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def encode_token(cls, username: str, iat=datetime.utcnow()):
        payload = {
            "exp": iat + timedelta(days=0, minutes=cls.access_token_expire_minutes),
            "iat": iat,
            "sub": username,
        }
        return jwt.encode(payload, cls.secret, algorithm=cls.algorithm)

    @classmethod
    def decode_token(cls, token: str):
        try:
            payload = jwt.decode(token, cls.secret, algorithms=[cls.algorithm])
            return payload
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Signature has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )

    @classmethod
    def auth_wrapper(cls, auth: HTTPAuthorizationCredentials = Security(security)):
        return cls.decode_token(auth.credentials)


auth_handler = AuthHandler()
