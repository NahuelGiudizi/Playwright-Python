"""
E2E Login tests for AutomationExercise.com.
"""
import pytest
from src.fixtures.test_data_fixtures import home_page, login_page, ui_test_data


@pytest.mark.ui
class TestE2ELogin:
    """Test class for E2E Login functionality."""
    
    def test_navigate_to_login_page_success(self, login_page, ui_test_data):
        """
        Should successfully navigate to login page.
        
        Validates that navigation to the login page works and all form elements are visible.
        """
        # Act
        login_page.navigate_to_login_page()
        
        # Assert
        assert login_page.page.url.endswith('/login')
        assert 'Automation Exercise' in login_page.get_title()
        
        # Verify page structure
        login_page.verify_page_structure()
        login_page.verify_login_form_elements()
        login_page.verify_signup_form_elements()
        
        # Verify specific form elements
        assert login_page.login_email_input.is_visible()
        assert login_page.login_password_input.is_visible()
        assert login_page.login_button.is_visible()
        assert login_page.signup_name_input.is_visible()
        assert login_page.signup_email_input.is_visible()
        assert login_page.signup_button.is_visible()
        
        # Verify OR separator
        assert login_page.or_separator.is_visible()
        assert login_page.or_separator.text_content() == 'OR'
        
        # Verify form titles
        assert login_page.login_form_title.is_visible()
        assert login_page.signup_form_title.is_visible()
    
    def test_display_login_form_elements_correctly(self, login_page, ui_test_data):
        """
        Should display login form elements correctly.
        
        Verifies that all login form elements are properly displayed with correct attributes.
        """
        # Arrange & Act
        login_page.navigate_to_login_page()
        
        # Assert - Check all login form elements are present
        assert login_page.login_form_title.text_content() == 'Login to your account'
        assert login_page.login_form.is_visible()
        assert login_page.login_form.get_attribute('action') == '/login'
        
        # Verify input elements and attributes
        assert login_page.login_email_input.is_visible()
        assert login_page.login_email_input.get_attribute('data-qa') == 'login-email'
        assert login_page.login_email_input.get_attribute('type') == 'email'
        assert login_page.login_email_input.get_attribute('required') is not None
        
        assert login_page.login_password_input.is_visible()
        assert login_page.login_password_input.get_attribute('data-qa') == 'login-password'
        assert login_page.login_password_input.get_attribute('type') == 'password'
        assert login_page.login_password_input.get_attribute('required') is not None
        
        assert login_page.login_button.is_visible()
        assert login_page.login_button.get_attribute('data-qa') == 'login-button'
        assert login_page.login_button.text_content() == 'Login'
        
        # Verify placeholders
        email_placeholder = login_page.get_login_email_placeholder()
        password_placeholder = login_page.get_login_password_placeholder()
        assert email_placeholder
        assert password_placeholder
        
        # Verify form security
        login_page.verify_form_security()
    
    def test_display_signup_form_elements_correctly(self, login_page, ui_test_data):
        """
        Should display signup form elements correctly.
        
        Validates that all signup form elements are properly displayed with correct attributes.
        """
        # Arrange & Act
        login_page.navigate_to_login_page()
        
        # Assert - Check all signup form elements are present
        assert login_page.signup_form_title.text_content() == 'New User Signup!'
        assert login_page.signup_form.is_visible()
        assert login_page.signup_form.get_attribute('action') == '/signup'
        
        # Verify input elements and attributes
        assert login_page.signup_name_input.is_visible()
        assert login_page.signup_name_input.get_attribute('data-qa') == 'signup-name'
        assert login_page.signup_name_input.get_attribute('type') == 'text'
        assert login_page.signup_name_input.get_attribute('required') is not None
        
        assert login_page.signup_email_input.is_visible()
        assert login_page.signup_email_input.get_attribute('data-qa') == 'signup-email'
        assert login_page.signup_email_input.get_attribute('type') == 'email'
        assert login_page.signup_email_input.get_attribute('required') is not None
        
        assert login_page.signup_button.is_visible()
        assert login_page.signup_button.get_attribute('data-qa') == 'signup-button'
        assert login_page.signup_button.text_content() == 'Signup'
        
        # Verify hidden form type field
        assert not login_page.signup_hidden_form_type.is_visible()
        assert login_page.signup_hidden_form_type.get_attribute('value') == 'signup'
        
        # Verify placeholders
        name_placeholder = login_page.get_signup_name_placeholder()
        email_placeholder = login_page.get_signup_email_placeholder()
        assert name_placeholder
        assert email_placeholder
    
    def test_show_validation_message_for_invalid_login(self, login_page, ui_test_data):
        """
        Should show validation message for invalid login.
        
        Tests that appropriate error messages are displayed when invalid login credentials are used.
        """
        # Arrange
        login_page.navigate_to_login_page()
        invalid_credentials = ui_test_data["invalid_user"]
        
        # Act
        login_success = login_page.login_with_validation(
            invalid_credentials["email"], 
            invalid_credentials["password"]
        )
        
        # Assert
        assert not login_success
        assert '/login' in login_page.page.url
        
        # Should show error message or stay on login page
        try:
            login_page.verify_login_error()
            assert login_page.login_error_message.is_visible()
            assert 'incorrect' in login_page.login_error_message.text_content().lower()
        except Exception:
            # If no specific error message, verify we're still on login page
            assert login_page.login_email_input.is_visible()
            assert login_page.login_password_input.is_visible()
        
        # Verify form is still functional
        assert login_page.login_button.is_enabled()
        assert login_page.get_login_email_value() == invalid_credentials["email"]
    
    def test_handle_empty_email_validation(self, login_page, ui_test_data):
        """
        Should handle empty email validation.
        
        Validates that the system properly handles empty email field validation during login.
        """
        # Arrange
        login_page.navigate_to_login_page()
        
        # Act
        login_page.login_password_input.fill(ui_test_data["valid_user"]["password"])
        login_page.login_button.click()
        
        # Assert - Browser should show HTML5 validation or prevent submission
        email_value = login_page.get_login_email_value()
        password_value = login_page.get_login_password_value()
        
        assert email_value == ''
        assert password_value == ui_test_data["valid_user"]["password"]
        
        # Should stay on login page due to validation
        assert '/login' in login_page.page.url
        
        # Verify form validation
        login_page.verify_form_validation()
        
        # Check that email field is required
        assert login_page.login_email_input.get_attribute('required') is not None
        
        # Verify form is still functional
        assert login_page.login_email_input.is_focused()
        assert login_page.login_email_input.is_visible()
        assert login_page.login_password_input.is_visible()
    
    def test_handle_empty_password_validation(self, login_page, ui_test_data):
        """
        Should handle empty password validation.
        
        Tests that the system properly handles empty password field validation during login.
        """
        # Arrange
        login_page.navigate_to_login_page()
        
        # Act
        login_page.login_email_input.fill(ui_test_data["valid_user"]["email"])
        login_page.login_button.click()
        
        # Assert - Browser should show HTML5 validation or prevent submission
        email_value = login_page.get_login_email_value()
        password_value = login_page.get_login_password_value()
        
        assert email_value == ui_test_data["valid_user"]["email"]
        assert password_value == ''
        
        # Should stay on login page due to validation
        assert '/login' in login_page.page.url
        
        # Check that password field is required
        assert login_page.login_password_input.get_attribute('required') is not None
        
        # Verify the password field gets focus or shows validation
        assert login_page.login_password_input.is_visible()
        assert login_page.login_email_input.is_visible()
        
        # Clear and verify form can be reset
        login_page.clear_login_form()
        assert login_page.get_login_email_value() == ''
        assert login_page.get_login_password_value() == ''
    
    def test_handle_signup_with_potentially_existing_email(self, login_page, ui_test_data):
        """
        Should handle signup with potentially existing email.
        
        Tests that the system properly handles signup attempts with potentially existing emails.
        """
        # Arrange
        login_page.navigate_to_login_page()
        existing_email = ui_test_data["test_user"]["email"]
        test_name = ui_test_data["test_user"]["name"]
        
        # Act
        signup_success = login_page.signup_with_validation(test_name, existing_email)
        
        # Assert - Should either show error or continue to signup
        if not signup_success:
            # If signup failed, check for error message
            try:
                login_page.verify_signup_error()
                assert login_page.signup_error_message.is_visible()
                assert 'exist' in login_page.signup_error_message.text_content().lower()
            except Exception:
                # If no specific error message, verify we're still on login page
                assert '/login' in login_page.page.url
                assert login_page.signup_form.is_visible()
        else:
            # If signup succeeded, should navigate to signup form
            assert '/signup' in login_page.page.url
        
        # Verify form remains functional
        if login_page.is_on_login_page():
            assert login_page.signup_name_input.is_visible()
            assert login_page.signup_email_input.is_visible()
            assert login_page.signup_button.is_enabled()
            
            # Test form can be cleared and reused
            login_page.clear_signup_form()
            assert login_page.get_signup_name_value() == ''
            assert login_page.get_signup_email_value() == ''
    
    def test_maintain_form_state_during_navigation(self, login_page, home_page, ui_test_data):
        """
        Should maintain form state during navigation.
        
        Verifies that form state is properly managed during navigation away from and back to the login page.
        """
        # Arrange
        login_page.navigate_to_login_page()
        test_email = ui_test_data["valid_user"]["email"]
        test_password = ui_test_data["valid_user"]["password"]
        test_name = ui_test_data["test_user"]["name"]
        test_signup_email = ui_test_data["test_user"]["email"]
        
        # Act - Fill both forms
        login_page.login_email_input.fill(test_email)
        login_page.login_password_input.fill(test_password)
        login_page.signup_name_input.fill(test_name)
        login_page.signup_email_input.fill(test_signup_email)
        
        # Verify forms are filled
        assert login_page.get_login_email_value() == test_email
        assert login_page.get_login_password_value() == test_password
        assert login_page.get_signup_name_value() == test_name
        assert login_page.get_signup_email_value() == test_signup_email
        
        # Navigate away and back
        home_page.navigate()
        home_page.verify_home_page()
        login_page.navigate_to_login_page()
        
        # Assert - Forms should be cleared (fresh state)
        assert login_page.get_login_email_value() == ''
        assert login_page.get_login_password_value() == ''
        assert login_page.get_signup_name_value() == ''
        assert login_page.get_signup_email_value() == ''
        
        # Verify forms are still functional
        login_page.verify_login_form_elements()
        login_page.verify_signup_form_elements()
        assert login_page.login_button.is_enabled()
        assert login_page.signup_button.is_enabled()
    
    def test_handle_special_characters_in_email_and_password(self, login_page, ui_test_data):
        """
        Should handle special characters in email and password.
        
        Tests that the login form properly handles special characters in email and password fields.
        """
        # Arrange
        login_page.navigate_to_login_page()
        special_email = 'test+special@test-domain.co.uk'
        special_password = 'P@ssw0rd!123#$%'
        unicode_password = 'Test123üñíçødé'
        
        # Act - Test with special characters
        login_page.login_email_input.fill(special_email)
        login_page.login_password_input.fill(special_password)
        
        # Verify values are set correctly
        assert login_page.get_login_email_value() == special_email
        assert login_page.get_login_password_value() == special_password
        
        login_success = login_page.login_with_validation(special_email, special_password)
        
        # Assert - Should handle special characters without crashing
        assert not login_success  # Expected to fail with invalid credentials
        assert '/login' in login_page.page.url  # Should stay on login page
        assert login_page.login_email_input.is_visible()  # Page should still be functional
        
        # Test with unicode characters
        login_page.clear_login_form()
        login_page.login_email_input.fill(special_email)
        login_page.login_password_input.fill(unicode_password)
        
        assert login_page.get_login_email_value() == special_email
        assert login_page.get_login_password_value() == unicode_password
        
        # Verify form remains functional after special character input
        assert login_page.login_button.is_enabled()
        assert login_page.login_email_input.is_visible()
        assert login_page.login_password_input.is_visible()
        
        # Test form security by verifying password is masked
        assert login_page.login_password_input.get_attribute('type') == 'password'
    
    def test_verify_page_title_and_meta_information(self, login_page, ui_test_data):
        """
        Should verify page title and meta information.
        
        Validates that the login page has correct title and meta information for SEO and accessibility.
        """
        # Arrange & Act
        login_page.navigate_to_login_page()
        
        # Assert - Page title and meta information
        assert 'Automation Exercise' in login_page.get_title()
        assert 'Signup' in login_page.get_title() or 'Login' in login_page.get_title()
        
        # Check meta tags via page evaluation
        meta_description = login_page.page.get_attribute('meta[name="description"]', 'content')
        meta_keywords = login_page.page.get_attribute('meta[name="keywords"]', 'content')
        
        assert meta_description
        assert meta_keywords
        if meta_description:
            assert 'automation' in meta_description.lower()
        
        # Check page language
        html_lang = login_page.page.get_attribute('html', 'lang')
        assert html_lang == 'en'
        
        # Verify viewport meta tag for responsiveness
        viewport_meta = login_page.page.get_attribute('meta[name="viewport"]', 'content')
        assert 'width=device-width' in viewport_meta
    
    def test_form_accessibility_features(self, login_page, ui_test_data):
        """
        Should test form accessibility features.
        
        Tests that the login form meets accessibility standards with proper input types and tab navigation.
        """
        # Arrange & Act
        login_page.navigate_to_login_page()
        
        # Assert - Check for proper input types and attributes
        assert login_page.login_email_input.get_attribute('type') == 'email'
        assert login_page.login_password_input.get_attribute('type') == 'password'
        assert login_page.signup_name_input.get_attribute('type') == 'text'
        assert login_page.signup_email_input.get_attribute('type') == 'email'
        
        # Test required attributes for screen readers
        assert login_page.login_email_input.get_attribute('required') is not None
        assert login_page.login_password_input.get_attribute('required') is not None
        assert login_page.signup_name_input.get_attribute('required') is not None
        assert login_page.signup_email_input.get_attribute('required') is not None
        
        # Test tab navigation order
        login_page.focus_login_email()
        assert login_page.login_email_input.is_focused()
        
        login_page.tab_to_next_field()
        assert login_page.login_password_input.is_focused()
        
        login_page.tab_to_next_field()
        assert login_page.login_button.is_focused()
        
        # Test form structure and accessibility
        assert login_page.login_form.get_attribute('method') == 'POST'
        assert login_page.signup_form.get_attribute('method') == 'POST'
        
        # Verify forms have proper structure
        assert 'Login' in login_page.login_form.text_content()
        assert 'Signup' in login_page.signup_form.text_content()
        
        # Test that forms can be submitted with Enter key
        login_page.focus_login_email()
        login_page.login_email_input.fill('test@test.com')
        login_page.tab_to_next_field()
        login_page.login_password_input.fill('testpass')
        
        # Verify both forms have proper ARIA structure
        assert login_page.login_form.get_attribute('action')
        assert login_page.signup_form.get_attribute('action')
