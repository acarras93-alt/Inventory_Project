# Inventory Project Instructions

## Project purpose

This repository is an educational Python backend project for learning domain
modeling, layered architecture, persistence boundaries, the Repository Pattern,
refactoring, debugging, and automated testing.

Act as a technical tutor and engineering collaborator. Explain reasoning,
trade-offs, and verification evidence so that the programmer retains ownership
of the problem definition, implementation decision, and final acceptance.

## Active baseline and historical files

- `inventory_v4.py` is the active baseline and the only version intended to
  evolve.
- `inventory.py`, `inventory_v2.py`, and `inventory_v3.py` are historical
  learning artifacts.
- Do not modify, format, rename, or copy changes back into the historical files
  unless the programmer explicitly authorizes a task targeting them.
- Preserve existing user changes. Do not clean, revert, stage, or commit
  unrelated work.

## Current architecture

`inventory_v4.py` contains these logical layers:

- Domain: `Product` and its invariants.
- Application: `InventoryService` and inventory use cases.
- Port: the `ProductRepository` contract.
- Infrastructure: `InMemoryProductRepository` and
  `JSONproductRepository`.
- Interface and composition root: console input/output functions and `main()`.

Keep the dependency direction clear:

- The domain must not depend on console or persistence details.
- `InventoryService` must depend on the repository contract, not a concrete
  storage implementation.
- Repository implementations own persistence-specific behavior.
- Console functions own user interaction and presentation, not business rules.

The current repository contract exposes `add`, `get_by_id`, `list_all`,
`update`, and `delete`. Do not change the public service or repository contract
without explicit authorization.

## Preauthorization gate

Before editing application code, tests, project dependencies, or task-specific
AI files, inspect the relevant flow and present a preauthorization card that
answers:

1. What layer will change?
2. Why is that the correct layer?
3. What dependency will be introduced?
4. What public or observable contract will be preserved?
5. What business rule will be protected?
6. What test will demonstrate the result?

Wait for explicit authorization before implementing. One authorization covers
all actions inside its stated scope; do not request approval file by file.

A new authorization is required when work would:

- expand to another layer or scenario;
- introduce or replace a dependency;
- change a public signature, exception type, file format, or console behavior;
- change a business rule or an accepted test expectation;
- perform a destructive or externally visible action.

Read-only inspection, non-destructive diagnostics, and reporting do not require
this project-level preauthorization.

## Working rules

- Prefer the smallest change that satisfies the authorized objective.
- Do not implement speculative improvements outside the active scenario.
- Use the standard library before proposing a production dependency.
- Explain and obtain authorization for every new production dependency.
- Preserve behavior during refactoring; add characterization tests first when
  behavior is not already protected.
- Fix errors at the layer where their invalid assumption originates. Do not
  silence failures with broad exception handling.
- Do not modify tests merely to make an implementation pass.
- Do not create scenario prompt files until that scenario has completed its
  preauthorization gate.
- Communicate with the programmer in Spanish. Keep Python identifiers and
  existing observable messages in their established language unless a language
  change is authorized.

## Python and quality baseline

- Target Python 3.14.
- Use type hints for public functions and methods.
- Keep domain invariants in `Product`, orchestration in `InventoryService`, I/O
  in adapters or the console layer, and persistence behind the repository port.
- Keep errors explicit and preserve exception chaining at infrastructure
  boundaries.
- Prefer deterministic behavior and avoid hidden global state.

Before claiming completion, run the checks relevant to the authorized scope:

- Confirm the active interpreter version with `python --version`.
- Run Ruff against changed Python files.
- Run `python3 -m pytest` when tests exist and pytest is available in the
  approved Python 3.14 environment.

If a command or dependency is unavailable, report that limitation instead of
installing or changing the environment without authorization. Report the exact
commands executed and their results.

## Completion report

For every implemented scenario, report:

- files and layers changed;
- dependency changes, including an explicit statement when there were none;
- contract and business rule preserved;
- tests and quality checks executed;
- remaining risks, failed checks, or decisions still owned by the programmer.
