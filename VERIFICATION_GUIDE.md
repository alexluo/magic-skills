# Magic Skills 功能验证指南

本指南帮助你全面验证 Magic Skills 项目的所有功能和 Skills。

## 验证清单

### 1. 环境检查

```bash
# 检查 Python 版本
python3 --version  # 需要 3.9+

# 检查虚拟环境
source venv/bin/activate
which python

# 检查依赖安装
pip list | grep -E "(fastapi|typer|httpx|pydantic|pytest)"
```

### 2. 核心模块验证

#### 2.1 技能管理器验证

```bash
# 进入 Python 交互模式
python3 << 'EOF'
from src.core.skill_manager import SkillManager

# 创建管理器实例
sm = SkillManager()

# 加载所有技能
count = sm.load_all_skills()
print(f"✅ 已加载 {count} 个技能")

# 列出所有技能
skills = sm.list_skills()
print(f"✅ 技能列表: {len(skills)} 个")

# 获取技能信息
if skills:
    info = sm.get_skill_schema(skills[0]["name"])
    print(f"✅ 技能详情: {info}")

print("✅ SkillManager 验证通过")
EOF
```

#### 2.2 LLM 提供商验证

```bash
# 测试所有 LLM 提供商
python3 << 'EOF'
from src.models import ModelManager

mm = ModelManager()

# 列出所有提供商
providers = mm.list_providers()
print(f"✅ 提供商数量: {len(providers)}")
for p in providers:
    print(f"  - {p}")

# 测试模型列表
for provider in ["openai", "anthropic", "google"]:
    try:
        models = mm.list_models(provider)
        print(f"✅ {provider}: {len(models)} 个模型")
    except Exception as e:
        print(f"⚠️ {provider}: {e}")

print("✅ ModelManager 验证通过")
EOF
```

#### 2.3 自我优化引擎验证

```bash
python3 << 'EOF'
from src.optimization import PromptOptimizer, ModelSelector, FeedbackProcessor, ABTester

# PromptOptimizer
po = PromptOptimizer()
result = po.optimize_prompt("test", "prompt", [{"rating": 2, "comment": "unclear"}], "auto")
print("✅ PromptOptimizer 工作正常")

# ModelSelector
ms = ModelSelector()
result = ms.select_model("code-generation", "balanced")
print(f"✅ ModelSelector 推荐: {result['provider']}/{result['model']}")

# FeedbackProcessor
fp = FeedbackProcessor(feedback_dir="/tmp/test_feedback")
fp.record_feedback("test-skill", 5, "Great!")
analysis = fp.analyze_feedback("test-skill")
print(f"✅ FeedbackProcessor: {analysis['total_feedback']} 条反馈")

# ABTester
ab = ABTester(tests_dir="/tmp/test_ab")
test_id = ab.create_test("test", {"a": 1}, {"b": 2}, sample_size=10)
variant = ab.assign_variant(test_id)
print(f"✅ ABTester: 分配到变体 {variant}")

print("✅ 自我优化引擎验证通过")
EOF
```

### 3. 接口层验证

#### 3.1 CLI 验证

```bash
# 测试 CLI 帮助
magic-skill --help

# 列出所有技能
magic-skill list

# 获取特定领域技能
magic-skill list --category java-backend

# 测试技能信息
magic-skill info spring-boot-controller-gen

# 执行技能（需要 API Key）
# export OPENAI_API_KEY="your-key"
# magic-skill exec spring-boot-controller-gen -p '{"input": "test"}'
```

#### 3.2 REST API 验证

```bash
# 启动 API 服务器（后台运行）
python -m api.main &
API_PID=$!
sleep 2

# 健康检查
curl -s http://localhost:3000/health | jq .

# 列出技能
curl -s http://localhost:3000/api/skills/list | jq '. | length'

# 获取技能详情
curl -s http://localhost:3000/api/skills/info/spring-boot-controller-gen | jq .

# 列出模型
curl -s http://localhost:3000/api/models/list | jq .

# 执行技能（需要 API Key）
# curl -X POST http://localhost:3000/api/skills/execute \
#   -H "Content-Type: application/json" \
#   -H "X-API-Key: your-key" \
#   -d '{"skill_name": "unit-test-gen", "params": {"input": "def add(a,b): return a+b"}}'

# 停止 API 服务器
kill $API_PID
```

#### 3.3 MCP Server 验证

```bash
# 检查 MCP Server 配置
cat .cursor/mcp.json
cat claude_desktop_config.json

# 测试 MCP Server 启动
python -m src.mcp.server --help
```

### 4. Skills 验证

#### 4.1 批量验证所有 Skills

```bash
python3 << 'EOF'
from src.core.skill_manager import SkillManager
from pathlib import Path

sm = SkillManager()
sm.load_all_skills()

# 按领域统计
from collections import defaultdict
domain_stats = defaultdict(int)
incomplete = []

for skill_info in sm.list_skills():
    name = skill_info["name"]
    category = skill_info["category"]
    domain_stats[category] += 1
    
    # 检查技能完整性
    skill = sm.get_skill(name)
    if not skill:
        incomplete.append(f"{name}: 无法加载")
        continue
    
    if not skill.prompt_template:
        incomplete.append(f"{name}: 缺少 prompt")

# 打印统计
print("=" * 60)
print("📊 Skills 统计")
print("=" * 60)
for domain, count in sorted(domain_stats.items()):
    print(f"✅ {domain}: {count} 个技能")

print(f"\n总计: {sum(domain_stats.values())} 个技能")

if incomplete:
    print(f"\n⚠️ 不完整技能: {len(incomplete)}")
    for item in incomplete[:10]:
        print(f"  - {item}")
else:
    print("\n✅ 所有技能结构完整")
EOF
```

