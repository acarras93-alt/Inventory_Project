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

## GitHub Copilot scenario launch protocol

When creating, documenting, or explaining how to run any reusable scenario
prompt under `.github/prompts/`, always include the complete launch protocol
below. Do not assume that the prompt file alone supplies enough context or that
its presence causes it to run automatically.

1. Define the scenario checkpoint before launch. Record the expected branch,
   clean-worktree state, and latest baseline commit in the scenario-specific
   launch card. Never reuse branch names or commit hashes from an older
   scenario.
2. In the VS Code terminal, require the programmer to run:

   ```text
   git branch --show-current
   git status --short
   git log -1 --oneline
   ```

3. Compare all three results with the scenario checkpoint. Stop if the branch
   or commit differs, or if any local change has not been identified.
4. Start a new Copilot Chat session and select the built-in `Plan` agent, not
   `Agent`, for analysis and preauthorization. If `Plan` is unavailable, stop
   and report the limitation instead of falling back silently.
5. Through **Add Context**, attach explicitly:

   - `AGENTS.md`;
   - `.github/copilot-instructions.md`;
   - the active `.github/prompts/<scenario>.prompt.md`;
   - every path-specific `.instructions.md` file relevant to the files that a
     later implementation could modify, including Python and test instructions
     when those files are in the proposed scope;
   - the production, test, configuration, and documentation files needed to
     analyze the active scenario.

   Attach path-specific instructions during the analysis phase even when their
   `applyTo` patterns would only activate after a Python or test file becomes
   the current editing context.
6. Invoke the prompt manually with its slash command and add a launch message
   that limits the run to Phase 1. The message must require the agent to:

   - confirm it read every attached instruction and scenario file;
   - summarize one binding rule from each attached file;
   - recheck the branch, worktree, and baseline commit;
   - use read-only tools exclusively;
   - create, edit, format, move, or delete no files;
   - deliver the six-answer preauthorization card and every analysis artifact
     required by the scenario;
   - finish by waiting for explicit implementation authorization.

   Use this copy-pasteable launcher as the default template, replacing the
   placeholders and expanding the required deliverables for the active
   scenario:

   ```text
   /<nombre-del-escenario>

   Ejecuta únicamente la Fase 1 de análisis y preautorización.

   Antes del análisis:

   1. Confirma que has leído todos los archivos adjuntos, AGENTS.md y el prompt
      del escenario.
   2. Resume una regla vinculante de cada archivo.
   3. Verifica la rama, el estado de Git y el commit base indicados en la
      tarjeta de lanzamiento.
   4. Trabaja exclusivamente con herramientas de lectura.
   5. No crees, edites, formatees, muevas ni elimines archivos.

   Entrega la tarjeta con las seis respuestas y todos los artefactos de análisis
   exigidos por el prompt activo.

   No implementes nada. Finaliza esperando mi autorización explícita para la
   siguiente fase.
   ```

7. Switch from `Plan` to `Agent` only after the programmer has reviewed the
   Phase 1 result and explicitly authorized the matching implementation scope.

Whenever you provide a programmer-facing workflow for a scenario prompt,
include the exact expected checkpoint values, the explicit **Add Context** file
list, the `Plan` selection, and a copy-pasteable Phase 1 launch message. Do not
shorten these controls to a generic instruction such as “run the prompt.”

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
