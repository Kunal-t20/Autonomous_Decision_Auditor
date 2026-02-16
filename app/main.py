from api.routes import router
from fastapi import FastAPI

app=FastAPI()

app.include_router(router)

@app.get('/')
def health():
    return {"health:Okay"}

from db.session import engine, Base
from db.models import AuditRecord

Base.metadata.create_all(bind=engine)
