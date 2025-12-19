# Part 1: Hands-On Coding Practice - Complete Practical Guide

## 🎯 Overview

This guide transforms you from reading about automation to **actually building it**. By the end, you'll have a production-ready test automation framework in your GitHub portfolio.

---

## Week 1-2: Build Your First Framework

### Day 1: Environment Setup

#### Install Required Software

```bash
# 1. Install Python 3.11+ (Check if already installed)
python --version

# If not installed, download from python.org

# 2. Install pip (usually comes with Python)
pip --version

# 3. Install virtualenv
pip install virtualenv

# 4. Create project directory
mkdir selenium-gxp-framework
cd selenium-gxp-framework

# 5. Create virtual environment
python -m venv venv

# 6. Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 7. Install Selenium and dependencies
pip install selenium pytest pytest-html allure-pytest openpyxl pandas python-dotenv

# 8. Install Chrome WebDriver
pip install webdriver-manager

# 9. Create requirements.txt
pip freeze > requirements.txt
```

#### Project Structure

```bash
# Create directory structure
selenium-gxp-framework/
│
├── .github/
│   └── workflows/
│       └── tests.yml
├── config/
│   ├── __init__.py
│   ├── config.py
│   └── environments.json
├── pages/
│   ├── __init__.py
│   ├── base_page.py
│   └── login_page.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_login.py
├── utils/
│   ├── __init__.py
│   ├── logger.py
│   └── screenshot_helper.py
├── test_data/
│   └── test_users.json
├── reports/
├── screenshots/
├── .env
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

#### Create Basic Files

**1. `.gitignore`**
```
# Virtual Environment
venv/
env/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# Test Reports
reports/
screenshots/
.pytest_cache/
htmlcov/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Environment
.env

# OS
.DS_Store
Thumbs.db
```

**2. `.env`**
```
# Environment Configuration
ENVIRONMENT=dev
BASE_URL=https://demo.opencart.com/
HEADLESS=false
IMPLICIT_WAIT=10
EXPLICIT_WAIT=20
BROWSER=chrome
```

**3. `pytest.ini`**
```ini
[pytest]
markers =
    smoke: Quick smoke tests (15 minutes)
    regression: Full regression suite
    critical: Critical path tests
    login: Login functionality tests
    search: Search functionality tests
    
addopts = 
    -v 
    --html=reports/report.html 
    --self-contained-html
    --capture=no
    
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

---

### Day 2: Build Base Page Class

**File: `config/config.py`**

```python
"""
Configuration Manager
Handles environment settings and configuration
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for test settings"""
    
    # Environment
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'dev')
    
    # URLs
    BASE_URL = os.getenv('BASE_URL', 'https://demo.opencart.com/')
    
    # Browser Settings
    BROWSER = os.getenv('BROWSER', 'chrome')
    HEADLESS = os.getenv('HEADLESS', 'false').lower() == 'true'
    
    # Timeouts
    IMPLICIT_WAIT = int(os.getenv('IMPLICIT_WAIT', 10))
    EXPLICIT_WAIT = int(os.getenv('EXPLICIT_WAIT', 20))
    PAGE_LOAD_TIMEOUT = int(os.getenv('PAGE_LOAD_TIMEOUT', 30))
    
    # Screenshots
    SCREENSHOT_ON_FAILURE = True
    SCREENSHOT_DIR = 'screenshots/'
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = 'logs/test_execution.log'
    
    @classmethod
    def get_url(cls, path=''):
        """Get full URL with path"""
        return f"{cls.BASE_URL.rstrip('/')}/{path.lstrip('/')}"
```

**File: `utils/logger.py`**

```python
"""
Logger Utility
Provides logging functionality for test execution
"""
import logging
import os
from datetime import datetime
from config.config import Config

class Logger:
    """Custom logger for test automation"""
    
    _logger = None
    
    @classmethod
    def get_logger(cls, name=__name__):
        """Get or create logger instance"""
        if cls._logger is None:
            # Create logs directory if it doesn't exist
            os.makedirs('logs', exist_ok=True)
            
            # Create logger
            cls._logger = logging.getLogger(name)
            cls._logger.setLevel(getattr(logging, Config.LOG_LEVEL))
            
            # Create formatters
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            
            # File handler
            log_file = f"logs/test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            cls._logger.addHandler(file_handler)
            
            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            cls._logger.addHandler(console_handler)
        
        return cls._logger

# Convenience function
def get_logger(name=__name__):
    """Get logger instance"""
    return Logger.get_logger(name)
```

