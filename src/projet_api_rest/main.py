from fastapi import FastAPI
from contextlib import asynccontextmanager
from projet_api_rest.routers.auth import router as auth_router
from projet_api_rest.routers.tasks import router as tasks_router
from projet_api_rest.database.init_db import init_db

init_db()  # Initialize the database tables
app = FastAPI(
    title="Tasks API",
    description="API REST de gestion de tâches avec authentification JWT",
    version="1.0.0",
)


app.include_router(auth_router)
app.include_router(tasks_router)


@app.get("/")
def root():
    return {
        "message": "Tasks API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }