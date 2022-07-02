from email.policy import default
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table, Enum
from sqlalchemy.orm import relationship

from .database import Base

import enum


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_staff = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)


class AssociationPizzaIngrediente(Base):
    __tablename__ = "pizza_ingredientes_r"
    pizza_id = Column(ForeignKey("pizzas.id"), primary_key=True)
    ingrediente_id = Column(ForeignKey("ingredientes.id"), primary_key=True)
    ingrediente = relationship("Ingrediente", back_populates="pizzas_usando")
    pizza = relationship("Pizza", back_populates="sus_ingredientes")




class Pizza(Base):
    __tablename__ = "pizzas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    precio = Column(Integer, index=True)
    is_active = Column(Boolean, default=False)

    sus_ingredientes = relationship(
        "AssociationPizzaIngrediente", back_populates="pizza"
    )

    def get_cantidad_ingredientes(self):
        return len(self.sus_ingredientes)


class IngreCategory(enum.Enum):
   Basico = 'basico'
   Premium = 'premium'

class Ingrediente(Base):
    __tablename__ = "ingredientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    categoria = Column(Enum(IngreCategory), index=True, default=IngreCategory.Basico)

    pizzas_usando = relationship(
        "AssociationPizzaIngrediente", back_populates="ingrediente"
    )







