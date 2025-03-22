from fastapi import FastAPI
from .routers import home, user, exercise
from .database import create_db_and_tables

app = FastAPI()

app.include_router(home.router)
app.include_router(user.router)
app.include_router(exercise.router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


