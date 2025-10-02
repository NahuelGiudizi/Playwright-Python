"""
Base API Client for AutomationExercise.com API testing.
"""
import os
from typing import Dict, Any, Optional
import httpx
from playwright.sync_api import APIRequestContext


class BaseAPIClient:
    """Base API client for AutomationExercise.com APIs."""
    
    def __init__(self, request_context: APIRequestContext, base_url: Optional[str] = None):
        """
        Initialize the API client.
        
        Args:
            request_context: Playwright API request context
            base_url: Base URL for API requests (optional)
        """
        self.request = request_context
        self.base_url = base_url or os.getenv('API_BASE_URL', 'https://automationexercise.com/api')
    
    def init(self) -> None:
        """Initialize the API client (no authentication required for AutomationExercise.com)."""
        # No authentication required for AutomationExercise.com APIs
        pass
    
    def _get_headers(self) -> Dict[str, str]:
        """Get standard headers for JSON requests."""
        return {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    
    def _get_form_headers(self) -> Dict[str, str]:
        """Get headers for form data requests."""
        return {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make a GET request to the API.
        
        Args:
            endpoint: API endpoint path
            params: Query parameters
            
        Returns:
            Dictionary containing status code and response data
        """
        response = self.request.get(
            f"{self.base_url}{endpoint}",
            headers=self._get_headers(),
            params=params
        )
        
        status = response.status
        data = self._parse_response(response)
        
        return {"status": status, "data": data}
    
    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make a POST request to the API.
        
        Args:
            endpoint: API endpoint path
            data: Request body data
            
        Returns:
            Dictionary containing status code and response data
        """
        response = self.request.post(
            f"{self.base_url}{endpoint}",
            headers=self._get_headers(),
            data=data
        )
        
        status = response.status
        response_data = self._parse_response(response)
        
        return {"status": status, "data": response_data}
    
    def post_form(self, endpoint: str, form_data: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Make a POST request with form data to the API.
        
        Args:
            endpoint: API endpoint path
            form_data: Form data to send
            
        Returns:
            Dictionary containing status code and response data
        """
        response = self.request.post(
            f"{self.base_url}{endpoint}",
            headers=self._get_form_headers(),
            form=form_data
        )
        
        status = response.status
        response_data = self._parse_response(response)
        
        return {"status": status, "data": response_data}
    
    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make a PUT request to the API.
        
        Args:
            endpoint: API endpoint path
            data: Request body data
            
        Returns:
            Dictionary containing status code and response data
        """
        response = self.request.put(
            f"{self.base_url}{endpoint}",
            headers=self._get_headers(),
            data=data
        )
        
        status = response.status
        response_data = self._parse_response(response)
        
        return {"status": status, "data": response_data}
    
    def put_form(self, endpoint: str, form_data: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Make a PUT request with form data to the API.
        
        Args:
            endpoint: API endpoint path
            form_data: Form data to send
            
        Returns:
            Dictionary containing status code and response data
        """
        response = self.request.put(
            f"{self.base_url}{endpoint}",
            headers=self._get_form_headers(),
            form=form_data
        )
        
        status = response.status
        response_data = self._parse_response(response)
        
        return {"status": status, "data": response_data}
    
    def delete(self, endpoint: str, form_data: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Make a DELETE request to the API.
        
        Args:
            endpoint: API endpoint path
            form_data: Form data to send
            
        Returns:
            Dictionary containing status code and response data
        """
        response = self.request.delete(
            f"{self.base_url}{endpoint}",
            headers=self._get_form_headers(),
            form=form_data
        )
        
        status = response.status
        data = self._parse_response(response)
        
        return {"status": status, "data": data}
    
    def _parse_response(self, response) -> Any:
        """
        Parse the response from the API.
        
        Args:
            response: Playwright response object
            
        Returns:
            Parsed response data
        """
        try:
            return response.json()
        except Exception:
            # If JSON parsing fails, return text content
            return response.text()
