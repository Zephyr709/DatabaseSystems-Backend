from fastapi import FastAPI, APIRouter, Depends, HTTPException
from models import Item, Subscription, Professional, User, Base, Metrics, DailyMealLog
from functions import get_users_by_prof_id, delete_professional_by_id, get_role_from_db, search_table_column_row
from database import get_db, engine, setRole, getRole
from sqlalchemy.orm import Session, Query, mapped_column, Mapped
from sqlalchemy.sql import text
from sqlalchemy.inspection import inspect
from sqlalchemy import Integer, String
from typing import ClassVar
# Create database tables
Base.metadata.create_all(bind=engine)


router = APIRouter()


@router.get("/sortData")
async def sort_data(
    table: str,
    sortBy: str,
    order: str = Query(text("asc")),
    db: Session = Depends(get_db)
):
    # Define a mapping for tables and their corresponding models
    table_models = {
        "items": Item,
        "subscriptions": Subscription,
        "professionals": Professional,
        "users": User,
        "daily_meal_logs": DailyMealLog,
        "metrics": Metrics
    }

    # Validate if the provided table name is valid
    if table not in table_models:
        raise HTTPException(status_code=400, detail="Invalid table name provided")

    # Get the model for the requested table
    model = table_models[table]

    # Check if the column exists in the model's schema
    columns = {column.name for column in model.__table__.columns}
    if sortBy not in columns:
        raise HTTPException(status_code=400, detail=f"Invalid column name '{sortBy}' for table '{table}'")

    # Dynamically fetch the sorted data
    query = db.query(model)
    if order == "asc":
        query = query.order_by(getattr(model, sortBy).asc())
    else:
        query = query.order_by(getattr(model, sortBy).desc())
    print(model)
    # Get the results from the database
    results = query.all()

    response = []
    for item in results:
        # Create a dictionary of column names and their corresponding values
        #item_data = {column.name: getattr(item, column.name) for column in model.__table__.columns}
        if (model == Subscription):
            item_data = {"subscriptionid": getattr(item, "subscriptionid"), "subscriptiontype": getattr(item, "subscriptiontype"),"billingcycle": getattr(item, "billingcycle")}
            response.append(item_data)
        elif (model == Professional):
            item_data = {"professionalid": getattr(item, "professionalid"), "name": getattr(item, "name"),"email": getattr(item, "email"),"maxseats": getattr(item, "maxseats"),"currentseats": getattr(item, "currentseats"),"subscriptionid": getattr(item, "subscriptionid")}
            response.append(item_data)
        elif (model == User):
            item_data = {"userid": getattr(item, "userid"), "name": getattr(item, "name"),"email": getattr(item, "email")}
            response.append(item_data)
        elif (model == DailyMealLog):
            item_data = {"meallogid": getattr(item, "meallogid"), "userid": getattr(item, "userid"),"fooditemid": getattr(item, "fooditemid"),"datelogged": getattr(item, "datelogged")}
            response.append(item_data)
        elif (model == Metrics):
            item_data = {"metricsid": getattr(item, "metricsid"), "inputtokenusage": getattr(item, "inputtokenusage"), "outputtokenusage": getattr(item, "outputtokenusage"),"userid": getattr(item, "userid")}
            response.append(item_data)
    

    return response

@router.get("/login/{userId}", response_model=dict)
async def get_users(userId: str, db: Session = Depends(get_db)):
    # Perform any necessary string operations on userId
    role = get_role_from_db(db, userId)  # Assume get_role accepts a string ID
    setRole(role)
    return {"role":role}

@router.get("/role", response_model=dict)
async def get_role(db: Session = Depends(get_db)):
    return {"role":getRole()}

@router.get("/search")
async def sort_data(
    table: str,
    column: str,
    searchQ: str,
    db: Session = Depends(get_db)
):
    items = search_table_column_row(db, table, column, searchQ)
    return items