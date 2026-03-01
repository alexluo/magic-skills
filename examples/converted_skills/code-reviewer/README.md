# code-reviewer

Converted from Anthropic Skills to Magic Skills

## Original Description
Review code for best practices, bugs, and improvements

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
magic-skill exec code-reviewer -p '{"code": "def hello(): pass"}'
```

### Python
```python
from src.core.skill_manager import SkillManager

sm = SkillManager()
sm.load_all_skills()
result = sm.execute_skill("code-reviewer", {
    "code": "your code here",
    "language": "python"
})
print(result["review"])
print(f"Score: {result['score']}/10")
```

### REST API
```bash
curl -X POST http://localhost:3000/api/skills/execute \
  -H "Content-Type: application/json" \
  -d '{
    "skill_name": "code-reviewer",
    "params": {"code": "def hello(): pass"}
  }'
```

## Files

- `skill.yaml` - Skill metadata and schemas
- `prompt.txt` - Original Anthropic instructions
- `handler.py` - Enhanced Python implementation

## License

Original: Anthropic Skills License  
Enhancements: MIT License
