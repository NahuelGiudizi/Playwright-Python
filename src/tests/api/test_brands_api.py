"""
Brands API tests for AutomationExercise.com.
"""
import pytest
import time
from src.fixtures.test_data_fixtures import brands_controller, api_test_data


@pytest.mark.api
class TestBrandsAPI:
    """Test class for Brands API endpoints."""
    
    def test_get_all_brands_list_success(self, brands_controller, api_test_data):
        """
        API 3: GET All Brands List - Should return 200 with brands data.
        
        Validates that the GET All Brands endpoint returns 200 status with proper brands data structure.
        """
        # Act
        response = brands_controller.get_all_brands()
        
        # Assert
        assert response["status"] == 200
        assert "responseCode" in response["data"]
        assert response["data"]["responseCode"] == 200
        assert "brands" in response["data"]
        assert isinstance(response["data"]["brands"], list)
        assert len(response["data"]["brands"]) > 0
        
        # Validate brand structure
        first_brand = response["data"]["brands"][0]
        assert "id" in first_brand
        assert "brand" in first_brand
        assert first_brand["id"] is not None
        assert first_brand["brand"], "Brand name should not be empty"
    
    def test_put_to_brands_list_method_not_allowed(self, brands_controller):
        """
        API 4: PUT To All Brands List - Should return 405 Method Not Allowed.
        
        Validates that the PUT method on brands list endpoint returns 405 Method Not Allowed error.
        """
        # Act
        response = brands_controller.put_to_brands_list()
        
        # Assert
        assert response["status"] == 200
        assert "responseCode" in response["data"]
        assert response["data"]["responseCode"] == 405
        assert "message" in response["data"]
        assert response["data"]["message"] == "This request method is not supported."
    
    def test_verify_brands_data_integrity(self, brands_controller):
        """
        Verify brands data integrity.
        
        Validates that all brands have required fields and proper data structure integrity.
        """
        # Get all brands
        response = brands_controller.get_all_brands()
        
        assert response["status"] == 200
        assert len(response["data"]["brands"]) > 0
        
        # Check each brand has required fields
        for i, brand in enumerate(response["data"]["brands"]):
            assert "id" in brand, f"Brand {i} should have id"
            assert brand["id"] is not None, f"Brand {i} id should not be None"
            assert isinstance(brand["id"], int), f"Brand {i} id should be integer"
            
            assert "brand" in brand, f"Brand {i} should have brand name"
            assert brand["brand"], f"Brand {i} brand name should not be empty"
            assert isinstance(brand["brand"], str), f"Brand {i} brand name should be string"
    
    def test_brands_api_performance_response_time(self, brands_controller):
        """
        Brands API Performance - Response time should be under 3 seconds.
        
        Validates that the brands endpoint responds within acceptable time limits (under 3 seconds).
        """
        start_time = time.time()
        
        response = brands_controller.get_all_brands()
        
        response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        assert response["status"] == 200
        assert response_time < 3000, f"Response time {response_time}ms should be under 3000ms"
    
    def test_brands_api_data_consistency(self, brands_controller):
        """
        Test brands API data consistency.
        
        Tests that the API returns consistent data across multiple calls.
        """
        # Make multiple calls to the same endpoint
        responses = []
        for _ in range(3):
            response = brands_controller.get_all_brands()
            responses.append(response)
        
        # All responses should be successful
        for response in responses:
            assert response["status"] == 200
            assert "brands" in response["data"]
        
        # All responses should have the same number of brands
        brand_counts = [len(response["data"]["brands"]) for response in responses]
        assert len(set(brand_counts)) == 1, "Brand count should be consistent across calls"
        
        # All responses should have the same brand IDs
        brand_ids = [set(brand["id"] for brand in response["data"]["brands"]) for response in responses]
        assert all(ids == brand_ids[0] for ids in brand_ids), "Brand IDs should be consistent across calls"
    
    def test_brands_api_error_handling(self, brands_controller):
        """
        Test brands API error handling.
        
        Tests that the API handles various error conditions gracefully.
        """
        # Test with invalid method (should return 405)
        response = brands_controller.put_to_brands_list()
        
        assert response["status"] == 200
        assert "responseCode" in response["data"]
        assert response["data"]["responseCode"] == 405
        assert "message" in response["data"]
    
    def test_brands_list_contains_expected_brands(self, brands_controller, api_test_data):
        """
        Test that brands list contains expected brands.
        
        Tests that the API returns expected brand names.
        """
        response = brands_controller.get_all_brands()
        
        assert response["status"] == 200
        assert "brands" in response["data"]
        
        brand_names = [brand["brand"] for brand in response["data"]["brands"]]
        expected_brands = api_test_data["brands_data"]["expected_brands"]
        
        # Check that at least some expected brands are present
        found_brands = [brand for brand in expected_brands if brand in brand_names]
        assert len(found_brands) > 0, f"Should find at least some expected brands: {expected_brands}"
    
    def test_brands_api_response_structure(self, brands_controller):
        """
        Test brands API response structure.
        
        Tests that the API response has the correct structure.
        """
        response = brands_controller.get_all_brands()
        
        assert response["status"] == 200
        assert "data" in response
        assert "responseCode" in response["data"]
        assert "brands" in response["data"]
        
        # Check response structure
        assert isinstance(response["data"], dict)
        assert isinstance(response["data"]["brands"], list)
        assert response["data"]["responseCode"] == 200
    
    def test_brands_api_empty_response_handling(self, brands_controller):
        """
        Test brands API empty response handling.
        
        Tests that the API handles empty responses gracefully.
        """
        response = brands_controller.get_all_brands()
        
        assert response["status"] == 200
        assert "brands" in response["data"]
        
        # Even if empty, should return valid structure
        assert isinstance(response["data"]["brands"], list)
        assert response["data"]["responseCode"] == 200
    
    def test_brands_api_concurrent_requests(self, brands_controller):
        """
        Test brands API concurrent requests.
        
        Tests that the API can handle concurrent requests.
        """
        import threading
        import time
        
        results = []
        errors = []
        
        def make_request():
            try:
                response = brands_controller.get_all_brands()
                results.append(response)
            except Exception as e:
                errors.append(e)
        
        # Make concurrent requests
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # All requests should succeed
        assert len(errors) == 0, f"Should not have errors: {errors}"
        assert len(results) == 5, "Should have 5 successful responses"
        
        # All responses should be successful
        for response in results:
            assert response["status"] == 200
            assert "brands" in response["data"]
    
    def test_brands_api_data_types(self, brands_controller):
        """
        Test brands API data types.
        
        Tests that the API returns data with correct types.
        """
        response = brands_controller.get_all_brands()
        
        assert response["status"] == 200
        assert "brands" in response["data"]
        
        brands = response["data"]["brands"]
        assert len(brands) > 0, "Should have brands"
        
        for brand in brands:
            assert isinstance(brand["id"], int), f"Brand ID should be integer: {brand['id']}"
            assert isinstance(brand["brand"], str), f"Brand name should be string: {brand['brand']}"
            assert brand["id"] > 0, f"Brand ID should be positive: {brand['id']}"
            assert len(brand["brand"]) > 0, f"Brand name should not be empty: {brand['brand']}"
    
    def test_brands_api_unique_ids(self, brands_controller):
        """
        Test brands API unique IDs.
        
        Tests that all brand IDs are unique.
        """
        response = brands_controller.get_all_brands()
        
        assert response["status"] == 200
        assert "brands" in response["data"]
        
        brands = response["data"]["brands"]
        brand_ids = [brand["id"] for brand in brands]
        
        # All IDs should be unique
        assert len(set(brand_ids)) == len(brand_ids), "All brand IDs should be unique"
        
        # All IDs should be positive integers
        for brand_id in brand_ids:
            assert isinstance(brand_id, int), f"Brand ID should be integer: {brand_id}"
            assert brand_id > 0, f"Brand ID should be positive: {brand_id}"
