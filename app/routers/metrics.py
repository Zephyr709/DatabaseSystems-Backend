from fastapi import FastAPI, APIRouter, Depends, HTTPException
from models import Item, Subscription, Professional, User, Base, Metrics, DailyMealLog
from functions import get_users_by_prof_id, delete_professional_by_id
from database import get_db, engine
from sqlalchemy.orm import Session, Query, mapped_column, Mapped
from sqlalchemy.sql import text
from sqlalchemy.inspection import inspect
from sqlalchemy import Integer, String
from typing import ClassVar
# Create database tables
Base.metadata.create_all(bind=engine)


router = APIRouter()

# Read Metrics
@router.get("/metrics", response_model=list[dict])
async def read_metrics(db: Session = Depends(get_db)):
    metrics = db.query(Metrics).all()
    return [{"metricsid": metric.metricsid, "inputtokenusage": metric.inputtokenusage, "outputtokenusage": metric.outputtokenusage, "userid": metric.userid} for metric in metrics]

# Create Metrics
@router.post("/metrics", response_model=dict)
async def create_metrics(inputtokenusage: int, outputtokenusage: int, userid: int, db: Session = Depends(get_db)):
    new_metrics = Metrics(
        inputtokenusage=inputtokenusage,
        outputtokenusage=outputtokenusage,
        userid=userid
    )
    db.add(new_metrics)
    db.commit()
    db.refresh(new_metrics)
    return {"metricsid": new_metrics.metricsid, "inputtokenusage": new_metrics.inputtokenusage, "outputtokenusage": new_metrics.outputtokenusage, "userid": new_metrics.userid}

# Update Metrics
@router.put("/metrics/{metricsid}", response_model=dict)
async def update_metrics(metricsid: int, inputtokenusage: int, outputtokenusage: int, userid: int, db: Session = Depends(get_db)):
    metrics = db.query(Metrics).filter(Metrics.metricsid == metricsid).first()
    metrics.inputtokenusage = inputtokenusage
    metrics.outputtokenusage = outputtokenusage
    metrics.userid = userid
    db.commit()
    db.refresh(metrics)
    return {"metricsid": metrics.metricsid, "inputtokenusage": metrics.inputtokenusage, "outputtokenusage": metrics.outputtokenusage, "userid": metrics.userid}

# Delete Metrics
@router.delete("/metrics/{metricsid}", response_model=dict)
async def delete_metrics(metricsid: int, db: Session = Depends(get_db)):
    metrics = db.query(Metrics).filter(Metrics.metricsid == metricsid).first()
    db.delete(metrics)
    db.commit()
    return {"metricsid": metrics.metricsid, "inputtokenusage": metrics.inputtokenusage, "outputtokenusage": metrics.outputtokenusage, "userid": metrics.userid}

# Get Metrics by ID
@router.get("/metrics/{metricsid}")
async def get_metrics(metricsid: int, db: Session = Depends(get_db)):
    metrics = db.query(Metrics).filter(Metrics.metricsid == metricsid).first()
    return {"metricsid": metrics.metricsid, "inputtokenusage": metrics.inputtokenusage, "outputtokenusage": metrics.outputtokenusage, "userid": metrics.userid}