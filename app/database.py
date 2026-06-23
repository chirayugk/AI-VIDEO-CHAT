from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

DATABASE_URL = "postgresql://postgres:postgres@localhost/video_platform"

engine = create_engine(DATABASE_URL)
try:
    conn = engine.connect()
    print("Database Connected Successfully")
    conn.close()
except Exception as e:
    print("Error:", e)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()