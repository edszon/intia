from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel

from .db import engine
from .config import settings
from .routers.persons import router as persons_router
from .routers.messages import router as messages_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

 

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

app.include_router(persons_router, prefix=settings.api_prefix)
app.include_router(messages_router, prefix=settings.api_prefix)