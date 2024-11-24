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


# Create Daily Meal Log
@router.post("/daily_meal_logs/", response_model=dict)
async def create_daily_meal_log(
    userid: int,
    fooditemid: int,
    datelogged: str,
    db: Session = Depends(get_db)
):
    new_daily_meal_log = DailyMealLog(
        userid=userid,
        fooditemid=fooditemid,
        datelogged=datelogged
    )
    db.add(new_daily_meal_log)
    db.commit()
    db.refresh(new_daily_meal_log)
    return {
        "meallogid": new_daily_meal_log.meallogid,
        "userid": new_daily_meal_log.userid,
        "fooditemid": new_daily_meal_log.fooditemid,
        "datelogged": new_daily_meal_log.datelogged
    }


# Read Daily Meal Logs
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

# Update Daily Meal Log
@router.put("/daily_meal_logs/{meallogid}", response_model=dict)
async def update_daily_meal_log(
    meallogid: int,
    userid: int,
    fooditemid: int,
    datelogged: str,
    db: Session = Depends(get_db)
):
    daily_meal_log = db.query(DailyMealLog).filter(DailyMealLog.meallogid == meallogid).first()
    daily_meal_log.userid = userid
    daily_meal_log.fooditemid = fooditemid
    daily_meal_log.datelogged = datelogged
    db.commit()
    db.refresh(daily_meal_log)
    return {
        "meallogid": daily_meal_log.meallogid,
        "userid": daily_meal_log.userid,
        "fooditemid": daily_meal_log.fooditemid,
        "datelogged": daily_meal_log.datelogged
    }
    
# Delete Daily Meal Log
@router.delete("/daily_meal_logs/{meallogid}", response_model=dict)
async def delete_daily_meal_log(meallogid: int, db: Session = Depends(get_db)):
    daily_meal_log = db.query(DailyMealLog).filter(DailyMealLog.meallogid == meallogid).first()
    db.delete(daily_meal_log)
    db.commit()
    return {
        "meallogid": daily_meal_log.meallogid,
        "userid": daily_meal_log.userid,
        "fooditemid": daily_meal_log.fooditemid,
        "datelogged": daily_meal_log.datelogged
    }