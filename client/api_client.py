import requests

BASE_URL = "http://127.0.0.1:8000"


class ApiClient:
    def __init__(self):
        self.base_url = BASE_URL
        self.current_user = None

    def register(self, username, password, age=None, weight=None,
                 height=None, gender=None):
        response = requests.post(f"{self.base_url}/auth/register", json={
            "username": username,
            "password": password,
            "age": age,
            "weight": weight,
            "height": height,
            "gender": gender,
        })
        if response.status_code == 200:
            self.current_user = response.json()
        return response

    def login(self, username, password):
        response = requests.post(f"{self.base_url}/auth/login", json={
            "username": username,
            "password": password,
        })
        if response.status_code == 200:
            self.current_user = response.json()
        return response

    def get_products(self, search=""):
        return requests.get(
            f"{self.base_url}/products/",
            params={"search": search}
        )

    def add_product(self, name, calories, proteins=0, fats=0, carbs=0):
        return requests.post(f"{self.base_url}/products/", json={
            "name": name,
            "calories": calories,
            "proteins": proteins,
            "fats": fats,
            "carbs": carbs,
        })

    def delete_product(self, product_id):
        return requests.delete(f"{self.base_url}/products/{product_id}")

    def add_meal(self, date, meal_type, items):
        return requests.post(f"{self.base_url}/meals/", json={
            "user_id": self.current_user["id"],
            "date": date,
            "meal_type": meal_type,
            "items": items,
        })

    def get_daily_summary(self, date):
        user_id = self.current_user["id"]
        return requests.get(
            f"{self.base_url}/meals/daily/{user_id}/{date}"
        )

    def delete_meal(self, meal_id):
        return requests.delete(f"{self.base_url}/meals/{meal_id}")
