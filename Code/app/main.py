from fastapi import FastAPI
from app.routers import auth, home, exercise, vm
from app.database import create_db_and_tables

app = FastAPI(debug=True)

app.include_router(home.router)
app.include_router(auth.router)
app.include_router(exercise.router)
app.include_router(vm.router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()