# Distribution and Discovery

Templates are typically stored in a git repository under a `src/` directory. Multiple templates in a repo form a "collection."

## Packaging

Templates are distributed as tarballs containing the entire contents of the template sub-directory (including `devcontainer-template.json` and `.devcontainer/devcontainer.json`).

The tarball is named `devcontainer-template-<id>.tgz`.

## Distribution

The primary distribution mechanism is via an OCI Registry implementing the OCI Artifact Distribution Specification.

The namespace format: `<registry>/<namespace>/<id>[:version]`.
Example: `ghcr.io/devcontainers/templates/go:1.0.0`.

Media types used:
- `application/vnd.devcontainers`
- `application/vnd.devcontainers.layer.v1+tar`

### devcontainer-collection.json
A collection of templates also requires an auto-generated `devcontainer-collection.json` that contains metadata from all `devcontainer-template.json` files. This is also pushed to the registry.
