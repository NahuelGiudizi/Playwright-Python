"""
User Authentication API tests for AutomationExercise.com.
"""
import pytest
import time
from src.fixtures.test_data_fixtures import user_controller, api_test_data


@pytest.mark.api
class TestUserAuthenticationAPI:
    """Test class for User Authentication API endpoints."""
    
    def test_verify_login_with_valid_details(self, user_controller, api_test_data):
        """
        API 7: POST To Verify Login with valid details - Should return 200.
        
        Validates that login with valid credentials returns 200 status.
        """
        # Arrange
        valid_credentials = api_test_data["user_data"]["valid_credentials"]
        
        # Act
        response = user_controller.verify_login(
            valid_credentials["email"], 
            valid_credentials["password"]
        )
        
        # Assert
        assert response["status"] == 200
        assert "responseCode" in response["data"]
        assert response["data"]["responseCode"] == 200
        assert "message" in response["data"]
        assert "user" in response["data"]
    
    def test_verify_login_without_email_parameter(self, user_controller):
        """
        API 8: POST To Verify Login without email parameter - Should return 400.
        
        Validates that login without email parameter returns 400 Bad Request error.
        """
        # Act
        response = user_controller.verify_login_without_email("testpassword")
        
        # Assert
        assert response["status"] == 200
        assert "responseCode" in response["data"]
        assert response["data"]["responseCode"] == 400
        assert "message" in response["data"]
        assert "email" in response["data"]["message"].lower()
    
    def test_delete_verify_login_method_not_allowed(self, user_controller):
        """
        API 9: DELETE To Verify Login - Should return 405 Method Not Allowed.
        
        Validates that DELETE method on login endpoint returns 405 Method Not Allowed error.
        """
        # Act
        response = user_controller.delete_verify_login()
        
        # Assert
        assert response["status"] == 200
        assert "responseCode" in response["data"]
        assert response["data"]["responseCode"] == 405
        assert "message" in response["data"]
        assert response["data"]["message"] == "This request method is not supported."
    
    def test_verify_login_with_invalid_details(self, user_controller, api_test_data):
        """
        API 10: POST To Verify Login with invalid details - Should return 404.
        
        Validates that login with invalid credentials returns 404 Not Found error.
        """
        # Arrange
        invalid_credentials = api_test_data["user_data"]["invalid_credentials"]
        
        # Act
        response = user_controller.verify_login_invalid_details(
            invalid_credentials["email"], 
            invalid_credentials["password"]
        )
        
        # Assert
        assert response["status"] == 200
        assert "responseCode" in response["data"]
        assert response["data"]["responseCode"] == 404
        assert "message" in response["data"]
        assert "incorrect" in response["data"]["message"].lower()
    
    def test_create_user_account_success(self, user_controller, sample_user):
        """
        API 11: POST To Create/Register User Account - Should return 201.
        
        Validates that user account creation returns 201 Created status.
        """
        # Act
        response = user_controller.create_user_account(
            name=sample_user["name"],
            email=sample_user["email"],
            password=sample_user["password"],
            first_name=sample_user["first_name"],
            last_name=sample_user["last_name"],
            address1=sample_user["address1"],
            address2=sample_user["address2"],
            country=sample_user["country"],
            state=sample_user["state"],
            city=sample_user["city"],
            zipcode=sample_user["zipcode"],
            mobile_number=sample_user["mobile_number"]
        )
        
        # Assert
        assert response["status"] == 200
        assert "responseCode" in response["data"]
        assert response["data"]["responseCode"] == 201
        assert "message" in response["data"]
        assert "user" in response["data"]
    
    def test_delete_user_account_success(self, user_controller, sample_user):
        """
        API 12: DELETE To Delete User Account - Should return 200.
        
        Validates that user account deletion returns 200 OK status.
        """
        # Act
        response = user_controller.delete_user_account(
            sample_user["email"], 
            sample_user["password"]
        )
        
        # Assert
        assert response["status"] == 200
        assert "responseCode" in response["data"]
        assert response["data"]["responseCode"] == 200
        assert "message" in response["data"]
    
    def test_update_user_account_success(self, user_controller, sample_user):
        """
        API 13: PUT To Update User Account - Should return 200.
        
        Validates that user account update returns 200 OK status.
        """
        # Act
        response = user_controller.update_user_account(
            name=sample_user["name"],
            email=sample_user["email"],
            password=sample_user["password"],
            first_name=sample_user["first_name"],
            last_name=sample_user["last_name"],
            address1=sample_user["address1"],
            address2=sample_user["address2"],
            country=sample_user["country"],
            state=sample_user["state"],
            city=sample_user["city"],
            zipcode=sample_user["zipcode"],
            mobile_number=sample_user["mobile_number"]
        )
        
        # Assert
        assert response["status"] == 200
        assert "responseCode" in response["data"]
        assert response["data"]["responseCode"] == 200
        assert "message" in response["data"]
        assert "user" in response["data"]
    
    def test_get_user_account_detail_by_email(self, user_controller, sample_user):
        """
        API 14: GET user account detail by email - Should return 200.
        
        Validates that getting user account details by email returns 200 OK status.
        """
        # Act
        response = user_controller.get_user_account_detail(sample_user["email"])
        
        # Assert
        assert response["status"] == 200
        assert "responseCode" in response["data"]
        assert response["data"]["responseCode"] == 200
        assert "user" in response["data"]
    
    def test_user_authentication_api_performance(self, user_controller, api_test_data):
        """
        User Authentication API Performance - Response time should be under 3 seconds.
        
        Validates that the authentication endpoints respond within acceptable time limits.
        """
        valid_credentials = api_test_data["user_data"]["valid_credentials"]
        
        start_time = time.time()
        
        response = user_controller.verify_login(
            valid_credentials["email"], 
            valid_credentials["password"]
        )
        
        response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        assert response["status"] == 200
        assert response_time < 3000, f"Response time {response_time}ms should be under 3000ms"
    
    def test_user_authentication_api_error_handling(self, user_controller):
        """
        Test user authentication API error handling.
        
        Tests that the API handles various error conditions gracefully.
        """
        # Test with empty email
        response = user_controller.verify_login_without_email("testpassword")
        
        assert response["status"] == 200
        assert "responseCode" in response["data"]
        assert response["data"]["responseCode"] == 400
        
        # Test with invalid method
        response = user_controller.delete_verify_login()
        
        assert response["status"] == 200
        assert "responseCode" in response["data"]
        assert response["data"]["responseCode"] == 405
    
    def test_user_authentication_api_data_consistency(self, user_controller, api_test_data):
        """
        Test user authentication API data consistency.
        
        Tests that the API returns consistent data across multiple calls.
        """
        valid_credentials = api_test_data["user_data"]["valid_credentials"]
        
        # Make multiple calls to the same endpoint
        responses = []
        for _ in range(3):
            response = user_controller.verify_login(
                valid_credentials["email"], 
                valid_credentials["password"]
            )
            responses.append(response)
        
        # All responses should be successful
        for response in responses:
            assert response["status"] == 200
            assert "responseCode" in response["data"]
        
        # All responses should have the same response code
        response_codes = [response["data"]["responseCode"] for response in responses]
        assert len(set(response_codes)) == 1, "Response codes should be consistent across calls"
    
    def test_user_authentication_api_response_structure(self, user_controller, api_test_data):
        """
        Test user authentication API response structure.
        
        Tests that the API response has the correct structure.
        """
        valid_credentials = api_test_data["user_data"]["valid_credentials"]
        
        response = user_controller.verify_login(
            valid_credentials["email"], 
            valid_credentials["password"]
        )
        
        assert response["status"] == 200
        assert "data" in response
        assert "responseCode" in response["data"]
        assert "message" in response["data"]
        
        # Check response structure
        assert isinstance(response["data"], dict)
        assert response["data"]["responseCode"] == 200
    
    def test_user_authentication_api_invalid_credentials(self, user_controller):
        """
        Test user authentication API with invalid credentials.
        
        Tests that the API properly handles invalid credentials.
        """
        # Test with non-existent user
        response = user_controller.verify_login_invalid_details(
            "nonexistent@example.com", 
            "wrongpassword"
        )
        
        assert response["status"] == 200
        assert "responseCode" in response["data"]
        assert response["data"]["responseCode"] == 404
        assert "message" in response["data"]
    
    def test_user_authentication_api_missing_parameters(self, user_controller):
        """
        Test user authentication API with missing parameters.
        
        Tests that the API properly handles missing parameters.
        """
        # Test without email
        response = user_controller.verify_login_without_email("testpassword")
        
        assert response["status"] == 200
        assert "responseCode" in response["data"]
        assert response["data"]["responseCode"] == 400
        assert "message" in response["data"]
    
    def test_user_authentication_api_concurrent_requests(self, user_controller, api_test_data):
        """
        Test user authentication API concurrent requests.
        
        Tests that the API can handle concurrent requests.
        """
        import threading
        import time
        
        valid_credentials = api_test_data["user_data"]["valid_credentials"]
        results = []
        errors = []
        
        def make_request():
            try:
                response = user_controller.verify_login(
                    valid_credentials["email"], 
                    valid_credentials["password"]
                )
                results.append(response)
            except Exception as e:
                errors.append(e)
        
        # Make concurrent requests
        threads = []
        for _ in range(3):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # All requests should succeed
        assert len(errors) == 0, f"Should not have errors: {errors}"
        assert len(results) == 3, "Should have 3 successful responses"
        
        # All responses should be successful
        for response in results:
            assert response["status"] == 200
            assert "responseCode" in response["data"]
    
    def test_user_authentication_api_data_types(self, user_controller, api_test_data):
        """
        Test user authentication API data types.
        
        Tests that the API returns data with correct types.
        """
        valid_credentials = api_test_data["user_data"]["valid_credentials"]
        
        response = user_controller.verify_login(
            valid_credentials["email"], 
            valid_credentials["password"]
        )
        
        assert response["status"] == 200
        assert "data" in response
        assert isinstance(response["data"], dict)
        assert isinstance(response["data"]["responseCode"], int)
        assert isinstance(response["data"]["message"], str)
        
        if "user" in response["data"]:
            user = response["data"]["user"]
            assert isinstance(user, dict)
            assert "name" in user
            assert "email" in user
            assert isinstance(user["name"], str)
            assert isinstance(user["email"], str)
