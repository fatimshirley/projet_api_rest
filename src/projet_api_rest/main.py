from fastapi import FastAPI

from projet_api_rest.routers.auth import router as auth_router
from projet_api_rest.routers.tasks import router as tasks_router


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