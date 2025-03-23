from fastapi import FastAPI
from .routers import auth, home, exercise, vm
from .database import create_db_and_tables

app = FastAPI()

app.include_router(home.router)
app.include_router(auth.router)
app.include_router(exercise.router)
app.include_router(vm.router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()