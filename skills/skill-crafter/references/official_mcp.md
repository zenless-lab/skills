# MCP for Official Documentation Access

Load this file when a skill needs to search or retrieve content from official documentation as part of its workflow.

## Adding the MCP server to the user's environment

When the task requires MCP and the server is not yet configured, instruct the user to add it. **Always add at workspace scope by default.** Add globally only when the user explicitly asks for a global configuration.

Use the example that matches the user's environment.

### VS Code (GitHub Copilot)

**Workspace (default):** add to `.vscode/mcp.json`:

```json
{
  "servers": {
    "skills-spec": {
      "url": "https://agentskills.io/mcp",
      "type": "sse"
    }
  }
}
```

**Global (only if requested):** add the same block under `"mcp"` in the user's VS Code `settings.json`.

### GitHub Copilot CLI

GitHub Copilot CLI does not have a standalone MCP config file. MCP servers for Copilot in the terminal are configured through VS Code's MCP settings (see above) or via the `gh copilot` extension settings if supported in the installed version.

### Gemini CLI

**Workspace (default):** add to `.gemini/settings.json` in the workspace root:

```json
{
  "mcpServers": {
    "skills-spec": {
      "httpUrl": "https://agentskills.io/mcp"
    }
  }
}
```

**Global (only if requested):** add to `~/.gemini/settings.json`.

### OpenAI Codex CLI

**Workspace (default):** add to `codex.md` or `.codex/config.json` in the workspace root (check the installed Codex CLI version for the exact file name):

```json
{
  "mcpServers": {
    "skills-spec": {
      "url": "https://agentskills.io/mcp"
    }
  }
}
```

**Global (only if requested):** add to `~/.codex/config.json`.

### Claude Code (Anthropic)

**Workspace (default):** run the following command from the workspace root to register the server at project scope:

```bash
claude mcp add --scope project skills-spec --transport http https://agentskills.io/mcp
```

This writes the entry to `.mcp.json` in the workspace root.

**Global (only if requested):**

```bash
claude mcp add --scope user skills-spec --transport http https://agentskills.io/mcp
```

### Claude Desktop

Claude Desktop has no workspace concept. Add to the global config file:

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "skills-spec": {
      "url": "https://agentskills.io/mcp"
    }
  }
}
```

### Cursor

**Workspace (default):** add to `.cursor/mcp.json` in the workspace root:

```json
{
  "mcpServers": {
    "skills-spec": {
      "url": "https://agentskills.io/mcp"
    }
  }
}
```

**Global (only if requested):** add to `~/.cursor/mcp.json`.

### Windsurf

**Workspace (default):** add to `.windsurf/mcp.json` in the workspace root if supported, otherwise:

**Global:** add to `~/.codeium/windsurf/mcp_config.json`:

```json
{
  "mcpServers": {
    "skills-spec": {
      "url": "https://agentskills.io/mcp"
    }
  }
}
```

### Continue

**Workspace (default):** add to `.continue/config.json` in the workspace root:

```json
{
  "mcpServers": [
    {
      "name": "skills-spec",
      "url": "https://agentskills.io/mcp"
    }
  ]
}
```

**Global (only if requested):** add to `~/.continue/config.json`.

### General notes for all environments

- Replace `skills-spec` with any unique name; the name is local to the client.
- The `url` is the only required field for HTTP-based MCP servers.
- If the server requires authentication in the future, add a `headers` object with the relevant token.
- After editing the config, restart the client or reload the MCP connection for the server to appear.

## Available tools

The `skills-spec` MCP server exposes two tools.

### `search_agent_skills`

Search the Agent Skills knowledge base for relevant documentation, code examples, API references, and guides.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `query` | string | yes | Free-text query describing what you are looking for |

Returns a list of result snippets with titles and page paths. Use this tool first to locate the relevant section.

### `get_page_agent_skills`

Retrieve the full content of a documentation page by its path.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `page` | string | yes | Page path from a `search_agent_skills` result (e.g. `api-reference/create-customer`) |

Use this tool when a search snippet is insufficient and you need the complete page content.

## Documentation lookup

When uncertain about a skill specification, frontmatter field, format rule, or any API detail, use the `skills-spec` MCP server before guessing or inventing a convention.

Two-step workflow:

1. Call `search_agent_skills` with a focused query (e.g. `"mcp frontmatter declaration"`, `"skill folder layout"`).
2. If the returned snippet is incomplete, call `get_page_agent_skills` with the page path from the search result to get the full page.

Rules:
- prefer official documentation results over training knowledge when they conflict
- cite the source URL when accuracy is critical
- if both tools return nothing relevant, fall back to [Specification](specification.md) and state the assumption explicitly
