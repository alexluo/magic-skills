"""
Command parser for /mgc- style skill commands.

Supports:
- /mgc-<category>-<skill-name> - Execute specific skill
- /mgc-list - List all available skills
- /mgc-help - Show help
- /mgc-models - List available LLM models
"""

import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class ParsedCommand:
    """Parsed command structure."""
    raw_command: str
    category: Optional[str]
    skill_name: Optional[str]
    params: Dict
    is_valid: bool
    error_message: Optional[str] = None


class CommandParser:
    """Parser for /mgc- style commands."""
    
    # Command patterns
    SKILL_PATTERN = re.compile(r'^/mgc-([a-z-]+)-([a-z-]+)$')
    SPECIAL_COMMANDS = {
        '/mgc-list': 'list_all_skills',
        '/mgc-help': 'show_help',
        '/mgc-models': 'list_models',
        '/mgc-version': 'show_version',
    }
    
    def __init__(self, skill_manager=None):
        self.skill_manager = skill_manager
    
    def parse(self, command: str, context: Dict = None) -> ParsedCommand:
        """
        Parse a command string.
        
        Args:
            command: Command string (e.g., "/mgc-java-backend-controller-gen")
            context: Additional context (selected text, file info, etc.)
            
        Returns:
            ParsedCommand object
        """
        command = command.strip()
        
        # Check for special commands
        if command in self.SPECIAL_COMMANDS:
            return ParsedCommand(
                raw_command=command,
                category=None,
                skill_name=self.SPECIAL_COMMANDS[command],
                params=context or {},
                is_valid=True
            )
        
        # Parse skill command
        match = self.SKILL_PATTERN.match(command)
        if not match:
            return ParsedCommand(
                raw_command=command,
                category=None,
                skill_name=None,
                params={},
                is_valid=False,
                error_message=f"Invalid command format. Expected: /mgc-<category>-<skill-name>"
            )
        
        category = match.group(1)
        skill_name = match.group(2)
        
        # Build full skill name
        full_skill_name = f"{category}-{skill_name}"
        
        # Validate skill exists
        if self.skill_manager:
            skill = self.skill_manager.get_skill(full_skill_name)
            if not skill:
                # Try without category prefix
                skill = self.skill_manager.get_skill(skill_name)
                if not skill:
                    return ParsedCommand(
                        raw_command=command,
                        category=category,
                        skill_name=skill_name,
                        params={},
                        is_valid=False,
                        error_message=f"Skill not found: {full_skill_name}"
                    )
                full_skill_name = skill_name
        
        # Build params from context
        params = self._build_params(context)
        
        return ParsedCommand(
            raw_command=command,
            category=category,
            skill_name=full_skill_name,
            params=params,
            is_valid=True
        )
    
    def _build_params(self, context: Dict = None) -> Dict:
        """Build skill parameters from context."""
        params = {}
        
        if not context:
            return params
        
        # Add context information
        if 'selected_text' in context:
            params['selected_text'] = context['selected_text']
        
        if 'file_path' in context:
            params['file_path'] = context['file_path']
            # Detect language from file extension
            params['language'] = self._detect_language(context['file_path'])
        
        if 'file_content' in context:
            params['file_content'] = context['file_content']
        
        if 'project_structure' in context:
            params['project_structure'] = context['project_structure']
        
        return params
    
    def _detect_language(self, file_path: str) -> str:
        """Detect programming language from file extension."""
        ext_map = {
            '.py': 'python',
            '.java': 'java',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.jsx': 'jsx',
            '.tsx': 'tsx',
            '.go': 'go',
            '.rs': 'rust',
            '.cpp': 'cpp',
            '.c': 'c',
            '.h': 'c',
            '.swift': 'swift',
            '.kt': 'kotlin',
            '.rb': 'ruby',
            '.php': 'php',
            '.cs': 'csharp',
        }
        
        from pathlib import Path
        ext = Path(file_path).suffix.lower()
        return ext_map.get(ext, 'unknown')
    
    def get_completions(self, partial: str) -> List[Dict]:
        """
        Get command completions for partial input.
        
        Args:
            partial: Partial command (e.g., "/mgc-java-" or "/mgc-")
            
        Returns:
            List of completion suggestions
        """
        completions = []
        
        # Special commands
        for cmd in self.SPECIAL_COMMANDS.keys():
            if cmd.startswith(partial):
                completions.append({
                    'command': cmd,
                    'description': self._get_special_command_desc(cmd),
                    'type': 'special'
                })
        
        # Skill commands
        if self.skill_manager and partial.startswith('/mgc-'):
            # Extract category filter if present
            parts = partial[5:].split('-')  # Remove "/mgc-"
            
            if len(parts) >= 1 and parts[0]:
                # Filter by category
                category_filter = parts[0]
                skills = self.skill_manager.list_skills()
                
                for skill_info in skills:
                    category = skill_info.get('category', '')
                    name = skill_info.get('name', '')
                    
                    # Build command
                    cmd = f"/mgc-{category}-{name.replace(category + '-', '')}"
                    
                    if cmd.startswith(partial):
                        completions.append({
                            'command': cmd,
                            'description': skill_info.get('description', ''),
                            'category': category,
                            'type': 'skill'
                        })
            else:
                # List all categories
                skills = self.skill_manager.list_skills()
                categories = set()
                
                for skill_info in skills:
                    category = skill_info.get('category', '')
                    if category:
                        categories.add(category)
                
                for category in sorted(categories):
                    cmd = f"/mgc-{category}-"
                    if cmd.startswith(partial):
                        completions.append({
                            'command': cmd,
                            'description': f'{category} skills',
                            'category': category,
                            'type': 'category'
                        })
        
        return completions
    
    def _get_special_command_desc(self, cmd: str) -> str:
        """Get description for special commands."""
        descriptions = {
            '/mgc-list': 'List all available skills',
            '/mgc-help': 'Show help information',
            '/mgc-models': 'List available LLM models',
            '/mgc-version': 'Show version information',
        }
        return descriptions.get(cmd, 'Special command')
    
    def format_skill_list(self) -> str:
        """Format skill list for display."""
        if not self.skill_manager:
            return "Skill manager not available"
        
        skills = self.skill_manager.list_skills()
        
        # Group by category
        from collections import defaultdict
        by_category = defaultdict(list)
        
        for skill in skills:
            category = skill.get('category', 'uncategorized')
            by_category[category].append(skill)
        
        # Format output
        lines = ["# Available Magic Skills\n"]
        lines.append("Usage: `/mgc-<category>-<skill-name>`\n")
        
        for category in sorted(by_category.keys()):
            lines.append(f"\n## {category.replace('-', ' ').title()}\n")
            
            for skill in by_category[category]:
                name = skill.get('name', '')
                description = skill.get('description', '')
                # Extract short name
                short_name = name.replace(f"{category}-", "")
                cmd = f"/mgc-{category}-{short_name}"
                lines.append(f"- `{cmd}` - {description}")
        
        lines.append("\n## Special Commands\n")
        for cmd, desc in [
            ('/mgc-list', 'List all skills'),
            ('/mgc-help', 'Show help'),
            ('/mgc-models', 'List available models'),
            ('/mgc-version', 'Show version'),
        ]:
            lines.append(f"- `{cmd}` - {desc}")
        
        return '\n'.join(lines)


# Global parser instance
_command_parser: Optional[CommandParser] = None


def get_command_parser(skill_manager=None) -> CommandParser:
    """Get or create global command parser instance."""
    global _command_parser
    if _command_parser is None or skill_manager is not None:
        _command_parser = CommandParser(skill_manager)
    return _command_parser
