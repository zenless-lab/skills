# Ruff Settings Reference

This file consolidates every Ruff configuration key covered by the skill into a single reference.

Use it when you need to:

* look up the exact meaning of a Ruff setting
* decide whether a key belongs at top level, under `format`, under `lint`, or under `analyze`
* compare defaults before changing project behavior
* translate command-line or documentation terminology into `pyproject.toml` layout

For direct CLI lookup, Ruff can also describe settings interactively:

* `ruff config`
* `ruff config <key>`

## Default Configuration and Discovery

When a repository does not override Ruff, its baseline behavior is equivalent to the following shape:

```toml
[tool.ruff]
exclude = [
	".bzr",
	".direnv",
	".eggs",
	".git",
	".git-rewrite",
	".hg",
	".ipynb_checkpoints",
	".mypy_cache",
	".nox",
	".pants.d",
	".pyenv",
	".pytest_cache",
	".pytype",
	".ruff_cache",
	".svn",
	".tox",
	".venv",
	".vscode",
	"__pypackages__",
	"_build",
	"buck-out",
	"build",
	"dist",
	"node_modules",
	"site-packages",
	"venv",
]
line-length = 88
indent-width = 4
target-version = "py310"

[tool.ruff.lint]
select = ["E4", "E7", "E9", "F"]
ignore = []
fixable = ["ALL"]
unfixable = []
dummy-variable-rgx = "^(_+|(_+[a-zA-Z0-9_]*[a-zA-Z0-9]+?))$"

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
skip-magic-trailing-comma = false
line-ending = "auto"
docstring-code-format = false
docstring-code-line-length = "dynamic"
```

Discovery rules that matter during debugging:

* Ruff uses the closest matching config file for each analyzed file.
* A `pyproject.toml` without `[tool.ruff]` is ignored during config discovery.
* `.ruff.toml` takes precedence over `ruff.toml`, and `ruff.toml` takes precedence over `pyproject.toml` in the same directory.
* Ruff does not implicitly merge parent configs; use `extend` for inheritance.
* If `--config` points to a file, relative paths inside that config are resolved from the current working directory.
* If `target-version` is omitted, Ruff may infer it from `requires-python` in a nearby `pyproject.toml`.

Default file discovery rules:

* Ruff discovers `*.py`, `*.pyi`, `*.ipynb`, and `pyproject.toml` by default.
* In preview mode, Ruff also discovers `*.pyw` by default.
* Notebook linting and formatting are enabled by default on Ruff `0.6.0+`.
* `include` patterns must match files, not directories.

## 1. Top-level Settings

These settings apply across Ruff commands unless a more specific section overrides them.

#### `builtins`
- **Description**: Extra builtins to treat as defined references.
- **Default**: `[]`
- **Type**: `list[str]`
- **Example**: `builtins = ["_"]`

#### `cache-dir`
- **Description**: Path to the cache directory. Respects `RUFF_CACHE_DIR` env var.
- **Default**: `.ruff_cache`
- **Type**: `str`
- **Example**: `cache-dir = "~/.cache/ruff"`

#### `exclude`
- **Description**: File patterns to exclude from formatting and linting.
- **Default**: `[".bzr", ".direnv", ".eggs", ".git", ".git-rewrite", ".hg", ".ipynb_checkpoints", ".mypy_cache", ".nox", ".pants.d", ".pyenv", ".pytest_cache", ".pytype", ".ruff_cache", ".svn", ".tox", ".venv", ".vscode", "__pypackages__", "_build", "buck-out", "build", "dist", "node_modules", "site-packages", "venv"]`
- **Type**: `list[str]`
- **Example**: `exclude = [".venv"]`

#### `extend`
- **Description**: Path to a local configuration file to merge into this one.
- **Default**: `null`
- **Type**: `str`
- **Example**: `extend = "../pyproject.toml"`

#### `extend-exclude`
- **Description**: Patterns to omit in addition to `exclude`.
- **Default**: `[]`
- **Type**: `list[str]`
- **Example**: `extend-exclude = ["tests", "src/bad.py"]`

