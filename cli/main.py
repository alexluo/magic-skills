"""CLI main module."""

import asyncio
import json
import os
import shutil
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.table import Table

from src.core.skill_manager import SkillManager, SkillNotFoundError
from src.models.model_manager import ModelManager

console = Console()


@click.group()
@click.option("--skills-dir", type=click.Path(), help="Skills directory")
@click.pass_context
def cli(ctx, skills_dir):
    """Magic Skills CLI - AI-powered skill platform."""
    ctx.ensure_object(dict)
    ctx.obj["skill_manager"] = SkillManager(skills_dir)
    ctx.obj["skill_manager"].load_all_skills()
    ctx.obj["model_manager"] = ModelManager()


@cli.command()
@click.argument("skill_name")
@click.option("--params", "-p", help="JSON parameters")
@click.option("--model", "-m", help="LLM model to use")
@click.pass_context
def exec(ctx, skill_name: str, params: Optional[str], model: Optional[str]):
    """Execute a skill."""
    skill_manager = ctx.obj["skill_manager"]

    try:
        params_dict = json.loads(params) if params else {}
        result = skill_manager.execute_skill(skill_name, params_dict)

        if result.success:
            console.print("[green]✓ Success[/green]")
            console.print(result.data)
        else:
            console.print(f"[red]✗ Error: {result.error}[/red]")
    except SkillNotFoundError:
        console.print(f"[red]Skill not found: {skill_name}[/red]")
    except json.JSONDecodeError:
        console.print("[red]Invalid JSON parameters[/red]")


@cli.command()
@click.option("--category", "-c", help="Filter by category")
@click.pass_context
def list(ctx, category: Optional[str]):
    """List all available skills."""
    skill_manager = ctx.obj["skill_manager"]
    skills = skill_manager.list_skills(category)

    if not skills:
        console.print("No skills found.")
        return

    table = Table(title="Available Skills")
    table.add_column("Name", style="cyan")
    table.add_column("Description", style="white")
    table.add_column("Category", style="green")

    for skill in skills:
        table.add_row(skill["name"], skill["description"], skill["category"])

    console.print(table)


@cli.command()
@click.argument("skill_name")
@click.pass_context
def info(ctx, skill_name: str):
    """Show skill information."""
    skill_manager = ctx.obj["skill_manager"]
    skill = skill_manager.get_skill(skill_name)

    if not skill:
        console.print(f"[red]Skill not found: {skill_name}[/red]")
        return

    console.print(f"[bold cyan]{skill.config.name}[/bold cyan]")
    console.print(f"Description: {skill.config.description}")
    console.print(f"Version: {skill.config.version}")
    console.print(f"Category: {skill.config.category}")
    console.print(f"Author: {skill.config.author}")

    if skill.config.tags:
        console.print(f"Tags: {', '.join(skill.config.tags)}")


@cli.command()
@click.argument("tool", required=False, default="global")
@click.option("--force", "-f", is_flag=True, help="Overwrite existing configuration")
def init(tool: str, force: bool):
    """Initialize Magic Skills for AI Tools.
    
    TOOL can be: kiro, cursor, claude, windsurf, or global (default)
    
    Examples:
        magic-skill init              # Initialize global config
        magic-skill init kiro         # Initialize for Kiro IDE
        magic-skill init cursor       # Initialize for Cursor
        magic-skill init claude       # Initialize for Claude Desktop
        magic-skill init windsurf     # Initialize for Windsurf
    """
    # 获取当前工作目录（项目目录）
    cwd = Path.cwd()
    
    # 创建隐藏的 .magic-skills 父文件夹
    magic_skills_dir = cwd / ".magic-skills"
    magic_skills_dir.mkdir(exist_ok=True)
    
    # 创建项目配置文件（不包含 LLM 信息）
    config_file = magic_skills_dir / "config.json"
    if not config_file.exists() or force:
        config = {
            "skills_dir": str(magic_skills_dir / "skills"),
            "initialized_tools": [],
            "version": "1.0.0"
        }
        with open(config_file, "w") as f:
            json.dump(config, f, indent=2)
        console.print(f"[green]✓ Created project config at {config_file}[/green]")
    
    # 根据工具类型初始化
    tool = tool.lower()
    
    if tool == "kiro":
        _init_kiro(magic_skills_dir, force)
    elif tool == "cursor":
        _init_cursor(magic_skills_dir, force)
    elif tool == "claude":
        _init_claude(magic_skills_dir, force)
    elif tool == "windsurf":
        _init_windsurf(magic_skills_dir, force)
    elif tool == "global":
        _init_global_config(magic_skills_dir, force)
    else:
        console.print(f"[red]Unknown tool: {tool}[/red]")
        console.print("Supported tools: kiro, cursor, claude, windsurf, global")
        return
    
    # 复制 skills 到 .magic-skills/skills 目录
    _copy_skills_to_project(magic_skills_dir, force)
    
    console.print(f"\n[bold green]✓ Initialization complete for {tool}![/bold green]")
    console.print(f"Skills are available at: {magic_skills_dir / 'skills'}")
    console.print(f"Configuration created in: {magic_skills_dir}")


