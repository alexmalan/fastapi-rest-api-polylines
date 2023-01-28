"""
Poly data model.
"""
from sqlalchemy import Column, Float, Integer, String, Text

from app.config import Base


class Poly(Base):
    """
    Poly data model.
    """

    __tablename__ = "poly"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    npinput = Column(Text, nullable=True)
    xsize = Column(Integer, nullable=True)
    ysize = Column(Integer, nullable=True)
    imagefile = Column(String(255), nullable=True)
    arrayfile = Column(String(255), nullable=True)
    exectime = Column(Float, nullable=True)
    algorithm = Column(String(255), nullable=False, unique=False)

    def __repr__(self):
        """
        Poly representation string.
        """
        return f"Poly name: {self.name}"
