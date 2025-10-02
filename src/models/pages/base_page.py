"""
Base Page Object Model for AutomationExercise testing framework.
"""
import os
from typing import Optional
from playwright.sync_api import Page, Locator, expect


class BasePage:
    """Base page class with common functionality."""
    
    def __init__(self, page: Page):
        """
        Initialize the base page.
        
        Args:
            page: Playwright page object
        """
        self.page = page
        self.base_url = os.getenv('BASE_URL', 'https://automationexercise.com')
    
    def navigate(self, url: str = "") -> None:
        """
        Navigate to a URL.
        
        Args:
            url: URL to navigate to (relative to base URL if not absolute)
        """
        if url.startswith('http'):
            full_url = url
        else:
            full_url = f"{self.base_url}{url}"
        
        self.page.goto(full_url)
        self.wait_for_page_load()
    
    def wait_for_page_load(self) -> None:
        """Wait for page to load completely."""
        self.page.wait_for_load_state('networkidle')
    
    def get_title(self) -> str:
        """
        Get the page title.
        
        Returns:
            Page title
        """
        return self.page.title()
    
    def get_url(self) -> str:
        """
        Get the current URL.
        
        Returns:
            Current URL
        """
        return self.page.url
    
    def take_screenshot(self, name: str) -> None:
        """
        Take a screenshot of the page.
        
        Args:
            name: Screenshot name
        """
        self.page.screenshot(
            path=f"results/screenshots/{name}-{self.page.url.split('/')[-1]}.png",
            full_page=True
        )
    
    def scroll_to_element(self, locator: Locator) -> None:
        """
        Scroll to an element.
        
        Args:
            locator: Element locator
        """
        locator.scroll_into_view_if_needed()
    
    def scroll_to_bottom(self) -> None:
        """Scroll to the bottom of the page."""
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        self.page.wait_for_timeout(1000)
    
    def scroll_to_top(self) -> None:
        """Scroll to the top of the page."""
        self.page.evaluate("window.scrollTo(0, 0)")
        self.page.wait_for_timeout(1000)
    
    def wait_for_element(self, locator: Locator, timeout: int = 30000) -> None:
        """
        Wait for an element to be visible.
        
        Args:
            locator: Element locator
            timeout: Timeout in milliseconds
        """
        locator.wait_for(state="visible", timeout=timeout)
    
    def is_element_visible(self, locator: Locator) -> bool:
        """
        Check if an element is visible.
        
        Args:
            locator: Element locator
            
        Returns:
            True if element is visible, False otherwise
        """
        try:
            return locator.is_visible()
        except Exception:
            return False
    
    def get_element_text(self, locator: Locator) -> str:
        """
        Get text content of an element.
        
        Args:
            locator: Element locator
            
        Returns:
            Element text content
        """
        return locator.text_content() or ""
    
    def get_element_attribute(self, locator: Locator, attribute: str) -> Optional[str]:
        """
        Get an attribute value of an element.
        
        Args:
            locator: Element locator
            attribute: Attribute name
            
        Returns:
            Attribute value or None
        """
        return locator.get_attribute(attribute)
    
    def click_element(self, locator: Locator) -> None:
        """
        Click an element.
        
        Args:
            locator: Element locator
        """
        locator.click()
    
    def fill_input(self, locator: Locator, text: str) -> None:
        """
        Fill an input field.
        
        Args:
            locator: Input element locator
            text: Text to fill
        """
        locator.fill(text)
    
    def clear_input(self, locator: Locator) -> None:
        """
        Clear an input field.
        
        Args:
            locator: Input element locator
        """
        locator.clear()
    
    def select_option(self, locator: Locator, value: str) -> None:
        """
        Select an option from a dropdown.
        
        Args:
            locator: Select element locator
            value: Option value to select
        """
        locator.select_option(value)
    
    def hover_element(self, locator: Locator) -> None:
        """
        Hover over an element.
        
        Args:
            locator: Element locator
        """
        locator.hover()
    
    def wait_for_url(self, url_pattern: str, timeout: int = 30000) -> None:
        """
        Wait for URL to match a pattern.
        
        Args:
            url_pattern: URL pattern to match
            timeout: Timeout in milliseconds
        """
        self.page.wait_for_url(url_pattern, timeout=timeout)
    
    def verify_url_contains(self, text: str) -> None:
        """
        Verify that the current URL contains specific text.
        
        Args:
            text: Text to check in URL
        """
        expect(self.page).to_have_url(f"*{text}*")
    
    def verify_title_contains(self, text: str) -> None:
        """
        Verify that the page title contains specific text.
        
        Args:
            text: Text to check in title
        """
        expect(self.page).to_have_title(f"*{text}*")
