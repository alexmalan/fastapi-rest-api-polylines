"""
Poly serializer.
"""
from typing import Optional

from pydantic import BaseModel


class PolySerializer(BaseModel):
    """
    Poly serializer.
    """

    name: str
    npinput: Optional[str]
    imagefile: Optional[str]
    arrayfile: Optional[str]
    exectime: Optional[float]
    algorithm: Optional[str]

    class Config:
        """
        ORM mode.
        """

        orm_mode = True
