from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from fastapi.security import OAuth2PasswordRequestForm

from . import crud, modelos, schemas
from .database import SessionLocal, engine
from .deps import get_current_user

from .utils import (
    get_hashed_password,
    create_access_token,
    create_refresh_token,
    verify_password
)





modelos.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/signup', summary="Crear nuevo usuario", response_model=schemas.User)
def create_user(data: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=data.username)
    if db_user is not None:
        raise HTTPException(status_code=400, detail="Ya se creo un user con este username")
    return crud.create_user(db=db, user=data)

@app.post('/login', summary="Crear access y refresh para el usuario", response_model=schemas.TokenJWT)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username=form_data.username)
    if user is None:
        raise HTTPException(status_code=400, detail="username o password incorrectos")
    

    hashed_pass = user.hashed_password
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(status_code=400, detail="username o password incorrectos")
    
    return {
        "access_token": create_access_token(user.username),
        "refresh_token": create_refresh_token(user.username),
    }

# igual al anterior pero para poder usar en postman solo con dos valores
@app.post('/logear-jwt', summary="Crear access y refresh para el usuario", response_model=schemas.TokenJWT)
def login(username:str, password:str, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username=username)
    if user is None:
        raise HTTPException(status_code=400, detail="username o password incorrectos")
    

    hashed_pass = user.hashed_password
    if not verify_password(password, hashed_pass):
        raise HTTPException(status_code=400, detail="username o password incorrectos")
    
    return {
        "access_token": create_access_token(user.username),
        "refresh_token": create_refresh_token(user.username),
    }
    
    
@app.get('/me', summary='Obtiene los detalles de un usuario, se usa solo para testeo', response_model=schemas.User)
async def get_me(user: modelos.Usuario = Depends(get_current_user)):
    return user

@app.get("/")
def root():
    return {"message": "Hello World"}



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
def create_pizza(pizza: schemas.PizzaCreate, db: Session = Depends(get_db),  user: modelos.Usuario = Depends(get_current_user)):
    """
    Crear una pizza, SOLO STAFF O SUPER USER
    """
    # Si el usuario no es staff o superuser
    if user.is_superuser==False and user.is_staff==False:
        raise HTTPException(status_code=400, detail="No se puede crear la pizza, Usuario sin permisos")
    db_pizza = crud.get_pizza_by_nombre(db, nombre=pizza.nombre)
    if db_pizza: # Si la pizza ya existe
        raise HTTPException(status_code=400, detail="Ya existe la pizza con ese nombre")
    if pizza.precio <= 0:
        raise HTTPException(status_code=400, detail="El precio debe mayor a 0")

    return crud.create_pizza(db=db, pizza=pizza)
    

@app.get("/pizzas/", response_model=List[schemas.PizzaNoId])
def read_pizzas(db: Session = Depends(get_db), user: modelos.Usuario = Depends(get_current_user)):
    """
    Listar las pizzas
    """
    list_only_active = True
    # Si el usuario es staff o superuser entonces se cambia el bool para traer tambien las pizzas no activas
    if user.is_staff or user.is_superuser:
        list_only_active = False
    pizzas = crud.get_pizzas( db, list_only_active)
    for pizza in pizzas:
        pizza.cantidad_ingredientes = pizza.get_cantidad_ingredientes()
    return pizzas

@app.get("/pizzas/{pizza_id}", response_model=schemas.PizzaDetallado)
def read_pizza_detallado(pizza_id: int, db: Session = Depends(get_db),  user: modelos.Usuario = Depends(get_current_user)):
    """
    Ver en detalle una sola pizza por un id
    """
    
    db_pizza = crud.get_pizza(pizza_id=pizza_id , db=db )
    if db_pizza is None: # Si el usuario no se encontro
        raise HTTPException(status_code=404, detail="Pizza no existe.")
    
    return db_pizza

@app.patch("/pizzas/{pizza_id}", response_model = schemas.PizzaModificado)
def modificar_pizza(pizza_id: int, nombre: str, precio: str, is_active:bool, db: Session = Depends(get_db), user: modelos.Usuario = Depends(get_current_user)):
    """
    Modificar valores de la pizza como su nombre, precio ysi es activo o no,  
    SOLO STAFF O SUPER USER
    """
    # Si el usuario no es staff o superuser
    if user.is_superuser==False and user.is_staff==False:
        raise HTTPException(status_code=400, detail="No se puede modificar la pizza, Usuario sin permisos")
    db_pizza = crud.get_pizza(pizza_id=pizza_id , db=db )
    if db_pizza is None: # Si el usuario no se encontro
        raise HTTPException(status_code=404, detail="Pizza no existe.")
    db_pizza = crud.modificar_pizza(db_pizza, nombre, precio, is_active, db)

    return db_pizza


