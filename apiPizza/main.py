from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, modelos, schemas
from .database import SessionLocal, engine

modelos.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user: # Si el usuario ya existe
        raise HTTPException(status_code=400, detail="Ya se creo un user con este username")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None: # Si el usuario no se encontro
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_user

# ENDPOINTS PIZZAS
@app.post("/pizzas/", response_model=schemas.Pizza)
def create_pizza(pizza: schemas.PizzaCreate, db: Session = Depends(get_db)):
    db_pizza = crud.get_pizza_by_nombre(db, nombre=pizza.nombre)
    if db_pizza: # Si la pizza ya existe
        raise HTTPException(status_code=400, detail="Ya existe la pizza con ese nombre")
    if pizza.precio < 0:
        raise HTTPException(status_code=400, detail="El precio debe ser un valor positivo")

    return crud.create_pizza(db=db, pizza=pizza)

@app.get("/pizzas/", response_model=List[schemas.PizzaNoId])
def read_pizzas(user_type: int, db: Session = Depends(get_db)):
    pizzas = crud.get_pizzas(user_type, db)
    for pizza in pizzas:
        pizza.cantidad_ingredientes = pizza.get_cantidad_ingredientes()
    return pizzas

@app.get("/pizzas/{pizza_id}", response_model=schemas.PizzaDetallado)
def read_pizza_detallado(pizza_id: int, db: Session = Depends(get_db)):
    db_pizza = crud.get_pizza(pizza_id=pizza_id , db=db )
    if db_pizza is None: # Si el usuario no se encontro
        raise HTTPException(status_code=404, detail="Pizza no existe.")
    
    return db_pizza

# ENDPOINTS INGREDIENTES

@app.post("/ingredientes/", response_model=schemas.Ingrediente)
def create_ingrediente(ingrediente: schemas.IngredienteCreate, db: Session = Depends(get_db)):
    db_ingrediente = crud.get_ingrediente_by_nombre(db, nombre=ingrediente.nombre)
    if db_ingrediente: # Si el ingrediente ya existe
        raise HTTPException(status_code=400, detail="Ya se creo un ingrediente con este nombre")
    return crud.create_ingrediente(db=db, ingrediente=ingrediente)

