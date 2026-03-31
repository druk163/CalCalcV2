from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import date

from server.database import get_db
from server.models import Meal, MealItem, Product

router = APIRouter(prefix="/meals", tags=["meals"])


class MealItemCreate(BaseModel):
    product_id: int
    weight_grams: float


class MealCreate(BaseModel):
    user_id: int
    date: date
    meal_type: str
    items: list[MealItemCreate]


@router.post("/")
def create_meal(data: MealCreate, db: Session = Depends(get_db)):
    meal = Meal(
        user_id=data.user_id,
        date=data.date,
        meal_type=data.meal_type,
    )
    db.add(meal)
    db.flush()

    for item_data in data.items:
        product = db.query(Product).filter(Product.id == item_data.product_id).first()
        if not product:
            raise HTTPException(
                status_code=404,
                detail=f"Продукт {item_data.product_id} не найден"
            )
        item = MealItem(
            meal_id=meal.id,
            product_id=item_data.product_id,
            weight_grams=item_data.weight_grams,
        )
        db.add(item)

    db.commit()
    return {"message": "Приём пищи добавлен", "meal_id": meal.id}


@router.get("/daily/{user_id}/{day}")
def get_daily_summary(user_id: int, day: date, db: Session = Depends(get_db)):
    meals = db.query(Meal).filter(
        Meal.user_id == user_id,
        Meal.date == day
    ).all()

    total_cal = 0
    total_prot = 0
    total_fat = 0
    total_carb = 0
    meals_data = []

    for meal in meals:
        meal_cal = 0
        meal_prot = 0
        meal_fat = 0
        meal_carb = 0
        items_data = []

        for item in meal.items:
            cal = item.product.calories * item.weight_grams / 100
            prot = item.product.proteins * item.weight_grams / 100
            fat = item.product.fats * item.weight_grams / 100
            carb = item.product.carbs * item.weight_grams / 100

            meal_cal += cal
            meal_prot += prot
            meal_fat += fat
            meal_carb += carb

            items_data.append({
                "id": item.id,
                "product_id": item.product_id,
                "product_name": item.product.name,
                "weight_grams": item.weight_grams,
                "calories": round(cal, 1),
                "proteins": round(prot, 1),
                "fats": round(fat, 1),
                "carbs": round(carb, 1),
            })

        total_cal += meal_cal
        total_prot += meal_prot
        total_fat += meal_fat
        total_carb += meal_carb

        meals_data.append({
            "id": meal.id,
            "meal_type": meal.meal_type,
            "date": str(meal.date),
            "items": items_data,
            "total_calories": round(meal_cal, 1),
            "total_proteins": round(meal_prot, 1),
            "total_fats": round(meal_fat, 1),
            "total_carbs": round(meal_carb, 1),
        })

    return {
        "date": str(day),
        "total_calories": round(total_cal, 1),
        "total_proteins": round(total_prot, 1),
        "total_fats": round(total_fat, 1),
        "total_carbs": round(total_carb, 1),
        "meals": meals_data,
    }


@router.delete("/{meal_id}")
def delete_meal(meal_id: int, db: Session = Depends(get_db)):
    meal = db.query(Meal).filter(Meal.id == meal_id).first()
    if not meal:
        raise HTTPException(status_code=404, detail="Приём пищи не найден")
    db.delete(meal)
    db.commit()
    return {"message": "Приём пищи удалён"}