@app.post("/pizza-ingrediente/")
def agregar_ingrediente_pizza(p_id: int, ingr_id , db: Session = Depends(get_db), user: modelos.Usuario = Depends(get_current_user)):
    """
    agrega un ingrediente a tal pizza, ambos dados sus id's, 
    DEBE SER NECESARIO  QUE EL USUARIO SEA STAFF O SUPERUSER
    """
    # Si el usuario no es staff o superuser
    if user.is_superuser==False and user.is_staff==False:
        raise HTTPException(status_code=400, detail="No se puede agregar ingrediente a la pizza, Usuario sin permisos")
    result = crud.agregar_ingrediente_a_la_pizza(p_id, ingr_id, db)
    return result

@app.delete("/pizza-ingrediente/{p_id}/{ingr_id}")
def quitar_ingrediente_pizza(p_id: int, ingr_id: int, db: Session = Depends(get_db), user: modelos.Usuario = Depends(get_current_user)):
    """
    Quitar el ingrediente ingr_id a la pizza p_id
    DEBE SER NECESARIO  QUE EL USUARIO SEA STAFF O SUPERUSER

    """
    
    # Si el usuario no es staff o superuser
    if user.is_superuser==False and user.is_staff==False:
        raise HTTPException(status_code=400, detail="No se puede quitar ingrediente a la pizza, Usuario sin permisos")

    p_ingre_relacion = crud.get_pizza_ingrediente_relacion(p_id, ingr_id, db)
    if p_ingre_relacion is None:
        raise HTTPException(status_code=404, detail="Relacion pizza - ingrediente no existe.")
    crud.quitar_ingrediente_a_la_pizza(p_ingre_relacion, db)
    return {"detail": 'Se quito el ingrediente de la pizza correctamente'}



# ENDPOINTS INGREDIENTES

@app.post("/ingredientes/", response_model=schemas.Ingrediente)
def create_ingrediente(ingrediente: schemas.IngredienteCreate, db: Session = Depends(get_db), user: modelos.Usuario = Depends(get_current_user)):
    """
    Ruta para crear un ingrediente
    Permisos de staff o superusuarios es necesario
    """
    # Si el usuario no es staff o superuser
    if user.is_superuser==False and user.is_staff==False:
        raise HTTPException(status_code=400, detail="No se  puede crear un ingrediente, Usuario sin permisos")

    db_ingrediente = crud.get_ingrediente_by_nombre(db, nombre=ingrediente.nombre)
    if db_ingrediente: # Si el ingrediente ya existe
        raise HTTPException(status_code=400, detail="Ya se creo un ingrediente con este nombre")
    return crud.create_ingrediente(db=db, ingrediente=ingrediente)



@app.patch("/ingredientes/{ingrediente_id}", response_model = schemas.IngredienteCreate)
def modificar_ingrediente(ingrediente_id: int, ingrediente: schemas.IngredienteCreate, db: Session = Depends(get_db), user: modelos.Usuario = Depends(get_current_user)):
    """
    Modificar valores del ingrediente como su nombre y su categoria
    Permisos de staff o superusuarios es necesario

    """
    # Si el usuario no es staff o superuser
    if user.is_superuser==False and user.is_staff==False:
        raise HTTPException(status_code=400, detail="No se puede modificar un ingrediente, Usuario sin permisos")

    db_ingrediente = crud.get_ingrediente(db, id=ingrediente_id)
    if db_ingrediente is None: # Si el usuario no se encontro
        raise HTTPException(status_code=404, detail="El ingrediente no existe.")
    
    db_ingrediente = crud.modificar_ingrediente(db_ingrediente, nombre=ingrediente.nombre, categoria=ingrediente.categoria, db=db)
    return db_ingrediente

@app.delete("/ingredientes/{ingrediente_id}/")
def eliminar_ingrediente( ingrediente_id: int ,db: Session = Depends(get_db), user: modelos.Usuario = Depends(get_current_user)):
    """
    Eliminar un ingrediente si es que no esta en uso en ninguna pizza
    Permisos de staff o superusuarios es necesario

    """

     # Si el usuario no es staff o superuser
    if user.is_superuser==False and user.is_staff==False:
        raise HTTPException(status_code=400, detail="No se puede eliminar un ingrediente, Usuario sin permisos")

    db_ingrediente_relacion = crud.verificar_si_ingrediente_en_uso(id =  ingrediente_id, db=db)
    if db_ingrediente_relacion:
        raise HTTPException(status_code=400, detail="No se pudo eliminar, hay pizzas asociadas a este ingrediente.")

    crud.eliminar_ingrediente(id=ingrediente_id, db=db)
    return {"detail": "Se elimino el ingrediente correctamente."}  
    