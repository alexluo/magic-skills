"""Skill management core module."""

import importlib.util
import json
import os
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Protocol

import yaml
from pydantic import BaseModel, Field


class SkillConfig(BaseModel):
    """Skill configuration model."""

    name: str
    description: str
    version: str = "1.0.0"
    author: str = ""
    parameters: Dict[str, Any] = Field(default_factory=dict)
    tags: List[str] = Field(default_factory=list)
    category: str = "general"


class SkillExecutionResult(BaseModel):
    """Skill execution result."""

    success: bool
    data: Any = None
    error: Optional[str] = None
    execution_time_ms: float = 0.0


class SkillNotFoundError(Exception):
    """Raised when a skill is not found."""

    pass


class SkillExecutionError(Exception):
    """Raised when skill execution fails."""

    pass


class SkillHandler(Protocol):
    """Protocol for skill handler functions."""

    def __call__(self, params: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Any:
        ...


class Skill:
    """Represents a single skill."""

    def __init__(self, config: SkillConfig, handler: SkillHandler, prompt_template: str = ""):
        self.config = config
        self.handler = handler
        self.prompt_template = prompt_template
        self._execution_count = 0
        self._average_rating = 0.0

    @property
    def name(self) -> str:
        return self.config.name

    @property
    def description(self) -> str:
        return self.config.description

    def execute(self, params: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> SkillExecutionResult:
        """Execute the skill with given parameters."""
        import time

        start_time = time.time()
        try:
            result = self.handler(params, context)
            execution_time = (time.time() - start_time) * 1000

            self._execution_count += 1

            return SkillExecutionResult(
                success=True,
                data=result,
                execution_time_ms=execution_time
            )
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            return SkillExecutionResult(
                success=False,
                error=str(e),
                execution_time_ms=execution_time
            )

    def get_prompt(self, params: Dict[str, Any]) -> str:
        """Generate prompt from template with parameters."""
        if not self.prompt_template:
            return ""

        try:
            return self.prompt_template.format(**params)
        except KeyError as e:
            return self.prompt_template


class SkillManager:
    """Manages skill loading, registration, and execution."""

    def __init__(self, skills_dir: Optional[str] = None):
        self.skills_dir = Path(skills_dir) if skills_dir else Path("skills")
        self._skills: Dict[str, Skill] = {}
        self._categories: Dict[str, List[str]] = {}

    def load_all_skills(self) -> int:
        """Load all skills from the skills directory."""
        count = 0
        if not self.skills_dir.exists():
            return count

        for skill_dir in self.skills_dir.rglob("*"):
            if skill_dir.is_dir() and (skill_dir / "skill.yaml").exists():
                try:
                    self._load_skill_from_dir(skill_dir)
                    count += 1
                except Exception as e:
                    print(f"Failed to load skill from {skill_dir}: {e}")

        return count

    def _load_skill_from_dir(self, skill_dir: Path) -> None:
        """Load a single skill from directory."""
        config_path = skill_dir / "skill.yaml"
        handler_path = skill_dir / "handler.py"
        prompt_path = skill_dir / "prompt.txt"

        # Load configuration
        with open(config_path, "r", encoding="utf-8") as f:
            config_data = yaml.safe_load(f)
        config = SkillConfig(**config_data)

        # Load handler
        if not handler_path.exists():
            raise SkillExecutionError(f"Handler not found: {handler_path}")

        handler = self._load_handler_from_file(handler_path)

        # Load prompt template
        prompt_template = ""
        if prompt_path.exists():
            with open(prompt_path, "r", encoding="utf-8") as f:
                prompt_template = f.read()

        # Create and register skill
        skill = Skill(config, handler, prompt_template)
        self.register_skill(skill)

    def _load_handler_from_file(self, handler_path: Path) -> SkillHandler:
        """Load handler function from Python file."""
        spec = importlib.util.spec_from_file_location("handler", handler_path)
        if spec is None or spec.loader is None:
            raise SkillExecutionError(f"Cannot load handler: {handler_path}")

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if not hasattr(module, "execute"):
            raise SkillExecutionError(f"Handler must define 'execute' function: {handler_path}")

        return module.execute

    def register_skill(self, skill: Skill) -> None:
        """Register a skill."""
        self._skills[skill.name] = skill

        # Update category index
        category = skill.config.category
        if category not in self._categories:
            self._categories[category] = []
        if skill.name not in self._categories[category]:
            self._categories[category].append(skill.name)

    def unregister_skill(self, name: str) -> bool:
        """Unregister a skill."""
        if name not in self._skills:
            return False

        skill = self._skills.pop(name)
        category = skill.config.category
        if category in self._categories and name in self._categories[category]:
            self._categories[category].remove(name)

        return True

    def get_skill(self, name: str) -> Optional[Skill]:
        """Get a skill by name."""
        return self._skills.get(name)

    def list_skills(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all skills or skills in a category."""
        if category:
            skill_names = self._categories.get(category, [])
        else:
            skill_names = list(self._skills.keys())

        return [
            {
                "name": name,
                "description": self._skills[name].description,
                "category": self._skills[name].config.category,
                "version": self._skills[name].config.version,
            }
            for name in skill_names
            if name in self._skills
        ]

    def execute_skill(
        self,
        name: str,
        params: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> SkillExecutionResult:
        """Execute a skill by name."""
        skill = self.get_skill(name)
        if skill is None:
            raise SkillNotFoundError(f"Skill not found: {name}")

        return skill.execute(params, context)

    def get_categories(self) -> List[str]:
        """Get all skill categories."""
        return list(self._categories.keys())

    def get_skill_schema(self, name: str) -> Optional[Dict[str, Any]]:
        """Get JSON schema for skill parameters."""
        skill = self.get_skill(name)
        if skill is None:
            return None

        return {
            "name": skill.config.name,
            "description": skill.config.description,
            "parameters": skill.config.parameters,
        }
