from fastapi import FastAPI
from .routers import home, user
from .database import create_db_and_tables

app = FastAPI()

app.include_router(home.router)
app.include_router(user.router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