#### `extend-include`
- **Description**: Patterns to include in addition to `include`.
- **Default**: `[]`
- **Type**: `list[str]`
- **Example**: `extend-include = ["*.pyw"]`

#### `extension`
- **Description**: Mapping of custom extensions to known file types.
- **Default**: `{}`
- **Type**: `dict[str, Language]`
- **Example**: `extension = {rpy = "python"}`

#### `fix`
- **Description**: Enable fix behavior by default.
- **Default**: `false`
- **Type**: `bool`
- **Example**: `fix = true`

#### `fix-only`
- **Description**: Like `fix`, but disables reporting on leftover violations.
- **Default**: `false`
- **Type**: `bool`
- **Example**: `fix-only = true`

#### `force-exclude`
- **Description**: Respect exclusions even for paths passed explicitly to Ruff.
- **Default**: `false`
- **Type**: `bool`
- **Example**: `force-exclude = true`

#### `include`
- **Description**: Patterns to include during Ruff file discovery.
- **Default**: `["*.py", "*.pyi", "*.ipynb", "pyproject.toml"]`
- **Type**: `list[str]`
- **Example**: `include = ["*.py"]`

#### `indent-width`
- **Description**: Number of spaces per indentation level.
- **Default**: `4`
- **Type**: `int`
- **Example**: `indent-width = 2`

#### `line-length`
- **Description**: The line length at which Ruff prefers to wrap.
- **Default**: `88`
- **Type**: `int`
- **Example**: `line-length = 120`

#### `namespace-packages`
- **Description**: Mark directories as namespace packages, as if they had `__init__.py`.
- **Default**: `[]`
- **Type**: `list[str]`
- **Example**: `namespace-packages = ["airflow/providers"]`

#### `output-format`
- **Description**: Style in which violation messages are formatted.
- **Default**: `"full"`
- **Type**: `"concise" | "full" | "json" | "json-lines" | "junit" | "grouped" | "github" | "gitlab" | "pylint" | "rdjson" | "azure" | "sarif"`
- **Example**: `output-format = "grouped"`

#### `per-file-target-version`
- **Description**: Mapping from file patterns to Python versions.
- **Default**: `{}`
- **Type**: `dict[str, PythonVersion]`
- **Example**: `[tool.ruff.per-file-target-version]` then `"scripts/*.py" = "py312"`

#### `preview`
- **Description**: Enable preview mode for unstable rules and formatting.
- **Default**: `false`
- **Type**: `bool`
- **Example**: `preview = true`

#### `required-version`
- **Description**: Enforce a requirement on the Ruff version.
- **Default**: `null`
- **Type**: `str`
- **Example**: `required-version = ">=0.0.193"`

#### `respect-gitignore`
- **Description**: Exclude files ignored by `.gitignore` and related files.
- **Default**: `true`
- **Type**: `bool`
- **Example**: `respect-gitignore = false`

#### `show-fixes`
- **Description**: Show enumeration of all fixed violations.
- **Default**: `false`
- **Type**: `bool`
- **Example**: `show-fixes = true`

#### `src`
- **Description**: Directories to consider for first- vs. third-party import resolution.
- **Default**: `[".", "src"]`
- **Type**: `list[str]`
- **Example**: `src = ["src", "test"]`

#### `target-version`
- **Description**: Minimum Python version to target.
- **Default**: `"py310"`
- **Type**: `"py37" | "py38" | "py39" | "py310" | "py311" | "py312" | "py313" | "py314" | "py315"`
- **Example**: `target-version = "py37"`

#### `unsafe-fixes`
- **Description**: Enable application of unsafe fixes.
- **Default**: `null`
- **Type**: `bool`
- **Example**: `unsafe-fixes = true`

## 2. Analyze Settings (`[tool.ruff.analyze]`)

Use these with Ruff's analysis command when you need dependency and import-graph insight.

#### `detect-string-imports`
- **Description**: Detect imports from string literals.
- **Default**: `false`
- **Type**: `bool`
- **Example**: `detect-string-imports = true`

