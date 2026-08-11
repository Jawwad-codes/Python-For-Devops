from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Cloud Cost Guard")

app.include_router(router)