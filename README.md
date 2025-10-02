# 🛒 AutomationExercise E-commerce Testing Framework (Python)

[![Playwright](https://img.shields.io/badge/Playwright-45ba4b?style=for-the-badge&logo=playwright&logoColor=white)](https://playwright.dev/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)](https://pytest.org/)

> **Comprehensive automation testing framework for [AutomationExercise.com](https://automationexercise.com) e-commerce platform using Playwright and Python**

## 🏗️ Project Architecture

```
AutomationExercise.Tests.Python/
├── src/
│   ├── api_client/           # API client and controllers
│   │   ├── base_client.py    # Base API client class
│   │   └── controllers/      # Domain controllers (Products, Brands, User, etc.)
│   ├── configs/              # Test configurations
│   ├── data/                 # Static data and test files
│   │   └── attachments/      # Test documents and images
│   ├── fixtures/             # Test data fixtures
│   ├── helpers/              # Utilities and helper functions
│   ├── mailing/              # Email notification system
│   ├── models/               # Page Objects and data models
│   │   ├── pages/            # Page Object Models
│   │   ├── product/          # Product-related models
│   │   ├── user/             # User-related models
│   │   └── order/            # Order-related models
│   └── tests/                # Test suites
│       ├── api/              # API tests
│       └── user_interface/   # E2E/UI tests
├── results/                  # Reports and results (auto-generated)
├── conftest.py              # Global pytest configuration
├── pytest.ini              # Pytest configuration
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🚀 Installation and Setup

### Prerequisites

- **Python** (version 3.8 or higher)
- **Pip** (Python package installer)
- **Git**

### Installation

1. **Clone the repository:**

   ```bash
   git clone [REPOSITORY_URL]
   cd AutomationExercise.Tests.Python
   ```

2. **Create virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers:**

   ```bash
   playwright install
   ```

5. **Setup environment variables:**

   ```bash
   cp env.example .env
   ```

   Edit `.env` file with your configuration:

   ```env
   # AutomationExercise.com Configuration
   BASE_URL=https://automationexercise.com
   API_BASE_URL=https://automationexercise.com/api

   # Test User Credentials
   TEST_EMAIL=test.user@example.com
   TEST_PASSWORD=testpassword123
   TEST_USERNAME=TestUser

   # Email Configuration (for reporting)
   EMAIL_USER=your.email@gmail.com
   EMAIL_PASS=your_app_password
   EMAIL_RECIPIENTS="recipient@example.com"

   # Test Configuration
   HEADLESS=true
   BROWSER=chromium
   TIMEOUT=30000
   ```

## 🎯 Test Execution

### API Tests

Run all API tests:

```bash
pytest src/tests/api/ -v
```

### UI/E2E Tests

Run all UI tests:

```bash
pytest src/tests/user_interface/ -v
```

### Run Specific Test Files

```bash
# Run products API tests
pytest src/tests/api/test_products_api.py -v

# Run login UI tests
pytest src/tests/user_interface/test_e2e_login.py -v
```

### Run Tests with Markers

```bash
# Run only API tests
pytest -m api -v

# Run only UI tests
pytest -m ui -v

# Run smoke tests
pytest -m smoke -v
```

### Run Tests in Parallel

```bash
pytest -n auto -v
```

### Generate Reports

```bash
# Generate HTML report
pytest --html=results/playwright-report-python/index.html --self-contained-html

# Generate JUnit XML report
pytest --junitxml=results/test-results-python/python-junit-results.xml

# Generate coverage report
pytest --cov=src --cov-report=html:results/coverage-report
```

## 📊 API Test Coverage

Our framework covers all 14 AutomationExercise.com API endpoints:

### Products API

- ✅ **API 1**: GET All Products List
- ✅ **API 2**: POST To All Products List (Error handling)
- ✅ **API 5**: POST To Search Product
- ✅ **API 6**: POST To Search Product without parameter (Error handling)

### Brands API

- ✅ **API 3**: GET All Brands List
- ✅ **API 4**: PUT To All Brands List (Error handling)

### User Authentication API

- ✅ **API 7**: POST To Verify Login with valid details
- ✅ **API 8**: POST To Verify Login without email parameter
- ✅ **API 9**: DELETE To Verify Login (Error handling)
- ✅ **API 10**: POST To Verify Login with invalid details
- ✅ **API 11**: POST To Create/Register User Account
- ✅ **API 12**: DELETE METHOD To Delete User Account
- ✅ **API 13**: PUT METHOD To Update User Account
- ✅ **API 14**: GET user account detail by email

## 🖥️ UI Test Coverage

### Core E-commerce Functionality

- **Authentication Flow**: Login, Signup, Logout
- **Product Browsing**: Product listing, search, filtering, details
- **Shopping Cart**: Add/remove items, quantity updates, checkout
- **User Account**: Registration, profile management
- **Navigation**: Menu navigation, responsive design

### Page Objects

- `HomePage`: Main landing page interactions
- `LoginPage`: Authentication and registration
- `ProductsPage`: Product catalog and search
- `CartPage`: Shopping cart functionality

## 🏛️ Framework Architecture

### API Client Architecture

```python
# Base API Client
class BaseAPIClient:
    def __init__(self, request_context: APIRequestContext, base_url: str = None):
        self.request = request_context
        self.base_url = base_url or os.getenv('API_BASE_URL')

    def get(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        response = self.request.get(f"{self.base_url}{endpoint}")
        return {"status": response.status, "data": response.json()}

# Domain-specific Controllers
class ProductsController(BaseAPIClient):
    def get_all_products(self) -> Dict[str, Any]:
        return self.get("/productsList")

    def search_product(self, search_term: str) -> Dict[str, Any]:
        form_data = {"search_product": search_term}
        return self.post_form("/searchProduct", form_data)
```

### Page Object Model

```python
class ProductsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.products_section = page.locator('.features_items')
        self.search_product_input = page.locator('#search_product')
        self.add_to_cart_buttons = page.locator('a.add-to-cart[data-product-id]')

    def search_for_product(self, search_term: str) -> None:
        self.search_product_input.fill(search_term)
        self.submit_search_button.click()

    def add_product_to_cart(self, index: int) -> None:
        self.add_to_cart_buttons.nth(index).click()
```

## 📈 Reporting

### Test Reports

After test execution, reports are available in:

- **HTML Report**: `./results/playwright-report-python/index.html`
- **JUnit Report**: `./results/test-results-python/python-junit-results.xml`
- **Coverage Report**: `./results/coverage-report/index.html`

### Email Notifications

Automated email reports include:

- Test execution summary
- Failed test details
- Compressed artifacts (screenshots, videos, traces)

## 🔧 Configuration

### Pytest Configuration

The framework uses `pytest.ini` for configuration:

```ini
[tool:pytest]
testpaths = src/tests
python_files = test_*.py *_test.py
addopts =
    --strict-markers
    --verbose
    --html=results/playwright-report-python/index.html
    --junitxml=results/test-results-python/python-junit-results.xml
    --cov=src
```

### Environment Configuration

All environment-specific settings are managed through `.env` file:

- Base URLs for different environments
- Test user credentials
- Email notification settings

## 🧪 Test Data Management

### Fixtures

Test data is organized using Pytest fixtures:

```python
@pytest.fixture
def test_data():
    return {
        "valid_user": {
            "email": "test.user@example.com",
            "password": "testpassword123",
            "name": "TestUser"
        },
        "products_data": {
            "search_terms": ["dress", "tshirt", "jean"],
            "expected_product_count": 10
        }
    }
```

### Models

Strongly-typed data models ensure consistency:

```python
class Product(BaseModel):
    id: int
    name: str
    price: str
    brand: str
    category: ProductCategory
```

## 🚦 CI/CD Integration

### GitHub Actions

```yaml
name: E2E Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      - run: pip install -r requirements.txt
      - run: playwright install
      - run: pytest src/tests/api/ -v
      - run: pytest src/tests/user_interface/ -v
```

## 🛠️ Development Guidelines

### Adding New Tests

1. **API Tests**: Create new test files in `src/tests/api/`
2. **UI Tests**: Create new test files in `src/tests/user_interface/`
3. **Page Objects**: Add new page objects in `src/models/pages/`
4. **API Controllers**: Add new controllers in `src/api_client/controllers/`

### Best Practices

- Use Python type hints for better code clarity
- Follow Page Object Model for UI tests
- Implement proper error handling
- Add comprehensive assertions
- Use descriptive test names
- Maintain test independence
- Clean up test data after execution

## 📚 Resources

- [AutomationExercise.com](https://automationexercise.com) - Test application
- [AutomationExercise API Documentation](https://automationexercise.com/api_list) - API documentation
- [Playwright Documentation](https://playwright.dev/) - Testing framework
- [Python Documentation](https://docs.python.org/) - Programming language
- [Pytest Documentation](https://docs.pytest.org/) - Testing framework

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Commit changes: `git commit -am 'Add new feature'`
4. Push to branch: `git push origin feature/new-feature`
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Built with ❤️ using Playwright and Python**
