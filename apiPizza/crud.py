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


#
# CRUD para PIZZA
#
def get_pizzas(db: Session):
    """
    Default todas las pizzas que estan activas
    Si el usuario esta logueado y es usuario staff o superuser retorna todas las pizzas 
    """
    return db.query(modelos.Pizza).filter(modelos.Pizza.is_active == True).all()

def get_pizza_by_nombre(db: Session, nombre: str):
    return db.query(modelos.Pizza).filter(modelos.Pizza.nombre == nombre).first()

def create_pizza(db: Session, pizza: schemas.PizzaCreate):
    db_pizza = modelos.Pizza(**pizza.dict())
    db.add(db_pizza)
    db.commit()
    db.refresh(db_pizza)
    return db_pizza
#
# CRUD para INGREDIENTE
#

def get_ingrediente_by_nombre(db: Session, nombre: str):
    return db.query(modelos.Ingrediente).filter(modelos.Ingrediente.nombre == nombre).first()

def create_ingrediente(db: Session, ingrediente: schemas.IngredienteCreate):
    db_ingrediente = modelos.Ingrediente(**ingrediente.dict())
    db.add(db_ingrediente)
    db.commit()
    db.refresh(db_ingrediente)
    return db_ingrediente