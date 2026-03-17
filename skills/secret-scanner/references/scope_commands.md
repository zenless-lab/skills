# Commands for Scanning Scopes

When a user specifies a target scope for secret scanning, use the following commands to gather the contents efficiently.

## Git Changes (Working Directory & Staging)

*   **View unstaged changes (Working Tree):**
    ```bash
    git diff
    ```
    *To view only specific files:* `git diff -- <file_path>`

*   **View staged changes (Index):**
    ```bash
    git diff --staged
    ```
    *To view only specific files:* `git diff --staged -- <file_path>`

*   **View untracked files:**
    ```bash
    git ls-files --others --exclude-standard
    ```
    *(You will then need to read these files individually using the `read_file` tool).*

*   **View changes in the last commit:**
    ```bash
    git show HEAD
    ```

## Files and Directories

*   **List all files in a directory (recursive):**
    ```bash
    find <directory_path> -type f
    ```
    *Alternatively, use the agent `list_directory` tool if applicable.*

*   **List files tracked by git:**
    ```bash
    git ls-files
    ```

*   **Search for specific file extensions in a directory:**
    ```bash
    find <directory_path> -type f \( -name "*.py" -o -name "*.json" \)
    ```

## Searching for Patterns (Quick triage)

If you need to quickly locate potential files that *might* contain secrets before doing a deep reading:

*   **Grep for common secret keywords in a directory:**
    ```bash
    grep -rnE -i 'secret|token|password|key|auth|api_key|credential' <directory_path>
    ```

*   **Grep for email patterns:**
    ```bash
    grep -rnE '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}' <directory_path>
    ```
