# Scenario-Specific Properties

`devcontainer.json` supports different orchestrator scenarios: Image/Dockerfile-based and Docker Compose-based.

## Image or Dockerfile Specific Properties

| Property | Type | Description |
|----------|------|-------------|
| `image` | string | **Required** when using an image. The name of the image in a container registry. |
| `build.dockerfile` | string | **Required** when using a Dockerfile. The location of the Dockerfile relative to `devcontainer.json`. |
| `build.context` | string | Path the Docker build should run from relative to `devcontainer.json`. Defaults to `"."`. |
| `build.args` | object | Set of name-value pairs passed as Docker image build arguments (`--build-arg`). |
| `build.options` | array | Array of Docker image build options passed to the build command. |
| `build.target` | string | Specifies a Docker image build target (`--target`). |
| `build.cacheFrom` | string/array | One or more images to use as caches (`--cache-from`). |
| `appPort` | int/str/array | Port(s) published locally when the container is running. We generally recommend using `forwardPorts` instead unless publishing to all interfaces (`0.0.0.0`) is required. |
| `workspaceMount` | string | Overrides the default local mount point for the workspace. Requires `workspaceFolder`. |
| `workspaceFolder` | string | Sets the default path supporting tools should open when connecting. Requires `workspaceMount`. Defaults to automatic source code mount location. |
| `runArgs` | array | Array of Docker CLI arguments used when running the container (e.g., `["--network=host"]`). |

## Docker Compose Specific Properties

| Property | Type | Description |
|----------|------|-------------|
| `dockerComposeFile` | string/array | **Required** when using Docker Compose. Path(s) to Docker Compose files relative to `devcontainer.json`. Arrays merge files in order. |
| `service` | string | **Required** when using Docker Compose. The name of the service the supporting tool should connect to. |
| `runServices` | array | Array of services in the Docker Compose configuration that should be started. Defaults to all services. |
| `workspaceFolder` | string | Sets the default path supporting tools should open when connecting. Defaults to `"/"`. |
