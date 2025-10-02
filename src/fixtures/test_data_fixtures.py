"""
Test data fixtures for AutomationExercise testing framework.
"""
import pytest
from typing import Dict, Any, List
from playwright.sync_api import Page, APIRequestContext
from src.api_client.controllers.products_controller import ProductsController
from src.api_client.controllers.brands_controller import BrandsController
from src.api_client.controllers.user_controller import UserController
from src.models.pages.home_page import HomePage
from src.models.pages.login_page import LoginPage
from src.models.pages.products_page import ProductsPage
from src.models.pages.cart_page import CartPage


@pytest.fixture(scope="session")
def test_data():
    """Test data fixture with sample data for tests."""
    return {
        "valid_user": {
            "email": "test.user@example.com",
            "password": "testpassword123",
            "name": "TestUser"
        },
        "invalid_user": {
            "email": "invalid@example.com",
            "password": "wrongpassword",
            "name": "InvalidUser"
        },
        "test_user": {
            "email": "newuser@example.com",
            "password": "newpassword123",
            "name": "NewUser"
        },
        "products_data": {
            "search_terms": ["dress", "tshirt", "jean"],
            "expected_product_count": 10,
            "categories": ["Women", "Men", "Kids"],
            "brands": ["Polo", "H&M", "Madame", "Mast & Harbour", "Babyhug", "Allen Solly Junior", "Kookie Kids", "Biba"]
        },
        "api_test_data": {
            "products_data": {
                "search_terms": {
                    "valid": ["dress", "tshirt", "jean"],
                    "invalid": ["", "nonexistent"]
                },
                "expected_product_count": 10
            },
            "brands_data": {
                "expected_brands": ["Polo", "H&M", "Madame", "Mast & Harbour", "Babyhug", "Allen Solly Junior", "Kookie Kids", "Biba"]
            },
            "user_data": {
                "valid_credentials": {
                    "email": "test.user@example.com",
                    "password": "testpassword123"
                },
                "invalid_credentials": {
                    "email": "invalid@example.com",
                    "password": "wrongpassword"
                }
            }
        }
    }


@pytest.fixture
def api_test_data(test_data):
    """API test data fixture."""
    return test_data["api_test_data"]


@pytest.fixture
def ui_test_data(test_data):
    """UI test data fixture."""
    return {
        "valid_user": test_data["valid_user"],
        "invalid_user": test_data["invalid_user"],
        "test_user": test_data["test_user"],
        "products_data": test_data["products_data"]
    }


# API Controller Fixtures
@pytest.fixture
def products_controller(api_request_context):
    """Products controller fixture."""
    controller = ProductsController(api_request_context)
    controller.init()
    return controller


@pytest.fixture
def brands_controller(api_request_context):
    """Brands controller fixture."""
    controller = BrandsController(api_request_context)
    controller.init()
    return controller


@pytest.fixture
def user_controller(api_request_context):
    """User controller fixture."""
    controller = UserController(api_request_context)
    controller.init()
    return controller


# Page Object Fixtures
@pytest.fixture
def home_page(page):
    """Home page fixture."""
    return HomePage(page)


@pytest.fixture
def login_page(page):
    """Login page fixture."""
    return LoginPage(page)


@pytest.fixture
def products_page(page):
    """Products page fixture."""
    return ProductsPage(page)


@pytest.fixture
def cart_page(page):
    """Cart page fixture."""
    return CartPage(page)


# Test Data Fixtures
@pytest.fixture
def sample_products():
    """Sample products data fixture."""
    return [
        {
            "name": "Blue Top",
            "price": "Rs. 500",
            "category": "Women",
            "brand": "Polo"
        },
        {
            "name": "Men Tshirt",
            "price": "Rs. 400",
            "category": "Men",
            "brand": "H&M"
        },
        {
            "name": "Stylish Dress",
            "price": "Rs. 600",
            "category": "Women",
            "brand": "Madame"
        }
    ]


@pytest.fixture
def sample_user():
    """Sample user data fixture."""
    return {
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "testpassword123",
        "first_name": "Test",
        "last_name": "User",
        "address1": "123 Test Street",
        "address2": "Apt 1",
        "country": "United States",
        "state": "California",
        "city": "Los Angeles",
        "zipcode": "90210",
        "mobile_number": "1234567890"
    }


@pytest.fixture
def search_terms():
    """Search terms fixture."""
    return {
        "valid": ["dress", "tshirt", "jean", "top", "shirt"],
        "invalid": ["", "nonexistent", "xyz123"],
        "special_characters": ["dress!", "tshirt@", "jean#"]
    }