**File: `pages/base_page.py`**

```python
"""
Base Page Class
Contains reusable methods for all page objects
"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utils.logger import get_logger
from config.config import Config
import os
from datetime import datetime

logger = get_logger(__name__)

class BasePage:
    """Base page class with common methods"""
    
    def __init__(self, driver):
        """Initialize base page with driver"""
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.EXPLICIT_WAIT)
    
    # ============ Element Finding ============
    
    def find_element(self, locator):
        """
        Find element with explicit wait
        Args:
            locator: Tuple of (By.METHOD, "locator_value")
        Returns:
            WebElement
        """
        try:
            logger.info(f"Finding element: {locator}")
            element = self.wait.until(EC.presence_of_element_located(locator))
            return element
        except TimeoutException:
            logger.error(f"Element not found: {locator}")
            self.take_screenshot(f"element_not_found_{locator[1]}")
            raise
    
    def find_elements(self, locator):
        """Find multiple elements"""
        try:
            logger.info(f"Finding elements: {locator}")
            elements = self.wait.until(EC.presence_of_all_elements_located(locator))
            return elements
        except TimeoutException:
            logger.error(f"Elements not found: {locator}")
            return []
    
    # ============ Element Interactions ============
    
    def click(self, locator):
        """
        Click element with wait for clickable
        Args:
            locator: Tuple of (By.METHOD, "locator_value")
        """
        try:
            logger.info(f"Clicking element: {locator}")
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
        except Exception as e:
            logger.error(f"Failed to click element: {locator}. Error: {str(e)}")
            self.take_screenshot(f"click_failed_{locator[1]}")
            raise
    
    def enter_text(self, locator, text, clear_first=True):
        """
        Enter text into element
        Args:
            locator: Tuple of (By.METHOD, "locator_value")
            text: Text to enter
            clear_first: Clear existing text before entering
        """
        try:
            logger.info(f"Entering text in: {locator}")
            element = self.find_element(locator)
            if clear_first:
                element.clear()
            element.send_keys(text)
        except Exception as e:
            logger.error(f"Failed to enter text: {text}. Error: {str(e)}")
            self.take_screenshot(f"enter_text_failed_{locator[1]}")
            raise
    
    def get_text(self, locator):
        """Get text from element"""
        try:
            logger.info(f"Getting text from: {locator}")
            element = self.find_element(locator)
            return element.text
        except Exception as e:
            logger.error(f"Failed to get text. Error: {str(e)}")
            raise
    
    def get_attribute(self, locator, attribute_name):
        """Get attribute value from element"""
        try:
            element = self.find_element(locator)
            return element.get_attribute(attribute_name)
        except Exception as e:
            logger.error(f"Failed to get attribute {attribute_name}. Error: {str(e)}")
            raise
    
    # ============ Element State Checks ============
    
    def is_visible(self, locator, timeout=None):
        """
        Check if element is visible
        Args:
            locator: Tuple of (By.METHOD, "locator_value")
            timeout: Custom timeout (optional)
        Returns:
            Boolean
        """
        try:
            wait = WebDriverWait(self.driver, timeout or Config.EXPLICIT_WAIT)
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def is_present(self, locator, timeout=None):
        """Check if element is present in DOM"""
        try:
            wait = WebDriverWait(self.driver, timeout or Config.EXPLICIT_WAIT)
            wait.until(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def is_enabled(self, locator):
        """Check if element is enabled"""
        try:
            element = self.find_element(locator)
            return element.is_enabled()
        except Exception:
            return False
    
    # ============ Waits ============
    
    def wait_for_visible(self, locator, timeout=None):
        """Wait for element to be visible"""
        wait = WebDriverWait(self.driver, timeout or Config.EXPLICIT_WAIT)
        return wait.until(EC.visibility_of_element_located(locator))
    
    def wait_for_clickable(self, locator, timeout=None):
        """Wait for element to be clickable"""
        wait = WebDriverWait(self.driver, timeout or Config.EXPLICIT_WAIT)
        return wait.until(EC.element_to_be_clickable(locator))
    
    def wait_for_invisible(self, locator, timeout=None):
        """Wait for element to become invisible"""
        wait = WebDriverWait(self.driver, timeout or Config.EXPLICIT_WAIT)
        return wait.until(EC.invisibility_of_element_located(locator))
    
    def wait_for_text_in_element(self, locator, text, timeout=None):
        """Wait for specific text in element"""
        wait = WebDriverWait(self.driver, timeout or Config.EXPLICIT_WAIT)
        return wait.until(EC.text_to_be_present_in_element(locator, text))
    
    # ============ Advanced Interactions ============
    
    def select_dropdown_by_text(self, locator, text):
        """Select dropdown option by visible text"""
        try:
            element = self.find_element(locator)
            select = Select(element)
            select.select_by_visible_text(text)
            logger.info(f"Selected '{text}' from dropdown")
        except Exception as e:
            logger.error(f"Failed to select from dropdown. Error: {str(e)}")
            raise
    
    def select_dropdown_by_value(self, locator, value):
        """Select dropdown option by value"""
        try:
            element = self.find_element(locator)
            select = Select(element)
            select.select_by_value(value)
            logger.info(f"Selected value '{value}' from dropdown")
        except Exception as e:
            logger.error(f"Failed to select from dropdown. Error: {str(e)}")
            raise
    
    def hover_over_element(self, locator):
        """Hover mouse over element"""
        try:
            element = self.find_element(locator)
            actions = ActionChains(self.driver)
            actions.move_to_element(element).perform()
            logger.info(f"Hovered over element: {locator}")
        except Exception as e:
            logger.error(f"Failed to hover. Error: {str(e)}")
            raise
    
    def double_click(self, locator):
        """Double click element"""
        try:
            element = self.find_element(locator)
            actions = ActionChains(self.driver)
            actions.double_click(element).perform()
            logger.info(f"Double clicked element: {locator}")
        except Exception as e:
            logger.error(f"Failed to double click. Error: {str(e)}")
            raise
    
    def scroll_to_element(self, locator):
        """Scroll element into view"""
        try:
            element = self.find_element(locator)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            logger.info(f"Scrolled to element: {locator}")
        except Exception as e:
            logger.error(f"Failed to scroll. Error: {str(e)}")
            raise
    
    # ============ JavaScript Execution ============
    
    def execute_script(self, script, *args):
        """Execute JavaScript"""
        return self.driver.execute_script(script, *args)
    
    def js_click(self, locator):
        """Click using JavaScript (for problematic elements)"""
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].click();", element)
        logger.info(f"JS clicked element: {locator}")
    
    # ============ Alerts ============
    
    def accept_alert(self):
        """Accept alert"""
        try:
            alert = self.wait.until(EC.alert_is_present())
            alert_text = alert.text
            alert.accept()
            logger.info(f"Accepted alert: {alert_text}")
            return alert_text
        except TimeoutException:
            logger.error("No alert present")
            return None
    
    def dismiss_alert(self):
        """Dismiss alert"""
        try:
            alert = self.wait.until(EC.alert_is_present())
            alert_text = alert.text
            alert.dismiss()
            logger.info(f"Dismissed alert: {alert_text}")
            return alert_text
        except TimeoutException:
            logger.error("No alert present")
            return None
    
    # ============ Frame Handling ============
    
    def switch_to_frame(self, frame_locator):
        """Switch to frame"""
        try:
            frame = self.find_element(frame_locator)
            self.driver.switch_to.frame(frame)
            logger.info(f"Switched to frame: {frame_locator}")
        except Exception as e:
            logger.error(f"Failed to switch to frame. Error: {str(e)}")
            raise
    
    def switch_to_default_content(self):
        """Switch back to main content"""
        self.driver.switch_to.default_content()
        logger.info("Switched to default content")
    
    # ============ Window Handling ============
    
    def switch_to_window(self, window_handle):
        """Switch to specific window"""
        self.driver.switch_to.window(window_handle)
        logger.info(f"Switched to window: {window_handle}")
    
    def get_window_handles(self):
        """Get all window handles"""
        return self.driver.window_handles
    
    def switch_to_new_window(self):
        """Switch to newly opened window"""
        handles = self.get_window_handles()
        self.switch_to_window(handles[-1])
    
    # ============ Screenshot ============
    
    def take_screenshot(self, name="screenshot"):
        """
        Take screenshot with GxP metadata
        Args:
            name: Screenshot name
        Returns:
            Screenshot file path
        """
        try:
            # Create screenshots directory
            os.makedirs(Config.SCREENSHOT_DIR, exist_ok=True)
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{name}_{timestamp}.png"
            filepath = os.path.join(Config.SCREENSHOT_DIR, filename)
            
            # Take screenshot
            self.driver.save_screenshot(filepath)
            logger.info(f"Screenshot saved: {filepath}")
            
            return filepath
        except Exception as e:
            logger.error(f"Failed to take screenshot. Error: {str(e)}")
            return None
    
    # ============ Navigation ============
    
    def navigate_to(self, url):
        """Navigate to URL"""
        logger.info(f"Navigating to: {url}")
        self.driver.get(url)
    
    def refresh_page(self):
        """Refresh current page"""
        logger.info("Refreshing page")
        self.driver.refresh()
    
    def go_back(self):
        """Go back in browser history"""
        logger.info("Going back")
        self.driver.back()
    
    def go_forward(self):
        """Go forward in browser history"""
        logger.info("Going forward")
        self.driver.forward()
    
    def get_current_url(self):
        """Get current URL"""
        return self.driver.current_url
    
    def get_page_title(self):
        """Get page title"""
        return self.driver.title
```

