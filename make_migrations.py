"""
Database migration file.
"""
from app.config.database import Base, engine
from app.models import Poly

Base.metadata.create_all(engine)