#### `direction`
- **Description**: Generate a dependency map or a dependents map.
- **Default**: `"dependencies"`
- **Type**: `"dependents" | "dependencies"`
- **Example**: `direction = "dependencies"`

#### `exclude`
- **Description**: Patterns to exclude from analysis in addition to global excludes.
- **Default**: `[]`
- **Type**: `list[str]`
- **Example**: `exclude = ["generated"]`

#### `include-dependencies`
- **Description**: Manual mapping of file paths to dependencies.
- **Default**: `{}`
- **Type**: `dict[str, list[str]]`
- **Example**: `[tool.ruff.analyze.include-dependencies]` then `"foo/bar.py" = ["foo/baz/*.py"]`

#### `preview`
- **Description**: Enable preview mode for the `analyze` command.
- **Default**: `false`
- **Type**: `bool`
- **Example**: `preview = true`

#### `string-imports-min-dots`
- **Description**: Minimum number of dots in a string to consider it a valid import.
- **Default**: `2`
- **Type**: `usize`
- **Example**: `string-imports-min-dots = 2`

#### `type-checking-imports`
- **Description**: Include imports used only for type checking.
- **Default**: `true`
- **Type**: `bool`
- **Example**: `type-checking-imports = false`

## 3. Format Settings (`[tool.ruff.format]`)

Use these when Ruff formats Python code, notebooks, or docstring code examples.

#### `docstring-code-format`
- **Description**: Format Python code snippets inside docstrings.
- **Default**: `false`
- **Type**: `bool`
- **Example**: `docstring-code-format = true`

#### `docstring-code-line-length`
- **Description**: Line length for docstring snippets.
- **Default**: `"dynamic"`
- **Type**: `int | "dynamic"`
- **Example**: `docstring-code-line-length = 60`

#### `exclude`
- **Description**: Patterns to exclude from formatting in addition to global excludes.
- **Default**: `[]`
- **Type**: `list[str]`
- **Example**: `exclude = ["generated"]`

#### `indent-style`
- **Description**: Use spaces or tabs for indentation.
- **Default**: `"space"`
- **Type**: `"space" | "tab"`
- **Example**: `indent-style = "tab"`

#### `line-ending`
- **Description**: Character to use at the end of a line.
- **Default**: `"auto"`
- **Type**: `"auto" | "lf" | "cr-lf" | "native"`
- **Example**: `line-ending = "lf"`

#### `preview`
- **Description**: Enable unstable preview style formatting.
- **Default**: `false`
- **Type**: `bool`
- **Example**: `preview = true`

#### `quote-style`
- **Description**: Preferred quote character for strings.
- **Default**: `"double"`
- **Type**: `"double" | "single" | "preserve"`
- **Example**: `quote-style = "single"`

#### `skip-magic-trailing-comma`
- **Description**: If true, ignore magic trailing commas as line-break hints.
- **Default**: `false`
- **Type**: `bool`
- **Example**: `skip-magic-trailing-comma = true`

## 4. Lint Core Settings (`[tool.ruff.lint]`)

Use these when shaping rule selection, fix policy, per-file exceptions, or preview behavior.

#### `allowed-confusables`
- **Description**: Allowed confusable Unicode characters.
- **Default**: `[]`
- **Type**: `list[str]`
- **Example**: `allowed-confusables = ["−", "ρ", "∗"]`

#### `dummy-variable-rgx`
- **Description**: Regex used to identify dummy variables such as `_`.
- **Default**: `"^(_+|(_+[a-zA-Z0-9_]*[a-zA-Z0-9]+?))$"`
- **Type**: `str`
- **Example**: `dummy-variable-rgx = "^_$"`

#### `exclude`
- **Description**: Patterns to exclude from linting in addition to global excludes.
- **Default**: `[]`
- **Type**: `list[str]`
- **Example**: `exclude = ["generated"]`

#### `explicit-preview-rules`
- **Description**: Require exact codes, rather than prefixes, to select preview rules.
- **Default**: `false`
- **Type**: `bool`
- **Example**: `explicit-preview-rules = true`