---

### Day 3: Create Login Page Object

**File: `pages/login_page.py`**

```python
"""
Login Page Object
Contains locators and methods for login functionality
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import get_logger
from config.config import Config

logger = get_logger(__name__)

class LoginPage(BasePage):
    """Login page object model"""
    
    # ============ Locators ============
    # Using By.ID, By.XPATH, By.CSS_SELECTOR, etc.
    
    # Navigation
    MY_ACCOUNT_LINK = (By.XPATH, "//a[@title='My Account']")
    LOGIN_MENU_ITEM = (By.LINK_TEXT, "Login")
    
    # Login Form
    EMAIL_INPUT = (By.ID, "input-email")
    PASSWORD_INPUT = (By.ID, "input-password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "input[value='Login']")
    
    # Messages
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, "div.alert-success")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.alert-danger")
    
    # Logged in state
    MY_ACCOUNT_HEADER = (By.XPATH, "//h2[text()='My Account']")
    LOGOUT_LINK = (By.LINK_TEXT, "Logout")
    
    # ============ Methods ============
    
    def __init__(self, driver):
        """Initialize login page"""
        super().__init__(driver)
        self.url = Config.get_url("index.php?route=account/login")
    
    def navigate_to_login_page(self):
        """Navigate to login page"""
        logger.info("Navigating to login page")
        self.navigate_to(self.url)
        return self
    
    def click_my_account_menu(self):
        """Click My Account in header"""
        logger.info("Clicking My Account menu")
        self.click(self.MY_ACCOUNT_LINK)
        return self
    
    def click_login_menu_item(self):
        """Click Login menu item"""
        logger.info("Clicking Login menu item")
        self.click(self.LOGIN_MENU_ITEM)
        return self
    
    def enter_email(self, email):
        """
        Enter email address
        Args:
            email: Email address
        """
        logger.info(f"Entering email: {email}")
        self.enter_text(self.EMAIL_INPUT, email)
        return self
    
    def enter_password(self, password):
        """
        Enter password
        Args:
            password: Password (will be masked in logs)
        """
        logger.info("Entering password: ******")
        self.enter_text(self.PASSWORD_INPUT, password)
        return self
    
    def click_login_button(self):
        """Click login button"""
        logger.info("Clicking login button")
        self.click(self.LOGIN_BUTTON)
        return self
    
    def login(self, email, password):
        """
        Complete login flow
        Args:
            email: Email address
            password: Password
        Returns:
            self for method chaining
        """
        logger.info(f"Logging in with email: {email}")
        self.navigate_to_login_page()
        self.enter_email(email)
        self.enter_password(password)
        self.click_login_button()
        return self
    
    # ============ Verification Methods ============
    
    def is_login_successful(self):
        """Check if login was successful"""
        return self.is_visible(self.MY_ACCOUNT_HEADER, timeout=5)
    
    def is_error_message_displayed(self):
        """Check if error message is displayed"""
        return self.is_visible(self.ERROR_MESSAGE, timeout=3)
    
    def get_error_message(self):
        """Get error message text"""
        if self.is_error_message_displayed():
            return self.get_text(self.ERROR_MESSAGE)
        return None
    
    def is_logged_in(self):
        """Verify user is logged in"""
        # Check for presence of logout link or my account header
        return (self.is_present(self.LOGOUT_LINK, timeout=2) or 
                self.is_present(self.MY_ACCOUNT_HEADER, timeout=2))
    
    def logout(self):
        """Logout user"""
        if self.is_logged_in():
            logger.info("Logging out user")
            self.click_my_account_menu()
            self.click(self.LOGOUT_LINK)
```

