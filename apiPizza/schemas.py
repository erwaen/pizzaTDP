from typing import List, Union
from .modelos import IngreCategory

from pydantic import BaseModel


class PizzaBase(BaseModel):
    nombre: str
    precio: int

class PizzaCreate(PizzaBase):
    is_active: bool
    


class IngredienteBase(BaseModel):
    
    nombre: str
    categoria: IngreCategory

    
    
class IngredienteCreate(IngredienteBase):
    pass

# Estas 2 siguientes clases es la estructura que retornameros
# (recordar que heredan de otras clases).
# Se aparta de esta manera para EVITAR recursividad al mostrar
# los ingredientes de una pizza y de nuevo que pizzas usan estos ingredientes.
class Ingrediente(IngredienteBase):
    id: int
    pizzas_usando: List[PizzaBase]

    class Config:
        orm_mode = True

class Pizza(PizzaBase):
    id: int
    sus_ingredientes: List[IngredienteBase]

    class Config:
        orm_mode = True

class PizzaNoId(PizzaBase):
    cantidad_ingredientes: int
    class Config:
        orm_mode = True

class PizzaDetallado(PizzaBase):
    sus_ingredientes: List[IngredienteBase]
    is_active: bool
    class Config:
        orm_mode = True

    



class UserBase(BaseModel):
    username: str
    is_staff: bool
    is_superuser: bool


# La constrasenha ponemos a parte por motivos de seguridad
# Y no retornar la contrasenha en una peticion por ejemplo.
class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    
    #items: List[Item] = []

    class Config:
        orm_mode = True
