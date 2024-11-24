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

# Read Users
@router.get("/users", response_model=list[dict])
async def read_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [{"userid": user.userid, "name": user.name, "email": user.email} for user in users]

# Create User
@router.post("/users/", response_model=dict)
async def create_user(
    name: str,
    email: str,
    country: str,
    city: str,
    height: float,
    weight: float,
    gender: str,
    birthdate: str,
    nutritiongoal: str,
    macrosplit: str,
    subscriptionid: int,
    professionalid: int,
    db: Session = Depends(get_db)
):
    new_user = User(
        name=name,
        email=email,
        country=country,
        city=city,
        height=height,
        weight=weight,
        gender=gender,
        birthdate=birthdate,
        nutritiongoal=nutritiongoal,
        macrosplit=macrosplit,
        subscriptionid=subscriptionid,
        professionalid=professionalid
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"userid": new_user.userid, "name": new_user.name, "email": new_user.email}
