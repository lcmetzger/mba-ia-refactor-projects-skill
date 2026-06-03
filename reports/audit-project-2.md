---
generated_by: refactor-arch
phase: 2
project_dir: ecommerce-api-legacy
audit_file: audit-project-2.md
generated_at: 2026-06-02T10:00:00Z
stack: JavaScript + Express
---

================================
PHASE 1: PROJECT ANALYSIS
================================
Language:      JavaScript (Node.js)
Framework:     Express ^4.18.2
Dependencies:  express, sqlite3
Domain:        Frankenstein LMS (Learning Management System)
Architecture:  Monolithic - God Object (AppManager.js) with inline SQL and routes.
Source files:  3 files analyzed
DB tables:     users, courses, enrollments, payments, audit_logs
================================

================================
ARCHITECTURE AUDIT REPORT
================================
Project: ecommerce-api-legacy
Stack:   JavaScript + Express
Files:   3 analyzed | ~250 lines of code

## Summary
CRITICAL: 2 | HIGH: 3 | MEDIUM: 2 | LOW: 1

### [CRITICAL] God Class / God File
File: src/AppManager.js:4-162
Description: AppManager class centralizes database setup, route definitions, complex business logic, and raw SQL queries for all application entities.
Impact: Extremely high coupling making it difficult to maintain, test, or extend. Violates the Single Responsibility Principle.
Recommendation: Decompose AppManager into distinct layers: Routes (Views), Controllers, Models, and Services (Business Logic).

### [CRITICAL] Hardcoded Secrets / Credentials
File: src/utils.js:1-7
Description: Sensitive credentials including database passwords and payment gateway API keys are stored as plain text constants.
Impact: Severe security vulnerability; keys can be exposed via source control, leading to unauthorized system access.
Recommendation: Move all sensitive configuration to environment variables (.env) and load them using a configuration manager.

### [HIGH] Business Logic in Controllers / Routes
File: src/AppManager.js:42-88, 90-136
Description: Complex logic for checkout processing, payment validation, and financial report generation is implemented directly inside Express route handlers.
Impact: Business rules are not reusable, difficult to unit test independently of the HTTP layer, and bloating the controller logic.
Recommendation: Extract business logic into dedicated Service classes (e.g., CheckoutService, ReportService).

### [HIGH] Missing Authentication on Sensitive Routes
File: src/AppManager.js:90, 154
Description: Administrative and destructive endpoints (/api/admin/financial-report and DELETE /api/users/:id) lack any form of authentication or authorization.
Impact: Unauthorized users can access sensitive financial data or delete user records, compromising data privacy and integrity.
Recommendation: Implement and apply authentication/authorization middleware to all sensitive and administrative routes.

### [HIGH] Global Mutable State
File: src/utils.js:9-10
Description: globalCache and totalRevenue are defined as global objects and updated across different modules without encapsulation.
Impact: Risk of race conditions in concurrent requests and difficulty in tracking state changes or ensuring consistency.
Recommendation: Use a proper caching service/module and move state management to the database or a controlled state container.

### [MEDIUM] N+1 Query Pattern
File: src/AppManager.js:90-136
Description: The financial report endpoint executes multiple individual SQL queries inside loops (courses -> enrollments -> users/payments).
Impact: Significant performance degradation as the database grows due to excessive round-trips.
Recommendation: Refactor logic to use SQL JOINs to fetch all required data in a single or minimal set of queries.

### [MEDIUM] Missing Input Validation
File: src/AppManager.js:48
Description: The checkout endpoint performs only basic presence checks for required fields without validating formats (email, card number, etc.).
Impact: Potential for malformed data to enter the database, leading to runtime errors or inconsistent application state.
Recommendation: Use a validation library (like Joi or Zod) to enforce strict schema validation for all incoming request bodies.

### [LOW] Debug / Print Logging in Production Path
File: src/AppManager.js:63, src/utils.js:13
Description: Use of console.log for tracking execution flow and logging sensitive info (partial card numbers, gateway keys).
Impact: Information leakage in production logs and unnecessary performance overhead.
Recommendation: Replace console.log with a structured logging library (e.g., Winston or Pino) and ensure sensitive data is masked.

================================
Total: 8 findings
================================

---
**Persistido em:** `reports/audit-project-2.md`

Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]
