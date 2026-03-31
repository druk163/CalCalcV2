from server.database import SessionLocal, engine, Base
from server.models import Product

Base.metadata.create_all(bind=engine)

PRODUCTS = [
    {"name": "Куриная грудка", "calories": 165, "proteins": 31, "fats": 3.6, "carbs": 0},
    {"name": "Рис белый (варёный)", "calories": 130, "proteins": 2.7, "fats": 0.3, "carbs": 28},
    {"name": "Гречка (варёная)", "calories": 110, "proteins": 4.2, "fats": 1.1, "carbs": 21},
    {"name": "Яйцо куриное", "calories": 155, "proteins": 13, "fats": 11, "carbs": 1.1},
    {"name": "Молоко 2.5%", "calories": 52, "proteins": 2.8, "fats": 2.5, "carbs": 4.7},
    {"name": "Хлеб белый", "calories": 265, "proteins": 9, "fats": 3.2, "carbs": 49},
    {"name": "Банан", "calories": 89, "proteins": 1.1, "fats": 0.3, "carbs": 23},
    {"name": "Яблоко", "calories": 52, "proteins": 0.3, "fats": 0.2, "carbs": 14},
    {"name": "Творог 5%", "calories": 121, "proteins": 17, "fats": 5, "carbs": 1.8},
    {"name": "Овсянка (варёная)", "calories": 68, "proteins": 2.4, "fats": 1.4, "carbs": 12},
    {"name": "Макароны (варёные)", "calories": 131, "proteins": 5, "fats": 1.1, "carbs": 25},
    {"name": "Говядина", "calories": 250, "proteins": 26, "fats": 15, "carbs": 0},
    {"name": "Сёмга", "calories": 208, "proteins": 20, "fats": 13, "carbs": 0},
    {"name": "Картофель (варёный)", "calories": 82, "proteins": 2, "fats": 0.4, "carbs": 17},
    {"name": "Огурец", "calories": 15, "proteins": 0.7, "fats": 0.1, "carbs": 3.6},
    {"name": "Помидор", "calories": 18, "proteins": 0.9, "fats": 0.2, "carbs": 3.9},
    {"name": "Сыр твёрдый", "calories": 350, "proteins": 25, "fats": 27, "carbs": 0},
    {"name": "Кефир 1%", "calories": 40, "proteins": 3, "fats": 1, "carbs": 4},
    {"name": "Масло сливочное", "calories": 748, "proteins": 0.5, "fats": 82, "carbs": 0.8},
    {"name": "Сахар", "calories": 387, "proteins": 0, "fats": 0, "carbs": 100},
]


def seed():
    db = SessionLocal()
    existing = db.query(Product).count()
    if existing > 0:
        print(f"В базе уже есть {existing} продуктов. Пропускаю.")
        db.close()
        return

    for p in PRODUCTS:
        db.add(Product(**p))

    db.commit()
    print(f"Добавлено {len(PRODUCTS)} продуктов в базу данных.")
    db.close()


if __name__ == "__main__":
    seed()