def _init_kiro(magic_skills_dir: Path, force: bool):
    """Initialize Kiro IDE configuration for Skills Auto-Optimization."""
    # 获取项目根目录（.magic-skills 的父目录）
    project_root = magic_skills_dir.parent

    kiro_dir = magic_skills_dir / ".kiro"
    kiro_dir.mkdir(exist_ok=True)

    # MCP 配置 - Kiro 直接使用 Skills 进行自动优化
    mcp_config = {
        "mcpServers": {
            "magic-skills": {
                "command": "python",
                "args": ["-m", "src.mcp.server"],
                "env": {
                    "PYTHONPATH": str(magic_skills_dir),
                    "SKILLS_DIR": str(magic_skills_dir / "skills")
                },
                "workingDirectory": str(magic_skills_dir),
                "disabled": False,
                "autoApprove": ["execute_skill", "list_skills", "get_skill_info"]
            }
        }
    }

    mcp_file = kiro_dir / "mcp.json"
    if not mcp_file.exists() or force:
        with open(mcp_file, "w") as f:
            json.dump(mcp_config, f, indent=2)
        console.print(f"[green]✓ Created Kiro MCP config: {mcp_file}[/green]")

    # Settings 配置 - 优化 Skills 自动执行
    # 路径相对于项目根目录
    settings_config = {
        "kiro": {
            "spec": {
                "enabled": True,
                "specFile": ".magic-skills/.kiro/spec.md"
            },
            "mcp": {
                "enabled": True,
                "configFile": ".magic-skills/.kiro/mcp.json",
                "autoExecute": True
            },
            "skills": {
                "autoSuggest": True,
                "showInlineHints": True,
                "autoExecute": True,
                "inlineCompletion": True,
                "contextAware": True
            },
            "features": {
                "codeCompletion": True,
                "inlineChat": True,
                "skillExecution": True,
                "contextAwareness": True,
                "autoOptimization": True
            }
        }
    }

    settings_file = kiro_dir / "settings.json"
    if not settings_file.exists() or force:
        with open(settings_file, "w") as f:
            json.dump(settings_config, f, indent=2)
        console.print(f"[green]✓ Created Kiro settings: {settings_file}[/green]")

    # Spec 文档 - 说明 Skills 自动优化功能
    spec_content = """# Magic Skills - Kiro 自动优化配置

## 概述

本配置启用 Kiro IDE 的 **Skills 自动优化** 功能。Kiro 将直接调用本地 Skills 进行代码生成、优化和重构，无需额外配置 LLM。

## 自动优化功能

当您在 Kiro 中编写代码时，系统会自动：

1. **智能识别意图** - 根据代码上下文识别开发意图
2. **自动匹配 Skills** - 从 160+ Skills 中选择最合适的工具
3. **即时执行优化** - 自动调用 Skill 生成或优化代码
4. **无缝集成** - 优化结果直接插入编辑器

## 使用方法

### 方式一：自动触发（推荐）
直接编写代码，Kiro 会自动识别并应用最佳 Skills：
- 输入 `public class UserController` → 自动生成完整 Controller
- 输入测试方法名 → 自动生成单元测试
- 选中代码 → 自动提示优化建议

### 方式二：手动触发
输入 `/mgc-` 查看可用 Skills：
```
/mgc-java-backend-controller-gen endpoint=/api/users
/mgc-unit-test-gen function=myFunction
/mgc-code-review-java
```

## 可用 Skills 分类

- **Java Backend** (40+) - Controller/Service/DAO 生成、API 设计
- **Android OS** (30+) - AOSP 开发、系统服务、HAL 层
- **Digital Analytics** (25+) - GA4/GTM/CDP 代码生成
- **Mobile App** (35+) - iOS/Android/Flutter 开发
- **Translation** (20+) - 多语言内容生成
- **Testing** (20+) - 单元测试、集成测试、代码审查

## Skills 目录

所有 Skills 位于：`./skills/`

Kiro 会自动读取并执行这些本地 Skills，实现真正的"自动优化"。
"""

    spec_file = kiro_dir / "spec.md"
    if not spec_file.exists() or force:
        with open(spec_file, "w") as f:
            f.write(spec_content)
        console.print(f"[green]✓ Created Kiro spec: {spec_file}[/green]")


