"""
Products API tests for AutomationExercise.com.
"""
import pytest
import time
from src.fixtures.test_data_fixtures import products_controller, api_test_data


@pytest.mark.api
class TestProductsAPI:
    """Test class for Products API endpoints."""
    
    def test_get_all_products_list_success(self, products_controller, api_test_data):
        """
        API 1: GET All Products List - Should return 200 with products data.
        
        Validates that the GET All Products endpoint returns 200 status with proper products data structure.
        """
        # Act
        response = products_controller.get_all_products()
        
        # Assert
        assert response["status"] == 200
        assert "responseCode" in response["data"]
        assert response["data"]["responseCode"] == 200
        assert "products" in response["data"]
        assert isinstance(response["data"]["products"], list)
        assert len(response["data"]["products"]) > 0
        
        # Use fixture data for validation
        assert len(response["data"]["products"]) >= api_test_data["products_data"]["expected_product_count"]
        
        # Validate product structure
        first_product = response["data"]["products"][0]
        assert "id" in first_product
        assert "name" in first_product
        assert "price" in first_product
        assert "brand" in first_product
        assert "category" in first_product
        assert "usertype" in first_product["category"]
        assert "category" in first_product["category"]
    
    def test_post_to_products_list_method_not_allowed(self, products_controller):
        """
        API 2: POST To All Products List - Should return 405 Method Not Allowed.
        
        Validates that the POST method on products list endpoint returns 405 Method Not Allowed error.
        """
        # Act
        response = products_controller.post_to_products_list()
        
        # Assert
        assert response["status"] == 200
        assert "responseCode" in response["data"]
        assert response["data"]["responseCode"] == 405
        assert "message" in response["data"]
        assert response["data"]["message"] == "This request method is not supported."
    
    def test_search_product_success(self, products_controller, api_test_data):
        """
        API 5: POST To Search Product - Should return 200 with filtered products.
        
        Validates that the search product endpoint returns filtered products based on search term.
        """
        # Arrange
        search_term = api_test_data["products_data"]["search_terms"]["valid"][0]
        
        # Act
        response = products_controller.search_product(search_term)
        
        # Assert
        assert response["status"] == 200
        assert "responseCode" in response["data"]
        assert response["data"]["responseCode"] == 200
        assert "products" in response["data"]
        assert isinstance(response["data"]["products"], list)
        
        # Verify search results contain the search term
        if len(response["data"]["products"]) > 0:
            search_results = any(
                search_term.lower() in product["name"].lower() 
                for product in response["data"]["products"]
            )
            assert search_results, f"Search results should contain '{search_term}'"
    
    def test_search_product_without_parameter_bad_request(self, products_controller):
        """
        API 6: POST To Search Product without parameter - Should return 400 Bad Request.
        
        Validates that searching without required parameter returns 400 Bad Request error.
        """
        # Act
        response = products_controller.search_product_without_parameter()
        
        # Assert
        assert response["status"] == 200
        assert "responseCode" in response["data"]
        assert response["data"]["responseCode"] == 400
        assert "message" in response["data"]
        assert response["data"]["message"] == "Bad request, search_product parameter is missing in POST request."
    
    def test_search_different_product_categories(self, products_controller, api_test_data):
        """
        Search for different product categories.
        
        Tests product search functionality across multiple product categories (dress, tshirt, jean).
        """
        search_terms = api_test_data["products_data"]["search_terms"]["valid"]
        
        for term in search_terms:
            response = products_controller.search_product(term)
            
            assert response["status"] == 200
            assert "products" in response["data"]
            assert isinstance(response["data"]["products"], list)
    
    def test_verify_product_data_integrity(self, products_controller):
        """
        Verify product data integrity.
        
        Validates that all products have required fields and proper data structure integrity.
        """
        # Get all products
        response = products_controller.get_all_products()
        
        assert response["status"] == 200
        assert len(response["data"]["products"]) > 0
        
        # Check each product has required fields
        for i, product in enumerate(response["data"]["products"]):
            assert "id" in product, f"Product {i} should have id"
            assert product["id"] is not None, f"Product {i} id should not be None"
            
            assert "name" in product, f"Product {i} should have name"
            assert product["name"], f"Product {i} name should not be empty"
            
            assert "price" in product, f"Product {i} should have price"
            assert product["price"], f"Product {i} price should not be empty"
            
            assert "brand" in product, f"Product {i} should have brand"
            assert product["brand"], f"Product {i} brand should not be empty"
            
            assert "category" in product, f"Product {i} should have category"
            assert product["category"] is not None, f"Product {i} category should not be None"
    
    def test_api_performance_response_time(self, products_controller):
        """
        API Performance - Response time should be under 5 seconds.
        
        Validates that the products endpoint responds within acceptable time limits (under 5 seconds).
        """
        start_time = time.time()
        
        response = products_controller.get_all_products()
        
        response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        assert response["status"] == 200
        assert response_time < 5000, f"Response time {response_time}ms should be under 5000ms"
    
    def test_search_product_with_special_characters(self, products_controller):
        """
        Test search product with special characters.
        
        Tests that search functionality handles special characters properly.
        """
        special_terms = ["dress!", "tshirt@", "jean#", "top$", "shirt%"]
        
        for term in special_terms:
            response = products_controller.search_product(term)
            
            # Should not crash and should return a valid response
            assert response["status"] == 200
            assert "products" in response["data"]
            assert isinstance(response["data"]["products"], list)
    
    def test_search_product_case_insensitive(self, products_controller):
        """
        Test search product case insensitive.
        
        Tests that search is case insensitive.
        """
        search_terms = ["DRESS", "Tshirt", "JEAN", "Top", "Shirt"]
        
        for term in search_terms:
            response = products_controller.search_product(term)
            
            assert response["status"] == 200
            assert "products" in response["data"]
            assert isinstance(response["data"]["products"], list)
    
    def test_get_all_products_pagination(self, products_controller):
        """
        Test products list pagination.
        
        Tests that products list can handle pagination if implemented.
        """
        response = products_controller.get_all_products()
        
        assert response["status"] == 200
        assert "products" in response["data"]
        
        products = response["data"]["products"]
        assert len(products) > 0, "Should have products"
        
        # Verify products are properly ordered (if pagination is implemented)
        if len(products) > 1:
            # Check that products have sequential IDs or are properly ordered
            product_ids = [product["id"] for product in products]
            assert len(set(product_ids)) == len(product_ids), "Product IDs should be unique"
    
    def test_products_api_error_handling(self, products_controller):
        """
        Test products API error handling.
        
        Tests that the API handles various error conditions gracefully.
        """
        # Test with invalid search term
        response = products_controller.search_product("nonexistent_product_xyz")
        
        assert response["status"] == 200
        assert "products" in response["data"]
        # Should return empty results for non-existent product
        assert len(response["data"]["products"]) == 0
    
    def test_products_api_data_consistency(self, products_controller):
        """
        Test products API data consistency.
        
        Tests that the API returns consistent data across multiple calls.
        """
        # Make multiple calls to the same endpoint
        responses = []
        for _ in range(3):
            response = products_controller.get_all_products()
            responses.append(response)
        
        # All responses should be successful
        for response in responses:
            assert response["status"] == 200
            assert "products" in response["data"]
        
        # All responses should have the same number of products
        product_counts = [len(response["data"]["products"]) for response in responses]
        assert len(set(product_counts)) == 1, "Product count should be consistent across calls"
        
        # All responses should have the same product IDs
        product_ids = [set(product["id"] for product in response["data"]["products"]) for response in responses]
        assert all(ids == product_ids[0] for ids in product_ids), "Product IDs should be consistent across calls"
