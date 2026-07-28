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

## Mandatory scenario launch gate

Reusable files in `.github/prompts/` are invoked manually. Before analyzing or
implementing a scenario prompt:

1. Work from a new Copilot Chat session with the built-in `Plan` agent selected.
   Do not use `Agent` for the initial analysis. If `Plan` is unavailable, stop
   and report that limitation.
2. Require a scenario-specific launch card that states the expected branch,
   clean-worktree state, and latest baseline commit. Never infer these values
   from another scenario.
3. Verify all three values with:

   ```text
   git branch --show-current
   git status --short
   git log -1 --oneline
   ```

   Stop if the branch or commit differs, or if any local change has not been
   identified.
4. Confirm that **Add Context** explicitly includes:

   - `AGENTS.md`;
   - `.github/copilot-instructions.md`;
   - the active scenario prompt;
   - all path-specific instruction files relevant to the possible
     implementation scope;
   - the production, test, configuration, and documentation files needed for
     the scenario analysis.

   Python and test instructions must be attached during Phase 1 when a later
   phase could change Python or test files, even though their `applyTo` patterns
   are conditional.
5. After the slash command is invoked, execute only the scenario's Phase 1:

   - read every attached file and summarize one binding rule from each;
   - use read-only tools exclusively;
   - do not create, edit, format, move, or delete files;
   - deliver the six-answer preauthorization card and all additional analysis
     artifacts required by the active scenario;
   - finish by waiting for the programmer's explicit implementation
     authorization.

Do not start implementation or switch to `Agent` until the programmer approves
the Phase 1 result and its exact scope. When explaining how to launch a scenario
prompt, always provide the exact checkpoint values, explicit context list, and
a copy-pasteable Phase 1 launch message; “run the prompt” is not sufficient.

- Prefer minimal, scenario-scoped diffs.
- Prefer the standard library; never add a production dependency silently.
- Add characterization tests before behavior-preserving refactors.
- Fix the root invalid assumption rather than hiding errors with broad
  exception handling.
- Never weaken, delete, or rewrite tests only to obtain a passing result.
- Do not create task-specific prompt files before their scenario is authorized.
- Explain work in Spanish while preserving existing Python identifiers and
  observable messages unless a language change is authorized.