---

### Day 4-5: Write Test Cases

**File: `tests/conftest.py`**

```python
"""
Pytest Configuration
Contains fixtures and hooks for test execution
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from config.config import Config
from utils.logger import get_logger
from datetime import datetime

logger = get_logger(__name__)

@pytest.fixture(scope="function")
def driver(request):
    """
    WebDriver fixture
    Scope: function (new browser for each test)
    """
    logger.info("Setting up WebDriver")
    
    # Chrome options
    chrome_options = ChromeOptions()
    
    if Config.HEADLESS:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
    
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--start-maximized")
    
    # Initialize driver
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=chrome_options
    )
    
    # Set timeouts
    driver.implicitly_wait(Config.IMPLICIT_WAIT)
    driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)
    
    # Maximize window
    if not Config.HEADLESS:
        driver.maximize_window()
    
    # Yield driver to test
    yield driver
    
    # Teardown
    logger.info("Tearing down WebDriver")
    
    # Take screenshot on failure
    if request.node.rep_call.failed:
        test_name = request.node.name
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        screenshot_name = f"FAILED_{test_name}_{timestamp}"
        driver.save_screenshot(f"screenshots/{screenshot_name}.png")
        logger.error(f"Test failed. Screenshot: {screenshot_name}.png")
    
    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture test result for screenshot on failure
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)

@pytest.fixture(scope="session", autouse=True)
def test_session_setup():
    """Setup before test session"""
    logger.info("=" * 80)
    logger.info("Starting Test Session")
    logger.info(f"Environment: {Config.ENVIRONMENT}")
    logger.info(f"Base URL: {Config.BASE_URL}")
    logger.info(f"Browser: {Config.BROWSER}")
    logger.info(f"Headless: {Config.HEADLESS}")
    logger.info("=" * 80)
    
    yield
    
    logger.info("=" * 80)
    logger.info("Test Session Completed")
    logger.info("=" * 80)
```

