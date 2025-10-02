"""
Global pytest configuration and fixtures for AutomationExercise testing framework.
"""
import os
import pytest
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
from src.fixtures.test_data_fixtures import *  # Registrar fixtures de test_data, api controllers y pages

# Load environment variables
load_dotenv()

# Global test configuration
BASE_URL = os.getenv('BASE_URL', 'https://automationexercise.com')
API_BASE_URL = os.getenv('API_BASE_URL', 'https://automationexercise.com/api')
HEADLESS = os.getenv('HEADLESS', 'true').lower() == 'true'
BROWSER = os.getenv('BROWSER', 'chromium')
TIMEOUT = int(os.getenv('TIMEOUT', '30000'))


@pytest.fixture(scope="session")
def browser_context_args():
    """Browser context arguments for all tests."""
    return {
        "viewport": {"width": 1920, "height": 1080},
        "ignore_https_errors": True,
        "record_video_dir": "results/videos/",
        "record_video_size": {"width": 1920, "height": 1080}
    }


@pytest.fixture(scope="session")
def playwright_context():
    """Playwright context for the entire test session."""
    with sync_playwright() as p:
        browser = getattr(p, BROWSER).launch(headless=HEADLESS)
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            ignore_https_errors=True
        )
        yield context
        context.close()
        browser.close()


@pytest.fixture
def page(playwright_context):
    """Page fixture for individual tests."""
    page = playwright_context.new_page()
    page.set_default_timeout(TIMEOUT)
    yield page
    page.close()


@pytest.fixture
def api_request_context(playwright_context):
    """API request context for API tests."""
    return playwright_context.request


# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom markers and options."""
    config.addinivalue_line(
        "markers", "api: mark test as API test"
    )
    config.addinivalue_line(
        "markers", "ui: mark test as UI/E2E test"
    )
    config.addinivalue_line(
        "markers", "smoke: mark test as smoke test"
    )
    config.addinivalue_line(
        "markers", "regression: mark test as regression test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow test"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on test location."""
    for item in items:
        # Add markers based on test file location
        if "api" in str(item.fspath):
            item.add_marker(pytest.mark.api)
        if "user_interface" in str(item.fspath):
            item.add_marker(pytest.mark.ui)
        
        # Add slow marker for tests that might take longer
        if "performance" in item.name or "load" in item.name:
            item.add_marker(pytest.mark.slow)

        # Mark concurrent tests as xfail due to Playwright request context not being thread-safe
        if "concurrent" in item.name:
            item.add_marker(pytest.mark.xfail(reason="Playwright request context is not thread-safe across threads", strict=False))
