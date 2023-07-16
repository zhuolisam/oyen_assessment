from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import models, schemas
from auth import auth_handler


def get_user_by_username(db: Session, username: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    return user


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth_handler.hash_password(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def add_login_session(db: Session, user: schemas.UserInDB):
    iat = datetime.utcnow() + timedelta(hours=8)
    print(iat)

    db_login_session = models.LoginSession(user_id=user.id, created_at=iat)
    db.add(db_login_session)
    db.commit()
    db.refresh(db_login_session)

    return iat


def get_login_sessions(db: Session, user: schemas.UserInDB):
    return (
        db.query(models.LoginSession)
        .filter(models.LoginSession.user_id == user.id)
        .order_by(models.LoginSession.created_at.desc())
        .all()
    )


def get_users(db: Session):
    return db.query(models.User).all()
