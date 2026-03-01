"""Tests for SkillManager."""

import pytest
import tempfile
import shutil
from pathlib import Path

from src.core.skill_manager import SkillManager


@pytest.fixture
def temp_skills_dir():
    """Create temporary skills directory."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def skill_manager(temp_skills_dir):
    """Create SkillManager instance."""
    return SkillManager(skills_dir=temp_skills_dir)


def test_get_skill(skill_manager, temp_skills_dir):
    """Test getting a skill."""
    # Create a test skill
    skill_dir = Path(temp_skills_dir) / "test-skill"
    skill_dir.mkdir()

    skill_yaml = skill_dir / "skill.yaml"
    skill_yaml.write_text("""
name: test-skill
description: A test skill
version: 1.0.0
author: Test
parameters:
  type: object
  properties:
    input:
      type: string
  required: [input]
""")

    prompt_txt = skill_dir / "prompt.txt"
    prompt_txt.write_text("Test prompt: {input}")

    handler_py = skill_dir / "handler.py"
    handler_py.write_text("""
def execute(params, context=None):
    return f"Result: {params.get('input', '')}"
""")

    # Load the skill
    skill_manager._load_skill_from_dir(skill_dir)
    skill = skill_manager.get_skill("test-skill")

    assert skill is not None
    assert skill.name == "test-skill"
    assert skill.description == "A test skill"


def test_list_skills(skill_manager, temp_skills_dir):
    """Test listing skills."""
    # Create test skills
    for name in ["skill-a", "skill-b"]:
        skill_dir = Path(temp_skills_dir) / name
        skill_dir.mkdir()

        skill_yaml = skill_dir / "skill.yaml"
        skill_yaml.write_text(f"""
name: {name}
description: Test {name}
version: 1.0.0
""")

        prompt_txt = skill_dir / "prompt.txt"
        prompt_txt.write_text("Test")

        handler_py = skill_dir / "handler.py"
        handler_py.write_text("def execute(p, c=None): return 'ok'")

        skill_manager._load_skill_from_dir(skill_dir)

    skills = skill_manager.list_skills()

    assert len(skills) == 2
    skill_names = [s["name"] for s in skills]
    assert "skill-a" in skill_names
    assert "skill-b" in skill_names


def test_execute_skill(skill_manager, temp_skills_dir):
    """Test executing a skill."""
    # Create a test skill
    skill_dir = Path(temp_skills_dir) / "echo"
    skill_dir.mkdir()

    skill_yaml = skill_dir / "skill.yaml"
    skill_yaml.write_text("""
name: echo
description: Echo skill
version: 1.0.0
parameters:
  type: object
  properties:
    message:
      type: string
  required: [message]
""")

    prompt_txt = skill_dir / "prompt.txt"
    prompt_txt.write_text("Echo: {message}")

    handler_py = skill_dir / "handler.py"
    handler_py.write_text("""
def execute(params, context=None):
    return params.get('message', '')
""")

    skill_manager._load_skill_from_dir(skill_dir)

    # Execute
    result = skill_manager.execute_skill("echo", {"message": "hello"})

    assert result.success is True
    assert result.data == "hello"


def test_get_skill_schema(skill_manager, temp_skills_dir):
    """Test getting skill schema."""
    # Create a test skill
    skill_dir = Path(temp_skills_dir) / "info-test"
    skill_dir.mkdir()

    skill_yaml = skill_dir / "skill.yaml"
    skill_yaml.write_text("""
name: info-test
description: Info test skill
version: 2.0.0
author: Tester
category: test
tags: [test, demo]
parameters:
  type: object
  properties:
    input:
      type: string
""")

    prompt_txt = skill_dir / "prompt.txt"
    prompt_txt.write_text("Test")

    handler_py = skill_dir / "handler.py"
    handler_py.write_text("def execute(p, c=None): return 'ok'")

    skill_manager._load_skill_from_dir(skill_dir)

    schema = skill_manager.get_skill_schema("info-test")

    assert schema["name"] == "info-test"
    assert schema["description"] == "Info test skill"
