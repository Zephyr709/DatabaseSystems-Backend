from fastapi import APIRouter


router = APIRouter()


@router.post("/items/")
async def create_item():
    return {"message": "Item created successfully"}

@router.get("/items")
async def read_items():
    return [{"name": "Item One"}, {"name": "Item Two"}]