def _init_cursor(magic_skills_dir: Path, force: bool):
    """Initialize Cursor configuration for Skills Auto-Optimization."""
    cursor_dir = magic_skills_dir / ".cursor"
    cursor_dir.mkdir(exist_ok=True)

    mcp_config = {
        "mcpServers": {
            "magic-skills": {
                "command": "python",
                "args": ["-m", "src.mcp.server"],
                "env": {
                    "PYTHONPATH": str(magic_skills_dir),
                    "SKILLS_DIR": str(magic_skills_dir / "skills")
                }
            }
        }
    }

    mcp_file = cursor_dir / "mcp.json"
    if not mcp_file.exists() or force:
        with open(mcp_file, "w") as f:
            json.dump(mcp_config, f, indent=2)
        console.print(f"[green]✓ Created Cursor MCP config: {mcp_file}[/green]")

    # 创建使用说明
    readme_file = cursor_dir / "README.md"
    if not readme_file.exists() or force:
        readme_content = """# Magic Skills for Cursor

## Skills 自动优化

Cursor 将直接调用本地 Skills 进行代码生成和优化，无需配置 LLM。

## Usage

Type `/mgc-` in the chat to see available skills.

### Examples

- `/mgc-java-backend-controller-gen` - Generate Spring Boot controller
- `/mgc-unit-test-gen` - Generate unit tests
- `/mgc-code-review-java` - Review Java code

## Skills 目录

All skills are located at: `.magic-skills/skills/`
"""
        with open(readme_file, "w") as f:
            f.write(readme_content)
        console.print(f"[green]✓ Created Cursor README: {readme_file}[/green]")


def _init_claude(magic_skills_dir: Path, force: bool):
    """Initialize Claude Desktop configuration for Skills Auto-Optimization."""
    # Claude Desktop 配置在用户目录（这是特殊的设计）
    claude_dir = Path.home() / "Library/Application Support/Claude"
    claude_dir.mkdir(parents=True, exist_ok=True)

    mcp_config = {
        "mcpServers": {
            "magic-skills": {
                "command": "python",
                "args": ["-m", "src.mcp.server"],
                "env": {
                    "PYTHONPATH": str(magic_skills_dir),
                    "SKILLS_DIR": str(magic_skills_dir / "skills")
                }
            }
        }
    }

    mcp_file = claude_dir / "claude_desktop_config.json"
    if not mcp_file.exists() or force:
        with open(mcp_file, "w") as f:
            json.dump(mcp_config, f, indent=2)
        console.print(f"[green]✓ Created Claude Desktop config: {mcp_file}[/green]")
    else:
        # 合并配置
        try:
            with open(mcp_file, "r") as f:
                existing = json.load(f)
            if "mcpServers" not in existing:
                existing["mcpServers"] = {}
            existing["mcpServers"]["magic-skills"] = mcp_config["mcpServers"]["magic-skills"]
            with open(mcp_file, "w") as f:
                json.dump(existing, f, indent=2)
            console.print(f"[green]✓ Updated Claude Desktop config: {mcp_file}[/green]")
        except Exception as e:
            console.print(f"[yellow]Warning: Could not update Claude config: {e}[/yellow]")

    # 在 .magic-skills 目录创建说明
    readme_file = magic_skills_dir / "CLAUDE_INTEGRATION.md"
    if not readme_file.exists() or force:
        readme_content = """# Magic Skills for Claude Desktop

## Skills 自动优化

Claude Desktop 将直接调用本地 Skills 进行代码生成和优化，无需配置 LLM。

## Usage

In Claude Desktop, you can now use Magic Skills tools.

### Available Tools

- `mgc-command` - Execute any Magic Skill using `/mgc-<category>-<skill-name>` format

### Examples

Ask Claude:
- "Use /mgc-java-backend-controller-gen to create a user API"
- "Generate tests with /mgc-unit-test-gen"
- "Review this code with /mgc-code-review-java"

## Configuration

Claude Desktop configuration is stored in:
`~/Library/Application Support/Claude/claude_desktop_config.json`

## Skills 目录

All skills are located at: `.magic-skills/skills/`
"""
        with open(readme_file, "w") as f:
            f.write(readme_content)
        console.print(f"[green]✓ Created Claude integration guide: {readme_file}[/green]")