**File: `test_data/test_users.json`**

```json
{
  "valid_user": {
    "email": "test@example.com",
    "password": "Test123!"
  },
  "invalid_user": {
    "email": "invalid@example.com",
    "password": "WrongPass"
  },
  "empty_credentials": {
    "email": "",
    "password": ""
  }
}
```

**File: `tests/test_login.py`**

```python
"""
Login Tests
Test cases for login functionality
"""
import pytest
import json
from pages.login_page import LoginPage
from utils.logger import get_logger

logger = get_logger(__name__)

class TestLogin:
    """Test suite for login functionality"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Setup for each test"""
        self.driver = driver
        self.login_page = LoginPage(driver)
        
        # Load test data
        with open('test_data/test_users.json', 'r') as f:
            self.test_data = json.load(f)
    
    @pytest.mark.smoke
    @pytest.mark.critical
    def test_login_with_valid_credentials(self):
        """
        Test ID: TC-LOGIN-001
        Requirement: REQ-AUTH-001
        
        Test login with valid credentials
        Expected: User successfully logs in
        """
        logger.info("TEST: test_login_with_valid_credentials - START")
        
        # Get test data
        valid_user = self.test_data['valid_user']
        
        # Execute login
        self.login_page.login(
            email=valid_user['email'],
            password=valid_user['password']
        )
        
        # Verify login success
        assert self.login_page.is_login_successful(), \
            "Login failed with valid credentials"
        
        logger.info("TEST: test_login_with_valid_credentials - PASS")
    
    @pytest.mark.smoke
    @pytest.mark.critical
    def test_login_with_invalid_credentials(self):
        """
        Test ID: TC-LOGIN-002
        Requirement: REQ-AUTH-002
        
        Test login with invalid credentials
        Expected: Error message displayed
        """
        logger.info("TEST: test_login_with_invalid_credentials - START")
        
        # Get test data
        invalid_user = self.test_data['invalid_user']
        
        # Execute login
        self.login_page.login(
            email=invalid_user['email'],
            password=invalid_user['password']
        )
        
        # Verify error message
        assert self.login_page.is_error_message_displayed(), \
            "No error message displayed for invalid credentials"
        
        error_msg = self.login_page.get_error_message()
        logger.info(f"Error message: {error_msg}")
        
        logger.info("TEST: test_login_with_invalid_credentials - PASS")
    
    @pytest.mark.smoke
    def test_login_with_empty_credentials(self):
        """
        Test ID: TC-LOGIN-003
        Requirement: REQ-AUTH-003
        
        Test login with empty credentials
        Expected: Error message displayed
        """
        logger.info("TEST: test_login_with_empty_credentials - START")
        
        # Execute login with empty credentials
        self.login_page.login(email="", password="")
        
        # Verify error message
        assert self.login_page.is_error_message_displayed(), \
            "No error message displayed for empty credentials"
        
        logger.info("TEST: test_login_with_empty_credentials - PASS")
    
    @pytest.mark.regression
    def test_login_with_invalid_email_format(self):
        """
        Test ID: TC-LOGIN-004
        Requirement: REQ-AUTH-004
        
        Test login with invalid email format
        Expected: Validation error
        """
        logger.info("TEST: test_login_with_invalid_email_format - START")
        
        # Execute login with invalid email
        self.login_page.login(email="notanemail", password="Test123!")
        
        # Verify error
        assert self.login_page.is_error_message_displayed(), \
            "No error for invalid email format"
        
        logger.info("TEST: test_login_with_invalid_email_format - PASS")
    
    @pytest.mark.regression
    @pytest.mark.parametrize("email,password", [
        ("", "Test123!"),  # Empty email
        ("test@example.com", ""),  # Empty password
        ("", ""),  # Both empty
    ])
    def test_login_with_missing_fields(self, email, password):
        """
        Test ID: TC-LOGIN-005
        Requirement: REQ-AUTH-005
        
        Test login with missing required fields
        Expected: Validation error for missing fields
        """
        logger.info(f"TEST: test_login_with_missing_fields - Email: {email}, Password: {password}")
        
        # Execute login
        self.login_page.login(email=email, password=password)
        
        # Verify error
        assert self.login_page.is_error_message_displayed(), \
            f"No error for missing fields. Email: {email}, Password: {password}"
        
        logger.info("TEST: test_login_with_missing_fields - PASS")
```

