from typing import List
from fastapi import FastAPI, HTTPException, Query, Depends
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
from models import Address, Base
from pydantic import BaseModel
import math

# SQLAlchemy database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./address_book.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the database tables
Base.metadata.create_all(bind=engine)


# Define Pydantic response model
class AddressResponse(BaseModel):
    id: int
    address: str
    latitude: float
    longitude: float


# Define FastAPI app instance
app = FastAPI()


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# API endpoint to create a new address
@app.post("/addresses/", response_model=AddressResponse)
def create_address(address: AddressResponse, db: Session = Depends(get_db)):
    new_address = Address(**address.dict())  # Create a new Address instance
    db.add(new_address)
    db.commit()
    db.refresh(new_address)
    return new_address


# API endpoint to update an existing address
@app.put("/addresses/{address_id}", response_model=AddressResponse)
def update_address(address_id: int, address: AddressResponse, db: Session = Depends(get_db)):
    db_address = db.query(Address).filter(Address.id == address_id).first()
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")

    # Update the address fields
    for field, value in address.dict().items():
        setattr(db_address, field, value)

    db.commit()
    db.refresh(db_address)

    return db_address


# API endpoint to delete an address
@app.delete("/addresses/{address_id}")
def delete_address(address_id: int, db: Session = Depends(get_db)):
    db_address = db.query(Address).filter(Address.id == address_id).first()
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")

    db.delete(db_address)
    db.commit()

    return {"message": "Address deleted successfully"}


# API endpoint to get all addresses
@app.get("/address/", response_model=List[AddressResponse])
def get_all_addresses(db: Session = Depends(get_db)):
    addresses = db.query(Address).all()
    return addresses


# API endpoint to retrieve addresses within a given distance and location coordinates
@app.get("/addresses/within_distance/")
def get_addresses_within_distance(latitude: float, longitude: float, distance: float = Query(...),
                                  db: Session = Depends(get_db)):
    # Calculate distance in kilometers
    R = 6371.0  # Earth radius in kilometers
    addresses_within_distance = []
    all_addresses = db.query(Address).all()
    for addr in all_addresses:
        lat1 = math.radians(addr.latitude)
        lon1 = math.radians(addr.longitude)
        lat2 = math.radians(latitude)
        lon2 = math.radians(longitude)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = math.sin(dlat / 2) * 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) * 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distance_km = R * c
        if distance_km <= distance:
            addresses_within_distance.append(addr)

    return addresses_within_distance
