from fastapi import FastAPI, APIRouter, Depends, HTTPException
from models import Item, Subscription, Professional, User, Base, Metrics, DailyMealLog
from functions import get_users_by_prof_id, delete_professional_by_id, get_role
from database import get_db, engine
from sqlalchemy.orm import Session, Query, mapped_column, Mapped
from sqlalchemy.sql import text
from sqlalchemy.inspection import inspect
from sqlalchemy import Integer, String
from typing import ClassVar
# Create database tables
Base.metadata.create_all(bind=engine)


router = APIRouter()

# Read Items
@router.get("/items", response_model=list[dict])
async def read_items(db: Session = Depends(get_db)):
    items = db.query(Item).all()
    return [{"id": item.id, "name": item.name} for item in items]

# Create Item
@router.post("/items", response_model=dict)
async def create_item(name: str, db: Session = Depends(get_db)):
    new_item = Item(name=name)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return {"id": new_item.id, "name": new_item.name}

# Delete Item
@router.delete("/items/{item_id}", response_model=dict)
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    db.delete(item)
    db.commit()
    return {"id": item.id, "name": item.name}

# Update Item
@router.put("/items/{item_id}", response_model=dict)
async def update_item(item_id: int, name: str, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    item.name = name
    db.commit()
    db.refresh(item)
    return {"id": item.id, "name": item.name}

# Get Item by ID
@router.get("/items/{item_id}")
async def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    return {"id": item.id, "name": item.name}