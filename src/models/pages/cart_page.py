"""
Cart Page Object Model for AutomationExercise testing framework.
"""
from typing import List, Dict, Any
from playwright.sync_api import Page, Locator, expect
from .base_page import BasePage


class CartPage(BasePage):
    """Cart page object model."""
    
    def __init__(self, page: Page):
        """
        Initialize the cart page.
        
        Args:
            page: Playwright page object
        """
        super().__init__(page)
        
        # Page Header Elements
        self.page_header = page.locator('#header')
        self.navigation_menu = page.locator('.shop-menu.pull-right')
        self.cart_link = page.locator('a[href="/view_cart"]')
        
        # Cart Section Elements
        self.cart_section = page.locator('#cart_info_table')
        self.cart_table = page.locator('#cart_info_table table')
        self.cart_items = page.locator('#cart_info_table tbody tr')
        
        # Cart Item Elements
        self.item_images = page.locator('#cart_info_table tbody tr td.cart_product img')
        self.item_names = page.locator('#cart_info_table tbody tr td.cart_description h4 a')
        self.item_prices = page.locator('#cart_info_table tbody tr td.cart_price p')
        self.item_quantities = page.locator('#cart_info_table tbody tr td.cart_quantity input')
        self.item_totals = page.locator('#cart_info_table tbody tr td.cart_total p')
        self.remove_buttons = page.locator('#cart_info_table tbody tr td.cart_delete a')
        
        # Cart Summary Elements
        self.cart_summary = page.locator('.cart_info')
        self.total_price = page.locator('.cart_total_price')
        self.proceed_to_checkout_button = page.locator('.btn.btn-default.check_out')
        
        # Empty Cart Elements
        self.empty_cart_message = page.locator('p:has-text("Cart is empty!")')
        self.continue_shopping_button = page.locator('a:has-text("here")')
        
        # Checkout Elements
        self.checkout_modal = page.locator('#checkoutModal.modal')
        self.checkout_modal_dialog = page.locator('#checkoutModal .modal-dialog')
        self.checkout_modal_content = page.locator('#checkoutModal .modal-content')
        self.checkout_modal_header = page.locator('#checkoutModal .modal-header')
        self.checkout_modal_title = page.locator('#checkoutModal .modal-title')
        self.checkout_modal_body = page.locator('#checkoutModal .modal-body')
        self.checkout_modal_footer = page.locator('#checkoutModal .modal-footer')
        self.register_login_button = page.locator('#checkoutModal a:has-text("Register / Login")')
        self.checkout_as_guest_button = page.locator('#checkoutModal button:has-text("Checkout as Guest")')
        
        # Page Footer
        self.page_footer = page.locator('#footer')
    
    def navigate_to_cart(self) -> None:
        """Navigate to the cart page."""
        self.navigate('/view_cart')
        self.wait_for_page_load()
    
    def wait_for_page_load(self) -> None:
        """Wait for cart page to load."""
        self.page.wait_for_load_state('networkidle')
        # Wait for either cart items or empty cart message
        try:
            self.cart_items.first().wait_for(state='visible', timeout=5000)
        except Exception:
            # If no items, wait for empty cart message
            self.empty_cart_message.wait_for(state='visible', timeout=5000)
    
    # Cart Item Methods
    def get_cart_items_count(self) -> int:
        """Get the number of items in cart."""
        try:
            if self.empty_cart_message.is_visible():
                return 0
            return self.cart_items.count()
        except Exception:
            return 0
    
    def get_cart_item_by_index(self, index: int) -> Dict[str, str]:
        """
        Get cart item information by index.
        
        Args:
            index: Item index
            
        Returns:
            Dictionary with item information
        """
        item = self.cart_items.nth(index)
        
        return {
            'name': item.locator('td.cart_description h4 a').text_content() or '',
            'price': item.locator('td.cart_price p').text_content() or '',
            'quantity': item.locator('td.cart_quantity input').input_value() or '1',
            'total': item.locator('td.cart_total p').text_content() or '',
            'index': index
        }
    
    def get_all_cart_items(self) -> List[Dict[str, str]]:
        """Get all cart items information."""
        items = []
        count = self.get_cart_items_count()
        
        for i in range(count):
            item_info = self.get_cart_item_by_index(i)
            items.append(item_info)
        
        return items
    
    def update_item_quantity(self, index: int, quantity: int) -> None:
        """
        Update item quantity.
        
        Args:
            index: Item index
            quantity: New quantity
        """
        quantity_input = self.item_quantities.nth(index)
        quantity_input.clear()
        quantity_input.fill(str(quantity))
        # Trigger change event
        quantity_input.press('Tab')
        self.page.wait_for_load_state('networkidle')
    
    def remove_item(self, index: int) -> None:
        """
        Remove item from cart.
        
        Args:
            index: Item index
        """
        remove_button = self.remove_buttons.nth(index)
        remove_button.click()
        self.page.wait_for_load_state('networkidle')
    
    def remove_all_items(self) -> None:
        """Remove all items from cart."""
        count = self.get_cart_items_count()
        for i in range(count):
            self.remove_item(0)  # Always remove first item as list changes
    
    def get_item_total_price(self, index: int) -> float:
        """
        Get item total price.
        
        Args:
            index: Item index
            
        Returns:
            Item total price as float
        """
        total_text = self.item_totals.nth(index).text_content() or '0'
        # Extract number from text like "Rs. 500"
        try:
            return float(''.join(filter(str.isdigit, total_text)))
        except (ValueError, TypeError):
            return 0.0
    
    def get_cart_total_price(self) -> float:
        """Get cart total price."""
        try:
            total_text = self.total_price.text_content() or '0'
            # Extract number from text like "Rs. 500"
            return float(''.join(filter(str.isdigit, total_text)))
        except (ValueError, TypeError):
            return 0.0
    
    # Checkout Methods
    def proceed_to_checkout(self) -> None:
        """Proceed to checkout."""
        self.proceed_to_checkout_button.click()
        self.page.wait_for_load_state('networkidle')
    
    def verify_checkout_modal_visible(self) -> None:
        """Verify checkout modal is visible."""
        expect(self.checkout_modal).to_be_visible()
        expect(self.checkout_modal_title).to_be_visible()
        expect(self.register_login_button).to_be_visible()
        expect(self.checkout_as_guest_button).to_be_visible()
    
    def register_login_from_checkout(self) -> None:
        """Click register/login button from checkout modal."""
        self.register_login_button.click()
        expect(self.page).to_have_url('*login*')
    
    def checkout_as_guest(self) -> None:
        """Click checkout as guest button."""
        self.checkout_as_guest_button.click()
        self.page.wait_for_load_state('networkidle')
    
    def close_checkout_modal(self) -> None:
        """Close checkout modal."""
        # Click outside modal or close button
        self.page.keyboard.press('Escape')
        expect(self.checkout_modal).to_be_hidden()
    
    # Empty Cart Methods
    def is_cart_empty(self) -> bool:
        """Check if cart is empty."""
        try:
            return self.empty_cart_message.is_visible()
        except Exception:
            return False
    
    def continue_shopping_from_empty_cart(self) -> None:
        """Continue shopping from empty cart."""
        self.continue_shopping_button.click()
        expect(self.page).to_have_url('*products*')
    
    def get_empty_cart_message(self) -> str:
        """Get empty cart message."""
        return self.empty_cart_message.text_content() or ''
    
    # Verification Methods
    def verify_cart_page(self) -> None:
        """Verify cart page elements."""
        expect(self.page).to_have_url('*view_cart*')
        expect(self.cart_section).to_be_visible()
    
    def verify_page_structure(self) -> None:
        """Verify page structure."""
        expect(self.page_header).to_be_visible()
        expect(self.cart_section).to_be_visible()
        expect(self.page_footer).to_be_visible()
    
    def verify_cart_table_structure(self) -> None:
        """Verify cart table structure."""
        if not self.is_cart_empty():
            expect(self.cart_table).to_be_visible()
            expect(self.cart_items).to_have_count_greater_than(0)
            
            # Verify table headers
            expect(self.cart_table.locator('thead th')).to_have_count_greater_than(0)
    
    def verify_cart_items_structure(self) -> None:
        """Verify cart items structure."""
        if not self.is_cart_empty():
            first_item = self.cart_items.first()
            
            # Verify each item has required elements
            expect(first_item.locator('td.cart_product img')).to_be_visible()
            expect(first_item.locator('td.cart_description h4 a')).to_be_visible()
            expect(first_item.locator('td.cart_price p')).to_be_visible()
            expect(first_item.locator('td.cart_quantity input')).to_be_visible()
            expect(first_item.locator('td.cart_total p')).to_be_visible()
            expect(first_item.locator('td.cart_delete a')).to_be_visible()
    
    def verify_cart_summary(self) -> None:
        """Verify cart summary."""
        if not self.is_cart_empty():
            expect(self.cart_summary).to_be_visible()
            expect(self.total_price).to_be_visible()
            expect(self.proceed_to_checkout_button).to_be_visible()
    
    def verify_empty_cart(self) -> None:
        """Verify empty cart state."""
        expect(self.empty_cart_message).to_be_visible()
        expect(self.continue_shopping_button).to_be_visible()
    
    def verify_checkout_functionality(self) -> None:
        """Verify checkout functionality."""
        if not self.is_cart_empty():
            self.proceed_to_checkout()
            self.verify_checkout_modal_visible()
            self.close_checkout_modal()
    
    # State Checking Methods
    def is_on_cart_page(self) -> bool:
        """Check if on cart page."""
        return 'view_cart' in self.page.url
    
    def has_items(self) -> bool:
        """Check if cart has items."""
        return not self.is_cart_empty()
    
    def can_proceed_to_checkout(self) -> bool:
        """Check if can proceed to checkout."""
        try:
            return self.proceed_to_checkout_button.is_visible() and self.proceed_to_checkout_button.is_enabled()
        except Exception:
            return False
    
    # Utility Methods
    def get_cart_summary_info(self) -> Dict[str, Any]:
        """Get cart summary information."""
        return {
            'items_count': self.get_cart_items_count(),
            'total_price': self.get_cart_total_price(),
            'is_empty': self.is_cart_empty(),
            'can_checkout': self.can_proceed_to_checkout()
        }
    
    def calculate_expected_total(self) -> float:
        """Calculate expected cart total."""
        items = self.get_all_cart_items()
        total = 0.0
        
        for item in items:
            try:
                price = float(''.join(filter(str.isdigit, item['price'])))
                quantity = int(item['quantity'])
                total += price * quantity
            except (ValueError, TypeError):
                continue
        
        return total
    
    def verify_cart_totals(self) -> bool:
        """Verify cart totals are correct."""
        expected_total = self.calculate_expected_total()
        actual_total = self.get_cart_total_price()
        
        # Allow small difference due to rounding
        return abs(expected_total - actual_total) < 0.01
    
    def get_item_by_name(self, name: str) -> Dict[str, str]:
        """
        Get cart item by name.
        
        Args:
            name: Item name
            
        Returns:
            Item information or empty dict if not found
        """
        items = self.get_all_cart_items()
        for item in items:
            if name.lower() in item['name'].lower():
                return item
        return {}
    
    def update_item_quantity_by_name(self, name: str, quantity: int) -> bool:
        """
        Update item quantity by name.
        
        Args:
            name: Item name
            quantity: New quantity
            
        Returns:
            True if item found and updated, False otherwise
        """
        items = self.get_all_cart_items()
        for i, item in enumerate(items):
            if name.lower() in item['name'].lower():
                self.update_item_quantity(i, quantity)
                return True
        return False
    
    def remove_item_by_name(self, name: str) -> bool:
        """
        Remove item by name.
        
        Args:
            name: Item name
            
        Returns:
            True if item found and removed, False otherwise
        """
        items = self.get_all_cart_items()
        for i, item in enumerate(items):
            if name.lower() in item['name'].lower():
                self.remove_item(i)
                return True
        return False
    
    def clear_cart(self) -> None:
        """Clear all items from cart."""
        while not self.is_cart_empty():
            self.remove_item(0)
    
    def add_items_to_cart_from_products_page(self, products_page, item_indices: List[int]) -> None:
        """
        Add items to cart from products page.
        
        Args:
            products_page: Products page object
            item_indices: List of item indices to add
        """
        for index in item_indices:
            products_page.add_product_to_cart(index)
        
        # Navigate to cart
        self.navigate_to_cart()
    
    def verify_cart_contents(self, expected_items: List[str]) -> bool:
        """
        Verify cart contains expected items.
        
        Args:
            expected_items: List of expected item names
            
        Returns:
            True if all expected items are in cart, False otherwise
        """
        cart_items = self.get_all_cart_items()
        cart_item_names = [item['name'] for item in cart_items]
        
        for expected_item in expected_items:
            if not any(expected_item.lower() in name.lower() for name in cart_item_names):
                return False
        
        return True
