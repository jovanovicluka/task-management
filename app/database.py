from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    print("Connected!")
    conn.execute(text("SELECT 1"))

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)