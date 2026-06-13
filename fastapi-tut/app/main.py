from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from app.database import init_db
from app.routers import users


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    init_db()
    yield

app = FastAPI(lifespan=lifespan)


@app.get("/")
def root():
    return {"status": "ok"}


@app.get("/echo/{text}")
def echo(text: str):
    return {"message": text}


@app.get("/add")
def add(a: int, b: int):
    return {"sum": a + b}


@app.get("/repeat/{text}")
def repeat(text: str, times: int = 1):
    return {"repeat": text * times}


app.include_router(router=users.router)