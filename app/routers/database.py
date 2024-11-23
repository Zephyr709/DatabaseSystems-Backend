from fastapi import FastAPI, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Item, Subscription, Professional, User, Base
from functions import get_users_by_prof_id, delete_professional_by_id, get_specific_user_by_id
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

# Read Users
@router.get("/users", response_model=list[dict])
async def read_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [{"userid": user.userid, "name": user.name, "email": user.email, "country": user.country} for user in users]

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
    

#Added in branch
@router.get("/users/{sUserID}")
def get_specific_user(sUserID: int, db: Session = Depends(get_db)):
    
    #user = db.query(User).filter(User.userid == sUserID).first()
    #return {"userid": user.userid, "name": user.name, "email": user.email, "country": user.country}

    
    user = get_specific_user_by_id(db, sUserID)
    return {"user": user}