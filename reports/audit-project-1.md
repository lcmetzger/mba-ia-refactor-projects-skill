---
generated_by: refactor-arch
phase: 2
project_dir: code-smells-project
audit_file: audit-project-1.md
generated_at: 2026-06-02T14:30:00
stack: Python + Flask
---

================================
PHASE 1: PROJECT ANALYSIS
================================
Language:      Python
Framework:     Flask 3.1.1
Dependencies:  flask, flask-cors
Domain:        E-commerce (REST API for products, users, orders)
Architecture:  Partially organized (app.py, controllers.py, models.py, database.py) but with business logic and database queries scattered.
Source files:  4 files analyzed
DB tables:     produtos, usuarios, pedidos, itens_pedido
================================

================================
ARCHITECTURE AUDIT REPORT
================================
Project: code-smells-project
Stack:   Python + Flask
Files:   4 analyzed | ~650 lines of code

## Summary
CRITICAL: 5 | HIGH: 3 | MEDIUM: 1 | LOW: 2

### [CRITICAL] SQL Injection
File: models.py:27, 44, 53, 61, 100, 114, 129, 145, 258, 273
Description: Multiple functions in models.py use string concatenation and f-strings to build SQL queries with user-provided input.
Impact: Full database compromise; unauthorized access, modification, or deletion of data via SQL Injection.
Recommendation: Use parameterized queries with the standard sqlite3 placeholder (?) in all database interactions.

### [CRITICAL] Arbitrary SQL Execution Endpoint
File: app.py:53-76
Description: The /admin/query endpoint accepts arbitrary SQL from the request body and executes it directly against the database without any authorization.
Impact: Remote code execution at the database level; potential for full data exfiltration or destruction by any user.
Recommendation: Remove this endpoint entirely or strictly limit it to authenticated administrators with predefined safe queries.

### [CRITICAL] Missing Authentication on Sensitive Routes
File: app.py:43, 53
Description: Administrative and destructive routes like /admin/reset-db and /admin/query are exposed without any form of authentication or authorization.
Impact: Any unauthenticated user can wipe the database or execute arbitrary commands.
Recommendation: Implement authentication (e.g., JWT or API Keys) and an authorization middleware to protect all administrative routes.

### [CRITICAL] Hardcoded Credentials
File: app.py:7
Description: The Flask SECRET_KEY is defined as a literal string 'minha-chave-super-secreta-123' directly in the main application file.
Impact: If the source code is exposed (e.g., public repo), sessions can be forged and security mechanisms bypassed.
Recommendation: Move all secrets to environment variables and load them using a dedicated configuration class/module.

### [CRITICAL] God File — models.py
File: models.py:1-294
Description: A single module (models.py) handles all database operations and logic for Products, Users, and Orders, violating the Single Responsibility Principle.
Impact: High coupling and low maintainability; changes in one domain (e.g., Orders) can accidentally affect others (e.g., Users).
Recommendation: Split models.py into smaller, domain-specific modules (e.g., product_model.py, user_model.py, order_model.py).

### [HIGH] Sensitive Data Exposure
File: controllers.py:114, 261
Description: The listar_usuarios endpoint returns the full user object including the 'senha' field, and the health_check endpoint exposes the secret_key and db_path.
Impact: Leakage of user credentials and internal system details that can be used for further attacks.
Recommendation: Filter sensitive fields in the Model or Controller before returning JSON; ensure health checks only return non-sensitive status information.

### [HIGH] Business Logic in Controllers
File: controllers.py:195-197, 230-234
Description: Controllers handle business logic such as multi-channel notifications (Email, SMS, Push) and specific status transition side-effects.
Impact: Logic is difficult to test in isolation and cannot be easily reused by other interfaces (e.g., CLI tools or other API versions).
Recommendation: Extract business logic and external service interactions into a separate Service layer.

### [HIGH] Global Mutable State
File: database.py:4, 7
Description: The database connection is stored in a global variable and managed using the 'global' keyword within the get_db function.
Impact: Potential for race conditions in concurrent environments and makes unit testing harder due to shared state.
Recommendation: Implement a proper connection management pattern, such as a singleton or a connection factory that handles lifecycle without global variables.

### [MEDIUM] N+1 Query Pattern
File: models.py:155-177, 187-210
Description: Fetching orders involves a query for the orders, followed by a nested query per order for its items, and another query per item for product details.
Impact: Severe performance degradation as the number of orders and items grows due to excessive database roundtrips.
Recommendation: Use SQL JOINs to fetch orders and their associated items/products in fewer queries.

### [LOW] Magic Numbers / Strings
File: models.py:237-243
Description: Business rules for discounts (e.g., 10000, 5000, 1000 thresholds and 0.1, 0.05 rates) are hardcoded as literals in the report logic.
Impact: Brittle code that is difficult to update when business rules change; lacks clarity on what the numbers represent.
Recommendation: Define these values as named constants (e.g., DISCOUNT_THRESHOLD_GOLD) at the top of the module or in a config file.

### [LOW] Debug / Print Logging in Production Path
File: controllers.py:8, 53, 67, 203; app.py:50
Description: The application uses the print() function for logging errors, creation events, and general flow information.
Impact: Lacks log levels, timestamps, and structured formatting; difficult to monitor or aggregate in a production environment.
Recommendation: Replace all print() calls with a structured logging library like Python's built-in 'logging' module.

================================
Total: 11 findings
================================

---
**Persistido em:** `./reports/audit-project-1.md`

Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]
