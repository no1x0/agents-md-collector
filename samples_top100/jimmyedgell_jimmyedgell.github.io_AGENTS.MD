# Agents.md - AI coding agent "rules" / guidelines
*Last updated 2025-10-03*  

> **purpose** – This file is the onboarding manual for every AI agent (Cursor, Cascade, Roo, Copilot, Claude, etc.) and every human who edits this repository, providing essential rules and guidelines.

## SPARC Development Philosophy
Following SPARC principles for structured, quality-driven development:

1. **Simplicity** - Prioritize clear, maintainable solutions; minimize unnecessary complexity
2. **Pattern** - Follow established patterns and architectural designs; propose alternatives only with clear justification
3. **Architecture** - Design modular, maintainable system components with clearly defined integration points
4. **Refinement** - Iteratively optimize code using feedback loops and stakeholder inputs
5. **Completion** - Conduct rigorous testing, finalize documentation, and deploy monitoring strategies

# Non-negotiable golden rules
| #: | AI *may* do                                                            | AI *must NOT* do                                                                    |
|---|------------------------------------------------------------------------|-------------------------------------------------------------------------------------|
| G0 | Always read the repo `README.md` before writing any code; also check for `AGENTS.md` files in specific directories if you are writing code within one.              |  ❌ Write code if you don't have context for a particular feature/decision. |
| G1 | Whenever unsure about something that's related to the project, ask the developer for clarification before making changes.    |  ❌ Write changes or use tools when you are not sure about something project specific, or if you don't have context for a particular feature/decision. |
| G2 | Add/update **`AIDEV-NOTE:` anchor comments** near non-trivial edited code. | ❌ Delete or mangle existing `AIDEV-` comments.                                     |
| G3 | Stay within the current task context. Inform the dev if it'd be better to start afresh.                                  | ❌ Continue work from a prior prompt after "new task" – start a fresh session.      |
| G4 | Use symbolic reasoning to identify root causes and validate architectural decisions. | ❌ Make assumptions without employing critical analysis and pattern recognition.      |
| G5 | Directly modify existing code rather than duplicating or creating temporary versions during refactoring. | ❌ Create multiple versions of the same functionality without consolidation.         |
---


# Architecture - Repo structure
This is a monorepo using an "src layout" for different projects, where each project typically involves data products. The main project code resides in the `projects/` directory. Repo structure can be understood through the following root folders:
- **`projects/`**: Contains distinct projects, typically Python modules and submodules for data products and JavaScript projects for web apps.
    - `projects/utils`: A shared library of common tools for data, evaluations, infrastructure, and models.
- **`individuals/`**: A workspace for team members' experimental scripts and/or ad-hoc analysis. Do not modify code in other individuals' folders unless explicitly requested by the individual.
- **`conf/`**: Contains repository-wide environment variables and service configurations, e.g. for databases. However, project-specific configurations are located in `projects/<project_name>/conf/`.
- **`docs/`**: Documentation (project overview, features, PRDs, architecture, design etc) is written in Quarto (`.qmd` files) and mirrors the `projects/` structure.


# Dev Workflow - Environments
Development happens within specific project folders. You must navigate into a project directory to work on it.

All python projects in the monorepo use `uv` for package and virtual environment management, and so every python project should have its own `pyproject.toml` with dependencies. Therefore when working on a specific project, you should:
1. **Navigate to the project folder**:
    ```bash
    cd projects/recommender
    ```
2. **Create and activate the virtual environment**:
    ```bash
    uv venv
    source .venv/bin/activate
    ```
3. **Install dependencies** (the `-e` flag installs the project in editable mode):
    ```bash
    uv pip install -e ".[dev]"
    ```
All javascript projects use `npm` for package management, and so every javascript project should have its own `package.json` with dependencies.


# Dev Workflow - Testing
Code should be tested as it is built (test driven development, TDD approach).
- Define tests before implementing features or fixes
- Provide comprehensive coverage for critical paths and edge cases
- Ensure a minimum test coverage of 80%
- Use descriptive test names
- Limit failures for faster feedback
- Immediately address any failing tests to maintain high-quality standards
-   Complement automated tests with structured manual verification