#### `extend-fixable`
- **Description**: Extra rule codes to consider fixable.
- **Default**: `[]`
- **Type**: `list[RuleSelector]`
- **Example**: `extend-fixable = ["B"]`

#### `extend-ignore` (Deprecated)
- **Description**: Deprecated. Use `ignore` instead.

#### `extend-per-file-ignores`
- **Description**: Extra per-file ignores.
- **Default**: `{}`
- **Type**: `dict[str, list[RuleSelector]]`
- **Example**: `extend-per-file-ignores = {"__init__.py" = ["E402"]}`

#### `extend-safe-fixes`
- **Description**: Rules for which unsafe fixes should be considered safe.
- **Default**: `[]`
- **Type**: `list[RuleSelector]`
- **Example**: `extend-safe-fixes = ["E", "F401"]`

#### `extend-select`
- **Description**: Extra rules to enable on top of `select`.
- **Default**: `[]`
- **Type**: `list[RuleSelector]`
- **Example**: `extend-select = ["B", "Q"]`

#### `extend-unsafe-fixes`
- **Description**: Rules for which safe fixes should be considered unsafe.
- **Default**: `[]`
- **Type**: `list[RuleSelector]`
- **Example**: `extend-unsafe-fixes = ["E", "F401"]`

#### `external`
- **Description**: Rule codes unsupported by Ruff to preserve in `# noqa`.
- **Default**: `[]`
- **Type**: `list[str]`
- **Example**: `external = ["V"]`

#### `fixable`
- **Description**: Rule codes allowed to be fixed.
- **Default**: `["ALL"]`
- **Type**: `list[RuleSelector]`
- **Example**: `fixable = ["E", "F"]`

#### `future-annotations`
- **Description**: Allow rules to add `from __future__ import annotations`.
- **Default**: `false`
- **Type**: `bool`
- **Example**: `future-annotations = true`

#### `ignore`
- **Description**: Rule codes or prefixes to ignore.
- **Default**: `[]`
- **Type**: `list[RuleSelector]`
- **Example**: `ignore = ["F841"]`

#### `ignore-init-module-imports` (Deprecated)
- **Description**: Deprecated. Use preview mode `F401` recommendations instead.

#### `logger-objects`
- **Description**: Objects to treat as `logging.Logger`.
- **Default**: `[]`
- **Type**: `list[str]`
- **Example**: `logger-objects = ["logging_setup.logger"]`

#### `per-file-ignores`
- **Description**: File patterns mapped to ignored rule selectors.
- **Default**: `{}`
- **Type**: `dict[str, list[RuleSelector]]`
- **Example**: `per-file-ignores = {"__init__.py" = ["E402"]}`

#### `preview`
- **Description**: Enable preview mode for linting rules.
- **Default**: `false`
- **Type**: `bool`
- **Example**: `preview = true`

#### `select`
- **Description**: Rule codes or prefixes to enable.
- **Default**: `["E4", "E7", "E9", "F"]`
- **Type**: `list[RuleSelector]`
- **Example**: `select = ["E4", "E7", "E9", "F", "B", "Q"]`

#### `task-tags`
- **Description**: Task tags to recognize, such as TODO.
- **Default**: `["TODO", "FIXME", "XXX"]`
- **Type**: `list[str]`
- **Example**: `task-tags = ["HACK"]`

#### `typing-extensions`
- **Description**: Allow imports from `typing_extensions`.
- **Default**: `true`
- **Type**: `bool`
- **Example**: `typing-extensions = false`

#### `typing-modules`
- **Description**: Modules treated equivalently to `typing`.
- **Default**: `[]`
- **Type**: `list[str]`
- **Example**: `typing-modules = ["airflow.typing_compat"]`

#### `unfixable`
- **Description**: Rule codes or prefixes to consider non-fixable.
- **Default**: `[]`
- **Type**: `list[RuleSelector]`
- **Example**: `unfixable = ["F401"]`

## 5. Plugin-specific Lint Settings

