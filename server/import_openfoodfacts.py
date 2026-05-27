import time
import requests

from server.database import SessionLocal, Base, engine
from server.models import Product

URL = "https://world.openfoodfacts.org/cgi/search.pl"

HEADERS = {
    "User-Agent": "CalCalcV2/1.0 (contact: gythar2772@gmail.com)"
}


def safe_get(params, retries=5):
    for attempt in range(retries):
        response = requests.get(URL, params=params, headers=HEADERS, timeout=30)

        if response.status_code == 200:
            return response

        print(f"Ошибка {response.status_code}. Повтор через 5 секунд...")
        time.sleep(5)

    response.raise_for_status()


def import_products(count=20):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    params = {
        "search_terms": "молоко",
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": count,
        "fields": "product_name,nutriments",
    }

    response = safe_get(params)
    data = response.json()

    added = 0

    for item in data.get("products", []):
        name = item.get("product_name")
        nutriments = item.get("nutriments", {})

        calories = nutriments.get("energy-kcal_100g")
        proteins = nutriments.get("proteins_100g")
        fats = nutriments.get("fat_100g")
        carbs = nutriments.get("carbohydrates_100g")

        if not name or calories is None:
            continue

        exists = db.query(Product).filter(Product.name == name).first()
        if exists:
            continue

        db.add(Product(
            name=name,
            calories=float(calories or 0),
            proteins=float(proteins or 0),
            fats=float(fats or 0),
            carbs=float(carbs or 0),
        ))

        added += 1

    db.commit()
    db.close()

    print(f"Импортировано продуктов: {added}")


if __name__ == "__main__":
    import_products(20)
