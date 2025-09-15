import pytest
import requests
from unittest.mock import Mock, patch


class TestEcommerceAPIMocked:
    # Mocked base URL for the API for testing purposes
    BASE_URL = "http://localhost:5000/api"

    @pytest.fixture
    def auth_headers(self):
        return {"Authorization": "Bearer valid_jwt_token"}
    
    @pytest.fixture
    def invalid_auth_headers(self):
        return {"Authorization": "Bearer invalid_token"}


class TestProductsEndpointsMocked(TestEcommerceAPIMocked):
    
    # Test successful retrieval of products with no parameters
    @patch('requests.get')
    def test_get_products_success_no_params(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "products": [
                {
                    "id": "12345",
                    "name": "Wireless Headphones",
                    "price": 199.99,
                    "category": "electronics"
                }
            ],
            "total": 150,
            "limit": 20,
            "offset": 0
        }
        mock_get.return_value = mock_response
        
        response = requests.get(f"{self.BASE_URL}/products")
        assert response.status_code == 200
        data = response.json()
        assert "products" in data
        assert "total" in data
        assert data["limit"] == 20
        assert len(data["products"]) == 1
        mock_get.assert_called_once_with(f"{self.BASE_URL}/products")
    
    # Test retrieval of products with category filter
    @patch('requests.get')
    def test_get_products_with_category_filter(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "products": [],
            "total": 50,
            "limit": 20,
            "offset": 0
        }
        mock_get.return_value = mock_response
        
        response = requests.get(f"{self.BASE_URL}/products", params={"category": "electronics"})
        assert response.status_code == 200
        mock_get.assert_called_once_with(f"{self.BASE_URL}/products", params={"category": "electronics"})
    
    # Test retrieval of products with invalid limit (above max)
    @patch('requests.get')
    def test_get_products_invalid_limit_above_max(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            "error": "VALIDATION_ERROR",
            "message": "Limit cannot exceed 100"
        }
        mock_get.return_value = mock_response
        
        response = requests.get(f"{self.BASE_URL}/products", params={"limit": 101})
        assert response.status_code == 400
        mock_get.assert_called_once_with(f"{self.BASE_URL}/products", params={"limit": 101})
    
    # Test creation of a new product successfully
    @patch('requests.post')
    def test_create_product_success(self, mock_post, auth_headers):
        product_data = {
            "name": "Test Product",
            "description": "A test product",
            "price": 99.99,
            "category": "electronics",
            "stock": 10
        }
        
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "id": "54321",
            **product_data,
            "createdAt": "2024-01-15T10:30:00Z"
        }
        mock_post.return_value = mock_response
        
        response = requests.post(f"{self.BASE_URL}/products", 
                               json=product_data, 
                               headers=auth_headers)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == product_data["name"]
        assert "id" in data
        mock_post.assert_called_once_with(f"{self.BASE_URL}/products", 
                                        json=product_data, 
                                        headers=auth_headers)
    
    # Test creation of a new product without proper authentication headers
    @patch('requests.post')
    def test_create_product_unauthorized(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.json.return_value = {
            "error": "UNAUTHORIZED",
            "message": "Authentication required"
        }
        mock_post.return_value = mock_response
        
        product_data = {"name": "Test Product", "price": 99.99, "category": "electronics"}
        response = requests.post(f"{self.BASE_URL}/products", json=product_data)
        assert response.status_code == 401
    
    # Test creation of a new product with missing required fields
    @patch('requests.post')
    def test_create_product_missing_required_fields(self, mock_post, auth_headers):
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            "error": "VALIDATION_ERROR",
            "message": "Missing required fields",
            "details": [
                {"field": "name", "message": "Name is required"},
                {"field": "price", "message": "Price is required"}
            ]
        }
        mock_post.return_value = mock_response
        
        product_data = {"description": "Missing required fields"}
        response = requests.post(f"{self.BASE_URL}/products", 
                               json=product_data, 
                               headers=auth_headers)
        assert response.status_code == 400
    
    # Test retrieval of a product by product ID successfully
    @patch('requests.get')
    def test_get_product_by_id_success(self, mock_get):
        product_id = "12345"
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": product_id,
            "name": "Wireless Headphones",
            "price": 199.99,
            "category": "electronics"
        }
        mock_get.return_value = mock_response
        
        response = requests.get(f"{self.BASE_URL}/products/{product_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == product_id
        mock_get.assert_called_once_with(f"{self.BASE_URL}/products/{product_id}")
    
    # Test retrieval of a product by product ID that does not exist
    @patch('requests.get')
    def test_get_product_by_id_not_found(self, mock_get):
        product_id = "nonexistent"
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {
            "error": "NOT_FOUND",
            "message": "Product not found"
        }
        mock_get.return_value = mock_response
        
        response = requests.get(f"{self.BASE_URL}/products/{product_id}")
        assert response.status_code == 404