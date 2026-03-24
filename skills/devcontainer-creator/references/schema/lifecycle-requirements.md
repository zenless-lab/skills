# Lifecycle Scripts & Requirements

When creating or working with a dev container, commands run at different points in the lifecycle.

## Execution Formats
Lifecycle scripts can be formatted in three ways:
1.  **String**: Runs through a shell (`/bin/sh -c "..."`). Use `&&` for multiple commands.
2.  **Array**: Passed directly to the OS for execution without a shell (e.g., `["npm", "install"]`).
3.  **Object**: Executes multiple commands in **parallel**. Each key is an arbitrary name, and the value is a string or array command.

## Lifecycle Properties

| Property | Description | Context |
|----------|-------------|---------|
| `initializeCommand` | Runs on the **host machine** during initialization, before container creation. | Host OS |
| `onCreateCommand` | Runs **inside** the container immediately after it starts for the first time. Used by cloud services for caching/prebuilding. | Container |
| `updateContentCommand` | Runs **inside** the container after `onCreateCommand` whenever source code changes during creation. | Container |
| `postCreateCommand` | Runs **inside** the container after `updateContentCommand` once assigned to a user. Best for user-specific setup (`npm install`, `pip install`). | Container |
| `postStartCommand` | Runs each time the container is successfully started. | Container |
| `postAttachCommand` | Runs each time a tool successfully attaches to the container. | Container |
| `waitFor` | Enum specifying which command the tool should wait for before allowing user connection. Defaults to `updateContentCommand`. | Host Tool |

*Note: If a lifecycle script fails, subsequent scripts are skipped.*

## Minimum Host Requirements

Used to define hardware or VM provisioning constraints (e.g., for cloud environments).

| Property | Type | Description |
|----------|------|-------------|
| `hostRequirements.cpus` | integer | Minimum required number of CPUs / cores. |
| `hostRequirements.memory` | string | Minimum memory (e.g., `"4gb"`). |
| `hostRequirements.storage` | string | Minimum storage (e.g., `"32gb"`). |
| `hostRequirements.gpu` | bool/str/obj | Indicates if GPU is required (`true`, `false`, `"optional"`), or specifies core/memory details. |
