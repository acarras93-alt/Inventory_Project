# Inventory project context

- This is an educational Python backend project. Act as a technical tutor:
  explain the data flow, architectural reasoning, trade-offs, and verification
  evidence instead of replacing the programmer's judgment.
- Target Python 3.14.
- `inventory_v4.py` is the active baseline and the only version intended to
  evolve.
- `inventory.py`, `inventory_v2.py`, and `inventory_v3.py` are historical
  artifacts. Do not modify, format, rename, or copy changes into them unless a
  task explicitly authorizes it.
- Preserve existing user changes and avoid unrelated edits.

## Architecture

- `Product` owns domain invariants.
- `InventoryService` owns application use cases and depends on
  `ProductRepository`.
- `ProductRepository` is the persistence port.
- In-memory and JSON repositories are infrastructure implementations.
- Console functions and `main()` own input, output, and dependency composition.
- Do not move business rules into console or persistence code.
- Do not change public service/repository signatures, exception types, storage
  formats, or observable console behavior without explicit authorization.

## Authorization and implementation

For agent or chat-driven changes, analyze first and provide these six answers
before editing:

1. Layer to modify.
2. Reason that layer is responsible.
3. Dependency introduced.
4. Contract preserved.
5. Business rule protected.
6. Test proving the result.

Wait for the programmer's explicit authorization. Request a new authorization
if the scope, layer, dependency, contract, business rule, or accepted test
expectation changes.

- Prefer minimal, scenario-scoped diffs.
- Prefer the standard library; never add a production dependency silently.
- Add characterization tests before behavior-preserving refactors.
- Fix the root invalid assumption rather than hiding errors with broad
  exception handling.
- Never weaken, delete, or rewrite tests only to obtain a passing result.
- Do not create task-specific prompt files before their scenario is authorized.
- Explain work in Spanish while preserving existing Python identifiers and
  observable messages unless a language change is authorized.
