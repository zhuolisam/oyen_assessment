from typing import Annotated, List, Dict
from fastapi import FastAPI, Form, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database import SessionLocal, engine
from auth import auth_handler
import crud, models, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://127.0.0.1:5000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> models.User:
    payload = auth_handler.decode_token(token)
    user = crud.get_user_by_username(db, username=payload["sub"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Username not found"
        )
    return user


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/me", response_model=Dict[str, List[schemas.LoginSessionBase]])
def get_login_sessions(
    db: Session = Depends(get_db), user: models.User = Depends(get_current_user)
):
    sessions = crud.get_login_sessions(db, user=schemas.UserInDB(**user.__dict__))
    sessions = [
        schemas.LoginSessionBase(created_at=session.created_at) for session in sessions
    ]
    return {"sessions": sessions}


@app.post("/login", response_model=schemas.TokenCreate)
def login_user(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    db: Session = Depends(get_db),
):
    user = crud.get_user_by_username(db, username=username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Username not found"
        )
    elif not auth_handler.verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password"
        )

    iat = crud.add_login_session(db, user=schemas.UserInDB(**user.__dict__))
    access_token = auth_handler.encode_token(username=user.username, iat=iat)
    return {
        "access_token": access_token,
        "token_type": "Bearer",
        "username": user.username,
    }


@app.post("/signup", response_model=schemas.UserBase)
def signup_user(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    db: Session = Depends(get_db),
):
    user = crud.get_user_by_username(db, username=username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username already registered",
        )
    new_user = crud.create_user(
        db, user=schemas.UserCreate(username=username, password=password)
    )
    return {"username": new_user.username}


@app.get("/users", response_model=Dict[str, List[schemas.UserBase]])
def get_users(db: Session = Depends(get_db)):
    users = crud.get_users(db)
    users = [schemas.UserBase(username=user.username) for user in users]
    return {"users": users}
