from fastapi import APIRouter


router = APIRouter()


router.post("/items/")
def create_item():
    return {"message": "Item created successfully"}
