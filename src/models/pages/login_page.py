"""
Login Page Object Model for AutomationExercise testing framework.
"""
from typing import Tuple
from playwright.sync_api import Page, Locator, expect
from .base_page import BasePage


class LoginPage(BasePage):
    """Login page object model."""
    
    def __init__(self, page: Page):
        """
        Initialize the login page.
        
        Args:
            page: Playwright page object
        """
        super().__init__(page)
        
        # Login Form Elements
        self.login_form = page.locator('form[action="/login"]')
        self.login_form_title = page.locator('h2:has-text("Login to your account")')
        self.login_email_input = page.locator('input[data-qa="login-email"]')
        self.login_password_input = page.locator('input[data-qa="login-password"]')
        self.login_button = page.locator('button[data-qa="login-button"]')
        self.login_error_message = page.locator('.login-form p:has-text("incorrect")')
        
        # Signup Form Elements
        self.signup_form = page.locator('form[action="/signup"]')
        self.signup_form_title = page.locator('h2:has-text("New User Signup!")')
        self.signup_name_input = page.locator('input[data-qa="signup-name"]')
        self.signup_email_input = page.locator('input[data-qa="signup-email"]')
        self.signup_button = page.locator('button[data-qa="signup-button"]')
        self.signup_hidden_form_type = page.locator('input[name="form_type"][value="signup"]')
        self.signup_error_message = page.locator('.signup-form p:has-text("exist")')
        
        # OR Separator
        self.or_separator = page.locator('p:has-text("OR")')
        
        # Page Structure Elements
        self.page_header = page.locator('#header')
        self.page_footer = page.locator('#footer')
        self.navigation_menu = page.locator('.shop-menu.pull-right')
        
        # Form Validation Elements
        self.form_validation_messages = page.locator('.form-group .help-block')
        self.required_field_indicators = page.locator('input[required]')
    
    def navigate_to_login_page(self) -> None:
        """Navigate to the login page."""
        self.navigate('/login')
        self.wait_for_page_load()
    
    def wait_for_page_load(self) -> None:
        """Wait for login page to load."""
        self.page.wait_for_load_state('networkidle')
        expect(self.login_form).to_be_visible()
        expect(self.signup_form).to_be_visible()
    
    # Login Form Methods
    def fill_login_form(self, email: str, password: str) -> None:
        """
        Fill the login form.
        
        Args:
            email: User email
            password: User password
        """
        self.login_email_input.fill(email)
        self.login_password_input.fill(password)
    
    def submit_login_form(self) -> None:
        """Submit the login form."""
        self.login_button.click()
    
    def login_with_credentials(self, email: str, password: str) -> bool:
        """
        Login with credentials.
        
        Args:
            email: User email
            password: User password
            
        Returns:
            True if login successful, False otherwise
        """
        self.fill_login_form(email, password)
        self.submit_login_form()
        
        # Wait for navigation or error
        try:
            self.page.wait_for_url('*', timeout=5000)
            # Check if we're still on login page (login failed)
            if self.is_on_login_page():
                return False
            return True
        except Exception:
            return False
    
    def login_with_validation(self, email: str, password: str) -> bool:
        """
        Login with validation (returns success status).
        
        Args:
            email: User email
            password: User password
            
        Returns:
            True if login successful, False otherwise
        """
        return self.login_with_credentials(email, password)
    
    def clear_login_form(self) -> None:
        """Clear the login form."""
        self.login_email_input.clear()
        self.login_password_input.clear()
    
    def get_login_email_value(self) -> str:
        """Get login email input value."""
        return self.login_email_input.input_value()
    
    def get_login_password_value(self) -> str:
        """Get login password input value."""
        return self.login_password_input.input_value()
    
    def get_login_email_placeholder(self) -> str:
        """Get login email placeholder."""
        return self.login_email_input.get_attribute('placeholder') or ''
    
    def get_login_password_placeholder(self) -> str:
        """Get login password placeholder."""
        return self.login_password_input.get_attribute('placeholder') or ''
    
    # Signup Form Methods
    def fill_signup_form(self, name: str, email: str) -> None:
        """
        Fill the signup form.
        
        Args:
            name: User name
            email: User email
        """
        self.signup_name_input.fill(name)
        self.signup_email_input.fill(email)
    
    def submit_signup_form(self) -> None:
        """Submit the signup form."""
        self.signup_button.click()
    
    def signup_with_credentials(self, name: str, email: str) -> bool:
        """
        Signup with credentials.
        
        Args:
            name: User name
            email: User email
            
        Returns:
            True if signup successful, False otherwise
        """
        self.fill_signup_form(name, email)
        self.submit_signup_form()
        
        # Wait for navigation or error
        try:
            self.page.wait_for_url('*', timeout=5000)
            # Check if we're on signup form page (signup successful)
            if 'signup' in self.page.url:
                return True
            return False
        except Exception:
            return False
    
    def signup_with_validation(self, name: str, email: str) -> bool:
        """
        Signup with validation (returns success status).
        
        Args:
            name: User name
            email: User email
            
        Returns:
            True if signup successful, False otherwise
        """
        return self.signup_with_credentials(name, email)
    
    def clear_signup_form(self) -> None:
        """Clear the signup form."""
        self.signup_name_input.clear()
        self.signup_email_input.clear()
    
    def get_signup_name_value(self) -> str:
        """Get signup name input value."""
        return self.signup_name_input.input_value()
    
    def get_signup_email_value(self) -> str:
        """Get signup email input value."""
        return self.signup_email_input.input_value()
    
    def get_signup_name_placeholder(self) -> str:
        """Get signup name placeholder."""
        return self.signup_name_input.get_attribute('placeholder') or ''
    
    def get_signup_email_placeholder(self) -> str:
        """Get signup email placeholder."""
        return self.signup_email_input.get_attribute('placeholder') or ''
    
    # Verification Methods
    def verify_page_structure(self) -> None:
        """Verify login page structure."""
        expect(self.page_header).to_be_visible()
        expect(self.navigation_menu).to_be_visible()
        expect(self.login_form).to_be_visible()
        expect(self.signup_form).to_be_visible()
        expect(self.page_footer).to_be_visible()
    
    def verify_login_form_elements(self) -> None:
        """Verify login form elements."""
        expect(self.login_form_title).to_be_visible()
        expect(self.login_form).to_be_visible()
        expect(self.login_email_input).to_be_visible()
        expect(self.login_password_input).to_be_visible()
        expect(self.login_button).to_be_visible()
    
    def verify_signup_form_elements(self) -> None:
        """Verify signup form elements."""
        expect(self.signup_form_title).to_be_visible()
        expect(self.signup_form).to_be_visible()
        expect(self.signup_name_input).to_be_visible()
        expect(self.signup_email_input).to_be_visible()
        expect(self.signup_button).to_be_visible()
    
    def verify_login_error(self) -> None:
        """Verify login error message."""
        expect(self.login_error_message).to_be_visible()
    
    def verify_signup_error(self) -> None:
        """Verify signup error message."""
        expect(self.signup_error_message).to_be_visible()
    
    def verify_form_validation(self) -> None:
        """Verify form validation."""
        # Check required fields
        expect(self.login_email_input).to_have_attribute('required')
        expect(self.login_password_input).to_have_attribute('required')
        expect(self.signup_name_input).to_have_attribute('required')
        expect(self.signup_email_input).to_have_attribute('required')
    
    def verify_form_security(self) -> None:
        """Verify form security features."""
        # Check password field type
        expect(self.login_password_input).to_have_attribute('type', 'password')
        
        # Check email field type
        expect(self.login_email_input).to_have_attribute('type', 'email')
        expect(self.signup_email_input).to_have_attribute('type', 'email')
        
        # Check form methods
        expect(self.login_form).to_have_attribute('method', 'POST')
        expect(self.signup_form).to_have_attribute('method', 'POST')
    
    def verify_or_separator(self) -> None:
        """Verify OR separator between forms."""
        expect(self.or_separator).to_be_visible()
        expect(self.or_separator).to_have_text('OR')
    
    # State Checking Methods
    def is_on_login_page(self) -> bool:
        """Check if on login page."""
        return 'login' in self.page.url
    
    def is_login_form_visible(self) -> bool:
        """Check if login form is visible."""
        try:
            return self.login_form.is_visible()
        except Exception:
            return False
    
    def is_signup_form_visible(self) -> bool:
        """Check if signup form is visible."""
        try:
            return self.signup_form.is_visible()
        except Exception:
            return False
    
    def is_login_button_enabled(self) -> bool:
        """Check if login button is enabled."""
        try:
            return self.login_button.is_enabled()
        except Exception:
            return False
    
    def is_signup_button_enabled(self) -> bool:
        """Check if signup button is enabled."""
        try:
            return self.signup_button.is_enabled()
        except Exception:
            return False
    
    # Form Interaction Methods
    def focus_login_email(self) -> None:
        """Focus on login email input."""
        self.login_email_input.focus()
    
    def focus_login_password(self) -> None:
        """Focus on login password input."""
        self.login_password_input.focus()
    
    def focus_signup_name(self) -> None:
        """Focus on signup name input."""
        self.signup_name_input.focus()
    
    def focus_signup_email(self) -> None:
        """Focus on signup email input."""
        self.signup_email_input.focus()
    
    def tab_to_next_field(self) -> None:
        """Tab to next field."""
        self.page.keyboard.press('Tab')
    
    def press_enter(self) -> None:
        """Press Enter key."""
        self.page.keyboard.press('Enter')
    
    # Accessibility Methods
    def test_keyboard_navigation(self) -> None:
        """Test keyboard navigation through forms."""
        # Test login form navigation
        self.focus_login_email()
        expect(self.login_email_input).to_be_focused()
        
        self.tab_to_next_field()
        expect(self.login_password_input).to_be_focused()
        
        self.tab_to_next_field()
        expect(self.login_button).to_be_focused()
        
        # Test signup form navigation
        self.focus_signup_name()
        expect(self.signup_name_input).to_be_focused()
        
        self.tab_to_next_field()
        expect(self.signup_email_input).to_be_focused()
        
        self.tab_to_next_field()
        expect(self.signup_button).to_be_focused()
    
    def verify_form_accessibility(self) -> None:
        """Verify form accessibility features."""
        # Check input types
        expect(self.login_email_input).to_have_attribute('type', 'email')
        expect(self.login_password_input).to_have_attribute('type', 'password')
        expect(self.signup_name_input).to_have_attribute('type', 'text')
        expect(self.signup_email_input).to_have_attribute('type', 'email')
        
        # Check required attributes
        expect(self.login_email_input).to_have_attribute('required')
        expect(self.login_password_input).to_have_attribute('required')
        expect(self.signup_name_input).to_have_attribute('required')
        expect(self.signup_email_input).to_have_attribute('required')
        
        # Test keyboard navigation
        self.test_keyboard_navigation()
    
    # Error Handling Methods
    def handle_login_error(self) -> str:
        """Handle login error and return error message."""
        try:
            if self.login_error_message.is_visible():
                return self.login_error_message.text_content() or 'Login failed'
            return 'No error message displayed'
        except Exception:
            return 'Error message not found'
    
    def handle_signup_error(self) -> str:
        """Handle signup error and return error message."""
        try:
            if self.signup_error_message.is_visible():
                return self.signup_error_message.text_content() or 'Signup failed'
            return 'No error message displayed'
        except Exception:
            return 'Error message not found'
    
    # Utility Methods
    def get_form_data(self) -> dict:
        """Get current form data."""
        return {
            'login_email': self.get_login_email_value(),
            'login_password': self.get_login_password_value(),
            'signup_name': self.get_signup_name_value(),
            'signup_email': self.get_signup_email_value()
        }
    
    def reset_forms(self) -> None:
        """Reset both forms to empty state."""
        self.clear_login_form()
        self.clear_signup_form()
    
    def verify_forms_are_empty(self) -> None:
        """Verify both forms are empty."""
        assert self.get_login_email_value() == '', "Login email should be empty"
        assert self.get_login_password_value() == '', "Login password should be empty"
        assert self.get_signup_name_value() == '', "Signup name should be empty"
        assert self.get_signup_email_value() == '', "Signup email should be empty"
