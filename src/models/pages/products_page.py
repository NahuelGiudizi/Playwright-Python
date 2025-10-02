"""
Products Page Object Model for AutomationExercise testing framework.
"""
from typing import List, Dict, Any
from playwright.sync_api import Page, Locator, expect
from .base_page import BasePage


class ProductsPage(BasePage):
    """Products page object model."""
    
    def __init__(self, page: Page):
        """
        Initialize the products page.
        
        Args:
            page: Playwright page object
        """
        super().__init__(page)
        
        # Page Header Elements
        self.page_header = page.locator('#header')
        self.navigation_menu = page.locator('.shop-menu.pull-right')
        self.products_link = page.locator('a[href="/products"]')
        
        # Products Section Elements
        self.products_section = page.locator('.features_items')
        self.products_title = page.locator('.title.text-center:has-text("All Products")')
        self.product_image_wrappers = page.locator('.product-image-wrapper')
        self.single_products = page.locator('.single-products')
        self.product_infos = page.locator('.productinfo.text-center')
        self.product_images = page.locator('.productinfo.text-center img[alt="ecommerce website products"]')
        self.product_prices = page.locator('.productinfo.text-center h2')
        self.product_names = page.locator('.productinfo.text-center p')
        self.add_to_cart_buttons = page.locator('a.add-to-cart[data-product-id]')
        self.view_product_links = page.locator('a[href*="/product_details/"]:has-text("View Product")')
        self.product_overlays = page.locator('.product-overlay .overlay-content')
        
        # Search and Filter Elements
        self.search_product_input = page.locator('#search_product')
        self.submit_search_button = page.locator('#submit_search')
        self.search_results = page.locator('.features_items .product-image-wrapper')
        
        # Category Filter Elements
        self.category_sidebar = page.locator('.left-sidebar')
        self.category_section = page.locator('.left-sidebar h2:has-text("Category")')
        self.category_accordion = page.locator('#accordian.category-products')
        self.category_panels = page.locator('#accordian .panel.panel-default')
        self.women_category = page.locator('#accordian a[href="#Women"]')
        self.men_category = page.locator('#accordian a[href="#Men"]')
        self.kids_category = page.locator('#accordian a[href="#Kids"]')
        self.category_links = page.locator('#accordian .panel-body a[href*="/category_products/"]')
        
        # Brand Filter Elements
        self.brands_section = page.locator('.brands_products')
        self.brands_title = page.locator('.brands_products h2:has-text("Brands")')
        self.brands_list = page.locator('.brands_products .brands-name')
        self.brand_links = page.locator('.brands_products a[href*="/brand_products/"]')
        
        # Cart Modal Elements
        self.cart_modal = page.locator('#cartModal.modal')
        self.cart_modal_dialog = page.locator('#cartModal .modal-dialog')
        self.cart_modal_content = page.locator('#cartModal .modal-content')
        self.cart_modal_header = page.locator('#cartModal .modal-header')
        self.cart_modal_title = page.locator('#cartModal .modal-title:has-text("Added!")')
        self.cart_modal_body = page.locator('#cartModal .modal-body')
        self.cart_modal_footer = page.locator('#cartModal .modal-footer')
        self.continue_shopping_button = page.locator('#cartModal button.close-modal:has-text("Continue Shopping")')
        self.view_cart_link = page.locator('#cartModal a[href="/view_cart"]:has-text("View Cart")')
        
        # Pagination Elements
        self.pagination = page.locator('.pagination')
        self.page_numbers = page.locator('.pagination li a')
        self.next_page_button = page.locator('.pagination .next')
        self.previous_page_button = page.locator('.pagination .prev')
        
        # Sort Elements
        self.sort_dropdown = page.locator('#sort')
        self.sort_options = page.locator('#sort option')
        
        # Page Footer
        self.page_footer = page.locator('#footer')
    
    def navigate_to_products(self) -> None:
        """Navigate to the products page."""
        self.navigate('/products')
        self.wait_for_page_load()
    
    def wait_for_page_load(self) -> None:
        """Wait for products page to load."""
        self.page.wait_for_load_state('networkidle')
        expect(self.products_section).to_be_visible()
        expect(self.products_title).to_be_visible()
    
    # Search Methods
    def search_for_product(self, search_term: str) -> None:
        """
        Search for a product.
        
        Args:
            search_term: Product search term
        """
        self.search_product_input.fill(search_term)
        self.submit_search_button.click()
        self.page.wait_for_load_state('networkidle')
    
    def get_search_results_count(self) -> int:
        """Get the number of search results."""
        return self.search_results.count()
    
    def get_search_results_names(self) -> List[str]:
        """Get names of search results."""
        return self.search_results.locator('.productinfo.text-center p').all_text_contents()
    
    def verify_search_results(self, search_term: str) -> bool:
        """
        Verify search results contain the search term.
        
        Args:
            search_term: Search term to verify
            
        Returns:
            True if results contain search term, False otherwise
        """
        results = self.get_search_results_names()
        return any(search_term.lower() in result.lower() for result in results)
    
    # Category Methods
    def expand_category_section(self, category_name: str) -> None:
        """
        Expand a category section.
        
        Args:
            category_name: Name of the category to expand
        """
        category_header = self.page.locator(f'#accordian a[href="#{category_name}"]')
        category_panel = self.page.locator(f'#{category_name}.panel-collapse')
        
        # Check if already expanded
        if category_panel.is_visible():
            return
        
        # Click to expand
        category_header.click()
        expect(category_panel).to_be_visible()
        self.page.wait_for_timeout(300)
    
    def click_category_link(self, category_name: str) -> None:
        """
        Click a category link.
        
        Args:
            category_name: Name of the category to click
        """
        # First expand the appropriate parent category
        if any(term in category_name.lower() for term in ['dress', 'tops', 'saree']):
            self.expand_category_section('Women')
        elif any(term in category_name.lower() for term in ['tshirts', 'jeans']):
            self.expand_category_section('Men')
        elif 'kids' in category_name.lower():
            self.expand_category_section('Kids')
        
        category_link = self.category_links.filter(has_text=category_name).first()
        category_link.click()
        self.page.wait_for_load_state('networkidle')
    
    def get_category_links(self) -> List[str]:
        """Get all category links."""
        # Expand all categories first
        self.expand_category_section('Women')
        self.expand_category_section('Men')
        self.expand_category_section('Kids')
        
        return self.category_links.all_text_contents()
    
    # Brand Methods
    def click_brand_link(self, brand_name: str) -> None:
        """
        Click a brand link.
        
        Args:
            brand_name: Name of the brand to click
        """
        brand_link = self.brand_links.filter(has_text=brand_name).first()
        brand_link.click()
        self.page.wait_for_load_state('networkidle')
    
    def get_brand_links(self) -> List[str]:
        """Get all brand links."""
        return self.brand_links.all_text_contents()
    
    def get_brand_with_count(self, brand_name: str) -> Dict[str, Any]:
        """
        Get brand name with product count.
        
        Args:
            brand_name: Name of the brand
            
        Returns:
            Dictionary with brand name and count
        """
        brand_link = self.brand_links.filter(has_text=brand_name).first()
        full_text = brand_link.text_content() or ''
        
        # Extract count from text like "Brand Name (5)"
        if '(' in full_text and ')' in full_text:
            start = full_text.rfind('(')
            end = full_text.rfind(')')
            if start != -1 and end != -1:
                count_text = full_text[start+1:end]
                try:
                    count = int(count_text)
                    return {"name": brand_name, "count": count}
                except ValueError:
                    pass
        
        return {"name": brand_name, "count": 0}
    
    # Product Methods
    def get_product_count(self) -> int:
        """Get the number of products on the page."""
        self.product_image_wrappers.first().wait_for(state='visible')
        return self.product_image_wrappers.count()
    
    def get_product_names(self) -> List[str]:
        """Get all product names."""
        self.product_names.first().wait_for(state='visible')
        return self.product_names.all_text_contents()
    
    def get_product_prices(self) -> List[str]:
        """Get all product prices."""
        self.product_prices.first().wait_for(state='visible')
        return self.product_prices.all_text_contents()
    
    def get_product_by_index(self, index: int) -> Dict[str, str]:
        """
        Get product information by index.
        
        Args:
            index: Product index
            
        Returns:
            Dictionary with product information
        """
        product_wrapper = self.product_image_wrappers.nth(index)
        name = product_wrapper.locator('.productinfo.text-center p').text_content() or ''
        price = product_wrapper.locator('.productinfo.text-center h2').text_content() or ''
        
        return {
            'name': name,
            'price': price,
            'index': index
        }
    
    def add_product_to_cart(self, index: int) -> None:
        """
        Add a product to cart by index.
        
        Args:
            index: Product index
        """
        self.add_to_cart_buttons.nth(index).click()
        expect(self.cart_modal).to_be_visible()
        self.continue_shopping_button.click()
        expect(self.cart_modal).to_be_hidden()
    
    def add_product_to_cart_by_id(self, product_id: str) -> None:
        """
        Add a product to cart by product ID.
        
        Args:
            product_id: Product ID
        """
        cart_button = self.add_to_cart_buttons.locator(f'[data-product-id="{product_id}"]').first()
        cart_button.click()
        expect(self.cart_modal).to_be_visible()
        self.continue_shopping_button.click()
        expect(self.cart_modal).to_be_hidden()
    
    def view_product(self, index: int) -> None:
        """
        View product details by index.
        
        Args:
            index: Product index
        """
        self.view_product_links.nth(index).click()
        expect(self.page).to_have_url('*product_details*')
    
    def hover_over_product(self, index: int) -> None:
        """
        Hover over a product.
        
        Args:
            index: Product index
        """
        self.product_image_wrappers.nth(index).hover()
        expect(self.product_overlays.nth(index)).to_be_visible()
    
    def get_product_overlay_buttons(self, index: int) -> List[Locator]:
        """
        Get product overlay buttons.
        
        Args:
            index: Product index
            
        Returns:
            List of overlay button locators
        """
        overlay = self.product_overlays.nth(index)
        return [
            overlay.locator('a.add-to-cart'),
            overlay.locator('a:has-text("View Product")')
        ]
    
    # Cart Modal Methods
    def verify_cart_modal_visible(self) -> None:
        """Verify cart modal is visible."""
        expect(self.cart_modal).to_be_visible()
        expect(self.cart_modal_title).to_be_visible()
        expect(self.continue_shopping_button).to_be_visible()
        expect(self.view_cart_link).to_be_visible()
    
    def continue_shopping(self) -> None:
        """Click continue shopping button."""
        self.continue_shopping_button.click()
        expect(self.cart_modal).to_be_hidden()
    
    def view_cart(self) -> None:
        """Click view cart link."""
        self.view_cart_link.click()
        expect(self.page).to_have_url('*view_cart*')
    
    # Pagination Methods
    def get_current_page_number(self) -> int:
        """Get current page number."""
        active_page = self.page_numbers.filter(has_text='active')
        if active_page.count() > 0:
            return int(active_page.text_content() or '1')
        return 1
    
    def get_total_pages(self) -> int:
        """Get total number of pages."""
        return self.page_numbers.count()
    
    def go_to_page(self, page_number: int) -> None:
        """
        Go to a specific page.
        
        Args:
            page_number: Page number to navigate to
        """
        page_link = self.page_numbers.filter(has_text=str(page_number)).first()
        page_link.click()
        self.page.wait_for_load_state('networkidle')
    
    def go_to_next_page(self) -> None:
        """Go to next page."""
        self.next_page_button.click()
        self.page.wait_for_load_state('networkidle')
    
    def go_to_previous_page(self) -> None:
        """Go to previous page."""
        self.previous_page_button.click()
        self.page.wait_for_load_state('networkidle')
    
    def is_pagination_visible(self) -> bool:
        """Check if pagination is visible."""
        try:
            return self.pagination.is_visible()
        except Exception:
            return False
    
    # Sort Methods
    def get_sort_options(self) -> List[str]:
        """Get all sort options."""
        return [option.text_content() or '' for option in self.sort_options.all()]
    
    def select_sort_option(self, sort_option: str) -> None:
        """
        Select a sort option.
        
        Args:
            sort_option: Sort option to select
        """
        self.sort_dropdown.select_option(sort_option)
        self.page.wait_for_load_state('networkidle')
    
    def sort_by_price_low_to_high(self) -> None:
        """Sort products by price low to high."""
        self.select_sort_option('Price')
    
    def sort_by_price_high_to_low(self) -> None:
        """Sort products by price high to low."""
        self.select_sort_option('Price')
    
    def sort_by_name_a_to_z(self) -> None:
        """Sort products by name A to Z."""
        self.select_sort_option('Name')
    
    def sort_by_name_z_to_a(self) -> None:
        """Sort products by name Z to A."""
        self.select_sort_option('Name')
    
    # Verification Methods
    def verify_products_page(self) -> None:
        """Verify products page elements."""
        expect(self.products_section).to_be_visible()
        expect(self.products_title).to_be_visible()
        expect(self.page).to_have_url('*products*')
    
    def verify_page_structure(self) -> None:
        """Verify page structure."""
        expect(self.page_header).to_be_visible()
        expect(self.products_section).to_be_visible()
        expect(self.category_sidebar).to_be_visible()
        expect(self.brands_section).to_be_visible()
        expect(self.page_footer).to_be_visible()
    
    def verify_search_functionality(self) -> None:
        """Verify search functionality."""
        expect(self.search_product_input).to_be_visible()
        expect(self.submit_search_button).to_be_visible()
    
    def verify_category_filter(self) -> None:
        """Verify category filter."""
        expect(self.category_section).to_be_visible()
        expect(self.category_accordion).to_be_visible()
        expect(self.women_category).to_be_visible()
        expect(self.men_category).to_be_visible()
        expect(self.kids_category).to_be_visible()
    
    def verify_brand_filter(self) -> None:
        """Verify brand filter."""
        expect(self.brands_section).to_be_visible()
        expect(self.brands_title).to_be_visible()
        expect(self.brands_list).to_be_visible()
    
    def verify_product_structure(self) -> None:
        """Verify product structure."""
        first_product = self.product_image_wrappers.first()
        expect(first_product).to_be_visible()
        
        # Verify each product has required elements
        expect(first_product.locator('.productinfo.text-center')).to_be_visible()
        expect(first_product.locator('img')).to_be_visible()
        expect(first_product.locator('h2')).to_be_visible()  # Price
        expect(first_product.locator('p')).to_be_visible()  # Product name
        expect(first_product.locator('a.add-to-cart')).to_be_visible()
        expect(first_product.locator('a:has-text("View Product")')).to_be_visible()
    
    def verify_cart_modal_functionality(self) -> None:
        """Verify cart modal functionality."""
        # Add a product to cart to trigger modal
        if self.add_to_cart_buttons.count() > 0:
            self.add_to_cart_buttons.first().click()
            self.verify_cart_modal_visible()
            self.continue_shopping()
    
    def verify_pagination_functionality(self) -> None:
        """Verify pagination functionality."""
        if self.is_pagination_visible():
            expect(self.pagination).to_be_visible()
            expect(self.page_numbers).to_have_count_greater_than(0)
    
    def verify_sort_functionality(self) -> None:
        """Verify sort functionality."""
        expect(self.sort_dropdown).to_be_visible()
        sort_options = self.get_sort_options()
        assert len(sort_options) > 0, "Should have sort options"
    
    # State Checking Methods
    def is_on_products_page(self) -> bool:
        """Check if on products page."""
        return 'products' in self.page.url
    
    def has_products(self) -> bool:
        """Check if page has products."""
        try:
            return self.product_image_wrappers.count() > 0
        except Exception:
            return False
    
    def has_search_results(self) -> bool:
        """Check if page has search results."""
        try:
            return self.search_results.count() > 0
        except Exception:
            return False
    
    # Utility Methods
    def get_all_products_info(self) -> List[Dict[str, str]]:
        """Get information for all products on the page."""
        products = []
        count = self.get_product_count()
        
        for i in range(count):
            product_info = self.get_product_by_index(i)
            products.append(product_info)
        
        return products
    
    def filter_products_by_price_range(self, min_price: float, max_price: float) -> List[Dict[str, str]]:
        """
        Filter products by price range.
        
        Args:
            min_price: Minimum price
            max_price: Maximum price
            
        Returns:
            List of products within price range
        """
        all_products = self.get_all_products_info()
        filtered_products = []
        
        for product in all_products:
            # Extract price from string like "Rs. 500"
            price_text = product['price']
            try:
                # Remove currency symbols and extract number
                price_value = float(''.join(filter(str.isdigit, price_text)))
                if min_price <= price_value <= max_price:
                    filtered_products.append(product)
            except (ValueError, TypeError):
                continue
        
        return filtered_products
    
    def get_products_by_category(self, category: str) -> List[Dict[str, str]]:
        """
        Get products by category.
        
        Args:
            category: Category name
            
        Returns:
            List of products in category
        """
        # Click category link first
        self.click_category_link(category)
        
        # Get products after filtering
        return self.get_all_products_info()
    
    def get_products_by_brand(self, brand: str) -> List[Dict[str, str]]:
        """
        Get products by brand.
        
        Args:
            brand: Brand name
            
        Returns:
            List of products by brand
        """
        # Click brand link first
        self.click_brand_link(brand)
        
        # Get products after filtering
        return self.get_all_products_info()
