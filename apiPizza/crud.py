from unittest import result
from sqlalchemy.orm import Session
from . import utils

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
    pass_hashed = utils.get_hashed_password(user.password)
    db_user = modelos.Usuario(username=user.username, hashed_password=pass_hashed, is_staff=user.is_staff, is_superuser = user.is_superuser)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


#
# CRUD para PIZZA
#
def get_pizzas( db: Session, list_only_active: bool):
    """
    Default todas las pizzas que estan activas
    Si el usuario esta logueado y es usuario staff o superuser retorna todas las pizzas 
    """
    if list_only_active:
        pizzas = db.query(modelos.Pizza).filter(modelos.Pizza.is_active == True).all()
    else:
        pizzas = db.query(modelos.Pizza).all()
    return pizzas

def get_pizza(pizza_id: int, db: Session):
    """
    Retorna la informacion de la pizza dado un id de pizza
    """
    pizza = db.query(modelos.Pizza).filter(modelos.Pizza.id == pizza_id).first()
    if pizza is None:
        return None
    ingredientes = []
    for ing in pizza.sus_ingredientes:
        ingredientes.append(ing.ingrediente.nombre)
    pizza.ingredientes = ingredientes
    
    return pizza



def get_pizza_by_nombre(db: Session, nombre: str):
    return db.query(modelos.Pizza).filter(modelos.Pizza.nombre == nombre).first()

def create_pizza(db: Session, pizza: schemas.PizzaCreate):
    db_pizza = modelos.Pizza(**pizza.dict())
    db.add(db_pizza)
    db.commit()
    db.refresh(db_pizza)
    return db_pizza


def agregar_ingrediente_a_la_pizza(p_id: int, ingr_id: int, db: Session):
    dict = {
        'pizza_id' : p_id,
        'ingrediente_id' : ingr_id
    }
    
    db_p_ingr = modelos.AssociationPizzaIngrediente(**dict)
    db.add(db_p_ingr)
    db.commit()
    db.refresh(db_p_ingr)
    
    return db_p_ingr

def get_pizza_ingrediente_relacion(p_id: int, ingr_id: int, db: Session):
    return db.query(modelos.AssociationPizzaIngrediente).filter(
            modelos.AssociationPizzaIngrediente.pizza_id == p_id, 
            modelos.AssociationPizzaIngrediente.ingrediente_id == ingr_id
            ).first()

def modificar_pizza(db_pizza, nombre, precio, is_active, db):
    db_pizza.nombre = nombre
    db_pizza.precio = precio
    db_pizza.is_active = is_active
    db.commit()
    db.refresh(db_pizza)    
    return db_pizza




def quitar_ingrediente_a_la_pizza(p_ingre_relacion,  db):
    db.delete(p_ingre_relacion)
    db.commit()



#
# CRUD para INGREDIENTE
#

def get_ingrediente(db: Session, id: int):
    return db.query(modelos.Ingrediente).filter(modelos.Ingrediente.id == id).first()

def get_ingrediente_by_nombre(db: Session, nombre: str):
    return db.query(modelos.Ingrediente).filter(modelos.Ingrediente.nombre == nombre).first()

def create_ingrediente(db: Session, ingrediente: schemas.IngredienteCreate):
    db_ingrediente = modelos.Ingrediente(**ingrediente.dict())
    db.add(db_ingrediente)
    db.commit()
    db.refresh(db_ingrediente)
    return db_ingrediente

def modificar_ingrediente(db_ingrediente, nombre: str, categoria, db: Session):
    db_ingrediente.nombre = nombre
    db_ingrediente.categoria = categoria
    db.commit()
    db.refresh(db_ingrediente)    
    return db_ingrediente

def verificar_si_ingrediente_en_uso(id:int, db: Session):
    return db.query(modelos.AssociationPizzaIngrediente).filter(modelos.AssociationPizzaIngrediente.ingrediente_id == id).first()


def eliminar_ingrediente(id:int,  db: Session):
    db_ingrediente = db.query(modelos.Ingrediente).filter(modelos.Ingrediente.id == id).first()
    db.delete(db_ingrediente)
    db.commit()