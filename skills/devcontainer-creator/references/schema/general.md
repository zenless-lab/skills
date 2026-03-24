# General Properties

The `devcontainer.json` file contains metadata to configure a development container. Below are the general properties available.

| Property | Type | Description |
|----------|------|-------------|
| `name` | string | A name for the dev container displayed in the UI. |
| `forwardPorts` | array | An array of port numbers or `"host:port"` values (e.g., `[3000, "db:5432"]`) that should always be forwarded from inside the primary container to the local machine. Defaults to `[]`. |
| `portsAttributes` | object | Object that maps a port number, `"host:port"` value, range, or regular expression to a set of default options. Example: `"portsAttributes": {"3000": {"label": "Application port"}}`. |
| `otherPortsAttributes` | object | Default options for ports, port ranges, and hosts that aren't configured using `portsAttributes`. |
| `containerEnv` | object | A set of name-value pairs that sets or overrides environment variables for the container. Variables are static for the life of the container (requires rebuild to update). |
| `remoteEnv` | object | A set of name-value pairs that sets or overrides environment variables for the supporting service / tool (or sub-processes like terminals) but not the container as a whole. Can be updated without rebuilding. |
| `remoteUser` | string | Overrides the user that supporting tools run as in the container (along with sub-processes like terminals). Defaults to the user the container as a whole is running as (often `root`). |
| `containerUser` | string | Overrides the user for all operations run as inside the container. Defaults to either `root` or the last `USER` instruction in the Dockerfile. |
| `updateRemoteUserUID` | boolean | On Linux, if `containerUser` or `remoteUser` is specified, the user's UID/GID will be updated to match the local user's UID/GID to avoid permission problems with bind mounts. Defaults to `true`. |
| `userEnvProbe` | enum | Type of shell to use to "probe" for user environment variables: `none`, `interactiveShell`, `loginShell`, or `loginInteractiveShell` (default). |
| `overrideCommand` | boolean | Tells supporting tools whether they should run `/bin/sh -c "while sleep 1000; do :; done"` instead of the container's default command. Defaults to `true` for image/Dockerfile and `false` for Docker Compose. |
| `shutdownAction` | enum | Indicates whether supporting tools should stop the containers when the tool window is closed. Values: `none`, `stopContainer` (default for image/Dockerfile), `stopCompose` (default for Docker Compose). |
| `init` | boolean | Indicates whether the `tini` init process should be used to handle zombie processes. Defaults to `false`. |
| `privileged` | boolean | Runs the container in privileged mode (`--privileged`). Required for Docker-in-Docker. Defaults to `false`. |
| `capAdd` | array | Adds capabilities typically disabled. Most often used for debugging (e.g., `"capAdd": ["SYS_PTRACE"]`). Defaults to `[]`. |
| `securityOpt` | array | Sets container security options (e.g., `"securityOpt": ["seccomp=unconfined"]`). Defaults to `[]`. |
| `mounts` | array | Cross-orchestrator way to add additional mounts. Accepts values identical to the Docker CLI `--mount` flag. |
| `features` | object | An object of Dev Container Feature IDs and related options. Example: `"features": { "ghcr.io/devcontainers/features/github-cli:1": {} }`. |
| `overrideFeatureInstallOrder` | array | Array of Feature IDs (without versions) to explicitly control the installation order of Features. |
| `customizations` | object | Product-specific properties (e.g., `vscode` settings and extensions). |
| `secrets` | object | Declarative map of secret names and details (e.g., description, documentationUrl) required by the dev container. |
