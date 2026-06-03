---
generated_by: refactor-arch
phase: 2
project_dir: task-manager-api
audit_file: audit-project-3.md
generated_at: 2026-06-02T14:30:00Z
stack: Python + Flask
---

================================
PHASE 1: PROJECT ANALYSIS
================================
Language:      Python
Framework:     Flask 3.0.0
Dependencies:  flask-sqlalchemy, flask-cors, marshmallow, requests, python-dotenv
Domain:        Task Manager API (REST)
Architecture:  Partially organized — Layers (models, routes, services) present but likely violating separation of concerns (logic in routes).
Source files:  10 files analyzed
DB tables:     users, tasks, categories
================================

================================
ARCHITECTURE AUDIT REPORT
================================
Project: task-manager-api
Stack:   Python + Flask
Files:   10 analyzed | ~1500 lines of code

## Summary
CRITICAL: 2 | HIGH: 2 | MEDIUM: 1 | LOW: 2

### [CRITICAL] Hardcoded Credentials
File: app.py:13, services/notification_service.py:9
Description: SECRET_KEY and email password ('senha123') hardcoded in the source code.
Impact: Exposure of sensitive credentials in version control; severe security risk if the repository is compromised.
Recommendation: Move credentials to environment variables and load them via python-dotenv.

### [CRITICAL] Insecure Password Hashing
File: models/user.py:28-34
Description: Application uses MD5 for password hashing, which is obsolete and insecure.
Impact: User passwords can be easily cracked if the database is compromised.
Recommendation: Replace MD5 with a modern, secure hashing algorithm like Argon2 or Bcrypt.

### [HIGH] Sensitive Data Exposure
File: models/user.py:16-26, routes/user_routes.py:15-25
Description: The User model's to_dict() method and several user endpoints return the hashed password in the JSON response.
Impact: Unnecessary exposure of sensitive information (hashed passwords) to API clients.
Recommendation: Remove sensitive fields from model serialization methods and use schemas to control output.

### [HIGH] Business Logic in Controllers / Routes
File: routes/report_routes.py:12-101, routes/task_routes.py:15-54
Description: Controllers/Routes contain heavy business logic for reports, statistics, and data formatting.
Impact: Violates separation of concerns, making the code harder to test, reuse, and maintain.
Recommendation: Move business logic to service classes and use schemas for data formatting.

### [MEDIUM] Missing Input Validation
File: routes/report_routes.py:112-115, routes/task_routes.py:84-110
Description: Incomplete or weak validation of user input for categories and tasks (e.g., no color validation, weak tags check).
Impact: Potential for data corruption or unexpected application behavior with malformed input.
Recommendation: Implement robust input validation using Marshmallow schemas or similar validation layers.

### [LOW] Debug / Print Logging in Production Path
File: routes/task_routes.py:149, routes/user_routes.py:83, services/notification_service.py:21, utils/helpers.py:39
Description: Use of print() statements for logging throughout the application instead of a proper logging framework.
Impact: Poor observability and difficulty in managing logs across different environments.
Recommendation: Replace print() calls with Python's native logging module.

### [LOW] Inconsistent Naming / Response Shape
File: routes/task_routes.py:15-54
Description: Response shapes for tasks are inconsistent, with some fields manually added in routes instead of being part of a standard model serialization.
Impact: Inconsistent API contract makes integration more difficult for clients.
Recommendation: Standardize response shapes using consistent serialization patterns (e.g., schemas).

================================
Total: 7 findings
================================

---
**Persistido em:** `../reports/audit-project-3.md`

Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]
