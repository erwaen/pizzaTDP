from sqlalchemy.orm import Session

from . import modelos, schemas

#
# CRUD para USUARIO
#

def get_user(db: Session, user_id: int):
    return db.query(modelos.Usuario).filter(modelos.Usuario.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(modelos.Usuario).filter(modelos.Usuario.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(modelos.Usuario).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    pass_hashed = user.password + "megustalapizza"
    db_user = modelos.Usuario(username=user.username, hashed_password=pass_hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


