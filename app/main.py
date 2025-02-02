from fastapi import FastAPI
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

@app.get("/")
async def root():
    return {"message": "Bem-vindo a leiturece"}


app.include_router(auth.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=5000)

