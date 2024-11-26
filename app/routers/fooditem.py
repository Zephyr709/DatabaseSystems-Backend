from fastapi import FastAPI, APIRouter, Depends, HTTPException, Request
from models import Item, Subscription, Professional, User, Base, Metrics, DailyMealLog, DailyMealLogView, FoodItem
from functions import get_users_by_prof_id, delete_professional_by_id
from database import get_db, engine, getRole
from sqlalchemy.orm import Session, Query, Mapped
from sqlalchemy.sql import text
from sqlalchemy.inspection import inspect
from sqlalchemy import Integer, String
from typing import ClassVar

from functions import get_meal_view

# Create database tables
Base.metadata.create_all(bind=engine)


router = APIRouter()


# Update Daily Meal Log
@router.put("/fooditems/{fooditemid}", response_model=dict)
async def update_fooditem(fooditemid: int, request: Request, db: Session = Depends(get_db)):
    if getRole() == "it_admin":
        data = await request.json()
        food_item = db.query(FoodItem).filter(
            FoodItem.fooditemid == fooditemid
        ).first()
        food_item.fooditemid = data['fooditemid']
        food_item.name = data['name']
        food_item.calories = data['calories']
        food_item.protein = data['protein']
        food_item.carbs = data['carbs']
        food_item.fats = data['fats']
        food_item.fiber = data['fiber']
        food_item.sugar = data['sugar']
        food_item.sodium = data['sodium']
        food_item.cholesterol = data['cholesterol']
        db.commit()
        db.refresh(food_item)
        return {
            "fooditemid": food_item.fooditemid,
            "name": food_item.name,
            "calories": food_item.calories,
            "protein": food_item.protein,
            "carbs": food_item.carbs,
            "fats": food_item.fats,
            "fiber": food_item.fiber,
            "sugar": food_item.sugar,
            "sodium": food_item.sodium,
            "cholesterol": food_item.cholesterol
        }
    else:
        raise HTTPException(status_code=403, detail="Access Denied")  # 403 Forbidden
   