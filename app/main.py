from api.routes import router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from db.session import engine, Base
from services.redis_cache import REDIS_ENABLED, redis_ping

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
def root():
    return {"health": "OK"}


@app.get("/health")
def health():
    db_status = "down"
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        db_status = "up"
    except Exception:
        pass

    if not REDIS_ENABLED:
        redis_status = "disabled"
    else:
        redis_status = "up" if redis_ping() else "down"

    overall = "ok" if db_status == "up" else "degraded"
    return {
        "status": overall,
        "database": db_status,
        "redis": redis_status,
    }


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
