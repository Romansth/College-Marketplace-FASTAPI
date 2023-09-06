from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import listing, user, auth, order
from .config import Settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(listing.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(order.router)

@app.get("/")
def root():
    return {"message": "Welcome to my api!!"}