def _init_windsurf(magic_skills_dir: Path, force: bool):
    """Initialize Windsurf configuration for Skills Auto-Optimization."""
    windsurf_dir = magic_skills_dir / ".windsurf"
    windsurf_dir.mkdir(exist_ok=True)

    # Windsurf 使用类似的 MCP 配置
    mcp_config = {
        "mcpServers": {
            "magic-skills": {
                "command": "python",
                "args": ["-m", "src.mcp.server"],
                "env": {
                    "PYTHONPATH": str(magic_skills_dir),
                    "SKILLS_DIR": str(magic_skills_dir / "skills")
                }
            }
        }
    }

    mcp_file = windsurf_dir / "mcp.json"
    if not mcp_file.exists() or force:
        with open(mcp_file, "w") as f:
            json.dump(mcp_config, f, indent=2)
        console.print(f"[green]✓ Created Windsurf MCP config: {mcp_file}[/green]")

    # 配置 - 启用 Skills 自动优化
    config = {
        "ai": {
            "enabled": True,
            "skills": {
                "autoSuggest": True,
                "showInlineHints": True,
                "autoExecute": True,
                "inlineCompletion": True
            }
        }
    }

    config_file = windsurf_dir / "config.json"
    if not config_file.exists() or force:
        with open(config_file, "w") as f:
            json.dump(config, f, indent=2)
        console.print(f"[green]✓ Created Windsurf config: {config_file}[/green]")


def _init_global_config(magic_skills_dir: Path, force: bool):
    """Initialize global configuration only (no LLM info)."""
    config_file = magic_skills_dir / "config.json"
    if not config_file.exists() or force:
        config = {
            "skills_dir": str(magic_skills_dir / "skills"),
            "initialized_tools": [],
            "version": "1.0.0"
        }
        with open(config_file, "w") as f:
            json.dump(config, f, indent=2)
        console.print(f"[green]✓ Created project config: {config_file}[/green]")
    else:
        console.print(f"[yellow]Project config already exists: {config_file}[/yellow]")


