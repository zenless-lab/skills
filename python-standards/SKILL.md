---
name: python-standards
description: A modular guide for Python code structure, documentation styles, and testing frameworks. Uses progressive loading to enforce consistency based on existing code patterns.
compatibility: Python 3.8+
---

# Python Standards & Patterns

## Usage Strategy
Do not dump all rules at once. **First, analyze the user's file structure or code snippet**, then match it to one of the patterns below. **Only load the specific reference file** that matches the user's context.

---

## 1. Project Layout Identification
Check the root directory structure:

### A. The "Src" Layout (Production Standard)
* **Signature**: Presence of a `src/` directory containing the package.
* **Use Case**: Library packaging, strict import isolation, modern CI/CD.
* **Action**: Load `references/layouts/src.md`.

### B. The "Flat" Layout (Simple/Script)
* **Signature**: Package folder sits directly in the root (no `src/`).
* **Use Case**: Simple scripts, micro-services, legacy projects.
* **Action**: Load `references/layouts/flat.md`.

### C. Data Science / Machine Learning
* **Signature**: Folders like `data/`, `notebooks/`, `models/`.
* **Use Case**: Model training, experimentation, DAG workflows.
* **Action**: Load `references/layouts/data_science.md`.

### D. FastAPI / Web Modular
* **Signature**: `app/` folder with `routers/`, `schemas/`, `dependencies.py`.
* **Use Case**: Scalable web APIs.
* **Action**: Load `references/layouts/fastapi_modular.md`.

---

## 2. Docstring Style Identification
Check functions/classes for these specific syntax markers:

### A. Google Style (Readable)
* **Signature**: Sections named `Args:`, `Returns:`, `Raises:` (no colons around names).
    ```python
    """
    Args:
        name (str): The name of the user.
    """
    ```
* **Action**: Load `references/doc_styles/google.md`.

### B. Sphinx / reST Style (Formal)
* **Signature**: Directives like `:param name:`, `:return:`, `:type:`.
    ```python
    """
    :param name: The name of the user.
    :type name: str
    """
    ```
* **Action**: Load `references/doc_styles/sphinx_rest.md`.

### C. NumPy Style (Scientific)
* **Signature**: Section headers underlined with dashes `----`.
    ```python
    """
    Parameters
    ----------
    x : array_like
        Input array.
    """
    ```
* **Action**: Load `references/doc_styles/numpy.md`.

---

## 3. Testing Framework Identification
Check test files or `pyproject.toml`:

* **pytest**: Uses `def test_foo():` and bare `assert`. -> Load `references/testing/pytest.md`.
* **unittest**: Uses `class TestFoo(unittest.TestCase):` and `self.assertEqual`. -> Load `references/testing/unittest.md`.
* **BDD**: Uses `.feature` files, `@given`, `@when`, `@then`. -> Load `references/testing/bdd.md`.

---

## 4. General Coding Style
If the request involves general code cleanup, refactoring, or linting errors, always reference the core PEP 8 rules.
* **Action**: Load `references/style/pep8_core.md`.
