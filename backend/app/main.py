from fastapi import FastAPI
from app.database import Base, engine
from app.models import models

app = FastAPI()

# 🔹 Create the tables in DB
Base.metadata.create_all(bind=engine)

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}