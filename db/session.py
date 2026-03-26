from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# -----------------------------
# ENV LOAD (simplified)
# -----------------------------
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in environment variables.")

# -----------------------------
# CONFIG
# -----------------------------
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# -----------------------------
# ENGINE (production ready)
# -----------------------------
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    echo=DEBUG,
)

# -----------------------------
# SESSION
# -----------------------------
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

Base = declarative_base()


# -----------------------------
# 🔥 DEPENDENCY (FASTAPI ready)
# -----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()