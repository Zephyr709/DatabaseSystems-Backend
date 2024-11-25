from fastapi import FastAPI, APIRouter, Depends, HTTPException, Request
from models import Item, Subscription, Professional, User, Base, Metrics, DailyMealLog
from functions import get_users_by_prof_id, delete_professional_by_id
from database import get_db, engine
from sqlalchemy.orm import Session, Query, mapped_column, Mapped
from sqlalchemy.sql import text
from sqlalchemy.inspection import inspect
from sqlalchemy import Integer, String
from typing import ClassVar
from pydantic import BaseModel

# Create database tables
Base.metadata.create_all(bind=engine)

router = APIRouter()

class UserCreate(BaseModel):
    name: str
    email: str
    country: str
    city: str
    height: float
    weight: float
    gender: str
    birthdate: str
    nutritiongoal: str
    macrosplit: str
    subscriptionid: int
    professionalid: int

# Create User
@router.post("/users", response_model=dict)
async def create_user(request: Request, db: Session = Depends(get_db)):
    body = await request.json()
    new_user = User(
        name=body["name"],
        email=body["email"],
        country=body["country"],
        city=body["city"],
        height=body["height"],
        weight=body["weight"],
        gender=body["gender"],
        birthdate=body["birthdate"],
        nutritiongoal=body["nutritiongoal"],
        macrosplit=body["macrosplit"],
        subscriptionid=body["subscriptionid"],
        professionalid=body["professionalid"]
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"userid": new_user.userid, "name": new_user.name, "email": new_user.email}

# Read Users
@router.get("/users", response_model=list[dict])
async def read_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [{"userid": user.userid, "name": user.name, "email": user.email} for user in users]

# Update User
@router.put("/users/{userid}", response_model=dict)
async def update_user(userid: int, request: Request, db: Session = Depends(get_db)):
    body = await request.json()
    existing_user = db.query(User).filter(User.userid == userid).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    existing_user.name = body["name"]
    existing_user.email = body["email"]
    existing_user.country = body["country"]
    existing_user.city = body["city"]
    existing_user.height = body["height"]
    existing_user.weight = body["weight"]
    existing_user.gender = body["gender"]
    existing_user.birthdate = body["birthdate"]
    existing_user.nutritiongoal = body["nutritiongoal"]
    existing_user.macrosplit = body["macrosplit"]
    existing_user.subscriptionid = body["subscriptionid"]
    existing_user.professionalid = body["professionalid"]
    db.commit()
    db.refresh(existing_user)
    return {"userid": existing_user.userid, "name": existing_user.name, "email": existing_user.email}

# Delete User
@router.delete("/users/{userid}", response_model=dict)
async def delete_user(userid: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.userid == userid).first()
    db.delete(user)
    db.commit()
    return {"userid": user.userid, "name": user.name, "email": user.email}

# Read User by ID
@router.get("/users/{userid}")
async def get_user(userid: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.userid == userid).first()
    
    return user