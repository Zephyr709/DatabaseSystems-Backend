from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Item, Base
from database import get_db, engine

# Create database tables
Base.metadata.create_all(bind=engine)

router = APIRouter()

@router.get("/items", response_model=list[dict])
async def read_items(db: Session = Depends(get_db)):
    items = db.query(Item).all()
    return [{"id": item.id, "name": item.name} for item in items]

@router.post("/items/", response_model=dict)
async def create_item(name: str, db: Session = Depends(get_db)):
    new_item = Item(name=name)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return {"id": new_item.id, "name": new_item.name}
