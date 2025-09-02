from fastapi import FastAPI
from app.database import Base, engine
from app.models import models
from dotenv import load_dotenv

load_dotenv()  

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}