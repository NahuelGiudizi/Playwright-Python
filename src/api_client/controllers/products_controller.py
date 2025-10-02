"""
Products API Controller for AutomationExercise.com.
"""
from typing import Dict, Any
from ..base_client import BaseAPIClient


class ProductsController(BaseAPIClient):
    """Controller for Products API endpoints."""
    
    def get_all_products(self) -> Dict[str, Any]:
        """
        Get all products list.
        
        Returns:
            Dictionary containing status code and products data
        """
        return self.get("/productsList")
    
    def post_to_products_list(self) -> Dict[str, Any]:
        """
        POST to products list (should return 405 Method Not Allowed).
        
        Returns:
            Dictionary containing status code and error data
        """
        return self.post("/productsList")
    
    def search_product(self, search_term: str) -> Dict[str, Any]:
        """
        Search for products by term.
        
        Args:
            search_term: Product search term
            
        Returns:
            Dictionary containing status code and search results
        """
        form_data = {"search_product": search_term}
        return self.post_form("/searchProduct", form_data)
    
    def search_product_without_parameter(self) -> Dict[str, Any]:
        """
        Search product without parameter (should return 400 Bad Request).
        
        Returns:
            Dictionary containing status code and error data
        """
        return self.post_form("/searchProduct")