When testing:
- **Python Testing**: Python tests are written with `pytest` and are located in `tests/`, mirroring the `src/` directory structure. Run tests from the relevant project working directory:
    ```bash
    pytest --cov=src
    ```
- **JS Testing**: JavaScript tests are written with `jest` and are located in `tests/`, mirroring the `src/` directory structure. Run tests from the relevant project working directory:
    ```bash
    npm test
    ```

# Dev Workflow - Code quality
Code should be linted and formatted according to a common standard, with focus on maintainability:
- **Keep files concise** (under 300 lines) and proactively refactor when necessary
- **Write modular, scalable code** optimized for clarity and maintenance
- **Use symbolic reasoning to systematically identify redundancy** and apply DRY principles

When linting:
- **Python Linting & Formatting**: Use `ruff` for both linting and formatting. Run from the project root:
    ```bash
    # Check for issues
    ruff check src/
    # Format code
    ruff format src/
    ```
- **JS Linting & Formatting**: Use `eslint` for linting and `prettier` for formatting. Run from the project root:
    ```bash
    # Check for issues
    eslint src/
    # Format code
    prettier --write src/
    ```


# Dev Workflow - Naming conventions
Use descriptive, permanent, and standardized naming conventions.

-   directory_names: lowercase-with-dashes                  # e.g. components/auth-wizard
-   variable_names: descriptive_with_underscores            # Use auxiliary verbs for booleans, e.g. is_loading, has_error
-   environment_variable_names: UPPERCASE_WITH_UNDERSCORES  # e.g. DATABASE_URL


# Dev Workflow - Versioning and documentation

This repo involves strict versioning (Semantic Versioning, SemVer: `MAJOR.MINOR.PATCH`) and documentation process. When you add or modify a file, follow these steps:

1. **Update the file's docstring**: Add an entry to the version history table in the header of the file, e.g. for a Python file:

    ```python
    """
    Version | Date       | Author       | Change comment
    --------|------------|--------------|---------------
    0.0.2   | 2025-09-01 | A. Coder     | Refactor function X
    0.0.1   | 2025-02-21 | James Edgell | Initial version
    """
    ```

2. **Increment Python module version**: Only if the change is significant (minor or major), update the `__version__` variable in the corresponding module's `src/<project_name>/<module_name>/__init__.py` file, as well as in the `pyproject.toml` file.

3. **Update repo-level version**: Only if the change is significant, update the version tables in the root `README.md` and `docs/index.qmd`.

4. **Update documentation**: Only if the change is significant, document the repo `README.md` minimally; document in detail as appropriate in the relevant project-specific quarto page `docs/<project_name>/<module_name>.qmd`; and be sure to document as appropriate in the project directory's `AGENTS.md`
    * If a directory's `AGENTS.md` is outdated or incorrect, **update it**
    * If you make significant changes to a directory's structure, patterns, or critical implementation details, **document these in its `AGENTS.md`**
    * If a directory lacks a `AGENTS.md` but contains complex logic or patterns worth documenting for AI/humans, **suggest creating one**


# Dev workflow - Styling and UI/UX guideline specification
- use_tailwind_css: true
- prefer_functional_components: true


# Dev workflow - Python standards specification
Always use Python3.13 unless otherwise specified (use uv).
- run_scripts_with_uv: true                     # Use `uv run` for running scripts instead of `python`
- use_uv_add: true                               # Use `uv add` for installing python libs (do NOT pip install)
- utilise_uv_for_adhoc_dependencies: true       # Begin ad-hoc scripts declaring the dependencies with TOML so that `uv run` will install dependencies when script is run
- docstrings: NumPy                             # Include NumPy-style docstrings for all functions, classes, and modules
- use_type_hints: true                          # Include hints for function parameters and return values, not for variables
- prefer_f-strings: true                        # Format strings with f-strings where possible
- prefer_loguru: true                           # Use logging instead of print statements with loguru where possible
- destructure_imports: true                     # e.g. import {foo} from bar
 

# Dev workflow - Python tools/packages/libraries specification
The following are preferred libraries for different tasks:
- data_processing:
    - pandas
    - numpy
- data_validation:
    - pydantic
- database:
    - sqlalchemy
- gen_ai:
    - inspect-ai  # Log traces of LLM calls with InspectAI
