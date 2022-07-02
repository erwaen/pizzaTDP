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


association_table_pizza_ingrediente = Table(
    "association",
    Base.metadata,
    Column("pizza_id", ForeignKey("pizzas.id"), primary_key=True),
    Column("ingrediente_id", ForeignKey("ingredientes.id"), primary_key=True),
)


class Pizza(Base):
    __tablename__ = "pizzas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    precio = Column(Integer, index=True)
    is_active = Column(Boolean, default=True)

    sus_ingredientes = relationship(
        "Ingrediente", secondary=association_table_pizza_ingrediente, back_populates="pizzas_usando"
    )


class IngreCategory(enum.Enum):
   Basico = 'basico'
   Premium = 'premium'

class Ingrediente(Base):
    __tablename__ = "ingredientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    categoria = Column(Enum(IngreCategory), index=True, default=IngreCategory.Basico)

    pizzas_usando = relationship(
        "Pizza", secondary=association_table_pizza_ingrediente, back_populates="sus_ingredientes"
    )





