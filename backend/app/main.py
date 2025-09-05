from fastapi import FastAPI
from app.database import Base, engine
from app.routes import auth as auth_routes
from app.routes import users as users_routes
from app.models import models
from dotenv import load_dotenv

load_dotenv()  

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"status": "ok"}

app.include_router(auth_routes.router)
app.include_router(users_routes.router)
