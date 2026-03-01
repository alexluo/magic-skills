"""MCP Server implementation for AI tool integration."""

import asyncio
from typing import Any, Dict, List, Optional

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

from ..core.skill_manager import SkillManager
from ..core.command_parser import get_command_parser, ParsedCommand


class MagicSkillsMCPServer:
    """MCP Server for Magic Skills."""

    def __init__(self, skill_manager: SkillManager):
        self.skill_manager = skill_manager
        self.command_parser = get_command_parser(skill_manager)
        self.server = Server("magic-skills")
        self._setup_handlers()

    def _setup_handlers(self) -> None:
        """Setup MCP handlers."""

        @self.server.list_tools()
        async def list_tools() -> List[Tool]:
            """List all available skills as tools."""
            skills = self.skill_manager.list_skills()
            tools = []
            
            # Add command-based tool
            tools.append(
                Tool(
                    name="mgc-command",
                    description="Execute Magic Skills using /mgc-<category>-<skill-name> format",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "command": {
                                "type": "string",
                                "description": "Command in format /mgc-<category>-<skill-name>, e.g., /mgc-java-backend-controller-gen"
                            },
                            "context": {
                                "type": "object",
                                "description": "Optional context (selected_text, file_path, etc.)"
                            }
                        },
                        "required": ["command"]
                    }
                )
            )
            
            # Add skill list tool
            tools.append(
                Tool(
                    name="mgc-list",
                    description="List all available Magic Skills with /mgc- commands",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                )
            )
            
            # Add autocomplete tool
            tools.append(
                Tool(
                    name="mgc-complete",
                    description="Get command completions for partial /mgc- input",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "partial": {
                                "type": "string",
                                "description": "Partial command, e.g., /mgc-java-"
                            }
                        },
                        "required": ["partial"]
                    }
                )
            )
            
            # Add traditional skill tools
            for skill in skills:
                schema = self.skill_manager.get_skill_schema(skill["name"])
                # Also add /mgc- format name
                short_name = skill["name"].replace(f"{skill.get('category', '')}-", "")
                mgc_name = f"mgc-{skill.get('category', 'general')}-{short_name}"
                
                tools.append(
                    Tool(
                        name=skill["name"],
                        description=f"{skill['description']} | Use: /mgc-{skill.get('category', 'general')}-{short_name}",
                        inputSchema=schema.get("parameters", {}) if schema else {},
                    )
                )
            return tools

        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
            """Execute a skill or command."""
            try:
                # Handle special command-based tools
                if name == "mgc-command":
                    return await self._handle_command(arguments)
                elif name == "mgc-list":
                    return await self._handle_list()
                elif name == "mgc-complete":
                    return await self._handle_complete(arguments)
                
                # Handle traditional skill execution
                result = self.skill_manager.execute_skill(name, arguments)
                if result.success:
                    return [TextContent(type="text", text=str(result.data))]
                else:
                    return [TextContent(type="text", text=f"Error: {result.error}")]
            except Exception as e:
                return [TextContent(type="text", text=f"Error: {str(e)}")]

    async def _handle_command(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Handle /mgc- command execution."""
        command = arguments.get("command", "")
        context = arguments.get("context", {})
        
        parsed = self.command_parser.parse(command, context)
        
        if not parsed.is_valid:
            return [TextContent(type="text", text=f"❌ {parsed.error_message}")]
        
        # Handle special commands
        if parsed.skill_name == "list_all_skills":
            return [TextContent(type="text", text=self.command_parser.format_skill_list())]
        elif parsed.skill_name == "show_help":
            return [TextContent(type="text", text=self._get_help_text())]
        elif parsed.skill_name == "list_models":
            return [TextContent(type="text", text=self._get_models_text())]
        elif parsed.skill_name == "show_version":
            return [TextContent(type="text", text="Magic Skills v1.0.0")]
        
        # Execute skill
        result = self.skill_manager.execute_skill(parsed.skill_name, parsed.params)
        
        if result.success:
            return [
                TextContent(type="text", text=f"✅ Executed: {command}\n\n{result.data}"),
            ]
        else:
            return [TextContent(type="text", text=f"❌ Error: {result.error}")]

    async def _handle_list(self) -> List[TextContent]:
        """Handle skill list request."""
        return [TextContent(type="text", text=self.command_parser.format_skill_list())]

    async def _handle_complete(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Handle command completion request."""
        partial = arguments.get("partial", "")
        completions = self.command_parser.get_completions(partial)
        
        if not completions:
            return [TextContent(type="text", text="No completions found.")]
        
        lines = [f"# Completions for '{partial}'\n"]
        
        # Group by type
        skills = [c for c in completions if c['type'] == 'skill']
        categories = [c for c in completions if c['type'] == 'category']
        special = [c for c in completions if c['type'] == 'special']
        
        if special:
            lines.append("\n## Special Commands")
            for c in special:
                lines.append(f"- `{c['command']}` - {c['description']}")
        
        if categories:
            lines.append("\n## Categories")
            for c in categories:
                lines.append(f"- `{c['command']}` - {c['description']}")
        
        if skills:
            lines.append("\n## Skills")
            for c in skills[:20]:  # Limit to 20 skills
                lines.append(f"- `{c['command']}` - {c['description']}")
            if len(skills) > 20:
                lines.append(f"- ... and {len(skills) - 20} more")
        
        return [TextContent(type="text", text='\n'.join(lines))]

    def _get_help_text(self) -> str:
        """Get help text."""
        return """# Magic Skills Help

## Command Format

Use `/mgc-<category>-<skill-name>` to execute skills:

- `/mgc-java-backend-controller-gen` - Generate Spring Boot controller
- `/mgc-software-testing-unit-test-gen` - Generate unit tests
- `/mgc-android-os-aidl-interface-gen` - Generate AIDL interface

## Special Commands

- `/mgc-list` - List all available skills
- `/mgc-help` - Show this help
- `/mgc-models` - List available LLM models
- `/mgc-version` - Show version

## Auto-completion

Type `/mgc-` and the AI tool will show available completions.

## Context Passing

The following context is automatically passed to skills:
- Selected text
- Current file path and content
- Project structure
- Programming language (detected from file extension)
"""

    def _get_models_text(self) -> str:
        """Get available models text."""
        from ..models import ModelManager
        mm = ModelManager()
        providers = mm.list_providers()
        
        lines = ["# Available LLM Models\n"]
        
        for provider in providers:
            try:
                models = mm.list_models(provider)
                lines.append(f"\n## {provider.upper()}")
                for model in models[:5]:  # Show top 5
                    lines.append(f"- {model}")
                if len(models) > 5:
                    lines.append(f"- ... and {len(models) - 5} more")
            except:
                lines.append(f"\n## {provider.upper()}")
                lines.append("- (models not available)")
        
        return '\n'.join(lines)

    async def run(self) -> None:
        """Run the MCP server."""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options(),
            )


def main():
    """Main entry point for MCP server."""
    skill_manager = SkillManager()
    skill_manager.load_all_skills()

    server = MagicSkillsMCPServer(skill_manager)
    asyncio.run(server.run())


if __name__ == "__main__":
    main()
