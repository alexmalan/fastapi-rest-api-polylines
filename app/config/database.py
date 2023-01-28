"""
Database configuration file.
"""
import os
from pathlib import Path

import dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Load environment variables from .env file
BASE_DIR = Path(__file__).resolve().parents[2]
dotenv_file = os.path.join(BASE_DIR, ".env")

if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

# Engine connection string
engine = create_engine(
    f'postgresql://{os.environ.get("DATABASE_USER")}:{os.environ.get("DATABASE_PASSWORD")}@{os.environ.get("DATABASE_HOST")}/{os.environ.get("DATABASE_NAME")}',
    echo=True,
)

# Create a configured "Session" class
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)
