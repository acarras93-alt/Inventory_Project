---
applyTo: "**/tests/**/*.py,**/test_*.py,**/*_test.py"
---

# Pytest instructions

- Use `pytest` and write deterministic tests with descriptive behavior-focused
  names.
- Cover normal cases, boundary cases, and error/exception behavior required by
  the authorized scenario.
- Test public behavior and contracts rather than private implementation details.
- Separate domain, service, repository-contract, infrastructure, and interface
  tests when those layers are in scope.
- Test `InventoryService` with `InMemoryProductRepository` unless persistence
  behavior is the subject under test.
- Use `tmp_path` for JSON or CSV tests. Never read or overwrite the real
  `inventory_data.json`.
- Use `monkeypatch` and `capsys` for console behavior instead of interactive
  input or global side effects.
- Parameterize shared repository-contract tests when both in-memory and JSON
  implementations must satisfy the same behavior.
- Assert relevant exception types and stable contract details; avoid coupling
  tests to incidental implementation structure.
- Do not skip, mark `xfail`, weaken assertions, or change expected values merely
  to obtain a green suite.
- In a testing-only scenario, report defects exposed by tests and do not edit
  production code without a separate authorization.
- Run the smallest relevant test selection first, then the complete suite.
  Report exact commands, passed/failed counts, and any unexecuted checks.
