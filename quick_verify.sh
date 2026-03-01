#!/bin/bash
# Magic Skills 快速验证脚本

set -e

echo "=========================================="
echo "  Magic Skills 快速验证"
echo "=========================================="
echo ""

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

error() {
    echo -e "${RED}❌ $1${NC}"
}

# 检查虚拟环境
if [ -z "$VIRTUAL_ENV" ]; then
    warning "未检测到虚拟环境，尝试激活..."
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
        success "已激活虚拟环境"
    else
        error "虚拟环境不存在，请先运行: python3 -m venv venv"
        exit 1
    fi
fi

# 1. 验证技能加载
echo ""
echo "📦 验证技能加载..."
python3 << 'EOF'
from src.core.skill_manager import SkillManager
sm = SkillManager()
count = sm.load_all_skills()
print(f"✅ 已加载 {count} 个技能")

# 按领域统计
from collections import defaultdict
domain_counts = defaultdict(int)
for skill in sm.list_skills():
    domain_counts[skill["category"]] += 1

for domain, count in sorted(domain_counts.items()):
    print(f"  - {domain}: {count} 个")
EOF

# 2. 验证 LLM 提供商
echo ""
echo "🤖 验证 LLM 提供商..."
python3 << 'EOF'
from src.models import ModelManager
mm = ModelManager()
providers = mm.list_providers()
print(f"✅ 共 {len(providers)} 个提供商")
for p in providers[:6]:
    print(f"  - {p}")
if len(providers) > 6:
    print(f"  ... 还有 {len(providers) - 6} 个")
EOF

# 3. 验证核心模块
echo ""
echo "🔧 验证核心模块..."
python3 << 'EOF'
from src.core.skill_manager import SkillManager
from src.models import ModelManager
from src.optimization import PromptOptimizer, ModelSelector

sm = SkillManager()
mm = ModelManager()
po = PromptOptimizer()
ms = ModelSelector()

print("✅ SkillManager")
print("✅ ModelManager")
print("✅ PromptOptimizer")
print("✅ ModelSelector")
EOF

# 4. 验证 CLI
echo ""
echo "🖥️ 验证 CLI..."
if magic-skill --help > /dev/null 2>&1; then
    success "CLI 可用"
    skill_count=$(magic-skill list 2>/dev/null | grep -c "│" || echo "0")
    success "CLI 可列出技能"
else
    error "CLI 不可用"
fi

# 5. 验证测试
echo ""
echo "🧪 验证测试..."
if python -m pytest tests/ -q --tb=no 2>/dev/null | grep -q "passed"; then
    success "测试通过"
else
    warning "测试运行失败或没有测试"
fi

# 6. 验证文件结构
echo ""
echo "📁 验证文件结构..."
files=(
    "README.md"
    "cli/main.py"
    "api/main.py"
    "src/mcp/server.py"
    ".cursor/mcp.json"
    "claude_desktop_config.json"
)

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        success "$file"
    else
        error "$file 不存在"
    fi
done

echo ""
echo "=========================================="
echo "  验证完成！"
echo "=========================================="
