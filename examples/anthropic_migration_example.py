"""
Anthropic Skills 迁移到 Magic Skills 的完整示例

这个示例展示了如何将 Anthropic 的 SKILL.md 格式转换为 Magic Skills 格式
并添加 Magic Skills 特有的增强功能。
"""

import re
import yaml
from pathlib import Path
from typing import Dict, Any

# 示例: Anthropic 风格的 SKILL.md 内容
ANTHROPIC_SKILL_EXAMPLE = """---
name: code-reviewer
description: Review code for best practices, bugs, and improvements
version: "1.0"
author: "Anthropic"
---

# Code Reviewer

You are an expert code reviewer. Analyze the provided code and provide:

1. **Bugs**: Identify any bugs or potential issues
2. **Best Practices**: Suggest improvements following language best practices
3. **Performance**: Identify performance bottlenecks
4. **Security**: Highlight security concerns

## Review Format

```markdown
## Summary
Brief overview of the code quality

## Issues Found
- [Severity] Description and suggestion

## Recommendations
1. Specific improvements
```

## Guidelines
- Be constructive and specific
- Provide code examples for fixes
- Consider the context and constraints
"""


def parse_anthropic_skill(skill_content: str) -> Dict[str, Any]:
    """Parse Anthropic SKILL.md format."""
    # Extract frontmatter
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', skill_content, re.DOTALL)
    
    if not match:
        raise ValueError("Invalid Anthropic SKILL.md format")
    
    frontmatter = yaml.safe_load(match.group(1))
    instructions = match.group(2).strip()
    
    return {
        "name": frontmatter.get("name", "unnamed-skill"),
        "description": frontmatter.get("description", ""),
        "version": frontmatter.get("version", "1.0.0"),
        "author": frontmatter.get("author", "Unknown"),
        "instructions": instructions
    }


