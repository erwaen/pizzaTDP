from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# El URL del archivo de la base de datos (./pizza_app.db)
SQLALCHEMY_DATABASE_URL = "sqlite:///./pizza_app.db"

# Se crea un SQLAlchemy 'engine'
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Cada instancia de esta clase ("SessionLocal") sera una sesion de la base de datos.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Esta clase 'Base' se utilizara para heredar de el los modelos a crear para
# la base de datos
Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()