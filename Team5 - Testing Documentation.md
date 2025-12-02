# Team5 - Testing Documentation

# 1. Testing Strategy

 The overall testing strategy for our project combines **unit testing**, **integration testing**, and **behavioral testing** to ensure both correctness and robustness of the *Job Description Generator* Django application. 

The application contains several key components:

- **Database Model:** `Past` model storing job description histories
- **User Authentication Workflow:** registration, login, logout
- **Template Rendering:** home page, login page, register page, past history page
- **Core Functionality:** generating job descriptions using OpenAI API
- **View Logic:** form validation, session handling, DB persistence

Our strategy ensures all of these are validated through isolated and integrated test flows.

### **Unit Testing**

Unit tests focus on verifying the correctness of individual components in isolation.

Applied to:

- Django model (`Past`)
- View logic (GET/POST handlers)
- Form handling
- Authentication workflow

### **Integration Testing**

Integration tests validate interactions between multiple components.

Applied to:

- POST workflows (form → OpenAI mock → database write → template render)
- User registration/login/logout flows
- Displaying historical records

### **Mock Testing**

Since the system integrates with an external AI model (OpenAI API), mock objects are used to replace external dependencies during testing.

Mock testing enables:

- Deterministic behaviors
- Elimination of network latency
- Avoidance of API cost
- Verification of invocation correctness

This ensures the AI-related pipeline remains testable while preserving full control over the testing environment.

# **2. Scope of Testing**

## **2.1 Included in Scope**

The following subsystems and functionalities were included within the testing framework:

1. **Data Model Validation**
    - Database field storage and retrieval
    - String representation functions
    - Timestamp-based ordering
2. **View Layer Behavior**
    - Template rendering
    - GET and POST request handling
    - Form submission and validation
    - Interaction with data persistence mechanisms
3. **Authentication Workflow**
    - User registration
    - Credential verification
    - Session initiation and termination
4. **Core Application Logic**
    - Handling and storing historical job descriptions
    - Generative workflow (via mocked OpenAI API)

## **2.2 Excluded from Scope**

- Front-end (JavaScript, CSS)
- Email validation / password recovery flows

# **3. Testing Environment**

The following table summarizes the environment used:

| Component | Configuration |
| --- | --- |
| Operating System | macOS |
| Python Version | **3.11 (virtual environment)** |
| Django Version | Django 4.2.25 |
| Database | SQLite (in-memory test DB) |
| Test Framework | `unittest` via `Django TestCase` |
| Client Simulator | Django test client (built on Python’s `unittest, client.get`, `client.post`) |
| Mocking Library | `unittest.mock` for OpenAI |

All tests executed using:

```python
python manage.py test
# Please make sure you have Python 3.11 version that's compatible to Django default python version
```

Each test runs in isolation with its own auto-generated database.

# **4. Test Cases and Detailed Results**

This section enumerates the **12** executed test cases, providing an academic description of their purpose, methodology, and results.

## **4.1 Model-Level Tests**

### **Test 1: `test_past_model_str`**

**Objective:**

To verify the correctness of the `__str__()` method of the `Past` model.

**Methodology:**

A `Past` instance is constructed, converted to a string, and compared with the expected textual representation.

**Expected Outcome:**

The string output should equal the `question` field.

**Observed Outcome:**

Passed—representation conforms to specification.

---

### **Test 2: `test_past_model_fields`**

**Objective:**

To validate the integrity of field storage and retrieval in the `Past` model.

**Methodology:**

A saved instance is retrieved using ORM queries and its fields are compared with the original input.

**Expected Outcome:**

All fields match expected values.

**Observed Outcome:**

Passed.

---

### **Test 3: `test_past_model_ordering`**

**Objective:**

To confirm that past entries are ordered in descending order of creation time.

**Methodology:**

Two instances are created sequentially. The query ordering is examined to verify that the latest entry appears first.

**Expected Outcome:**

The most recent record precedes earlier entries.

**Observed Outcome:**

Passed.

---

## **4.2 View-Level Tests**

### **Test 4: `test_home_view_get`**

**Objective:**

To validate the correct rendering of the home page via HTTP GET.

**Methodology:**

Authenticated request is simulated using Django’s test client.

**Expected Outcome:**

HTTP 200 status; correct template rendered.

**Observed Outcome:**

Passed.

---

### **Test 5: `test_register_view_get`**

**Objective:**

To examine whether the registration interface loads correctly.

**Methodology:**

GET request simulated without user authentication.

**Expected Outcome:**

HTTP 200 status; `register.html` rendered.

**Observed Outcome:**

Passed.

---

### **Test 6: `test_login_view_get`**

**Objective:**

To ensure proper rendering of the login interface.

**Methodology:**

Unauthenticated GET request initiated.

**Expected Outcome:**

HTTP 200 status; `login.html` rendered.

**Observed Outcome:**

Passed.

---

### **Test 7: `test_past_view_get`**

**Objective:**

To verify rendering of the historical job description page.

**Methodology:**

Authenticated GET request simulated.

**Expected Outcome:**

HTTP 200 status; correct template rendered.

**Observed Outcome:**

Passed.

---

### **Test 8: `test_home_view_post_success`**

**Objective:**

To validate the full POST-based workflow for generating job descriptions.

**Methodology:**

A POST request is issued with form data.

The OpenAI API call is replaced with a mock object to simulate AI responses.

**Expected Outcome:**

- Correct template rendered
- `Past` entry created
- AI mock invoked exactly once

**Observed Outcome:**

Passed—demonstrates correctness of the primary system function.

---

### **Test 9: `test_register_user_post_success`**

**Objective:**

To evaluate successful user account creation.

**Methodology:**

Simulated POST containing valid registration data.

**Expected Outcome:**

System redirects to the login page; new user exists in database.

**Observed Outcome:**

Passed.

---

### **Test 10: `test_register_user_password_mismatch`**

**Objective:**

To verify robustness of the registration logic under incorrect input.

**Methodology:**

Submitted mismatching passwords via POST.

**Expected Outcome:**

Registration fails; no new user created.

**Observed Outcome:**

Passed.

---

### **Test 11: `test_login_user_success`**

**Objective:**

To confirm correct credential validation and session initiation.

**Methodology:**

Valid username/password submitted via POST.

**Expected Outcome:**

Successful redirection to the home page.

**Observed Outcome:**

Passed.

---

### **Test 12: `test_logout_user`**

**Objective:**

To validate correct session termination.

**Methodology:**

Logout endpoint accessed via GET.

**Expected Outcome:**

Redirection to login interface.

**Observed Outcome:**

Passed.

Here is the screenshot of running our test cases successfully. 

![image.png](Team5%20-%20Testing%20Documentation/image.png)

![image.png](Team5%20-%20Testing%20Documentation/image%201.png)

![image.png](Team5%20-%20Testing%20Documentation/image%202.png)

# **5. Summary**

The test suite, here we contain **12 systematically designed test cases**, provides comprehensive coverage of all major backend functionalities of the *Job Description Generator* application. The tests can help to affirm that:

- Model behavior is consistent, deterministic, and stable.
- View rendering functions correctly across both authenticated and unauthenticated states.
- Authentication workflows—including registration, login, and logout—operate as intended.
- The primary AI-driven job description generation pipeline behaves reliably when isolated from external dependencies via mocking.

All test cases produced results consistent with the expected behavior, indicating that the backend system satisfies the requirements within the defined scope of testing.