"""
User Authentication API Controller for AutomationExercise.com.
"""
from typing import Dict, Any
from ..base_client import BaseAPIClient


class UserController(BaseAPIClient):
    """Controller for User Authentication API endpoints."""
    
    def verify_login(self, email: str, password: str) -> Dict[str, Any]:
        """
        Verify login with valid credentials.
        
        Args:
            email: User email
            password: User password
            
        Returns:
            Dictionary containing status code and login response
        """
        form_data = {
            "email": email,
            "password": password
        }
        return self.post_form("/verifyLogin", form_data)
    
    def verify_login_without_email(self, password: str) -> Dict[str, Any]:
        """
        Verify login without email parameter (should return 400 Bad Request).
        
        Args:
            password: User password
            
        Returns:
            Dictionary containing status code and error data
        """
        form_data = {"password": password}
        return self.post_form("/verifyLogin", form_data)
    
    def delete_verify_login(self) -> Dict[str, Any]:
        """
        DELETE to verify login (should return 405 Method Not Allowed).
        
        Returns:
            Dictionary containing status code and error data
        """
        return self.delete("/verifyLogin")
    
    def verify_login_invalid_details(self, email: str, password: str) -> Dict[str, Any]:
        """
        Verify login with invalid credentials.
        
        Args:
            email: Invalid user email
            password: Invalid user password
            
        Returns:
            Dictionary containing status code and error response
        """
        form_data = {
            "email": email,
            "password": password
        }
        return self.post_form("/verifyLogin", form_data)
    
    def create_user_account(self, name: str, email: str, password: str, 
                           first_name: str = "", last_name: str = "", 
                           address1: str = "", address2: str = "", 
                           country: str = "", state: str = "", 
                           city: str = "", zipcode: str = "", 
                           mobile_number: str = "") -> Dict[str, Any]:
        """
        Create/Register user account.
        
        Args:
            name: User name
            email: User email
            password: User password
            first_name: User first name
            last_name: User last name
            address1: User address line 1
            address2: User address line 2
            country: User country
            state: User state
            city: User city
            zipcode: User zipcode
            mobile_number: User mobile number
            
        Returns:
            Dictionary containing status code and user creation response
        """
        form_data = {
            "name": name,
            "email": email,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
            "address1": address1,
            "address2": address2,
            "country": country,
            "state": state,
            "city": city,
            "zipcode": zipcode,
            "mobile_number": mobile_number
        }
        return self.post_form("/createAccount", form_data)
    
    def delete_user_account(self, email: str, password: str) -> Dict[str, Any]:
        """
        Delete user account.
        
        Args:
            email: User email
            password: User password
            
        Returns:
            Dictionary containing status code and deletion response
        """
        form_data = {
            "email": email,
            "password": password
        }
        return self.delete("/deleteAccount", form_data)
    
    def update_user_account(self, name: str, email: str, password: str, 
                           first_name: str = "", last_name: str = "", 
                           address1: str = "", address2: str = "", 
                           country: str = "", state: str = "", 
                           city: str = "", zipcode: str = "", 
                           mobile_number: str = "") -> Dict[str, Any]:
        """
        Update user account.
        
        Args:
            name: User name
            email: User email
            password: User password
            first_name: User first name
            last_name: User last name
            address1: User address line 1
            address2: User address line 2
            country: User country
            state: User state
            city: User city
            zipcode: User zipcode
            mobile_number: User mobile number
            
        Returns:
            Dictionary containing status code and update response
        """
        form_data = {
            "name": name,
            "email": email,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
            "address1": address1,
            "address2": address2,
            "country": country,
            "state": state,
            "city": city,
            "zipcode": zipcode,
            "mobile_number": mobile_number
        }
        return self.put_form("/updateAccount", form_data)
    
    def get_user_account_detail(self, email: str) -> Dict[str, Any]:
        """
        Get user account detail by email.
        
        Args:
            email: User email
            
        Returns:
            Dictionary containing status code and user details
        """
        params = {"email": email}
        return self.get("/getUserDetailByEmail", params)
