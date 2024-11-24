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

@router.get("/metrics", response_model=list[dict])
async def read_metrics(db: Session = Depends(get_db)):
    metrics = db.query(Metrics).all()
    return [{"metricsid": metric.metricsid, "inputtokenusage": metric.inputtokenusage, "outputtokenusage": metric.outputtokenusage, "userid": metric.userid} for metric in metrics]
