from fastapi import FastAPI, APIRouter, Depends, HTTPException, Request
from models import Item, Subscription, Professional, User, Base, Metrics, DailyMealLog
from functions import get_users_by_prof_id, delete_professional_by_id
from database import get_db, engine, getRole
from sqlalchemy.orm import Session, Query, Mapped
from sqlalchemy.sql import text
from sqlalchemy.inspection import inspect
from sqlalchemy import Integer, String
from typing import ClassVar
# Create database tables
Base.metadata.create_all(bind=engine)


router = APIRouter()

# Create Subscription
@router.post("/subscriptions", response_model=dict)
async def create_subscription(request: Request, db: Session = Depends(get_db)):
    if getRole() == "it_admin":
        data = await request.json()
        new_subscription = Subscription(
            subscriptiontype=data['subscriptiontype'],
            billingcycle=data['billingcycle'],
            startdate=data['startdate'],
            renewaldate=data['renewaldate'],
            paymentstatus=data['paymentstatus']
        )
        db.add(new_subscription)
        db.commit()
        db.refresh(new_subscription)
        return {"subscriptionid": new_subscription.subscriptionid, "subscriptiontype": new_subscription.subscriptiontype, "billingcycle": new_subscription.billingcycle}
    else:
        raise HTTPException(status_code=403, detail="Access Denied")  # 403 Forbidden
# Read Subscriptions
@router.get("/subscriptions", response_model=list[dict])
async def read_subscriptions(db: Session = Depends(get_db)):
    subscriptions = db.query(Subscription).all()
    return [{"subscriptionid": sub.subscriptionid, "subscriptiontype": sub.subscriptiontype, "billingcycle": sub.billingcycle} for sub in subscriptions]

# Update Subscription
@router.put("/subscriptions/{subscriptionid}", response_model=dict)
async def update_subscription(subscriptionid: int, request: Request, db: Session = Depends(get_db)):
    if getRole() == "it_admin":
        data = await request.json()
        subscription = db.query(Subscription).filter(Subscription.subscriptionid == subscriptionid).first()
        subscription.subscriptiontype = data['subscriptiontype']
        subscription.billingcycle = data['billingcycle']

        #These are commented out because they aren't in our menu for 
        #itmes that can be edited so backend screams in pain
        #subscription.startdate = data['startdate']         
        #subscription.renewaldate = data['renewaldate']
        #subscription.paymentstatus = data['paymentstatus']
        
        db.commit()
        db.refresh(subscription)
        return {"subscriptionid": subscription.subscriptionid, "subscriptiontype": subscription.subscriptiontype, "billingcycle": subscription.billingcycle}
    else:
        raise HTTPException(status_code=403, detail="Access Denied")  # 403 Forbidden

# Delete Subscription
@router.delete("/subscriptions/{subscriptionid}", response_model=dict)
async def delete_subscription(subscriptionid: int, db: Session = Depends(get_db)):
    if getRole() == "it_admin":
        subscription = db.query(Subscription).filter(Subscription.subscriptionid == subscriptionid).first()
        db.delete(subscription)
        db.commit()
        return {"subscriptionid": subscription.subscriptionid, "subscriptiontype": subscription.subscriptiontype, "billingcycle": subscription.billingcycle}
    else:
        raise HTTPException(status_code=403, detail="Access Denied")  # 403 Forbidden
# Get subscription by ID
@router.get("/subscriptions/{subscriptionid}")
async def get_subscription(subscriptionid: int, db: Session = Depends(get_db)):
    subscription = db.query(Subscription).filter(Subscription.subscriptionid == subscriptionid).first()
    return {"subscriptionid": subscription.subscriptionid, "subscriptiontype": subscription.subscriptiontype, "billingcycle": subscription.billingcycle}