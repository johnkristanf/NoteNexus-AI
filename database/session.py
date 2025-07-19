import os 
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent  # Adjust depth if needed
dotenv_path = root_dir / ".env.local"
if not dotenv_path.exists():
    dotenv_path = root_dir / ".env"

load_dotenv(dotenv_path=dotenv_path)
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    echo=True,  # log SQL statements
    pool_size=5,  # connection pool size
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=3600,  # recycle connections after 1 hour,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False)