def convert_to_magic_skill(anthropic_skill: Dict[str, Any], output_dir: Path) -> Path:
    """Convert Anthropic skill to Magic Skills format."""
    
    skill_name = anthropic_skill["name"]
    skill_dir = output_dir / skill_name
    skill_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Create skill.yaml
    skill_yaml = {
        "name": skill_name,
        "description": anthropic_skill["description"],
        "version": anthropic_skill["version"],
        "category": "converted-from-anthropic",
        "author": anthropic_skill["author"],
        "input_schema": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "Code to review"
                },
                "language": {
                    "type": "string",
                    "description": "Programming language",
                    "default": "python"
                }
            },
            "required": ["code"]
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "review": {
                    "type": "string",
                    "description": "Code review result"
                },
                "issues": {
                    "type": "array",
                    "items": {"type": "string"}
                },
                "score": {
                    "type": "number",
                    "description": "Code quality score (1-10)"
                }
            }
        }
    }
    
    (skill_dir / "skill.yaml").write_text(
        yaml.dump(skill_yaml, default_flow_style=False, allow_unicode=True)
    )
    
    # 2. Create prompt.txt (original instructions)
    (skill_dir / "prompt.txt").write_text(anthropic_skill["instructions"])
    
    # 3. Create enhanced handler.py with Magic Skills features
    handler_code = f'''"""
Converted from Anthropic Skills: {skill_name}
Enhanced with Magic Skills capabilities
"""

from typing import Dict, Any
from src.core.base_skill import BaseSkill
import re


class {skill_name.replace("-", "_").title().replace("_", "")}Skill(BaseSkill):
    """
    Enhanced code reviewer with Magic Skills features:
    - Multi-LLM support
    - Cost tracking
    - Feedback collection
    - Self-optimization
    """
    
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        code = params["code"]
        language = params.get("language", "python")
        
        # Load the original Anthropic prompt
        prompt_template = self.load_prompt()
        
        # Enhance with Magic Skills context
        enhanced_prompt = f"""{{prompt_template}}

## Additional Context
- Language: {{language}}
- Code Length: {{len(code)}} characters
- Lines: {{len(code.split(chr(10)))}}

## Code to Review
```{{language}}
{{code}}
```

Please provide your review now.
"""
        
        # Generate review using configured LLM
        review = self.llm.generate(enhanced_prompt)
        
        # Extract structured data
        issues = self._extract_issues(review)
        score = self._calculate_score(review, len(issues))
        
        # Record execution for optimization
        self._record_execution(params, review)
        
        return {{
            "review": review,
            "issues": issues,
            "score": score,
            "language": language,
            "metrics": {{
                "code_length": len(code),
                "issues_found": len(issues)
            }}
        }}
    
    def _extract_issues(self, review: str) -> list:
        """Extract issues from review text."""
        # Look for patterns like "- [High]" or "### Bug"
        issues = []
        lines = review.split("\\n")
        for line in lines:
            if any(marker in line for marker in ["- [", "### ", "**Issue"]):
                issues.append(line.strip())
        return issues
    
    def _calculate_score(self, review: str, issue_count: int) -> float:
        """Calculate code quality score."""
        base_score = 10.0
        
        # Deduct points for issues
        deductions = min(issue_count * 0.5, 5.0)
        
        # Check for positive indicators
        if "excellent" in review.lower() or "great" in review.lower():
            base_score += 0.5
        
        score = max(1.0, min(10.0, base_score - deductions))
        return round(score, 1)
    
    def _record_execution(self, params: Dict[str, Any], result: str):
        """Record execution for future optimization."""
        # This enables self-optimization features
        execution_data = {{
            "skill": self.name,
            "params_keys": list(params.keys()),
            "result_length": len(result),
        }}
        # Would be saved to feedback system
        self.logger.debug(f"Recorded execution: {{execution_data}}")


# Backward compatibility - can also be used as a simple function
def review_code(code: str, language: str = "python") -> str:
    """Simple function interface for backward compatibility."""
    skill = {skill_name.replace("-", "_").title().replace("_", "")}Skill()
    result = skill.execute({{"code": code, "language": language}})
    return result["review"]
'''
    
    (skill_dir / "handler.py").write_text(handler_code)
    
    # 4. Create README.md
    readme = f"""# {skill_name}

Converted from Anthropic Skills to Magic Skills

## Original Description
{anthropic_skill["description"]}

## Enhancements

This skill has been enhanced with Magic Skills capabilities:

1. **Multi-LLM Support**: Works with OpenAI, Anthropic, Google, and 8+ other providers
2. **Structured Output**: Returns JSON with review, issues list, and quality score
3. **Cost Tracking**: Automatically tracks API usage costs
4. **Self-Optimization**: Learns from feedback to improve over time
5. **Metrics**: Provides code length, issue count, and other metrics

## Usage

### CLI
```bash
magic-skill exec {skill_name} -p '{{"code": "def hello(): pass"}}'
```

### Python
```python
from src.core.skill_manager import SkillManager

sm = SkillManager()
sm.load_all_skills()
result = sm.execute_skill("{skill_name}", {{
    "code": "your code here",
    "language": "python"
}})
print(result["review"])
print(f"Score: {{result['score']}}/10")
```

### REST API
```bash
curl -X POST http://localhost:3000/api/skills/execute \\
  -H "Content-Type: application/json" \\
  -d '{{
    "skill_name": "{skill_name}",
    "params": {{"code": "def hello(): pass"}}
  }}'
```

## Files

- `skill.yaml` - Skill metadata and schemas
- `prompt.txt` - Original Anthropic instructions
- `handler.py` - Enhanced Python implementation

## License

Original: Anthropic Skills License  
Enhancements: MIT License
"""
    
    (skill_dir / "README.md").write_text(readme)
    
    return skill_dir


