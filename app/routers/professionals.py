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
