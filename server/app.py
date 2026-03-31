from fastapi import FastAPI
from server.database import engine, Base
from server.routes import auth, products, meals

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Nutrition Tracker API",
    description="API для мониторинга рациона питания",
    version="1.0.0",
)

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(meals.router)


@app.get("/")
def root():
    return {"message": "Nutrition Tracker API работает!"}