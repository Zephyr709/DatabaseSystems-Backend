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

@router.get("/daily_meal_logs", response_model=list[dict])
async def read_daily_meal_logs(db: Session = Depends(get_db)):
    daily_meal_logs = db.query(DailyMealLog).all()
    return [
        {
            "meallogid": log.meallogid,
            "userid": log.userid,
            "fooditemid": log.fooditemid,
            "datelogged": log.datelogged
        }
        for log in daily_meal_logs
    ]
