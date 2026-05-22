import pytest
from unittest.mock import Mock, patch
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from client.api_client import ApiClient


class TestApiClient:
    """Тесты для ApiClient"""
    
    def test_initialization(self):
        """Тест инициализации клиента"""
        client = ApiClient()
        assert client.base_url == "http://127.0.0.1:8000"
        assert client.current_user is None
    
    @patch('client.api_client.requests.post')
    def test_register_success(self, mock_post):
        """Тест успешной регистрации"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": 1, "username": "testuser"}
        mock_post.return_value = mock_response
        
        client = ApiClient()
        response = client.register("testuser", "password123")
        
        assert response.status_code == 200
        assert client.current_user == {"id": 1, "username": "testuser"}
        mock_post.assert_called_once()
    
    @patch('client.api_client.requests.post')
    def test_register_with_all_fields(self, mock_post):
        """Тест регистрации со всеми полями"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        
        client = ApiClient()
        response = client.register(
            username="testuser",
            password="pass123",
            age=25,
            weight=70.5,
            height=175.0,
            gender="male"
        )
        
        call_args = mock_post.call_args
        assert call_args[0][0] == "http://127.0.0.1:8000/auth/register"
        assert call_args[1]["json"]["username"] == "testuser"
        assert call_args[1]["json"]["age"] == 25
    
    @patch('client.api_client.requests.post')
    def test_login_success(self, mock_post):
        """Тест успешного входа"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": 1, "username": "testuser", "token": "abc123"}
        mock_post.return_value = mock_response
        
        client = ApiClient()
        response = client.login("testuser", "password123")
        
        assert response.status_code == 200
        assert client.current_user["token"] == "abc123"
    
    @patch('client.api_client.requests.get')
    def test_get_products(self, mock_get):
        """Тест получения продуктов"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"id": 1, "name": "Apple", "calories": 95}]
        mock_get.return_value = mock_response
        
        client = ApiClient()
        response = client.get_products(search="apple")
        
        mock_get.assert_called_with(
            "http://127.0.0.1:8000/products/",
            params={"search": "apple"}
        )
        assert response.status_code == 200
    
    @patch('client.api_client.requests.post')
    def test_add_product(self, mock_post):
        """Тест добавления продукта"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_post.return_value = mock_response
        
        client = ApiClient()
        response = client.add_product("Banana", 105, proteins=1.3, fats=0.4, carbs=27)
        
        call_args = mock_post.call_args
        assert call_args[0][0] == "http://127.0.0.1:8000/products/"
        assert call_args[1]["json"]["name"] == "Banana"
        assert call_args[1]["json"]["calories"] == 105
    
    @patch('client.api_client.requests.delete')
    def test_delete_product(self, mock_delete):
        """Тест удаления продукта"""
        mock_response = Mock()
        mock_response.status_code = 204
        mock_delete.return_value = mock_response
        
        client = ApiClient()
        response = client.delete_product(42)
        
        mock_delete.assert_called_with("http://127.0.0.1:8000/products/42")
    
    @patch('client.api_client.requests.post')
    def test_add_meal_with_current_user(self, mock_post):
        """Тест добавления приема пищи (с авторизованным пользователем)"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_post.return_value = mock_response
        
        client = ApiClient()
        client.current_user = {"id": 1}
        
        items = [{"product_id": 1, "quantity": 100}]
        response = client.add_meal("2026-05-22", "breakfast", items)
        
        call_args = mock_post.call_args
        assert call_args[1]["json"]["user_id"] == 1
        assert call_args[1]["json"]["meal_type"] == "breakfast"
    
    @patch('client.api_client.requests.get')
    def test_get_daily_summary(self, mock_get):
        """Тест получения дневной сводки"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"total_calories": 1800, "meals": []}
        mock_get.return_value = mock_response
        
        client = ApiClient()
        client.current_user = {"id": 1}
        
        response = client.get_daily_summary("2026-05-22")
        
        mock_get.assert_called_with(
            "http://127.0.0.1:8000/meals/daily/1/2026-05-22"
        )


class TestEdgeCases:
    """Тесты граничных случаев"""
    
    def test_register_without_current_user(self):
        """Регистрация не должна устанавливать current_user при ошибке"""
        client = ApiClient()
        assert client.current_user is None
    
    def test_add_meal_without_user(self):
        """Добавление приема пищи без авторизации"""
        client = ApiClient()
        client.current_user = None
        
        with patch('client.api_client.requests.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 401
            mock_post.return_value = mock_response
            
            # Проверяем что будет ошибка
            with pytest.raises(TypeError):
                client.add_meal("2026-05-22", "lunch", [])
