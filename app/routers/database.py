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

# Read Subscriptions
@router.get("/subscriptions", response_model=list[dict])
async def read_subscriptions(db: Session = Depends(get_db)):
    subscriptions = db.query(Subscription).all()
    return [{"subscriptionid": sub.subscriptionid, "subscriptiontype": sub.subscriptiontype, "billingcycle": sub.billingcycle} for sub in subscriptions]

# Create Subscription
@router.post("/subscriptions/", response_model=dict)
async def create_subscription(subscriptiontype: str, billingcycle: str, startdate: str, renewaldate: str, paymentstatus: str, db: Session = Depends(get_db)):
    new_subscription = Subscription(
        subscriptiontype=subscriptiontype,
        billingcycle=billingcycle,
        startdate=startdate,
        renewaldate=renewaldate,
        paymentstatus=paymentstatus
    )
    db.add(new_subscription)
    db.commit()
    db.refresh(new_subscription)
    return {"subscriptionid": new_subscription.subscriptionid, "subscriptiontype": new_subscription.subscriptiontype, "billingcycle": new_subscription.billingcycle}

# Read Professionals
@router.get("/professionals", response_model=list[dict])
async def read_professionals(db: Session = Depends(get_db)):
    professionals = db.query(Professional).all()
    return [{"professionalid": prof.professionalid, "name": prof.name, "email": prof.email, "maxseats":prof.maxseats, "currentseats":prof.currentseats,"subscriptionid":prof.subscriptionid} for prof in professionals]

# Create Professional
@router.post("/professional/", response_model=dict)
async def create_professional(name: str, email: str, maxseats: int, currentseats: int, subscriptionid: int, db: Session = Depends(get_db)):
    new_professional = Professional(
        name=name,
        email=email,
        maxseats=maxseats,
        currentseats=currentseats,
        subscriptionid=subscriptionid
    )
    db.add(new_professional)
    db.commit()
    db.refresh(new_professional)
    return {"professionalid": new_professional.professionalid, "name": new_professional.name, "email": new_professional.email}
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

@router.get("/metrics", response_model=list[dict])
async def read_metrics(db: Session = Depends(get_db)):
    metrics = db.query(Metrics).all()
    return [{"metricsid": metric.metricsid, "inputtokenusage": metric.inputtokenusage, "outputtokenusage": metric.outputtokenusage, "userid": metric.userid} for metric in metrics]

@router.get("/professionals/{prof_id}/users")
def get_users(prof_id: int, db: Session = Depends(get_db)):
    users = get_users_by_prof_id(db, prof_id)
    return {"users": users}

@router.delete("/professionals/{prof_id}")
def delete_professional(prof_id: int, db: Session = Depends(get_db)):
    try:
        result = delete_professional_by_id(db, prof_id)
        if "error" in result.lower():
            raise HTTPException(status_code=400, detail=result)
        return {"message": result}
    except Exception as e:
        # Log unexpected errors
        return {"error": f"Unexpected error occurred: {str(e)}"}

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

@router.get("/${userId}", response_model=list[dict])
async def get_users(userId: int, db: Session = Depends(get_db)):
    role = get_role(db, userId)
    return {"role": role}

