"""
Brands API Controller for AutomationExercise.com.
"""
from typing import Dict, Any
from ..base_client import BaseAPIClient


class BrandsController(BaseAPIClient):
    """Controller for Brands API endpoints."""
    
    def get_all_brands(self) -> Dict[str, Any]:
        """
        Get all brands list.
        
        Returns:
            Dictionary containing status code and brands data
        """
        return self.get("/brandsList")
    
    def put_to_brands_list(self) -> Dict[str, Any]:
        """
        PUT to brands list (should return 405 Method Not Allowed).
        
        Returns:
            Dictionary containing status code and error data
        """
        return self.put("/brandsList")
