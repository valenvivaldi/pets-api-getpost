# schemas/pet_schema.py
from enum import Enum

from pydantic import BaseModel
from typing import Optional, Dict


class Status(str, Enum):
    available = "available"
    pending = "pending"
    sold = "sold"


class PetBase(BaseModel):
    name: str
    status: Status
    info: Optional[Dict] = None


class PetCreate(PetBase):
    pass


class PetUpdate(PetBase):
    pass


class PetInDBBase(PetBase):
    id: int

    class Config:
        from_attributes = True
