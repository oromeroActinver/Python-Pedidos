from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Nota: agregar autocommit=False para que la sesión maneje commits manualmente
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

# Función para obtener la sesión y usarla en Depends()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
