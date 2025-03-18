from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .settings import config
from .routes import auth
from contextlib import asynccontextmanager
from .dependencies.database.db import SessionManager

import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    if SessionManager.get_engine() is not None:
        await SessionManager.close()

app = FastAPI(title="Leiturece Backend", lifespan=lifespan)

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
    f"https://{config.HOST_DOMAIN}",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Bem-vindo a leiturece"}


app.include_router(auth.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=5000)