### `lint.flake8-annotations`
- **`allow-star-arg-any`**: (bool, false) Suppress ANN401 for `*args` and `**kwargs`.
- **`ignore-fully-untyped`**: (bool, false) Suppress ANN rules for fully untyped declarations.
- **`mypy-init-return`**: (bool, false) Allow omission of a return hint for `__init__`.
- **`suppress-dummy-args`**: (bool, false) Suppress ANN000 for dummy args such as `_`.
- **`suppress-none-returning`**: (bool, false) Suppress ANN200 for functions returning `None`.

### `lint.flake8-bandit`
- **`allowed-markup-calls`**: (list[str]) Callables treated as safe for `markupsafe.Markup`.
- **`check-typed-exception`**: (bool, false) Disallow `try-except-pass` for specific exception types.
- **`extend-markup-names`**: (list[str]) Extra names behaving like `markupsafe.Markup`.
- **`hardcoded-tmp-directory`**: (list[str], `["/tmp", "/var/tmp", "/dev/shm"]`) Temporary directories.
- **`hardcoded-tmp-directory-extend`**: (list[str]) Additional temporary directories.

### `lint.flake8-boolean-trap`
- **`extend-allowed-calls`**: (list[str]) Functions allowed to use boolean-trap signatures.

### `lint.flake8-bugbear`
- **`extend-immutable-calls`**: (list[str]) Functions considered immutable for B008.

### `lint.flake8-builtins`
- **`allowed-modules`**: (list[str]) Builtin module names to allow.
- **`ignorelist`**: (list[str]) Ignore list of builtin names.
- **`strict-checking`**: (bool, false) Compare module names instead of paths.
- **Note**: Deprecated aliases remain recognized: `builtins-allowed-modules`, `builtins-ignorelist`, `builtins-strict-checking`.

### `lint.flake8-comprehensions`
- **`allow-dict-calls-with-keyword-arguments`**: (bool, false) Allow `dict(a=1)` patterns.

### `lint.flake8-copyright`
- **`author`**: (str, null) Required author in the notice.
- **`min-file-size`**: (int, 0) Minimum bytes for enforcement.
- **`notice-rgx`**: (str) Regex used to match the notice.

### `lint.flake8-errmsg`
- **`max-string-length`**: (int, 0) Maximum literal length in exception messages.

### `lint.flake8-gettext`
- **`extend-function-names`**: (list[str]) Additional i18n call names.
- **`function-names`**: (list[str], `["_", "gettext", "ngettext"]`) Recognized i18n call names.

### `lint.flake8-implicit-str-concat`
- **`allow-multiline`**: (bool, true) Allow implicit concatenation for multiline strings.

### `lint.flake8-import-conventions`
- **`aliases`**: (dict) Mapping of conventional aliases, for example `numpy = "np"`.
- **`banned-aliases`**: (dict) Mapping of modules to banned aliases.
- **`banned-from`**: (list[str]) Modules that cannot be used with `from ... import`.
- **`extend-aliases`**: (dict) Extra aliases for conventions.

### `lint.flake8-pytest-style`
- **`fixture-parentheses`**: (bool, false) Force `@pytest.fixture()`.
- **`mark-parentheses`**: (bool, false) Force `@pytest.mark.foo()`.
- **`parametrize-names-type`**: (string, `"tuple"`) `"csv" | "tuple" | "list"`.
- **`parametrize-values-row-type`**: (string, `"tuple"`) `"tuple" | "list"`.
- **`parametrize-values-type`**: (string, `"list"`) `"tuple" | "list"`.
- **`raises-extend-require-match-for`**: (list[str]) Extra exceptions requiring `match=`.
- **`raises-require-match-for`**: (list[str]) Default exceptions requiring `match=`.
- **`warns-extend-require-match-for`**: (list[str]) Extra warnings requiring `match=`.
- **`warns-require-match-for`**: (list[str]) Default warnings requiring `match=`.

### `lint.flake8-quotes`
- **`avoid-escape`**: (bool, true) Switch quote style to avoid escapes.
- **`docstring-quotes`**: (string, `"double"`) `"single" | "double"`.
- **`inline-quotes`**: (string, `"double"`) `"single" | "double"`.
- **`multiline-quotes`**: (string, `"double"`) `"single" | "double"`.

