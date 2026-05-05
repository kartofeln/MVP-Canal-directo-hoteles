from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.db import Base, engine
import app.routers.canal_directo as canal_directo
import app.routers.report as report


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="MVP Canal Directo Hoteles", lifespan=lifespan)

app.include_router(canal_directo.router)
app.include_router(report.router)


@app.get("/")
def root():
    return RedirectResponse(url="/analiza")
