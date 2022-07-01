from typing import List, Union

from pydantic import BaseModel


class PizzaBase(BaseModel):
    id: int
    nombre: str
    precio: int

    class Config:
        orm_mode = True


class IngredienteBase(BaseModel):
    id: int
    nombre: str
    categoria: int

    class Config:
        orm_mode = True
    

# Estas 2 siguientes clases es la estructura que retornameros
# (recordar que heredan de otras clases).
# Se aparta de esta manera para EVITAR recursividad al mostrar
# los ingredientes de una pizza y de nuevo que pizzas usan estos ingredientes.
class Ingrediente(IngredienteBase):
    pizzas_que_usa: List[PizzaBase]

class Pizza(PizzaBase):
    ingredientes: List[IngredienteBase]



class UserBase(BaseModel):
    username: str


# La constrasenha ponemos a parte por motivos de seguridad
# Y no retornar la contrasenha en una peticion por ejemplo.
class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    is_staff: bool
    is_superuser: bool
    #items: List[Item] = []

    class Config:
        orm_mode = True
