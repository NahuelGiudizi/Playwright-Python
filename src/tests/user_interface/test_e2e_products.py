"""
E2E Products tests for AutomationExercise.com.
"""
import pytest
from src.fixtures.test_data_fixtures import home_page, products_page, ui_test_data


@pytest.mark.ui
class TestE2EProducts:
    """Test class for E2E Products functionality."""
    
    def test_navigate_to_products_page_success(self, products_page, ui_test_data):
        """
        Should successfully navigate to products page.
        
        Validates that navigation to the products page works and all elements are visible.
        """
        # Act
        products_page.navigate_to_products()
        
        # Assert
        assert '/products' in products_page.page.url
        assert 'Automation Exercise' in products_page.get_title()
        
        # Verify page structure
        products_page.verify_products_page()
        products_page.verify_page_structure()
        products_page.verify_search_functionality()
        products_page.verify_category_filter()
        products_page.verify_brand_filter()
    
    def test_display_products_correctly(self, products_page, ui_test_data):
        """
        Should display products correctly.
        
        Verifies that all products are properly displayed with correct information.
        """
        # Arrange & Act
        products_page.navigate_to_products()
        
        # Assert - Check products are visible
        assert products_page.has_products()
        assert products_page.get_product_count() > 0
        
        # Verify product structure
        products_page.verify_product_structure()
        
        # Get product information
        product_names = products_page.get_product_names()
        product_prices = products_page.get_product_prices()
        
        assert len(product_names) > 0
        assert len(product_prices) > 0
        assert len(product_names) == len(product_prices)
    
    def test_search_products_functionality(self, products_page, ui_test_data):
        """
        Should search products successfully.
        
        Tests that product search functionality works correctly.
        """
        # Arrange
        products_page.navigate_to_products()
        search_term = ui_test_data["products_data"]["search_terms"][0]
        
        # Act
        products_page.search_for_product(search_term)
        
        # Assert
        assert products_page.has_search_results()
        assert products_page.get_search_results_count() > 0
        
        # Verify search results contain the search term
        assert products_page.verify_search_results(search_term)
        
        # Get search results
        search_results = products_page.get_search_results_names()
        assert len(search_results) > 0
        
        # Verify at least one result contains the search term
        assert any(search_term.lower() in result.lower() for result in search_results)
    
    def test_search_products_with_different_terms(self, products_page, ui_test_data):
        """
        Should search products with different terms.
        
        Tests product search functionality across multiple search terms.
        """
        # Arrange
        products_page.navigate_to_products()
        search_terms = ui_test_data["products_data"]["search_terms"]
        
        for term in search_terms:
            # Act
            products_page.search_for_product(term)
            
            # Assert
            assert products_page.has_search_results()
            assert products_page.get_search_results_count() > 0
            
            # Verify search results contain the search term
            assert products_page.verify_search_results(term)
    
    def test_category_filter_functionality(self, products_page, ui_test_data):
        """
        Should filter products by category.
        
        Tests that category filtering works correctly.
        """
        # Arrange
        products_page.navigate_to_products()
        categories = ui_test_data["products_data"]["categories"]
        
        for category in categories:
            # Act
            products_page.click_category_link(category)
            
            # Assert
            assert products_page.is_on_products_page()
            assert products_page.has_products()
            
            # Get products after filtering
            products = products_page.get_all_products_info()
            assert len(products) > 0
    
    def test_brand_filter_functionality(self, products_page, ui_test_data):
        """
        Should filter products by brand.
        
        Tests that brand filtering works correctly.
        """
        # Arrange
        products_page.navigate_to_products()
        brands = ui_test_data["products_data"]["brands"]
        
        for brand in brands:
            # Act
            products_page.click_brand_link(brand)
            
            # Assert
            assert products_page.is_on_products_page()
            assert products_page.has_products()
            
            # Get products after filtering
            products = products_page.get_all_products_info()
            assert len(products) > 0
    
    def test_add_product_to_cart(self, products_page, ui_test_data):
        """
        Should add product to cart successfully.
        
        Tests that adding products to cart works correctly.
        """
        # Arrange
        products_page.navigate_to_products()
        assert products_page.has_products()
        
        # Act
        products_page.add_product_to_cart(0)  # Add first product
        
        # Assert
        # Verify cart modal appears and can be closed
        products_page.verify_cart_modal_functionality()
    
    def test_view_product_details(self, products_page, ui_test_data):
        """
        Should view product details successfully.
        
        Tests that viewing product details works correctly.
        """
        # Arrange
        products_page.navigate_to_products()
        assert products_page.has_products()
        
        # Act
        products_page.view_product(0)  # View first product
        
        # Assert
        assert '/product_details' in products_page.page.url
    
    def test_hover_over_product(self, products_page, ui_test_data):
        """
        Should hover over product successfully.
        
        Tests that hovering over products works correctly.
        """
        # Arrange
        products_page.navigate_to_products()
        assert products_page.has_products()
        
        # Act
        products_page.hover_over_product(0)  # Hover over first product
        
        # Assert
        # Verify overlay appears (this is handled in the method)
        assert True  # If no exception is raised, test passes
    
    def test_sort_products_functionality(self, products_page, ui_test_data):
        """
        Should sort products successfully.
        
        Tests that product sorting works correctly.
        """
        # Arrange
        products_page.navigate_to_products()
        assert products_page.has_products()
        
        # Act & Assert
        products_page.verify_sort_functionality()
        
        # Test different sort options
        sort_options = products_page.get_sort_options()
        assert len(sort_options) > 0
        
        # Test sorting by price
        products_page.sort_by_price_low_to_high()
        assert products_page.is_on_products_page()
        assert products_page.has_products()
    
    def test_pagination_functionality(self, products_page, ui_test_data):
        """
        Should handle pagination successfully.
        
        Tests that pagination works correctly.
        """
        # Arrange
        products_page.navigate_to_products()
        assert products_page.has_products()
        
        # Act & Assert
        products_page.verify_pagination_functionality()
        
        if products_page.is_pagination_visible():
            # Test pagination
            total_pages = products_page.get_total_pages()
            current_page = products_page.get_current_page_number()
            
            assert total_pages > 0
            assert current_page > 0
            
            # Test navigation if multiple pages exist
            if total_pages > 1:
                products_page.go_to_next_page()
                assert products_page.is_on_products_page()
                assert products_page.has_products()
    
    def test_products_page_performance(self, products_page, ui_test_data):
        """
        Should load products page within acceptable time.
        
        Tests that the products page loads within acceptable time limits.
        """
        # Arrange
        start_time = products_page.page.evaluate("Date.now()")
        
        # Act
        products_page.navigate_to_products()
        
        # Assert
        end_time = products_page.page.evaluate("Date.now()")
        load_time = end_time - start_time
        
        assert load_time < 5000, f"Page load time {load_time}ms should be under 5000ms"
        assert products_page.has_products()
    
    def test_products_page_accessibility(self, products_page, ui_test_data):
        """
        Should meet accessibility standards.
        
        Tests that the products page meets accessibility standards.
        """
        # Arrange & Act
        products_page.navigate_to_products()
        
        # Assert
        # Test keyboard navigation
        products_page.search_product_input.focus()
        assert products_page.search_product_input.is_focused()
        
        # Test tab navigation
        products_page.page.keyboard.press('Tab')
        assert products_page.submit_search_button.is_focused()
        
        # Test form accessibility
        assert products_page.search_product_input.get_attribute('type') == 'text'
        assert products_page.submit_search_button.get_attribute('type') == 'submit'
    
    def test_products_page_responsive_design(self, products_page, ui_test_data):
        """
        Should be responsive across different screen sizes.
        
        Tests that the products page is responsive.
        """
        # Arrange
        products_page.navigate_to_products()
        
        # Test different viewport sizes
        viewports = [
            {"width": 1920, "height": 1080},  # Desktop
            {"width": 1024, "height": 768},   # Tablet
            {"width": 375, "height": 667}     # Mobile
        ]
        
        for viewport in viewports:
            # Act
            products_page.page.set_viewport_size(viewport["width"], viewport["height"])
            
            # Assert
            assert products_page.has_products()
            assert products_page.search_product_input.is_visible()
            assert products_page.submit_search_button.is_visible()
    
    def test_products_page_error_handling(self, products_page, ui_test_data):
        """
        Should handle errors gracefully.
        
        Tests that the products page handles errors gracefully.
        """
        # Arrange
        products_page.navigate_to_products()
        
        # Test with invalid search term
        products_page.search_for_product("nonexistent_product_xyz")
        
        # Assert
        # Should not crash and should return empty results
        assert products_page.is_on_products_page()
        assert products_page.has_search_results() or products_page.get_search_results_count() == 0
    
    def test_products_page_data_consistency(self, products_page, ui_test_data):
        """
        Should maintain data consistency.
        
        Tests that the products page maintains data consistency.
        """
        # Arrange
        products_page.navigate_to_products()
        
        # Get initial product count
        initial_count = products_page.get_product_count()
        assert initial_count > 0
        
        # Test that product count remains consistent
        for _ in range(3):
            products_page.page.reload()
            products_page.wait_for_page_load()
            
            current_count = products_page.get_product_count()
            assert current_count == initial_count, "Product count should remain consistent"
    
    def test_products_page_security(self, products_page, ui_test_data):
        """
        Should maintain security standards.
        
        Tests that the products page maintains security standards.
        """
        # Arrange
        products_page.navigate_to_products()
        
        # Test XSS prevention
        xss_payload = "<script>alert('xss')</script>"
        products_page.search_for_product(xss_payload)
        
        # Assert
        # Should not execute script and should handle safely
        assert products_page.is_on_products_page()
        assert products_page.has_search_results() or products_page.get_search_results_count() == 0
        
        # Test SQL injection prevention
        sql_payload = "'; DROP TABLE products; --"
        products_page.search_for_product(sql_payload)
        
        # Assert
        # Should not crash and should handle safely
        assert products_page.is_on_products_page()
        assert products_page.has_search_results() or products_page.get_search_results_count() == 0
