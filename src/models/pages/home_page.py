"""
Home Page Object Model for AutomationExercise testing framework.
"""
from typing import List
from playwright.sync_api import Page, Locator, expect
from .base_page import BasePage


class HomePage(BasePage):
    """Home page object model."""
    
    def __init__(self, page: Page):
        """
        Initialize the home page.
        
        Args:
            page: Playwright page object
        """
        super().__init__(page)
        
        # Header Elements
        self.header = page.locator('#header')
        self.header_middle = page.locator('.header-middle')
        self.logo_container = page.locator('.logo.pull-left')
        self.logo = page.locator('img[alt="Website for automation practice"]')
        self.logo_link = page.locator('.logo a[href="/"]')
        
        # Navigation Menu Elements
        self.shop_menu = page.locator('.shop-menu.pull-right')
        self.navbar_nav = page.locator('.nav.navbar-nav')
        self.home_link = page.locator('a[href="/"]').filter(has_text='Home')
        self.products_link = page.locator('a[href="/products"]')
        self.cart_link = page.locator('a[href="/view_cart"]')
        self.signup_login_link = page.locator('a[href="/login"]')
        self.test_cases_link = page.locator('a[href="/test_cases"]')
        self.api_testing_link = page.locator('a[href="/api_list"]')
        self.video_tutorials_link = page.locator('a[href="https://www.youtube.com/c/AutomationExercise"]')
        self.contact_us_link = page.locator('a[href="/contact_us"]')
        
        # Post-Login Navigation Elements
        self.logout_link = page.locator('a[href="/logout"]:has-text("Logout")')
        self.delete_account_link = page.locator('a[href="/delete_account"]:has-text("Delete Account")')
        self.logged_in_username = page.locator('.nav.navbar-nav b').first()
        
        # Main Slider/Carousel Section
        self.slider_section = page.locator('#slider')
        self.slider_carousel = page.locator('#slider-carousel.carousel.slide')
        self.carousel_indicators = page.locator('#slider-carousel .carousel-indicators')
        self.carousel_inner = page.locator('#slider-carousel .carousel-inner')
        self.carousel_items = page.locator('#slider-carousel .carousel-inner .item')
        self.carousel_active_item = page.locator('#slider-carousel .carousel-inner .item.active')
        self.carousel_left_control = page.locator('#slider-carousel .left.control-carousel')
        self.carousel_right_control = page.locator('#slider-carousel .right.control-carousel')
        
        # Carousel Content Elements
        self.carousel_title = page.locator('.carousel-inner h1:has-text("Automation")')
        self.carousel_subtitle = page.locator('.carousel-inner h2:has-text("Full-Fledged practice website")')
        self.carousel_description = page.locator('.carousel-inner p').first()
        self.test_cases_button = page.locator('a.test_cases_list button:has-text("Test Cases")')
        self.apis_list_button = page.locator('a.apis_list button:has-text("APIs list for practice")')
        self.carousel_images = page.locator('.carousel-inner img.girl.img-responsive')
        
        # Left Sidebar Elements
        self.left_sidebar = page.locator('.left-sidebar')
        self.category_section = page.locator('.left-sidebar h2:has-text("Category")')
        self.category_accordion = page.locator('#accordian.category-products')
        self.category_panels = page.locator('#accordian .panel.panel-default')
        self.women_category = page.locator('#accordian a[href="#Women"]')
        self.men_category = page.locator('#accordian a[href="#Men"]')
        self.kids_category = page.locator('#accordian a[href="#Kids"]')
        self.category_links = page.locator('#accordian .panel-body a[href*="/category_products/"]')
        
        # Brands Section
        self.brands_section = page.locator('.brands_products')
        self.brands_title = page.locator('.brands_products h2:has-text("Brands")')
        self.brands_list = page.locator('.brands_products .brands-name')
        self.brand_links = page.locator('.brands_products a[href*="/brand_products/"]')
        
        # Featured Items Section
        self.featured_items_section = page.locator('.features_items')
        self.featured_items_title = page.locator('.features_items .title.text-center:has-text("Features Items")')
        self.featured_items = page.locator('.features_items')
        self.product_image_wrappers = page.locator('.product-image-wrapper')
        self.single_products = page.locator('.single-products')
        self.product_infos = page.locator('.productinfo.text-center')
        self.product_images = page.locator('.productinfo.text-center img[alt="ecommerce website products"]')
        self.product_prices = page.locator('.productinfo.text-center h2')
        self.product_names = page.locator('.productinfo.text-center p')
        self.add_to_cart_buttons = page.locator('a.add-to-cart[data-product-id]')
        self.view_product_links = page.locator('a[href*="/product_details/"]:has-text("View Product")')
        self.product_overlays = page.locator('.product-overlay .overlay-content')
        
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
        
        # Recommended Items Section
        self.recommended_items_section = page.locator('.recommended_items')
        self.recommended_items_title = page.locator('.recommended_items .title.text-center:has-text("recommended items")')
        self.recommended_items_carousel = page.locator('#recommended-item-carousel.carousel.slide')
        self.recommended_carousel_inner = page.locator('#recommended-item-carousel .carousel-inner')
        self.recommended_carousel_items = page.locator('#recommended-item-carousel .carousel-inner .item')
        self.recommended_left_control = page.locator('#recommended-item-carousel .left.recommended-item-control')
        self.recommended_right_control = page.locator('#recommended-item-carousel .right.recommended-item-control')
        
        # Footer Elements
        self.footer = page.locator('#footer')
        self.footer_widget = page.locator('.footer-widget')
        self.footer_bottom = page.locator('.footer-bottom')
        self.copyright_text = page.locator('.footer-bottom p:has-text("Copyright © 2021")')
        
        # Subscription Section
        self.subscription_section = page.locator('.single-widget:has(h2:has-text("Subscription"))')
        self.subscription_title = page.locator('.single-widget h2:has-text("Subscription")')
        self.subscription_form = page.locator('.single-widget form.searchform')
        self.subscription_email_input = page.locator('#susbscribe_email')
        self.subscription_button = page.locator('#subscribe')
        self.subscription_description = page.locator('.single-widget p')
        self.subscription_success_message = page.locator('#success-subscribe .alert-success')
        self.subscription_csrf_token = page.locator('.single-widget input[name="csrfmiddlewaretoken"]')
        
        # Scroll Elements
        self.scroll_up_button = page.locator('#scrollUp')
    
    # Navigation Methods
    def navigate(self) -> None:
        """Navigate to the home page."""
        self.page.goto('/')
        self.wait_for_page_load()
    
    def navigate_to_products(self) -> None:
        """Navigate to products page."""
        self.products_link.click()
        expect(self.page).to_have_url('*products*')
    
    def navigate_to_cart(self) -> None:
        """Navigate to cart page."""
        self.cart_link.click()
        expect(self.page).to_have_url('*view_cart*')
    
    def navigate_to_login(self) -> None:
        """Navigate to login page."""
        self.signup_login_link.click()
        expect(self.page).to_have_url('*login*')
    
    def navigate_to_contact_us(self) -> None:
        """Navigate to contact us page."""
        self.contact_us_link.click()
        expect(self.page).to_have_url('*contact_us*')
    
    def navigate_to_test_cases(self) -> None:
        """Navigate to test cases page."""
        self.test_cases_link.click()
        expect(self.page).to_have_url('*test_cases*')
    
    def navigate_to_api_testing(self) -> None:
        """Navigate to API testing page."""
        self.api_testing_link.click()
        expect(self.page).to_have_url('*api_list*')
    
    def navigate_to_video_tutorials(self) -> None:
        """Navigate to video tutorials (external link)."""
        self.video_tutorials_link.click()
    
    def click_logo(self) -> None:
        """Click the logo to go to home page."""
        self.logo_link.click()
        expect(self.page).to_have_url('*/')
    
    # Carousel Methods
    def interact_with_carousel(self) -> None:
        """Interact with the main carousel."""
        self.carousel_left_control.click()
        self.page.wait_for_timeout(1000)
        self.carousel_right_control.click()
        self.page.wait_for_timeout(1000)
    
    def click_carousel_indicator(self, index: int) -> None:
        """Click a carousel indicator."""
        self.carousel_indicators.locator('li').nth(index).click()
        self.page.wait_for_timeout(1000)
    
    def get_active_carousel_slide(self) -> int:
        """Get the active carousel slide index."""
        indicators = self.carousel_indicators.locator('li')
        count = indicators.count()
        
        for i in range(count):
            indicator = indicators.nth(i)
            class_name = indicator.get_attribute('class')
            if class_name and 'active' in class_name:
                return i
        return -1
    
    def click_test_cases_button(self) -> None:
        """Click the test cases button in carousel."""
        self.test_cases_button.click()
        expect(self.page).to_have_url('*test_cases*')
    
    def click_apis_list_button(self) -> None:
        """Click the APIs list button in carousel."""
        self.apis_list_button.click()
        expect(self.page).to_have_url('*api_list*')
    
    # Category Methods
    def expand_category_section(self, category_name: str) -> None:
        """Expand a category section."""
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
        """Click a category link."""
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
        """Click a brand link."""
        brand_link = self.brand_links.filter(has_text=brand_name).first()
        brand_link.click()
        self.page.wait_for_load_state('networkidle')
    
    def get_brand_links(self) -> List[str]:
        """Get all brand links."""
        return self.brand_links.all_text_contents()
    
    def get_brand_with_count(self, brand_name: str) -> dict:
        """Get brand name with product count."""
        brand_link = self.brand_links.filter(has_text=brand_name).first()
        full_text = brand_link.text_content() or ''
        count_match = None
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
    
    def add_product_to_cart(self, index: int) -> None:
        """Add a product to cart by index."""
        self.add_to_cart_buttons.nth(index).click()
        expect(self.cart_modal).to_be_visible()
        self.continue_shopping_button.click()
        expect(self.cart_modal).to_be_hidden()
    
    def add_product_to_cart_by_id(self, product_id: str) -> None:
        """Add a product to cart by product ID."""
        cart_button = self.add_to_cart_buttons.locator(f'[data-product-id="{product_id}"]').first()
        cart_button.click()
        expect(self.cart_modal).to_be_visible()
        self.continue_shopping_button.click()
        expect(self.cart_modal).to_be_hidden()
    
    def view_product(self, index: int) -> None:
        """View product details by index."""
        self.view_product_links.nth(index).click()
        expect(self.page).to_have_url('*product_details*')
    
    def hover_over_product(self, index: int) -> None:
        """Hover over a product."""
        self.product_image_wrappers.nth(index).hover()
        expect(self.product_overlays.nth(index)).to_be_visible()
    
    # Recommended Items Carousel Methods
    def interact_with_recommended_carousel(self) -> None:
        """Interact with the recommended items carousel."""
        self.recommended_left_control.click()
        self.page.wait_for_timeout(1000)
        self.recommended_right_control.click()
        self.page.wait_for_timeout(1000)
    
    def add_recommended_product_to_cart(self, index: int) -> None:
        """Add a recommended product to cart."""
        recommended_add_to_cart_button = self.recommended_carousel_items.locator('.productinfo.text-center a.add-to-cart').nth(index)
        recommended_add_to_cart_button.click()
        expect(self.cart_modal).to_be_visible()
        self.continue_shopping_button.click()
        expect(self.cart_modal).to_be_hidden()
    
    # Post-Login Methods
    def logout(self) -> None:
        """Logout from the application."""
        self.logout_link.click()
        expect(self.page).to_have_url('*login*')
    
    def delete_account(self) -> None:
        """Delete user account."""
        self.delete_account_link.click()
        self.page.wait_for_load_state('networkidle')
    
    # Subscription Methods
    def subscribe_to_newsletter(self, email: str) -> None:
        """Subscribe to newsletter."""
        self.subscription_email_input.fill(email)
        self.subscription_button.click()
        self.page.wait_for_load_state('networkidle')
    
    def verify_subscription_success(self) -> None:
        """Verify subscription success message."""
        expect(self.subscription_success_message).to_be_visible()
    
    def get_subscription_placeholder(self) -> str:
        """Get subscription email placeholder."""
        return self.subscription_email_input.get_attribute('placeholder') or ''
    
    def get_csrf_token(self) -> str:
        """Get CSRF token."""
        return self.subscription_csrf_token.get_attribute('value') or ''
    
    # Verification Methods
    def verify_home_page(self) -> None:
        """Verify home page elements."""
        expect(self.logo).to_be_visible()
        expect(self.featured_items_section).to_be_visible()
        expect(self.slider_carousel).to_be_visible()
        expect(self.page).to_have_url('*automationexercise.com*')
    
    def verify_page_structure(self) -> None:
        """Verify page structure."""
        expect(self.header).to_be_visible()
        expect(self.slider_section).to_be_visible()
        expect(self.left_sidebar).to_be_visible()
        expect(self.featured_items_section).to_be_visible()
        expect(self.recommended_items_section).to_be_visible()
        expect(self.footer).to_be_visible()
    
    def verify_navigation_menu(self) -> None:
        """Verify navigation menu."""
        expect(self.shop_menu).to_be_visible()
        expect(self.home_link).to_be_visible()
        expect(self.products_link).to_be_visible()
        expect(self.cart_link).to_be_visible()
        expect(self.signup_login_link).to_be_visible()
        expect(self.test_cases_link).to_be_visible()
        expect(self.api_testing_link).to_be_visible()
        expect(self.video_tutorials_link).to_be_visible()
        expect(self.contact_us_link).to_be_visible()
    
    def verify_user_logged_in(self, username: str = None) -> None:
        """Verify user is logged in."""
        expect(self.logged_in_username).to_be_visible()
        expect(self.logout_link).to_be_visible()
        expect(self.delete_account_link).to_be_visible()
        
        if username:
            expect(self.logged_in_username).to_contain_text(username)
    
    def verify_user_logged_out(self) -> None:
        """Verify user is logged out."""
        expect(self.signup_login_link).to_be_visible()
        expect(self.logout_link).not_to_be_visible()
        expect(self.delete_account_link).not_to_be_visible()
    
    def verify_carousel_functionality(self) -> None:
        """Verify carousel functionality."""
        expect(self.slider_carousel).to_be_visible()
        expect(self.carousel_indicators).to_be_visible()
        expect(self.carousel_left_control).to_be_visible()
        expect(self.carousel_right_control).to_be_visible()
        
        item_count = self.carousel_items.count()
        assert item_count > 0, "Carousel should have items"
        
        # Verify active item exists
        expect(self.carousel_active_item).to_be_visible()
    
    def verify_carousel_content(self) -> None:
        """Verify carousel content."""
        expect(self.carousel_title).to_be_visible()
        expect(self.carousel_subtitle).to_be_visible()
        expect(self.carousel_description).to_be_visible()
        expect(self.test_cases_button).to_be_visible()
        expect(self.apis_list_button).to_be_visible()
        expect(self.carousel_images.first()).to_be_visible()
    
    def verify_categories_visible(self) -> None:
        """Verify categories are visible."""
        expect(self.category_section).to_be_visible()
        expect(self.category_accordion).to_be_visible()
        expect(self.women_category).to_be_visible()
        expect(self.men_category).to_be_visible()
        expect(self.kids_category).to_be_visible()
    
    def verify_brands_visible(self) -> None:
        """Verify brands are visible."""
        expect(self.brands_section).to_be_visible()
        expect(self.brands_title).to_be_visible()
        expect(self.brands_list).to_be_visible()
    
    def verify_featured_items_visible(self) -> None:
        """Verify featured items are visible."""
        expect(self.featured_items_section).to_be_visible()
        expect(self.featured_items_title).to_be_visible()
        
        product_count = self.get_product_count()
        assert product_count > 0, "Should have featured products"
    
    def verify_recommended_items_visible(self) -> None:
        """Verify recommended items are visible."""
        expect(self.recommended_items_section).to_be_visible()
        expect(self.recommended_items_title).to_be_visible()
        expect(self.recommended_items_carousel).to_be_visible()
    
    def verify_subscription_section(self) -> None:
        """Verify subscription section."""
        expect(self.subscription_section).to_be_visible()
        expect(self.subscription_title).to_be_visible()
        expect(self.subscription_email_input).to_be_visible()
        expect(self.subscription_button).to_be_visible()
        expect(self.subscription_description).to_be_visible()
    
    def verify_footer(self) -> None:
        """Verify footer."""
        expect(self.footer).to_be_visible()
        expect(self.footer_widget).to_be_visible()
        expect(self.footer_bottom).to_be_visible()
        expect(self.copyright_text).to_be_visible()
    
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
    
    # State Checking Methods
    def is_logged_in(self) -> bool:
        """Check if user is logged in."""
        try:
            return self.logged_in_username.is_visible()
        except Exception:
            return False
    
    def get_current_username(self) -> str:
        """Get current logged in username."""
        if self.is_logged_in():
            return self.logged_in_username.text_content() or ''
        return ''
    
    def is_on_home_page(self) -> bool:
        """Check if on home page."""
        url = self.page.url
        return 'automationexercise.com' in url and (url.endswith('/') or 'automationexercise.com' in url)
    
    # Utility Methods
    def wait_for_page_load(self) -> None:
        """Wait for page to load."""
        self.page.wait_for_load_state('networkidle')
        expect(self.logo).to_be_visible()
        expect(self.featured_items_section).to_be_visible()
    
    def scroll_to_featured_items(self) -> None:
        """Scroll to featured items section."""
        self.scroll_to_element(self.featured_items_section)
    
    def scroll_to_recommended_items(self) -> None:
        """Scroll to recommended items section."""
        self.scroll_to_element(self.recommended_items_section)
    
    def scroll_to_subscription(self) -> None:
        """Scroll to subscription section."""
        self.scroll_to_element(self.subscription_section)
    
    def use_scroll_up_button(self) -> None:
        """Use scroll up button."""
        # Scroll down first to make scroll up button visible
        self.scroll_to_bottom()
        expect(self.scroll_up_button).to_be_visible()
        self.scroll_up_button.click()
        self.page.wait_for_timeout(1000)
    
    def wait_for_all_images_loaded(self) -> None:
        """Wait for all images to load."""
        self.page.wait_for_function("""
            () => {
                const images = Array.from(document.querySelectorAll('img'));
                return images.every(img => img.complete);
            }
        """)
    
    def get_load_time(self) -> int:
        """Get page load time in milliseconds."""
        start_time = self.page.evaluate("Date.now()")
        self.wait_for_page_load()
        end_time = self.page.evaluate("Date.now()")
        return end_time - start_time
    
    # Accessibility Methods
    def verify_accessibility(self) -> None:
        """Verify accessibility features."""
        # Check logo has proper alt text
        expect(self.logo).to_have_attribute('alt', 'Website for automation practice')
        
        # Check input has proper attributes
        expect(self.subscription_email_input).to_have_attribute('type', 'email')
        expect(self.subscription_email_input).to_have_attribute('required')
        
        # Test keyboard navigation
        self.home_link.focus()
        self.page.keyboard.press('Tab')
        expect(self.products_link).to_be_focused()
