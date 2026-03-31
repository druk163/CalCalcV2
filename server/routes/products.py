from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from server.database import get_db
from server.models import Product

router = APIRouter(prefix="/products", tags=["products"])


class ProductCreate(BaseModel):
    name: str
    calories: float
    proteins: float = 0.0
    fats: float = 0.0
    carbs: float = 0.0


class ProductResponse(BaseModel):
    id: int
    name: str
    calories: float
    proteins: float
    fats: float
    carbs: float

    class Config:
        from_attributes = True


@router.get("/", response_model=list[ProductResponse])
def get_products(search: str = "", db: Session = Depends(get_db)):
    query = db.query(Product)
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))
    return query.all()


@router.post("/", response_model=ProductResponse)
def create_product(data: ProductCreate, db: Session = Depends(get_db)):
    product = Product(**data.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Продукт не найден")
    db.delete(product)
    db.commit()
    return {"message": "Продукт удалён"}