---

### Day 6-7: Run Tests and Create README

**Run Tests:**

```bash
# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run only smoke tests
pytest tests/ -m smoke

# Run with HTML report
pytest tests/ --html=reports/report.html --self-contained-html

# Run in parallel (install pytest-xdist first)
pip install pytest-xdist
pytest tests/ -n auto

# Run specific test
pytest tests/test_login.py::TestLogin::test_login_with_valid_credentials
```

**File: `README.md`**

```markdown
# Selenium GxP Test Automation Framework

A robust, scalable test automation framework for GxP-compliant applications using Selenium, Python, and pytest.

## 🎯 Features

- **Page Object Model (POM)**: Maintainable and reusable code structure
- **Configuration Management**: Environment-based configuration
- **Logging**: Comprehensive logging for debugging and audit trails
- **Screenshots**: Automatic screenshots on test failures
- **HTML Reports**: Beautiful test execution reports
- **GxP Compliance**: Built with pharmaceutical validation in mind

## 📋 Prerequisites

- Python 3.11+
- Chrome browser
- pip (Python package manager)

## 🚀 Quick Start

### 1. Clone Repository

\`\`\`bash
git clone https://github.com/yourusername/selenium-gxp-framework.git
cd selenium-gxp-framework
\`\`\`

### 2. Create Virtual Environment

\`\`\`bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
\`\`\`

### 3. Install Dependencies

\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 4. Configure Environment

Edit `.env` file:

\`\`\`
ENVIRONMENT=dev
BASE_URL=https://demo.opencart.com/
HEADLESS=false
BROWSER=chrome
\`\`\`

### 5. Run Tests

\`\`\`bash
# Run all tests
pytest tests/

# Run smoke tests
pytest tests/ -m smoke

# Generate HTML report
pytest tests/ --html=reports/report.html --self-contained-html
\`\`\`

## 📁 Project Structure

\`\`\`
selenium-gxp-framework/
│
├── config/                 # Configuration files
│   ├── config.py          # Configuration management
│   └── environments.json  # Environment-specific settings
│
├── pages/                  # Page Object Models
│   ├── base_page.py       # Base page with common methods
│   └── login_page.py      # Login page object
│
├── tests/                  # Test cases
│   ├── conftest.py        # Pytest fixtures
│   └── test_login.py      # Login tests
│
├── utils/                  # Utility modules
│   ├── logger.py          # Logging utility
│   └── screenshot_helper.py
│
├── test_data/             # Test data files
│   └── test_users.json    # User test data
│
├── reports/               # Test reports
├── screenshots/           # Test screenshots
├── logs/                  # Log files
│
├── .env                   # Environment variables
├── .gitignore            # Git ignore file
├── pytest.ini            # Pytest configuration
├── requirements.txt      # Python dependencies
└── README.md             # This file
\`\`\`

## 🧪 Writing Tests

### Example Test Case

\`\`\`python
import pytest
from pages.login_page import LoginPage

def test_login(driver):
    login_page = LoginPage(driver)
    login_page.login("test@example.com", "Test123!")
    assert login_page.is_login_successful()
\`\`\`

### Test Markers

- `@pytest.mark.smoke`: Quick smoke tests
- `@pytest.mark.regression`: Full regression suite
- `@pytest.mark.critical`: Critical path tests

## 📊 Test Reports

After test execution, find reports in:
- HTML Report: `reports/report.html`
- Logs: `logs/test_[timestamp].log`
- Screenshots: `screenshots/`

## 🔧 Configuration

### Browser Options

Set in `.env`:
- `BROWSER=chrome` (default)
- `HEADLESS=true` (for CI/CD)

### Timeouts

- `IMPLICIT_WAIT=10` (seconds)
- `EXPLICIT_WAIT=20` (seconds)
- `PAGE_LOAD_TIMEOUT=30` (seconds)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/NewFeature`)
3. Commit changes (`git commit -m 'Add NewFeature'`)
4. Push to branch (`git push origin feature/NewFeature`)
5. Open Pull Request