def _copy_skills_to_project(project_dir: Path, force: bool):
    """Copy converted SKILL.md files to project directory."""
    # 查找原始 skills 目录（包含转换后的 SKILL.md）
    possible_skills_dirs = [
        # 开发环境：从项目根目录的 skills
        Path(__file__).parent.parent / "skills",
        Path(__file__).parent.parent.parent / "skills",
    ]
    
    source_skills_dir = None
    for d in possible_skills_dirs:
        if d.exists() and d.is_dir():
            # 验证目录中是否有 SKILL.md 文件
            if any(d.rglob("SKILL.md")):
                source_skills_dir = d
                break
    
    if not source_skills_dir:
        console.print("[yellow]Warning: Could not find skills directory with SKILL.md files[/yellow]")
        console.print("[yellow]Please run 'python scripts/convert_skills.py' first[/yellow]")
        return
    
    target_skills_dir = project_dir / "skills"
    
    if target_skills_dir.exists() and not force:
        console.print(f"[yellow]Skills already exist at {target_skills_dir}[/yellow]")
        console.print("Use --force to overwrite")
        return
    
    # 复制转换后的 skills（只复制 SKILL.md）
    if target_skills_dir.exists():
        shutil.rmtree(target_skills_dir)
    
    target_skills_dir.mkdir(parents=True, exist_ok=True)
    
    # 只复制 SKILL.md 文件，保持目录结构
    skill_count = 0
    for skill_md in source_skills_dir.rglob("SKILL.md"):
        # 计算相对路径
        rel_path = skill_md.relative_to(source_skills_dir)
        target_path = target_skills_dir / rel_path
        target_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 复制文件
        shutil.copy2(skill_md, target_path)
        skill_count += 1
    
    console.print(f"[green]✓ Copied {skill_count} SKILL.md files to {target_skills_dir}[/green]")
    
    # 创建 SKILL_INDEX.md 供 AI 工具快速索引
    _create_skill_index(target_skills_dir)


def _create_skill_index(skills_dir: Path):
    """Create SKILL_INDEX.md for AI tools to quickly discover available skills."""
    index_file = skills_dir / "SKILL_INDEX.md"
    
    skills_list = []
    for skill_md in skills_dir.rglob("SKILL.md"):
        rel_path = skill_md.relative_to(skills_dir)
        category = rel_path.parts[0] if len(rel_path.parts) > 1 else "general"
        
        # 读取 frontmatter
        content = skill_md.read_text(encoding='utf-8')
        frontmatter = {}
        if content.startswith('---'):
            end = content.find('---', 3)
            if end != -1:
                import yaml
                try:
                    frontmatter = yaml.safe_load(content[3:end])
                except:
                    pass
        
        skills_list.append({
            'name': frontmatter.get('name', skill_md.parent.name),
            'description': frontmatter.get('description', ''),
            'category': frontmatter.get('category', category),
            'path': str(rel_path),
            'usage_count': frontmatter.get('usage_count', 0),
            'success_rate': frontmatter.get('success_rate', 0),
        })
    
    # 按类别分组
    by_category = {}
    for skill in skills_list:
        cat = skill['category']
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(skill)
    
    # 生成索引内容
    index_content = f"""# Magic Skills 索引

> 本文件由系统自动生成，供 AI 工具快速发现可用 Skills
> 总 Skills 数量: {len(skills_list)}

## 快速使用指南

AI 工具应读取此索引来：
1. **发现可用 Skills** - 根据用户意图匹配最合适的 Skill
2. **查看使用统计** - 优先推荐成功率高的 Skills
3. **自动执行优化** - 根据上下文自动触发相关 Skills

## 按类别分类

"""
    
    for category in sorted(by_category.keys()):
        skills = by_category[category]
        index_content += f"\n### {category} ({len(skills)} 个)\n\n"
        
        for skill in sorted(skills, key=lambda x: x['success_rate'], reverse=True):
            index_content += f"- **{skill['name']}** - {skill['description']}\n"
            index_content += f"  - 路径: `{skill['path']}`\n"
            if skill['success_rate'] > 0:
                index_content += f"  - 成功率: {skill['success_rate']}% | 使用次数: {skill['usage_count']}\n"
    
    index_content += """

## 自动匹配规则

当用户输入以下意图时，自动触发对应 Skill：

"""
    
    # 添加一些常见的触发规则示例
    for category in ['java-backend', 'software-testing', 'android-os', 'mobile-app']:
        if category in by_category:
            index_content += f"\n### {category}\n"
            for skill in by_category[category][:3]:  # 每个类别取前3个
                index_content += f"- `{skill['name']}`: {skill['description']}\n"
    
    index_content += """

---

*本索引文件由 magic-skill init 自动生成*
*更新 Skills 后请重新运行 `magic-skill init <tool> --force`*
"""
    
    index_file.write_text(index_content, encoding='utf-8')
    console.print(f"[green]✓ Created SKILL_INDEX.md with {len(skills_list)} skills[/green]")


@cli.command()
def version():
    """Show version information."""
    console.print("Magic Skills v1.0.0")


if __name__ == "__main__":
    cli()