- machine_learning:
    - scikit-learn
    - pytorch
    - mlflow  # Log experiments with MLflow
- static_visualisation:
    - seaborn
- interactive_visualisation:
    - plotly
    - dash
- command_line:
    - subprocess
    - pathlib
- documentation:
    - quarto
- web_apps:
    - flask


# Dev Workflow - Notebook guidelines specification
When working with Jupyter notebooks:
-   Add numbered markdown cells to explain the steps between code blocks.
-   Modularise functions where possible, importing them into the notebook from python files in `projects/utils` or `projects/<project_name>/` as appropriate.
-   Any SQL should be read in from a standalone .sql file(s).


# Dev Workflow - SQL guidelines specification
When querying databases: 
-   Keep SQL statements in a standalone .sql file(s) (i.e. they would still be executable in e.g. SQL Server) and read the file(s) from e.g. .ipynb notebooks or .py jobs
-   Multiple SQL statements can be contained within a single .sql file, separated by a semi-colon (as is the case for SQL Server)


# Dev Workflow - Debugging & Troubleshooting
- **Root Cause Resolution**: Employ symbolic reasoning to identify underlying causes of issues
- **Targeted Logging**: Integrate precise logging for efficient debugging
- **Research Tools**: Use advanced agentic tools (e.g. Perplexity) to resolve complex issues efficiently


# Dev Workflow - Security Best Practices
- **Server-Side Authority**: Maintain sensitive logic and data processing strictly server-side
- **Input Sanitization**: Enforce rigorous server-side input validation
- **Credential Management**: Securely manage credentials via environment variables; avoid any hardcoding
- **Never expose or log secrets and keys**; never commit secrets or keys to the repository


# Dev Workflow - Refactoring Guidelines
- **Purposeful Changes**: Refactor with clear objectives to improve readability, reduce redundancy, and meet architecture guidelines
- **Holistic Approach**: Consolidate similar components through symbolic analysis
- **Direct Modification**: Directly modify existing code rather than duplicating or creating temporary versions
- **Integration Verification**: Verify and validate all integrations after changes

# AI-collab Workflow - Anchor comments
Add specially formatted comments throughout the codebase, where appropriate, for yourself as inline knowledge that can be easily `grep`ped for.

Use `AIDEV-NOTE:`, `AIDEV-TODO:`, or `AIDEV-QUESTION:` (all-caps prefix) for comments aimed at AI and developers.
- Keep them concise (≤ 120 chars).
- **Important:** Before scanning files, always first try to **locate existing anchors** `AIDEV-*` in relevant subdirectories.
- **Update relevant anchors** when modifying associated code.
- **Do not remove `AIDEV-NOTE`s** without explicit human instruction.
- Make sure to add relevant anchor comments, whenever a file or piece of code is:
    * too long, or
    * too complex, or
    * very important, or
    * confusing, or
    * could have a bug unrelated to the task you are currently working on.
- Anchor comment example:
    ```python
    # AIDEV-NOTE: perf-hot-path; avoid extra allocations (see ADR-24)
    async def render_feed(...):
        ...
    ```


# AI-collab Workflow - Memory Bank & Context Management
- **Persistent Context**: Continuously retain relevant context across development stages for coherent long-term planning
- **Reference Prior Decisions**: Regularly review past decisions stored in memory to maintain consistency and reduce redundancy
- **Adaptive Learning**: Utilize historical data and previous solutions to adaptively refine new implementations


# AI-collab Workflow - Collaboration Standards
- **Clear Instructions**: Provide explicit directives with defined outcomes, constraints, and contextual information
- **Incremental Progress**: Break complex tasks into incremental, reviewable sub-steps
- **Focused Interaction**: Assign specific, clearly defined tasks to AI agents to maintain clarity
- **Leverage Agent Strengths**: Utilize AI for refactoring, symbolic reasoning, adaptive optimization, and test generation; human oversight remains on core logic and strategic architecture
- **Context Referencing**: Regularly reference previous stages and decisions
- **Standard Check-in**: Example: "Confirming understanding: Reviewed [context], goal is [goal], proceeding with [step]."
- **Critical Evaluation**: Thoroughly review all agentic outputs for accuracy and logical coherence