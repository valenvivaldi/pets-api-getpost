from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from db.database import Base, engine, get_db
from models.pet_model import Pet
from schemas.pet_schema import PetCreate, PetInDBBase, PetUpdate

# Crea las tablas de la base de datos en caso de no existir
Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/pets/", response_model=PetInDBBase, status_code=status.HTTP_201_CREATED)
def create_pet(pet: PetCreate, db: Session = Depends(get_db)):
    db_pet = Pet(name=pet.name, status=pet.status, info=pet.info)
    db.add(db_pet)
    db.commit()
    db.refresh(db_pet)
    return db_pet


@app.get("/pets/", response_model=List[PetInDBBase])
def read_pets(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    pets = db.query(Pet).offset(skip).limit(limit).all()
    return pets


@app.get("/pets/{pet_id}", response_model=PetInDBBase)
def read_pet(pet_id: int, db: Session = Depends(get_db)):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")
    return pet


@app.post("/pets/update/{pet_id}", response_model=PetInDBBase)
def update_pet(pet_id: int, pet: PetUpdate, db: Session = Depends(get_db)):
    db_pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if db_pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")
    db_pet.name = pet.name
    db_pet.status = pet.status
    db_pet.info = pet.info
    db.commit()
    db.refresh(db_pet)
    return db_pet


@app.post("/pets/delete/{pet_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pet(pet_id: int, db: Session = Depends(get_db)):
    db_pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if db_pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")
    db.delete(db_pet)
    db.commit()
    return {"detail": "Pet deleted successfully"}


@app.get("/pets/searchByName/", response_model=List[PetInDBBase])
def search_by_name(name: str, db: Session = Depends(get_db)):
    pets = db.query(Pet).filter(Pet.name == name).all()
    return pets


@app.get("/pets/searchByNameContains/", response_model=List[PetInDBBase])
def search_by_name_contains(searchterm: str, db: Session = Depends(get_db)):
    pets = db.query(Pet).filter(Pet.name.contains(searchterm)).all()
    return pets


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
