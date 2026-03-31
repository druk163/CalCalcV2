from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from server.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    age = Column(Integer, nullable=True)
    weight = Column(Float, nullable=True)
    height = Column(Float, nullable=True)
    gender = Column(String(10), nullable=True)
    activity_level = Column(Float, default=1.55)
    daily_goal_kcal = Column(Float, default=2000.0)

    meals = relationship("Meal", back_populates="user")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    calories = Column(Float, nullable=False)
    proteins = Column(Float, default=0.0)
    fats = Column(Float, default=0.0)
    carbs = Column(Float, default=0.0)

    meal_items = relationship("MealItem", back_populates="product")


class Meal(Base):
    __tablename__ = "meals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False)
    meal_type = Column(String(20), nullable=False)

    user = relationship("User", back_populates="meals")
    items = relationship("MealItem", back_populates="meal", cascade="all, delete-orphan")


class MealItem(Base):
    __tablename__ = "meal_items"

    id = Column(Integer, primary_key=True, index=True)
    meal_id = Column(Integer, ForeignKey("meals.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    weight_grams = Column(Float, nullable=False)

    meal = relationship("Meal", back_populates="items")
    product = relationship("Product", back_populates="meal_items")