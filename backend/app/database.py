from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
 

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:12345678@localhost:5432/fitnessapp"

# Create the database engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Session factory (creates DB sessions)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models to inherit from
Base = declarative_base()

# Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