@pytest.fixture
def category_data():
    """Category data fixture."""
    return {
        "women": {
            "parent": "Women",
            "subcategories": ["Dress", "Tops & Shirts", "Saree"]
        },
        "men": {
            "parent": "Men",
            "subcategories": ["Tshirts", "Jeans"]
        },
        "kids": {
            "parent": "Kids",
            "subcategories": ["Dress", "Tops & Shirts"]
        }
    }


@pytest.fixture
def brand_data():
    """Brand data fixture."""
    return {
        "popular_brands": ["Polo", "H&M", "Madame", "Mast & Harbour"],
        "all_brands": ["Polo", "H&M", "Madame", "Mast & Harbour", "Babyhug", "Allen Solly Junior", "Kookie Kids", "Biba"]
    }


# Test Environment Fixtures
@pytest.fixture
def test_environment():
    """Test environment fixture."""
    return {
        "base_url": "https://automationexercise.com",
        "api_base_url": "https://automationexercise.com/api",
        "timeout": 30000,
        "headless": True,
        "browser": "chromium"
    }


# Performance Test Fixtures
@pytest.fixture
def performance_thresholds():
    """Performance thresholds fixture."""
    return {
        "page_load_time": 5000,  # 5 seconds
        "api_response_time": 3000,  # 3 seconds
        "search_response_time": 2000,  # 2 seconds
        "cart_update_time": 1000  # 1 second
    }


# Test Data Cleanup Fixtures
@pytest.fixture(autouse=True)
def cleanup_test_data():
    """Cleanup test data after tests."""
    yield
    # Add cleanup logic here if needed
    pass


# Mock Data Fixtures
@pytest.fixture
def mock_api_responses():
    """Mock API responses fixture."""
    return {
        "products_list": {
            "responseCode": 200,
            "products": [
                {
                    "id": 1,
                    "name": "Blue Top",
                    "price": "Rs. 500",
                    "brand": "Polo",
                    "category": {
                        "usertype": {"usertype": "Women"},
                        "category": "Tops"
                    }
                }
            ]
        },
        "search_results": {
            "responseCode": 200,
            "products": [
                {
                    "id": 1,
                    "name": "Blue Top",
                    "price": "Rs. 500",
                    "brand": "Polo",
                    "category": {
                        "usertype": {"usertype": "Women"},
                        "category": "Tops"
                    }
                }
            ]
        },
        "brands_list": {
            "responseCode": 200,
            "brands": [
                {"id": 1, "brand": "Polo"},
                {"id": 2, "brand": "H&M"},
                {"id": 3, "brand": "Madame"}
            ]
        }
    }


# Test Configuration Fixtures
@pytest.fixture
def test_config():
    """Test configuration fixture."""
    return {
        "retry_count": 3,
        "timeout": 30000,
        "screenshot_on_failure": True,
        "video_recording": True,
        "trace_recording": True
    }


# Data Validation Fixtures
@pytest.fixture
def validation_rules():
    """Validation rules fixture."""
    return {
        "email_format": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        "password_min_length": 6,
        "name_min_length": 2,
        "phone_format": r"^\d{10}$",
        "price_format": r"^Rs\. \d+$"
    }


# Test Data Generators
@pytest.fixture
def random_test_data():
    """Random test data generator fixture."""
    import random
    import string
    
    def generate_random_email():
        return f"test{random.randint(1000, 9999)}@example.com"
    
    def generate_random_name():
        return f"TestUser{random.randint(100, 999)}"
    
    def generate_random_password():
        return f"pass{random.randint(100, 999)}"
    
    return {
        "email": generate_random_email,
        "name": generate_random_name,
        "password": generate_random_password
    }


# Test Data for Specific Scenarios
@pytest.fixture
def edge_case_data():
    """Edge case test data fixture."""
    return {
        "empty_strings": ["", " ", "  "],
        "special_characters": ["!@#$%^&*()", "test@#$", "123!@#"],
        "unicode_strings": ["测试", "café", "naïve"],
        "very_long_strings": ["a" * 1000, "test" * 250],
        "sql_injection": ["'; DROP TABLE users; --", "1' OR '1'='1"],
        "xss_attempts": ["<script>alert('xss')</script>", "<img src=x onerror=alert(1)>"]
    }


# Test Data for Performance Testing
@pytest.fixture
def performance_test_data():
    """Performance test data fixture."""
    return {
        "large_search_terms": ["dress"] * 100,
        "multiple_categories": ["Women", "Men", "Kids"] * 50,
        "bulk_products": [{"name": f"Product {i}", "price": f"Rs. {i * 10}"} for i in range(100)]
    }
