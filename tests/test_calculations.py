import pytest


class TestNutritionCalculations:
    """Тесты для расчетов питания (3 обязательные функции для лабы)"""
    
    def test_calculate_bmi(self):
        """Функция 1: Расчет ИМТ"""
        def calculate_bmi(weight_kg, height_m):
            if height_m <= 0:
                return 0
            return weight_kg / (height_m ** 2)
        
        # Тесты с округлением
        assert round(calculate_bmi(70, 1.75), 2) == 22.86
        assert round(calculate_bmi(50, 1.60), 2) == 19.53
        assert calculate_bmi(0, 1.75) == 0
    
    def test_calories_per_kg(self):
        """Функция 2: Расчет калорий на кг веса"""
        def calculate_calories_per_kg(weight, calories_per_kg=30):
            return weight * calories_per_kg
        
        assert calculate_calories_per_kg(70) == 2100
        assert calculate_calories_per_kg(80, 32) == 2560
        assert calculate_calories_per_kg(0) == 0
    
    def test_macro_percentage(self):
        """Функция 3: Расчет процента БЖУ от калорий"""
        def calculate_macro_percentage(total_calories, macro_calories):
            if total_calories <= 0:
                return 0
            return (macro_calories / total_calories) * 100
        
        assert calculate_macro_percentage(2000, 500) == 25.0
        assert calculate_macro_percentage(1500, 450) == 30.0
        assert calculate_macro_percentage(0, 100) == 0
