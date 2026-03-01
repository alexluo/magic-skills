# AI Tool Integration Guide

This guide explains how to integrate Magic Skills with popular AI programming tools.

## Supported AI Tools

- Cursor
- Claude Desktop
- VS Code (via MCP)
- Trae
- OpenCode

## MCP Server Setup

### Cursor

1. Open Cursor Settings
2. Navigate to MCP settings
3. Add the following configuration:

```json
{
  "mcpServers": {
    "magic-skills": {
      "command": "python",
      "args": ["-m", "src.mcp.server"],
      "env": {
        "PYTHONPATH": "${workspaceFolder}",
        "OPENAI_API_KEY": "${env:OPENAI_API_KEY}"
      }
    }
  }
}
```

### Claude Desktop

1. Open Claude Desktop
2. Go to Settings > Developer
3. Edit the configuration file:

```json
{
  "mcpServers": {
    "magic-skills": {
      "command": "python",
      "args": ["-m", "src.mcp.server"],
      "env": {
        "PYTHONPATH": "/path/to/magic_skills",
        "OPENAI_API_KEY": "YOUR_API_KEY"
      }
    }
  }
}
```

## Available Skills

Once integrated, you can use all 160+ skills across 6 domains:

- Java Backend Development
- Android OS Development
- Digital Analytics
- Mobile App Development
- Multi-language Translation
- Software Testing

## Usage Examples

### Generate Spring Boot Controller

```
Use magic-skills to generate a Spring Boot controller for user management
```

### Analyze Code

```
Use magic-skills to review this Java code for security issues
```

### Generate Tests

```
Use magic-skills to generate unit tests for this function
```

## Troubleshooting

### MCP Server Not Starting

1. Check Python path is correct
2. Verify API keys are set
3. Check logs for errors

### Skills Not Available

1. Ensure skills directory is populated
2. Run `magic-skill list` to verify
3. Check MCP server connection

## Best Practices

1. Set up environment variables for API keys
2. Use specific skill names for better results
3. Provide clear context when invoking skills
