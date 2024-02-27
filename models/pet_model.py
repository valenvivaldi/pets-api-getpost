# models/pet_model.py
from sqlalchemy import Column, Integer, String, JSON, Enum
from db.database import Base
from schemas.pet_schema import Status


class Pet(Base):
    __tablename__ = "pets"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    # status can be "available", "pending", "sold"
    status = Column(Enum(Status), index=True)
    info = Column(JSON)
