from fastapi import FastAPI, APIRouter, Depends, HTTPException, Request
from models import Item, Subscription, Professional, User, Base, Metrics, DailyMealLog
from functions import get_users_by_prof_id, delete_professional_by_id
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
async def create_item(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    new_item = Item(name=data['name'])
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
async def update_item(item_id: int, request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    item = db.query(Item).filter(Item.id == item_id).first()
    item.name = data['name']
    db.commit()
    db.refresh(item)
    return {"id": item.id, "name": item.name}

# Get Item by ID
@router.get("/items/{item_id}")
async def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    return {"id": item.id, "name": item.name}