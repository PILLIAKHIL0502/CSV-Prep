# GxP Testing & Test Automation Guide - Part 3

## Playwright Framework for Modern GxP Web Applications

**Part 3 of 6: Playwright Implementation for Interview Preparation**

---

## Table of Contents

- [1. Why Playwright for GxP Testing?](#1-why-playwright-for-gxp-testing)
- [2. Selenium vs Playwright Comparison](#2-selenium-vs-playwright-comparison)
- [3. Playwright Setup & Architecture](#3-playwright-setup--architecture)
- [4. Auto-Waiting & Retry Logic](#4-auto-waiting--retry-logic)
- [5. Network Interception for Testing](#5-network-interception-for-testing)
- [6. Built-in Tracing & Debugging](#6-built-in-tracing--debugging)
- [7. Converting Selenium Tests to Playwright](#7-converting-selenium-tests-to-playwright)
- [8. Interview Q&A - Playwright](#8-interview-qa---playwright)

---

## 1. Why Playwright for GxP Testing?

### Interview Question: "Why would you choose Playwright over Selenium?"

**Answer:**
"Playwright is Microsoft's modern automation framework with several advantages for GxP testing:

**1. AUTO-WAITING (Built-in Reliability)**
- Playwright automatically waits for elements to be actionable
- Reduces test flakiness significantly
- No need for explicit waits in most cases

**2. NETWORK INTERCEPTION**
- Can mock API responses for testing error scenarios
- Verify API calls without backend access
- Test offline modes

**3. MULTIPLE BROWSER CONTEXTS**
- Test with multiple users simultaneously in one test
- Faster than opening multiple browsers

**4. BUILT-IN TRACING**
- Automatic screenshot, video, and network recording
- Excellent debugging - view full test execution timeline
- GxP evidence collection out-of-the-box

**5. BETTER SELECTORS**
- Can use text content: `page.get_by_text('Login')`
- Role-based selectors: `page.get_by_role('button', name='Submit')`
- More resilient to UI changes

**When to Use Playwright:**
- ✅ Modern single-page applications (React, Angular, Vue)
- ✅ Cloud SaaS applications
- ✅ When test stability is critical
- ✅ Need advanced debugging capabilities
- ✅ Testing with multiple user roles simultaneously

**When to Stick with Selenium:**
- ✅ Legacy applications
- ✅ Team already expert in Selenium
- ✅ Existing large test suite (migration cost high)
- ✅ Need IE 11 support (Playwright doesn't support it)"

---

## 2. Selenium vs Playwright Comparison

### Side-by-Side Code Comparison

**Interview Scenario**: "Show me the difference between Selenium and Playwright for the same test"

#### Selenium Approach:
```python
# Selenium - Login Test
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://lims.pharma.com/login")

# Explicit waits needed
wait = WebDriverWait(driver, 10)
username = wait.until(EC.presence_of_element_located((By.ID, "username")))
username.send_keys("analyst1")

password = driver.find_element(By.ID, "password")
password.send_keys("password123")

login_btn = wait.until(EC.element_to_be_clickable((By.ID, "btnLogin")))
login_btn.click()

# Wait for navigation
wait.until(EC.url_contains("/dashboard"))

# Verify login
assert "Dashboard" in driver.title

driver.quit()
```

#### Playwright Approach:
```python
# Playwright - Same Login Test (Much Simpler!)
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    
    page.goto("https://lims.pharma.com/login")
    
    # Auto-waits built-in - no explicit waits needed!
    page.fill("#username", "analyst1")
    page.fill("#password", "password123")
    page.click("#btnLogin")
    
    # Auto-waits for navigation
    page.wait_for_url("**/dashboard")
    
    # Verify
    assert "Dashboard" in page.title()
    
    browser.close()
```

**Key Differences Table:**

| Feature | Selenium | Playwright | Winner |
|---------|----------|------------|--------|
| **Setup Complexity** | Moderate (need WebDriver) | Simple (no drivers needed) | Playwright |
| **Auto-Waiting** | Manual with WebDriverWait | Automatic | Playwright |
| **Selector Strategies** | 8 types (ID, CSS, XPath, etc) | 8 types + Text/Role/Label | Playwright |
| **Network Interception** | Not native (need proxy) | Built-in | Playwright |
| **Multi-Tab/Context** | Slow (switch windows) | Fast (contexts) | Playwright |
| **Screenshot/Video** | Manual implementation | Built-in | Playwright |
| **Trace Viewer** | No | Yes (amazing debugging) | Playwright |
| **Speed** | Slower | Faster (parallel by default) | Playwright |
| **Browser Support** | Chrome, Firefox, Safari, IE11 | Chrome, Firefox, Safari (no IE11) | Selenium for legacy |
| **Language Support** | Many (Java, Python, C#, JS, etc) | Python, JS/TS, C#, Java | Tie |
| **Community/Resources** | Mature, huge community | Growing fast | Selenium (for now) |
| **GxP Validation** | Well-established precedent | Newer, but widely adopted | Selenium (more history) |

---

## 3. Playwright Setup & Architecture

### Project Structure

```
pharma-playwright-framework/
├── tests/
│   ├── test_login.py
│   ├── test_samples.py
│   └── test_results.py
├── pages/
│   ├── base_page.py
│   ├── login_page.py
│   └── sample_page.py
├── playwright.config.py
├── conftest.py
└── requirements.txt
```

### Installation

```bash
# Install Playwright
pip install playwright pytest-playwright

# Install browsers (one-time)
playwright install

# Install specific browser
playwright install chromium
```

### Configuration (playwright.config.py)

```python
"""
Playwright Configuration for GxP Testing
"""

from playwright.sync_api import Playwright

class PlaywrightConfig:
    """Configuration for Playwright tests"""
    
    BASE_URL = "https://lims-val.pharma.com"
    
    # Browser settings
    HEADLESS = False  # Set True for CI/CD
    SLOW_MO = 100  # Slow down by 100ms (useful for debugging)
    
    # Timeout settings (ms)
    TIMEOUT = 30000  # 30 seconds default
    NAVIGATION_TIMEOUT = 30000
    
    # Screenshot/Video settings
    SCREENSHOTS = "only-on-failure"  # or "on" or "off"
    VIDEO = "retain-on-failure"  # or "on" or "off"
    
    # Trace for debugging
    TRACE = "retain-on-failure"  # or "on" or "off"
    
    # Browser context options
    VIEWPORT = {"width": 1920, "height": 1080}
    IGNORE_HTTPS_ERRORS = False  # Set True for self-signed certs in dev/val
    
    @staticmethod
    def get_browser_options():
        """Get browser launch options"""
        return {
            "headless": PlaywrightConfig.HEADLESS,
            "slow_mo": PlaywrightConfig.SLOW_MO,
        }
    
    @staticmethod
    def get_context_options():
        """Get browser context options"""
        return {
            "viewport": PlaywrightConfig.VIEWPORT,
            "ignore_https_errors": PlaywrightConfig.IGNORE_HTTPS_ERRORS,
            "record_video_dir": "test-results/videos" if PlaywrightConfig.VIDEO != "off" else None,
        }
```

### conftest.py (Pytest Fixtures)

```python
"""
Pytest fixtures for Playwright
"""

import pytest
from playwright.sync_api import sync_playwright
from playwright_config import PlaywrightConfig

@pytest.fixture(scope="session")
def playwright():
    """Session-scoped Playwright instance"""
    with sync_playwright() as p:
        yield p

@pytest.fixture(scope="session")
def browser(playwright):
    """Session-scoped browser"""
    browser = playwright.chromium.launch(**PlaywrightConfig.get_browser_options())
    yield browser
    browser.close()

@pytest.fixture
def context(browser):
    """Function-scoped browser context"""
    context = browser.new_context(**PlaywrightConfig.get_context_options())
    
    # Enable tracing for GxP evidence
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    
    yield context
    
    # Save trace on failure (checked in test)
    context.tracing.stop(path="test-results/trace.zip")
    context.close()

@pytest.fixture
def page(context):
    """Function-scoped page"""
    page = context.new_page()
    
    # Set default timeout
    page.set_default_timeout(PlaywrightConfig.TIMEOUT)
    
    yield page
    
    # Screenshot on test end (for evidence)
    page.screenshot(path="test-results/final-state.png")
```

---

## 4. Auto-Waiting & Retry Logic

### Interview Question: "Explain Playwright's auto-waiting. Why does it reduce flaky tests?"

**Answer & Demo:**

```python
"""
Playwright Auto-Waiting Demonstration
"""

def test_auto_waiting_demo(page):
    """
    Interview Answer:
    "Playwright has built-in smart waiting that makes tests more reliable:
    
    1. ACTIONABILITY CHECKS - Before every action, Playwright verifies:
       - Element is visible
       - Element is stable (not animating)
       - Element receives events (not covered by another element)
       - Element is enabled (not disabled)
    
    2. AUTO-RETRY - If checks fail, Playwright retries for up to timeout period
    
    3. NO SLEEP NEEDED - Unlike Selenium where we often add time.sleep(),
       Playwright waits intelligently
    
    This eliminates ~80% of flaky tests caused by timing issues."
    """
    
    page.goto("https://lims.pharma.com/login")
    
    # Example 1: Wait for element to appear and be clickable
    # If button is still loading, Playwright waits automatically
    page.click("#btnLogin")  # Auto-waits until clickable!
    
    # Example 2: Wait for element to have text
    # If text is being loaded via AJAX, Playwright waits
    page.get_by_role("heading").wait_for()  # Waits until visible
    
    # Example 3: Wait for network idle (AJAX completed)
    page.wait_for_load_state("networkidle")
    
    # Example 4: Fill field even if it's not yet visible
    # Playwright waits up to 30 seconds for it to appear
    page.fill("#username", "analyst1")  # Auto-waits for element!

def test_without_auto_waiting_selenium_style(page):
    """
    What you'd need in Selenium but is automatic in Playwright
    """
    # In Selenium, you'd write:
    # wait = WebDriverWait(driver, 10)
    # element = wait.until(EC.visibility_of_element_located((By.ID, "username")))
    # element = wait.until(EC.element_to_be_clickable((By.ID, "username")))
    # element.send_keys("analyst1")
    
    # In Playwright, just:
    page.fill("#username", "analyst1")  # That's it!
```

### Custom Waits

```python
def test_custom_waits(page):
    """
    Interview: Sometimes you need custom wait conditions
    """
    
    # Wait for specific text to appear
    page.get_by_text("Sample created successfully").wait_for()
    
    # Wait for element to disappear (loading spinner)
    page.locator(".loading-spinner").wait_for(state="hidden")
    
    # Wait for element to be enabled
    page.locator("#btnSubmit").wait_for(state="enabled")
    
    # Wait for URL to match pattern
    page.wait_for_url("**/dashboard")
    
    # Wait for function to return true
    page.wait_for_function("document.readyState === 'complete'")
    
    # Wait for API response
    with page.expect_response("**/api/samples") as response_info:
        page.click("#btnCreateSample")
    response = response_info.value
    assert response.status == 200
```

---

## 5. Network Interception for Testing

### Interview Question: "How do you test error scenarios like API failures?"

```python
"""
Network Interception - Test Error Scenarios
"""

def test_api_failure_handling(page):
    """
    Interview Answer:
    "With Playwright, we can intercept network requests and simulate
    failures without needing the actual backend to fail. This lets us test:
    - Server errors (500)
    - Network timeouts
    - Invalid responses
    - Offline mode
    
    This is critical for GxP because we need to verify error handling
    without actually breaking production systems."
    """
    
    # Intercept API call and return error
    page.route("**/api/samples", lambda route: route.fulfill(
        status=500,
        body='{"error": "Internal Server Error"}'
    ))
    
    page.goto("https://lims.pharma.com/samples")
    page.click("#btnCreateSample")
    
    # Verify error message displayed to user
    error_msg = page.get_by_text("Failed to create sample")
    assert error_msg.is_visible()
    
    # Verify user-friendly error, not technical details
    assert page.get_by_text("Internal Server Error").is_hidden()

def test_mock_successful_api_response(page):
    """
    Mock API response for faster testing
    """
    # Mock the sample creation API
    page.route("**/api/samples", lambda route: route.fulfill(
        status=201,
        json={
            "sample_id": "SAM-2024-MOCK-001",
            "status": "created",
            "tests_assigned": ["HPLC", "Dissolution"]
        }
    ))
    
    page.goto("https://lims.pharma.com/samples")
    page.click("#btnCreateSample")
    page.fill("#material", "ASPIRIN-100MG")
    page.click("#btnSave")
    
    # Verify UI shows mocked response
    assert page.get_by_text("SAM-2024-MOCK-001").is_visible()

def test_verify_api_call_made(page):
    """
    Verify correct API call is made (without mocking)
    """
    # Listen for API call
    with page.expect_request("**/api/samples") as request_info:
        page.goto("https://lims.pharma.com/samples")
        page.click("#btnCreateSample")
        page.fill("#material", "ASPIRIN-100MG")
        page.click("#btnSave")
    
    request = request_info.value
    
    # Verify request details
    assert request.method == "POST"
    payload = request.post_data_json
    assert payload['material'] == "ASPIRIN-100MG"
```

---

## 6. Built-in Tracing & Debugging

### Interview Question: "How do you debug failed tests in Playwright?"

**Answer:**
"Playwright has the BEST debugging tools I've ever used for test automation:

**1. TRACE VIEWER** - Shows complete test execution:
- Every action taken
- Screenshots at each step
- Network requests
- Console logs
- Full timeline

**2. INSPECTOR** - Step through tests interactively

**3. VIDEO RECORDING** - Automatic video of test execution

**4. SCREENSHOT ON FAILURE** - Automatic evidence"

### Using Trace Viewer

```python
def test_with_tracing(page, context):
    """
    Trace is automatically captured per conftest.py
    If test fails, examine trace with:
    
    playwright show-trace test-results/trace.zip
    
    This opens a web interface showing:
    - Every action (click, type, etc)
    - Screenshot at each step
    - Network traffic
    - Console output
    - DOM snapshots
    
    Interview Point:
    "This is invaluable for GxP validation. When QA reviews failed tests,
    they can see EXACTLY what happened, step by step. Much better than
    just a final screenshot."
    """
    page.goto("https://lims.pharma.com/login")
    page.fill("#username", "analyst1")
    page.fill("#password", "wrongpassword")
    page.click("#btnLogin")
    
    # This assertion will fail - trace will show why
    assert page.get_by_text("Welcome").is_visible()
    # Trace will show:
    # - Login button was clicked
    # - API returned 401
    # - Error message appeared instead of welcome
    # - Exact timestamp of failure

def test_codegen_for_learning(page):
    """
    Interview Tip:
    "When learning a new application, use Playwright Codegen:
    
    playwright codegen https://lims.pharma.com
    
    This opens a browser where you interact normally, and Playwright
    generates the test code for you! Great for quickly creating Page Objects."
    """
    pass
```

### Video Recording

```python
# Automatic video recording (configured in conftest.py)
def test_with_video(page):
    """
    Video automatically recorded if test fails.
    Saved to: test-results/videos/
    
    Interview Answer:
    "Video evidence is excellent for GxP validation documentation.
    We can show QA exactly what the test did, making test review faster."
    """
    page.goto("https://lims.pharma.com")
    # ... test steps ...
    # If this fails, video is automatically saved
```

---

## 7. Converting Selenium Tests to Playwright

### Interview Scenario: "Walk me through converting an existing Selenium test to Playwright"

**Selenium Version:**
```python
# OLD: Selenium Test
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_sample_creation_selenium():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    
    try:
        driver.get("https://lims.pharma.com/login")
        
        # Login
        username = wait.until(EC.presence_of_element_located((By.ID, "username")))
        username.send_keys("analyst1")
        driver.find_element(By.ID, "password").send_keys("pass123")
        driver.find_element(By.ID, "btnLogin").click()
        
        # Wait for dashboard
        wait.until(EC.url_contains("dashboard"))
        
        # Create sample
        driver.find_element(By.ID, "btnNewSample").click()
        wait.until(EC.visibility_of_element_located((By.ID, "materialCode")))
        driver.find_element(By.ID, "materialCode").send_keys("MAT-001")
        driver.find_element(By.ID, "batchNumber").send_keys("BATCH-123")
        driver.find_element(By.ID, "btnSave").click()
        
        # Verify
        success_msg = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".success-message"))
        )
        assert "Sample created" in success_msg.text
        
        # Get sample ID
        sample_id_element = driver.find_element(By.ID, "newSampleId")
        sample_id = sample_id_element.text
        
        # Verify in list
        driver.get("https://lims.pharma.com/samples")
        search_box = wait.until(EC.presence_of_element_located((By.ID, "search")))
        search_box.send_keys(sample_id)
        driver.find_element(By.ID, "btnSearch").click()
        
        results = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".sample-row"))
        )
        assert len(results) == 1
        
    finally:
        driver.quit()
```

**Playwright Version (Converted):**
```python
# NEW: Playwright Test (Much Cleaner!)
def test_sample_creation_playwright(page):
    """
    Interview Comparison:
    - 40% less code
    - No explicit waits needed
    - More readable
    - Better selectors (can use text, role)
    - Auto-retry on transient failures
    """
    
    # Login
    page.goto("https://lims.pharma.com/login")
    page.fill("#username", "analyst1")
    page.fill("#password", "pass123")
    page.click("#btnLogin")
    
    # Wait for dashboard (auto-waits for navigation)
    page.wait_for_url("**/dashboard")
    
    # Create sample
    page.click("#btnNewSample")
    page.fill("#materialCode", "MAT-001")
    page.fill("#batchNumber", "BATCH-123")
    page.click("#btnSave")
    
    # Verify (auto-waits for element)
    success_msg = page.locator(".success-message")
    assert "Sample created" in success_msg.inner_text()
    
    # Get sample ID
    sample_id = page.locator("#newSampleId").inner_text()
    
    # Verify in list
    page.goto("https://lims.pharma.com/samples")
    page.fill("#search", sample_id)
    page.click("#btnSearch")
    
    # Verify one result
    results = page.locator(".sample-row")
    assert results.count() == 1

# Even Better: Using Text and Role Selectors
def test_sample_creation_playwright_better_selectors(page):
    """
    Interview Advantage:
    "Playwright's text/role selectors are more resilient to HTML changes.
    If developers change IDs, tests don't break."
    """
    page.goto("https://lims.pharma.com/login")
    
    # Use role-based selectors (accessibility-first)
    page.get_by_role("textbox", name="Username").fill("analyst1")
    page.get_by_role("textbox", name="Password").fill("pass123")
    page.get_by_role("button", name="Login").click()
    
    # Use text content
    page.get_by_text("New Sample").click()
    
    # Use labels
    page.get_by_label("Material Code").fill("MAT-001")
    page.get_by_label("Batch Number").fill("BATCH-123")
    page.get_by_role("button", name="Save").click()
    
    # Verify
    assert page.get_by_text("Sample created successfully").is_visible()
```

### Conversion Checklist

**Interview Answer: "Here's how I approach Selenium to Playwright migration:"**

```
✅ STEP 1: Setup
   - Install: pip install playwright pytest-playwright
   - Install browsers: playwright install
   - Create conftest.py with page fixture

✅ STEP 2: Replace Driver with Page
   - driver = webdriver.Chrome() → page (from fixture)
   - driver.get(url) → page.goto(url)
   - driver.quit() → handled by fixture

✅ STEP 3: Replace Element Location
   - driver.find_element(By.ID, "x") → page.locator("#x")
   - driver.find_elements(By.CSS, ".x") → page.locator(".x")

✅ STEP 4: Replace Actions
   - element.send_keys("text") → page.fill("#id", "text")
   - element.click() → page.click("#id")
   - element.text → page.inner_text("#id")

✅ STEP 5: Remove Explicit Waits
   - WebDriverWait(...).until(...) → Remove! (auto-wait)
   - time.sleep(x) → Remove! (anti-pattern)

✅ STEP 6: Update Assertions
   - assert element.is_displayed() → assert page.is_visible("#id")
   - assert "text" in element.text → assert "text" in page.inner_text("#id")

✅ STEP 7: Add Better Selectors
   - Consider using text/role selectors for better stability
   - page.get_by_text("Login")
   - page.get_by_role("button", name="Submit")

✅ STEP 8: Add Tracing
   - Configure in conftest.py
   - Run tests
   - Review trace: playwright show-trace test-results/trace.zip
```

---

## 8. Interview Q&A - Playwright

### Q1: "When would you NOT use Playwright?"

**Answer:**
- Legacy browsers (IE11, old Safari) - Selenium better
- Desktop applications - Selenium or other tools
- Team has no JavaScript/Python knowledge - stick with familiar tools
- Existing huge Selenium suite - migration cost vs benefit
- Company policy requires more established tool - Selenium has longer track record in pharma

### Q2: "How do you handle authentication in Playwright?"

```python
# Interview Answer: "Store authentication state and reuse"

def test_setup_auth(page):
    """Login once and save state"""
    page.goto("https://lims.pharma.com/login")
    page.fill("#username", "analyst1")
    page.fill("#password", "pass123")
    page.click("#btnLogin")
    
    # Save authentication state
    page.context.storage_state(path="auth/analyst1.json")

# In conftest.py
@pytest.fixture
def authenticated_page(browser):
    """Provide pre-authenticated page"""
    context = browser.new_context(storage_state="auth/analyst1.json")
    page = context.new_page()
    yield page
    context.close()

# Use in tests
def test_with_auth(authenticated_page):
    """Test skips login - already authenticated!"""
    authenticated_page.goto("https://lims.pharma.com/samples")
    # Already logged in!
```

### Q3: "How do you test with multiple users simultaneously?"

```python
def test_multi_user_workflow(browser):
    """
    Interview Scenario:
    "Test requires QC Analyst to enter results and QC Manager to approve.
    With Playwright contexts, both can run in parallel in same test!"
    """
    # Context 1: QC Analyst
    analyst_context = browser.new_context(storage_state="auth/analyst.json")
    analyst_page = analyst_context.new_page()
    
    # Context 2: QC Manager
    manager_context = browser.new_context(storage_state="auth/manager.json")
    manager_page = manager_context.new_page()
    
    # Analyst enters results
    analyst_page.goto("https://lims.pharma.com/samples/SAM-001")
    analyst_page.fill("#result", "99.5")
    analyst_page.click("#btnSave")
    
    # Manager approves (without waiting for analyst to logout!)
    manager_page.goto("https://lims.pharma.com/samples/SAM-001")
    manager_page.click("#btnApprove")
    
    # Verify both see approved status
    assert analyst_page.get_by_text("Approved").is_visible()
    assert manager_page.get_by_text("Approved").is_visible()
    
    analyst_context.close()
    manager_context.close()
```

### Q4: "How do you handle file uploads/downloads?"

```python
def test_file_upload(page):
    """Upload test data file"""
    page.goto("https://lims.pharma.com/import")
    
    # Upload file
    page.set_input_files("#fileUpload", "test_data/samples.xlsx")
    page.click("#btnImport")
    
    assert page.get_by_text("Import successful").is_visible()

def test_file_download(page):
    """Download report"""
    page.goto("https://lims.pharma.com/reports")
    
    # Start waiting for download
    with page.expect_download() as download_info:
        page.click("#btnDownloadCOA")
    
    download = download_info.value
    
    # Verify file downloaded
    assert download.suggested_filename == "COA-BATCH-12345.pdf"
    
    # Save to specific location
    download.save_as("reports/downloaded_coa.pdf")
```

---

## Quick Reference - Playwright Common Commands

```python
# Navigation
page.goto(url)
page.go_back()
page.reload()

# Finding Elements
page.locator("#id")
page.locator(".class")
page.locator("text=Login")
page.get_by_role("button", name="Submit")
page.get_by_text("Welcome")
page.get_by_label("Username")

# Actions
page.click("#btn")
page.fill("#input", "text")
page.select_option("#dropdown", "value")
page.check("#checkbox")
page.uncheck("#checkbox")

# Assertions (auto-wait!)
expect(page.locator("#id")).to_be_visible()
expect(page.locator("#id")).to_have_text("text")
expect(page.locator("#id")).to_be_enabled()

# Waiting
page.wait_for_url("**/dashboard")
page.wait_for_load_state("networkidle")
page.locator("#id").wait_for(state="visible")

# Network
with page.expect_response("**/api") as response:
    page.click("#btn")
assert response.value.status == 200

# Multiple Elements
elements = page.locator(".item").all()
assert len(elements) == 5
```

---

**END OF PART 3 - PLAYWRIGHT FRAMEWORK**

**Key Interview Takeaways:**
- ✅ Playwright has better auto-waiting (reduces flaky tests)
- ✅ Network interception enables API failure testing
- ✅ Trace viewer is best-in-class debugging
- ✅ 40% less code than Selenium
- ✅ Better for modern SPAs
- ✅ Choose based on project needs, not hype

---

Ready for Part 4: GitHub Actions CI/CD Pipeline Integration