### `lint.flake8-self`
- **`extend-ignore-names`**: (list[str]) Extra private names to ignore.
- **`ignore-names`**: (list[str]) List of private names to ignore.

### `lint.flake8-tidy-imports`
- **`ban-lazy`**: (choice) Forbid lazy imports for specific or all modules.
- **`ban-relative-imports`**: (choice, `"parents"`) `"parents" | "all"`.
- **`banned-api`**: (dict) Banned modules or members with custom messages.
- **`banned-module-level-imports`**: (list[str]) Modules that must be imported lazily.
- **`require-lazy`**: (choice) Force lazy imports for specific or all modules. Python 3.15+ only.

### `lint.flake8-type-checking`
- **`exempt-modules`**: (list[str], `["typing"]`) Modules excluded from type-checking blocks.
- **`quote-annotations`**: (bool, false) Add quotes to move annotations into type-checking blocks.
- **`runtime-evaluated-base-classes`**: (list[str]) Base classes that must remain available at runtime.
- **`runtime-evaluated-decorators`**: (list[str]) Decorators that must remain available at runtime.
- **`strict`**: (bool, false) Enforce type-checking blocks even if runtime imports exist.

### `lint.flake8-unused-arguments`
- **`ignore-variadic-names`**: (bool, false) Allow unused `*args` and `**kwargs`.

### `lint.isort`
- **`case-sensitive`**: (bool, false) Use case-sensitive sorting.
- **`classes`**: (list[str]) Tokens treated as classes.
- **`combine-as-imports`**: (bool, false) Combine `as` imports on one line.
- **`constants`**: (list[str]) Tokens treated as constants.
- **`default-section`**: (str, `"third-party"`) Default section for unknown imports.
- **`detect-same-package`**: (bool, true) Mark same-package imports as first-party.
- **`extra-standard-library`**: (list[str]) Extra stdlib modules.
- **`force-single-line`**: (bool, false) One `from` import per line.
- **`force-sort-within-sections`**: (bool, false) Ignore import style when sorting.
- **`force-to-top`**: (list[str]) Force specific imports to a section top.
- **`force-wrap-aliases`**: (bool, false) One aliased member per line. Requires `combine-as-imports`.
- **`forced-separate`**: (list[str]) Modules placed in auxiliary blocks.
- **`from-first`**: (bool, false) Place `from` imports before straight imports.
- **`import-heading`**: (dict) Custom headings for sections.
- **`known-first-party`**: (list[str]) Modules treated as first-party.
- **`known-local-folder`**: (list[str]) Modules treated as local-folder.
- **`known-third-party`**: (list[str]) Modules treated as third-party.
- **`length-sort`**: (bool, false) Sort by string length.
- **`length-sort-straight`**: (bool, false) Sort straight imports by length.
- **`lines-after-imports`**: (int, -1) Blank lines after imports.
- **`lines-between-types`**: (int, 0) Lines between direct and `from` imports.
- **`no-lines-before`**: (list[str]) Sections with no preceding blank line.
- **`no-sections`**: (bool, false) Merge all imports into one block.
- **`order-by-type`**: (bool, true) Order by type then alphabetically.
- **`relative-imports-order`**: (choice, `"furthest-to-closest"`) `"furthest-to-closest" | "closest-to-furthest"`.
- **`required-imports`**: (list[str]) Imports added to every file.
- **`section-order`**: (list[str]) Vertical order of import groups.
- **`sections`**: (dict) Custom import section mapping.
- **`single-line-exclusions`**: (list[str]) Modules excluded from the single-line rule.
- **`split-on-trailing-comma`**: (bool, true) Prevent folding when a trailing comma exists.
- **`variables`**: (list[str]) Tokens treated as variables.

### `lint.mccabe`
- **`max-complexity`**: (int, 10) Threshold for C901.

### `lint.pep8-naming`
- **`classmethod-decorators`**: (list[str]) Extra classmethod decorators.
- **`extend-ignore-names`**: (list[str]) Extra names to ignore.
- **`ignore-names`**: (list[str]) Standard names to ignore.
- **`staticmethod-decorators`**: (list[str]) Extra staticmethod decorators.

