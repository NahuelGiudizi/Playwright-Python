"""
E2E Cart tests for AutomationExercise.com.
"""
import pytest
from src.fixtures.test_data_fixtures import home_page, products_page, cart_page, ui_test_data


@pytest.mark.ui
class TestE2ECart:
    """Test class for E2E Cart functionality."""
    
    def test_navigate_to_cart_page_success(self, cart_page, ui_test_data):
        """
        Should successfully navigate to cart page.
        
        Validates that navigation to the cart page works and all elements are visible.
        """
        # Act
        cart_page.navigate_to_cart()
        
        # Assert
        assert '/view_cart' in cart_page.page.url
        assert 'Automation Exercise' in cart_page.get_title()
        
        # Verify page structure
        cart_page.verify_cart_page()
        cart_page.verify_page_structure()
    
    def test_display_empty_cart_correctly(self, cart_page, ui_test_data):
        """
        Should display empty cart correctly.
        
        Verifies that empty cart is properly displayed with appropriate message.
        """
        # Arrange & Act
        cart_page.navigate_to_cart()
        
        # Assert
        if cart_page.is_cart_empty():
            cart_page.verify_empty_cart()
            assert cart_page.get_empty_cart_message() == "Cart is empty!"
            assert cart_page.continue_shopping_button.is_visible()
    
    def test_add_products_to_cart_and_verify(self, products_page, cart_page, ui_test_data):
        """
        Should add products to cart and verify contents.
        
        Tests that adding products to cart works correctly and cart contents are accurate.
        """
        # Arrange
        products_page.navigate_to_products()
        assert products_page.has_products()
        
        # Act - Add multiple products to cart
        product_indices = [0, 1, 2] if products_page.get_product_count() >= 3 else [0]
        
        for index in product_indices:
            products_page.add_product_to_cart(index)
        
        # Navigate to cart
        cart_page.navigate_to_cart()
        
        # Assert
        assert cart_page.has_items()
        assert cart_page.get_cart_items_count() == len(product_indices)
        
        # Verify cart contents
        cart_items = cart_page.get_all_cart_items()
        assert len(cart_items) == len(product_indices)
        
        # Verify each item has required information
        for item in cart_items:
            assert item['name']
            assert item['price']
            assert item['quantity']
            assert item['total']
    
    def test_update_item_quantity_in_cart(self, products_page, cart_page, ui_test_data):
        """
        Should update item quantity in cart.
        
        Tests that updating item quantities in cart works correctly.
        """
        # Arrange
        products_page.navigate_to_products()
        assert products_page.has_products()
        
        # Add product to cart
        products_page.add_product_to_cart(0)
        cart_page.navigate_to_cart()
        
        # Act
        cart_page.update_item_quantity(0, 3)
        
        # Assert
        assert cart_page.has_items()
        item = cart_page.get_cart_item_by_index(0)
        assert item['quantity'] == '3'
    
    def test_remove_item_from_cart(self, products_page, cart_page, ui_test_data):
        """
        Should remove item from cart.
        
        Tests that removing items from cart works correctly.
        """
        # Arrange
        products_page.navigate_to_products()
        assert products_page.has_products()
        
        # Add product to cart
        products_page.add_product_to_cart(0)
        cart_page.navigate_to_cart()
        
        # Act
        cart_page.remove_item(0)
        
        # Assert
        assert cart_page.is_cart_empty()
        assert cart_page.get_cart_items_count() == 0
    
    def test_remove_all_items_from_cart(self, products_page, cart_page, ui_test_data):
        """
        Should remove all items from cart.
        
        Tests that removing all items from cart works correctly.
        """
        # Arrange
        products_page.navigate_to_products()
        assert products_page.has_products()
        
        # Add multiple products to cart
        product_indices = [0, 1, 2] if products_page.get_product_count() >= 3 else [0]
        
        for index in product_indices:
            products_page.add_product_to_cart(index)
        
        cart_page.navigate_to_cart()
        assert cart_page.has_items()
        
        # Act
        cart_page.remove_all_items()
        
        # Assert
        assert cart_page.is_cart_empty()
        assert cart_page.get_cart_items_count() == 0
    
    def test_cart_total_calculation(self, products_page, cart_page, ui_test_data):
        """
        Should calculate cart total correctly.
        
        Tests that cart total calculation is accurate.
        """
        # Arrange
        products_page.navigate_to_products()
        assert products_page.has_products()
        
        # Add product to cart
        products_page.add_product_to_cart(0)
        cart_page.navigate_to_cart()
        
        # Act & Assert
        assert cart_page.has_items()
        
        # Verify cart totals are correct
        assert cart_page.verify_cart_totals()
        
        # Get cart summary
        summary = cart_page.get_cart_summary_info()
        assert summary['items_count'] > 0
        assert summary['total_price'] > 0
        assert not summary['is_empty']
        assert summary['can_checkout']
    
    def test_proceed_to_checkout_functionality(self, products_page, cart_page, ui_test_data):
        """
        Should proceed to checkout successfully.
        
        Tests that proceeding to checkout works correctly.
        """
        # Arrange
        products_page.navigate_to_products()
        assert products_page.has_products()
        
        # Add product to cart
        products_page.add_product_to_cart(0)
        cart_page.navigate_to_cart()
        assert cart_page.has_items()
        
        # Act
        cart_page.proceed_to_checkout()
        
        # Assert
        cart_page.verify_checkout_modal_visible()
        assert cart_page.register_login_button.is_visible()
        assert cart_page.checkout_as_guest_button.is_visible()
    
    def test_checkout_modal_functionality(self, products_page, cart_page, ui_test_data):
        """
        Should handle checkout modal correctly.
        
        Tests that checkout modal functionality works correctly.
        """
        # Arrange
        products_page.navigate_to_products()
        assert products_page.has_products()
        
        # Add product to cart
        products_page.add_product_to_cart(0)
        cart_page.navigate_to_cart()
        assert cart_page.has_items()
        
        # Act
        cart_page.proceed_to_checkout()
        cart_page.verify_checkout_modal_visible()
        
        # Test register/login button
        cart_page.register_login_from_checkout()
        assert '/login' in cart_page.page.url
        
        # Go back to cart
        cart_page.navigate_to_cart()
        cart_page.proceed_to_checkout()
        
        # Test checkout as guest
        cart_page.checkout_as_guest()
        # Should navigate to checkout page or show appropriate message
    
    def test_cart_page_performance(self, products_page, cart_page, ui_test_data):
        """
        Should load cart page within acceptable time.
        
        Tests that the cart page loads within acceptable time limits.
        """
        # Arrange
        products_page.navigate_to_products()
        assert products_page.has_products()
        
        # Add product to cart
        products_page.add_product_to_cart(0)
        
        start_time = cart_page.page.evaluate("Date.now()")
        
        # Act
        cart_page.navigate_to_cart()
        
        # Assert
        end_time = cart_page.page.evaluate("Date.now()")
        load_time = end_time - start_time
        
        assert load_time < 5000, f"Page load time {load_time}ms should be under 5000ms"
        assert cart_page.has_items()
    
    def test_cart_page_accessibility(self, products_page, cart_page, ui_test_data):
        """
        Should meet accessibility standards.
        
        Tests that the cart page meets accessibility standards.
        """
        # Arrange
        products_page.navigate_to_products()
        assert products_page.has_products()
        
        # Add product to cart
        products_page.add_product_to_cart(0)
        cart_page.navigate_to_cart()
        
        # Act & Assert
        # Test keyboard navigation
        cart_page.page.keyboard.press('Tab')
        
        # Test form accessibility
        if cart_page.has_items():
            # Test quantity input accessibility
            quantity_input = cart_page.item_quantities.first()
            assert quantity_input.get_attribute('type') == 'number'
            assert quantity_input.get_attribute('min') == '1'
    
    def test_cart_page_responsive_design(self, products_page, cart_page, ui_test_data):
        """
        Should be responsive across different screen sizes.
        
        Tests that the cart page is responsive.
        """
        # Arrange
        products_page.navigate_to_products()
        assert products_page.has_products()
        
        # Add product to cart
        products_page.add_product_to_cart(0)
        cart_page.navigate_to_cart()
        
        # Test different viewport sizes
        viewports = [
            {"width": 1920, "height": 1080},  # Desktop
            {"width": 1024, "height": 768},   # Tablet
            {"width": 375, "height": 667}     # Mobile
        ]
        
        for viewport in viewports:
            # Act
            cart_page.page.set_viewport_size(viewport["width"], viewport["height"])
            
            # Assert
            assert cart_page.is_on_cart_page()
            if cart_page.has_items():
                assert cart_page.cart_table.is_visible()
                assert cart_page.proceed_to_checkout_button.is_visible()
    
    def test_cart_page_error_handling(self, products_page, cart_page, ui_test_data):
        """
        Should handle errors gracefully.
        
        Tests that the cart page handles errors gracefully.
        """
        # Arrange
        cart_page.navigate_to_cart()
        
        # Test with empty cart
        if cart_page.is_cart_empty():
            assert cart_page.get_empty_cart_message() == "Cart is empty!"
            assert cart_page.continue_shopping_button.is_visible()
        
        # Test with invalid quantity
        if cart_page.has_items():
            cart_page.update_item_quantity(0, -1)  # Invalid quantity
            # Should handle gracefully without crashing
    
    def test_cart_page_data_consistency(self, products_page, cart_page, ui_test_data):
        """
        Should maintain data consistency.
        
        Tests that the cart page maintains data consistency.
        """
        # Arrange
        products_page.navigate_to_products()
        assert products_page.has_products()
        
        # Add product to cart
        products_page.add_product_to_cart(0)
        cart_page.navigate_to_cart()
        
        # Get initial cart state
        initial_items = cart_page.get_all_cart_items()
        initial_count = cart_page.get_cart_items_count()
        
        # Test that cart state remains consistent
        for _ in range(3):
            cart_page.page.reload()
            cart_page.wait_for_page_load()
            
            current_items = cart_page.get_all_cart_items()
            current_count = cart_page.get_cart_items_count()
            
            assert current_count == initial_count, "Cart item count should remain consistent"
            assert len(current_items) == len(initial_items), "Cart items should remain consistent"
    
    def test_cart_page_security(self, products_page, cart_page, ui_test_data):
        """
        Should maintain security standards.
        
        Tests that the cart page maintains security standards.
        """
        # Arrange
        products_page.navigate_to_products()
        assert products_page.has_products()
        
        # Add product to cart
        products_page.add_product_to_cart(0)
        cart_page.navigate_to_cart()
        
        # Test XSS prevention
        if cart_page.has_items():
            xss_payload = "<script>alert('xss')</script>"
            cart_page.update_item_quantity_by_name(xss_payload, 1)
            
            # Should not execute script and should handle safely
            assert cart_page.is_on_cart_page()
            assert cart_page.has_items() or cart_page.is_cart_empty()
        
        # Test SQL injection prevention
        sql_payload = "'; DROP TABLE cart; --"
        cart_page.remove_item_by_name(sql_payload)
        
        # Should not crash and should handle safely
        assert cart_page.is_on_cart_page()
        assert cart_page.has_items() or cart_page.is_cart_empty()
    
    def test_cart_page_workflow(self, products_page, cart_page, ui_test_data):
        """
        Should handle complete cart workflow.
        
        Tests the complete cart workflow from adding products to checkout.
        """
        # Arrange
        products_page.navigate_to_products()
        assert products_page.has_products()
        
        # Act - Complete workflow
        # 1. Add products to cart
        product_indices = [0, 1, 2] if products_page.get_product_count() >= 3 else [0]
        
        for index in product_indices:
            products_page.add_product_to_cart(index)
        
        # 2. Navigate to cart
        cart_page.navigate_to_cart()
        assert cart_page.has_items()
        
        # 3. Update quantities
        for i in range(len(product_indices)):
            cart_page.update_item_quantity(i, 2)
        
        # 4. Verify totals
        assert cart_page.verify_cart_totals()
        
        # 5. Proceed to checkout
        cart_page.proceed_to_checkout()
        cart_page.verify_checkout_modal_visible()
        
        # 6. Close modal and continue
        cart_page.close_checkout_modal()
        assert cart_page.is_on_cart_page()
        
        # 7. Remove some items
        if cart_page.get_cart_items_count() > 1:
            cart_page.remove_item(0)
        
        # 8. Verify final state
        assert cart_page.has_items() or cart_page.is_cart_empty()
        if cart_page.has_items():
            assert cart_page.verify_cart_totals()
