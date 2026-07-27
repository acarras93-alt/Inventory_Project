---
applyTo: "**/*.py"
---

# Python implementation instructions

- Write code compatible with Python 3.14.
- Use clear type hints on public functions, methods, and repository contracts.
- Preserve existing public signatures and observable behavior unless the
  programmer authorizes a contract change.
- Keep `Product` free from console, JSON, CSV, filesystem, and repository
  concerns.
- Keep application use cases in `InventoryService` and depend on the
  `ProductRepository` abstraction.
- Keep JSON, CSV, and filesystem behavior in infrastructure adapters.
- Keep input parsing and output formatting in the interface layer.
- Validate data at the responsible boundary; do not duplicate the same business
  rule across layers.
- Do not tighten or relax unresolved numeric rules, including treatment of
  `bool`, `NaN`, or infinity, without an explicit business decision.
- Prefer `pathlib` and explicit UTF-8 encodings for filesystem operations.
- Prefer the standard library for simple requirements.
- Use specific exception types. At infrastructure boundaries, translate
  low-level errors and preserve the original cause with exception chaining.
- Avoid broad `except Exception`, swallowed exceptions, hidden global state, and
  mutation unrelated to the active use case.
- Keep functions focused and extract reusable behavior only when it removes real
  duplication without obscuring the domain flow.
- Run Ruff on changed Python files and report the command and result.
