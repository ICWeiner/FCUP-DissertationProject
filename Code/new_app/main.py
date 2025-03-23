from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from .routers import home, user, exercise, vm
from .database import create_db_and_tables

app = FastAPI()

app.include_router(home.router)
app.include_router(user.router)
app.include_router(exercise.router)
app.include_router(vm.router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()