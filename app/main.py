from api.routes import router
from fastapi import FastAPI

from db.session import engine, Base

app = FastAPI()

app.include_router(router)

@app.get('/')
def health():
    return {"health": "OK"}


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
