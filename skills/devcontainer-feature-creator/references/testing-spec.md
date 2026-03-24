# Testing Features

The Dev Container CLI provides a robust testing framework for Features.

## The `test` Command
Use `devcontainer features test -f <feature> --base-image <image>` to run tests locally. This builds a temporary container and runs the test scripts.

## Directory Structure
```text
.
├── src
│   └── my-feature
│       ├── devcontainer-feature.json
│       └── install.sh
└── test
    ├── my-feature
    │   ├── test.sh                <-- Auto-generated test
    │   ├── scenarios.json         <-- Scenarios definition
    │   ├── some_scenario.sh       <-- Scenario assertion script
    │   └── duplicate.sh           <-- Duplicate assertion script
    └── _global
        └── scenarios.json         <-- Global scenarios across multiple features
```

## Testing Modes

### 1. Auto-generated Tests
- Evaluates the Feature with default options on a basic image.
- **Script:** `test/<feature>/test.sh`. The test passes if the build succeeds and this script exits with `0`.

### 2. Scenarios
- Tests different option combinations or multiple Features installed together.
- **Configuration:** `test/<feature>/scenarios.json`. Maps a scenario name to a `devcontainer.json` configuration snippet.
  ```json
  {
      "my_scenario": {
          "image": "ubuntu:22.04",
          "features": {
              "my-feature": {
                  "version": "2.0"
              }
          }
      }
  }
  ```
- **Script:** `test/<feature>/my_scenario.sh`.

### 3. Duplicate Tests
- Ensures idempotency by installing the same Feature twice with different options.
- The CLI automatically generates this configuration if a `test/<feature>/duplicate.sh` script is present.
- Both randomized options (`$OPTIONNAME`) and default options (`$OPTIONNAME__DEFAULT`) are passed to the script for assertions.

## Test Library (`dev-container-features-test-lib`)
A convenience helper injected by the CLI.
- `source dev-container-features-test-lib`
- `check "<Label>" <command> [args...]`: Prints success/fail depending on the exit code.
- `reportResults`: Prints a summary at the end of the script.