### `lint.pycodestyle`
- **`ignore-overlong-task-comments`**: (bool, false) Skip E501 for task comments.
- **`max-doc-length`**: (int, null) Maximum line length for docs, for W505.
- **`max-line-length`**: (int, null) Maximum line length for E501.

### `lint.pydoclint`
- **`ignore-one-line-docstrings`**: (bool, false) Skip checking short docstrings.

### `lint.pydocstyle`
- **`convention`**: (choice, null) `"google" | "numpy" | "pep257"`.
- **`ignore-decorators`**: (list[str]) Decorators to ignore for docstrings.
- **`ignore-var-parameters`**: (bool, false) Skip missing documentation for variadic args.
- **`property-decorators`**: (list[str]) Extra property decorators.

### `lint.pyflakes`
- **`allowed-unused-imports`**: (list[str]) Modules ignored for unused-import checks.
- **`extend-generics`**: (list[str]) Extra generic classes for subscript checks.

### `lint.pylint`
- **`allow-dunder-method-names`**: (list[str]) Extra dunder names to allow.
- **`allow-magic-value-types`**: (list[str], `["str", "bytes"]`) Types allowed for magic-value checks.
- **`max-args`**: (int, 5) Maximum arguments for PLR0913.
- **`max-bool-expr`**: (int, 5) Maximum boolean expressions for PLR0916.
- **`max-branches`**: (int, 12) Maximum branches for PLR0912.
- **`max-locals`**: (int, 15) Maximum locals for PLR0914.
- **`max-nested-blocks`**: (int, 5) Maximum nesting for PLR1702.
- **`max-positional-args`**: (int, 5) Maximum positional args for PLR0917.
- **`max-public-methods`**: (int, 20) Maximum public methods for PLR0904.
- **`max-returns`**: (int, 6) Maximum returns for PLR0911.
- **`max-statements`**: (int, 50) Maximum statements for PLR0915.

### `lint.pyupgrade`
- **`keep-runtime-typing`**: (bool, false) Avoid PEP 585 and PEP 604 rewrites for runtime typing usage.

### `lint.ruff`
- **`parenthesize-tuple-in-subscript`**: (bool, false) Force parentheses for tuples in subscripts.
- **`strictly-empty-init-modules`**: (bool, false) Require `__init__.py` modules to be code-free.
- **Note**: Deprecated items remain documented under this plugin family, including `allowed-markup-calls` and `extend-markup-names`.

## 6. Copy-paste Examples

### General Project

```toml
[tool.ruff]
line-length = 100
target-version = "py311"
preview = false
respect-gitignore = true
extend-exclude = ["build", "generated"]
src = ["src", "tests"]

[tool.ruff.lint]
select = ["E", "F", "B", "I", "UP"]
ignore = ["E501"]
fixable = ["ALL"]
unfixable = ["F401"]
future-annotations = true
task-tags = ["TODO", "FIXME", "HACK"]

[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["E402"]
"tests/**/*" = ["S"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
line-ending = "lf"
docstring-code-format = true
docstring-code-line-length = 80
skip-magic-trailing-comma = false
exclude = ["generated"]

[tool.ruff.analyze]
direction = "dependencies"
type-checking-imports = true
exclude = ["generated"]
```

### Imports and Style-heavy Project

```toml
[tool.ruff.lint.flake8-builtins]
ignorelist = ["id"]

[tool.ruff.lint.flake8-import-conventions.aliases]
numpy = "np"
pandas = "pd"

[tool.ruff.lint.flake8-quotes]
inline-quotes = "double"
docstring-quotes = "double"
avoid-escape = true

[tool.ruff.lint.flake8-tidy-imports]
ban-relative-imports = "all"

[tool.ruff.lint.isort]
known-first-party = ["my_package"]
section-order = ["future", "standard-library", "third-party", "first-party", "local-folder"]

[tool.ruff.lint.pydocstyle]
convention = "google"

[tool.ruff.lint.pylint]
max-args = 8
max-branches = 15
```