## 📝 License

This project is licensed under the MIT License.

## 👤 Author

Your Name - [@yourhandle](https://twitter.com/yourhandle)

## 🙏 Acknowledgments

- Selenium WebDriver
- pytest framework
- GxP validation best practices
\`\`\`

---

## 📸 Screenshots

Include in README:
- Test execution
- HTML report
- Framework structure

## 🚀 Next Steps

Week 3-4: Add more features:
- Database testing
- API testing
- Data-driven testing
- CI/CD integration
```

---

### Day 8-14: Push to GitHub

**Initialize Git:**

```bash
# Initialize repository
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Selenium GxP Framework with Login tests"

# Create repository on GitHub
# Then push:
git remote add origin https://github.com/yourusername/selenium-gxp-framework.git
git branch -M main
git push -u origin main
```

---

## ✅ Week 1-2 Checklist

- [ ] Python environment set up
- [ ] Project structure created
- [ ] Base page class implemented (50+ methods)
- [ ] Login page object created
- [ ] 5+ test cases written
- [ ] Tests running successfully
- [ ] README.md completed
- [ ] Code pushed to GitHub
- [ ] Repository is public and visible

---

## 🎯 Success Criteria

After Week 1-2, you should have:
1. ✅ Working test automation framework
2. ✅ Clean, documented code
3. ✅ Public GitHub repository
4. ✅ Tests passing (green)
5. ✅ Ready to show in interviews

---

## Week 3-4: Add Complexity (Next Guide)

Coming in Part 2:
- Data-driven testing with Excel
- Database integration
- API testing
- Custom reporting
- Traceability matrix

---

**🚀 You now have a REAL framework you can show employers!**

**Next: Continue to Part 2 for Week 3-4 activities**
