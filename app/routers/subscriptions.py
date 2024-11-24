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

# Read Subscriptions
@router.get("/subscriptions", response_model=list[dict])
async def read_subscriptions(db: Session = Depends(get_db)):
    subscriptions = db.query(Subscription).all()
    return [{"subscriptionid": sub.subscriptionid, "subscriptiontype": sub.subscriptiontype, "billingcycle": sub.billingcycle} for sub in subscriptions]

# Update Subscription
@router.put("/subscriptions/{subscriptionid}", response_model=dict)
async def update_subscription(subscriptionid: int, subscriptiontype: str, billingcycle: str, startdate: str, renewaldate: str, paymentstatus: str, db: Session = Depends(get_db)):
    subscription = db.query(Subscription).filter(Subscription.subscriptionid == subscriptionid).first()
    subscription.subscriptiontype = subscriptiontype
    subscription.billingcycle = billingcycle
    subscription.startdate = startdate
    subscription.renewaldate = renewaldate
    subscription.paymentstatus = paymentstatus
    db.commit()
    db.refresh(subscription)
    return {"subscriptionid": subscription.subscriptionid, "subscriptiontype": subscription.subscriptiontype, "billingcycle": subscription.billingcycle}

# Delete Subscription
@router.delete("/subscriptions/{subscriptionid}", response_model=dict)
async def delete_subscription(subscriptionid: int, db: Session = Depends(get_db)):
    subscription = db.query(Subscription).filter(Subscription.subscriptionid == subscriptionid).first()
    db.delete(subscription)
    db.commit()
    return {"subscriptionid": subscription.subscriptionid, "subscriptiontype": subscription.subscriptiontype, "billingcycle": subscription.billingcycle}