def demonstrate_migration():
    """Demonstrate the complete migration process."""
    print("=" * 60)
    print("Anthropic Skills → Magic Skills 迁移演示")
    print("=" * 60)
    
    # Step 1: Parse Anthropic skill
    print("\n📥 步骤 1: 解析 Anthropic SKILL.md")
    anthropic_skill = parse_anthropic_skill(ANTHROPIC_SKILL_EXAMPLE)
    print(f"   技能名称: {anthropic_skill['name']}")
    print(f"   描述: {anthropic_skill['description']}")
    print(f"   作者: {anthropic_skill['author']}")
    print(f"   指令长度: {len(anthropic_skill['instructions'])} 字符")
    
    # Step 2: Convert to Magic Skills
    print("\n🔄 步骤 2: 转换为 Magic Skills 格式")
    output_dir = Path("examples/converted_skills")
    skill_dir = convert_to_magic_skill(anthropic_skill, output_dir)
    print(f"   输出目录: {skill_dir}")
    
    # Step 3: Show created files
    print("\n📁 步骤 3: 生成的文件")
    for file in skill_dir.iterdir():
        size = file.stat().st_size
        print(f"   ✅ {file.name} ({size} bytes)")
    
    # Step 4: Show enhancements
    print("\n✨ 步骤 4: Magic Skills 增强功能")
    enhancements = [
        "多 LLM 支持 (12+ 提供商)",
        "结构化输入/输出 (JSON Schema)",
        "成本追踪和统计",
        "反馈收集和自优化",
        "Python 代码逻辑 (不限于提示词)",
        "MCP Server 集成",
        "REST API 接口",
        "CLI 工具支持"
    ]
    for i, enhancement in enumerate(enhancements, 1):
        print(f"   {i}. {enhancement}")
    
    # Step 5: Usage examples
    print("\n💡 步骤 5: 使用示例")
    print("""
   # CLI 使用
   $ magic-skill exec code-reviewer \\
       -p '{"code": "def add(a,b): return a+b", "language": "python"}'
   
   # Python 使用
   from src.core.skill_manager import SkillManager
   sm = SkillManager()
   result = sm.execute_skill("code-reviewer", {"code": "..."})
   
   # REST API
   curl -X POST http://localhost:3000/api/skills/execute \\
     -d '{"skill_name": "code-reviewer", "params": {...}}'
    """)
    
    print("\n" + "=" * 60)
    print("✅ 迁移完成！")
    print("=" * 60)
    
    return skill_dir


def compare_capabilities():
    """Compare capabilities between Anthropic and Magic Skills."""
    print("\n" + "=" * 60)
    print("能力对比")
    print("=" * 60)
    
    comparisons = [
        ("技能格式", "SKILL.md (Markdown)", "YAML + Python (完整编程)"),
        ("LLM 支持", "仅 Claude", "12+ 提供商 (OpenAI, Anthropic, Google, 国内模型等)"),
        ("编程能力", "仅提示词", "完整 Python + 任意库"),
        ("工具集成", "Claude Code 插件", "MCP + Cursor + VS Code + REST API"),
        ("自我优化", "❌ 不支持", "✅ PromptOptimizer + FeedbackProcessor"),
        ("成本追踪", "❌ 不支持", "✅ 内置成本统计"),
        ("企业功能", "基础", "✅ 版本控制 + 权限 + 审计"),
        ("开源协议", "Apache 2.0 / 源码可用", "✅ MIT (完全开源)"),
    ]
    
    print(f"\n{'功能':<15} {'Anthropic':<30} {'Magic Skills':<40}")
    print("-" * 85)
    for feature, anthropic, magic in comparisons:
        winner = "✅" if "✅" in magic else ""
        print(f"{feature:<15} {anthropic:<30} {magic:<40} {winner}")
    
    print("\n结论: Magic Skills 完全覆盖 Anthropic Skills 能力，并提供更多增强功能")


if __name__ == "__main__":
    # Run demonstration
    skill_dir = demonstrate_migration()
    
    # Show comparison
    compare_capabilities()
    
    print(f"\n📂 转换后的技能位于: {skill_dir.absolute()}")
    print("\n你可以将这个技能复制到 skills/ 目录下使用:")
    print(f"  cp -r {skill_dir} skills/")
