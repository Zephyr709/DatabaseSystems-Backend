from fastapi import FastAPI, APIRouter, Depends, HTTPException, Request
from models import Item, Subscription, Professional, User, Base, Metrics, DailyMealLog
from functions import get_users_by_prof_id, delete_professional_by_id
from database import get_db, engine, getRole
from sqlalchemy.orm import Session, Query, mapped_column, Mapped
from sqlalchemy.sql import text
from sqlalchemy.inspection import inspect
from sqlalchemy import Integer, String
from typing import ClassVar
# Create database tables
Base.metadata.create_all(bind=engine)


router = APIRouter()
# Create Professional
@router.post("/professionals", response_model=dict)
async def create_professional(request: Request, db: Session = Depends(get_db)):
    if getRole() == "it_admin":
        data = await request.json()
        new_professional = Professional(
            name=data['name'],
            email=data['email'],
            maxseats=data['maxseats'],
            currentseats=0,
            subscriptionid=data['subscriptionid']
        )
        db.add(new_professional)
        db.commit()
        db.refresh(new_professional)
        return {"professionalid": new_professional.professionalid, "name": new_professional.name, "email": new_professional.email,"maxseats":new_professional.maxseats,"currentseats":new_professional.currentseats,"subscriptionid":new_professional.subscriptionid }
    else:
        raise HTTPException(status_code=403, detail="Access Denied")  # 403 Forbidden

# Read Professionals
@router.get("/professionals", response_model=list[dict])
async def read_professionals(db: Session = Depends(get_db)):
    professionals = db.query(Professional).all()
    return [{"professionalid": prof.professionalid, "name": prof.name, "email": prof.email, "maxseats":prof.maxseats, "currentseats":prof.currentseats,"subscriptionid":prof.subscriptionid} for prof in professionals]

# Update Professional
@router.put("/professionals/{professionalid}", response_model=dict)
async def update_professional(professionalid: int, request: Request, db: Session = Depends(get_db)):
    if getRole() == "it_admin":
        data = await request.json()
        professional = db.query(Professional).filter(Professional.professionalid == professionalid).first()
        professional.name = data['name']
        professional.email = data['email']
        professional.maxseats = data['maxseats']
        professional.currentseats = data['currentseats']
        professional.subscriptionid = data['subscriptionid']
        db.commit()
        db.refresh(professional)
        return {"professionalid": professional.professionalid, "name": professional.name, "email": professional.email, "maxseats": professional.maxseats, "currentseats": professional.currentseats, "subscriptionid": professional.subscriptionid}
    else:
        raise HTTPException(status_code=403, detail="Access Denied")  # 403 Forbidden

# Delete Professional
@router.delete("/professionals/{professionalid}", response_model=dict)
async def delete_professional(professionalid: int, db: Session = Depends(get_db)):
    if getRole() == "it_admin":
        professional = db.query(Professional).filter(Professional.professionalid == professionalid).first()
        if professional:
            db.delete(professional)
            db.commit()
            return {
                "professionalid": professional.professionalid,
                "name": professional.name,
                "email": professional.email,
                "maxseats": professional.maxseats,
                "currentseats": professional.currentseats,
                "subscriptionid": professional.subscriptionid,
            }
        else:
            raise HTTPException(status_code=404, detail="Professional not found")
    else:
        raise HTTPException(status_code=403, detail="Access Denied")  # 403 Forbidden

# Get Professional by ID
@router.get("/professionals/{professionalid}")
async def get_professional(professionalid: int, db: Session = Depends(get_db)):
    professional = db.query(Professional).filter(Professional.professionalid == professionalid).first()
    return {
        "professionalid": professional.professionalid,
        "name": professional.name,
        "email": professional.email,
        "maxseats": professional.maxseats,
        "currentseats": professional.currentseats,
        "subscriptionid": professional.subscriptionid,
    }


# Read Users by Professional ID
@router.get("/professionals/{prof_id}/users")
async def get_users(prof_id: int, db: Session = Depends(get_db)):
    users = get_users_by_prof_id(db, prof_id)
    return users