#### 4.2 测试特定领域 Skills

```bash
# Java 后端技能测试
python3 << 'EOF'
from src.core.skill_manager import SkillManager

sm = SkillManager()
sm.load_all_skills()

java_skills = [s for s in sm.list_skills() if s["category"] == "java-backend"]
print(f"Java 后端技能: {len(java_skills)} 个")
for skill in java_skills[:5]:
    print(f"  - {skill['name']}: {skill['description']}")
EOF

# 测试其他领域...
```

### 5. AI 工具集成验证

#### 5.1 Cursor 集成

```bash
# 检查配置文件
ls -la .cursor/mcp.json

# 验证配置格式
cat .cursor/mcp.json | python3 -m json.tool
```

#### 5.2 Claude Desktop 集成

```bash
# 检查配置文件
ls -la claude_desktop_config.json

# 验证配置格式
cat claude_desktop_config.json | python3 -m json.tool
```

#### 5.3 VS Code 扩展

```bash
# 检查扩展文件
ls -la extensions/vscode/
ls -la extensions/vscode/package.json
ls -la extensions/vscode/src/extension.ts
```

### 6. 测试套件运行

```bash
# 运行所有测试
pytest -v

# 运行特定测试
pytest tests/test_skill_manager.py -v
pytest tests/test_optimization.py -v
pytest tests/test_model_manager.py -v

# 生成覆盖率报告
pytest --cov=src --cov-report=html
```

### 7. 端到端验证

#### 7.1 完整工作流测试

```bash
#!/bin/bash
set -e

echo "🧪 开始端到端验证..."

# 1. 环境检查
echo "✓ 检查环境..."
source venv/bin/activate

# 2. 加载技能
echo "✓ 加载技能..."
python3 -c "
from src.core.skill_manager import SkillManager
sm = SkillManager()
count = sm.load_all_skills()
assert count >= 160, f'技能数量不足: {count}'
print(f'✅ 已加载 {count} 个技能')
"

# 3. 测试 CLI
echo "✓ 测试 CLI..."
magic-skill list > /dev/null
magic-skill info spring-boot-controller-gen > /dev/null

# 4. 启动 API 并测试
echo "✓ 测试 API..."
python -m api.main &
API_PID=$!
sleep 3

curl -sf http://localhost:3000/health > /dev/null
curl -sf http://localhost:3000/api/skills/list > /dev/null

kill $API_PID

echo "✅ 端到端验证通过！"
```

### 8. 性能验证

```bash
# 技能加载性能
python3 << 'EOF'
import time
from src.core.skill_manager import SkillManager

start = time.time()
sm = SkillManager()
count = sm.load_all_skills()
elapsed = time.time() - start

print(f"加载 {count} 个技能耗时: {elapsed:.2f} 秒")
print(f"平均每个技能: {elapsed/count*1000:.2f} 毫秒")
EOF
```

### 9. 验证报告生成

```bash
# 生成完整验证报告
python3 << 'EOF'
from src.core.skill_manager import SkillManager
from src.models import ModelManager
from pathlib import Path
import json

report = {
    "project": "Magic Skills",
    "version": "1.0.0",
    "checks": {}
}

# 技能检查
sm = SkillManager()
skill_count = sm.load_all_skills()
report["checks"]["skills"] = {
    "total": skill_count,
    "expected": 160,
    "passed": skill_count >= 160
}

# 提供商检查
mm = ModelManager()
providers = mm.list_providers()
report["checks"]["providers"] = {
    "total": len(providers),
    "expected": 11,
    "passed": len(providers) >= 11,
    "list": providers
}

# 文件检查
report["checks"]["files"] = {
    "readme": Path("README.md").exists(),
    "cli": Path("cli/main.py").exists(),
    "api": Path("api/main.py").exists(),
    "mcp": Path("src/mcp/server.py").exists(),
}

print(json.dumps(report, indent=2, ensure_ascii=False))
EOF
```

## 常见问题排查

### 技能加载失败

```bash
# 检查技能文件完整性
find skills -name "skill.yaml" | wc -l
find skills -name "handler.py" | wc -l
find skills -name "prompt.txt" | wc -l

# 检查 YAML 格式
python3 -c "
import yaml
from pathlib import Path
errors = []
for f in Path('skills').rglob('skill.yaml'):
    try:
        yaml.safe_load(f.read_text())
    except Exception as e:
        errors.append(f'{f}: {e}')
if errors:
    print('YAML 错误:')
    for e in errors[:5]:
        print(f'  {e}')
else:
    print('✅ 所有 YAML 文件格式正确')
"
```

### API 启动失败

```bash
# 检查端口占用
lsof -i :3000

# 检查依赖
pip show fastapi uvicorn

# 查看错误日志
python -m api.main 2>&1 | head -20
```

### 测试失败

```bash
# 详细输出
pytest -v --tb=long

# 只运行特定测试
pytest tests/test_skill_manager.py::test_get_skill -v
```

## 验证完成标准

- [ ] 所有 160+ 技能已加载
- [ ] 所有 12 个 LLM 提供商可用
- [ ] CLI 命令正常执行
- [ ] API 服务器正常启动
- [ ] MCP Server 配置正确
- [ ] 所有测试通过
- [ ] 文档完整

完成以上验证后，项目即可投入使用！
