from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from .database import Base

import enum


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
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
    precio = Column(String, index=True)
    is_active = Column(Boolean, default=True)
    items = relationship("Item", back_populates="owner")

    sus_ingredientes = relationship(
        "Ingrediente", secondary=association_table_pizza_ingrediente, back_populates="pizzas_usando"
    )




class IngreCategory(enum.Enum):
   Basico = 'Basico'
   Premium = 'Premium'

class Ingrediente(Base):
    __tablename__ = "ingredientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    categoria = Column(IngreCategory, index=True)
    
    pizzas_usando = relationship(
        "Pizza", secondary=association_table_pizza_ingrediente, back_populates="sus_ingredientes"
    )





class Parent(Base):
    __tablename__ = "left"
    id = Column(Integer, primary_key=True)
    children = relationship(
        "Child", secondary=association_table, back_populates="parents"
    )


class Child(Base):
    __tablename__ = "right"
    id = Column(Integer, primary_key=True)
    parents = relationship(
        "Parent", secondary=association_table, back_populates="children"
    )