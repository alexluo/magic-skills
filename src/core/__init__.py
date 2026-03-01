"""Core module for Magic Skills."""

from .skill_manager import (
    Skill,
    SkillConfig,
    SkillExecutionResult,
    SkillManager,
    SkillNotFoundError,
    SkillExecutionError,
)

__all__ = [
    "Skill",
    "SkillConfig",
    "SkillExecutionResult",
    "SkillManager",
    "SkillNotFoundError",
    "SkillExecutionError",
]