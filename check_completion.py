#!/usr/bin/env python3
"""全局完成检查脚本"""

import os
import yaml
from pathlib import Path
from collections import defaultdict

# 定义6个领域的期望技能数量
EXPECTED_SKILLS = {
    "java-backend": 30,
    "android-os": 25,
    "digital-analytics": 30,
    "mobile-app": 25,
    "multi-language": 20,
    "software-testing": 30,
}

# 定义期望的LLM提供商
EXPECTED_PROVIDERS = [
    "openai", "anthropic", "google", "qwen", "ernie", 
    "spark", "kimi", "deepseek", "meta", "mistral", "cohere"
]

def check_skills():
    """检查所有领域技能"""
    print("=" * 60)
    print("📦 领域技能检查")
    print("=" * 60)
    
    skills_dir = Path("skills")
    total_skills = 0
    domain_counts = {}
    
    for domain in EXPECTED_SKILLS.keys():
        domain_dir = skills_dir / domain
        if not domain_dir.exists():
            print(f"❌ {domain}: 目录不存在")
            continue
            
        skill_files = list(domain_dir.rglob("skill.yaml"))
        actual_count = len(skill_files)
        expected_count = EXPECTED_SKILLS[domain]
        domain_counts[domain] = actual_count
        total_skills += actual_count
        
        status = "✅" if actual_count >= expected_count else "⚠️"
        print(f"{status} {domain}: {actual_count}/{expected_count} 技能")
        
        # 验证每个技能的文件完整性
        incomplete = []
        for skill_file in skill_files:
            skill_dir = skill_file.parent
            skill_name = skill_dir.name
            
            has_handler = (skill_dir / "handler.py").exists()
            has_prompt = (skill_dir / "prompt.txt").exists()
            
            if not (has_handler and has_prompt):
                incomplete.append(f"{skill_name}(缺{'handler' if not has_handler else ''}{'prompt' if not has_prompt else ''})")
        
        if incomplete:
            print(f"   ⚠️ 不完整技能: {', '.join(incomplete[:3])}{'...' if len(incomplete) > 3 else ''}")
    
    print(f"\n📊 技能总计: {total_skills}/160")
    return total_skills >= 160

def check_llm_providers():
    """检查LLM提供商"""
    print("\n" + "=" * 60)
    print("🤖 LLM 提供商检查")
    print("=" * 60)
    
    providers_dir = Path("src/models")
    found_providers = []
    
    for provider in EXPECTED_PROVIDERS:
        provider_file = providers_dir / f"{provider}_provider.py"
        if provider_file.exists():
            found_providers.append(provider)
            print(f"✅ {provider}")
        else:
            print(f"❌ {provider}: 文件不存在")
    
    # 检查 ModelManager
    model_manager = providers_dir / "model_manager.py"
    if model_manager.exists():
        content = model_manager.read_text()
        all_registered = all(p in content for p in EXPECTED_PROVIDERS)
        if all_registered:
            print(f"\n✅ ModelManager 已注册所有 {len(EXPECTED_PROVIDERS)} 个提供商")
        else:
            print(f"\n⚠️ ModelManager 可能缺少某些提供商注册")
    
    return len(found_providers) == len(EXPECTED_PROVIDERS)

def check_core_modules():
    """检查核心模块"""
    print("\n" + "=" * 60)
    print("🔧 核心模块检查")
    print("=" * 60)
    
    modules = {
        "SkillManager": "src/core/skill_manager.py",
        "ModelManager": "src/models/model_manager.py",
        "UpgradeManager": "src/core/upgrade_manager.py",
        "PromptOptimizer": "src/optimization/prompt_optimizer.py",
        "ModelSelector": "src/optimization/model_selector.py",
        "FeedbackProcessor": "src/optimization/feedback_processor.py",
        "ABTester": "src/optimization/ab_tester.py",
        "MCPServer": "src/mcp/server.py",
    }
    
    all_exist = True
    for name, path in modules.items():
        if Path(path).exists():
            print(f"✅ {name}")
        else:
            print(f"❌ {name}: 文件不存在")
            all_exist = False
    
    return all_exist

def check_interfaces():
    """检查接口层"""
    print("\n" + "=" * 60)
    print("🖥️ 接口层检查")
    print("=" * 60)
    
    interfaces = {
        "CLI": "cli/main.py",
        "REST API": "api/main.py",
        "MCP Server": "src/mcp/server.py",
    }
    
    all_exist = True
    for name, path in interfaces.items():
        if Path(path).exists():
            print(f"✅ {name}")
        else:
            print(f"❌ {name}: 文件不存在")
            all_exist = False
    
    return all_exist

def check_ai_tool_integration():
    """检查AI工具集成"""
    print("\n" + "=" * 60)
    print("🔌 AI 工具集成检查")
    print("=" * 60)
    
    configs = {
        "Cursor MCP": ".cursor/mcp.json",
        "Claude Desktop": "claude_desktop_config.json",
        "VS Code Extension": "extensions/vscode/package.json",
        "集成文档": "docs/ai-tool-integration.md",
    }
    
    all_exist = True
    for name, path in configs.items():
        if Path(path).exists():
            print(f"✅ {name}")
        else:
            print(f"❌ {name}: 文件不存在")
            all_exist = False
    
    return all_exist

def check_tests():
    """检查测试"""
    print("\n" + "=" * 60)
    print("🧪 测试套件检查")
    print("=" * 60)
    
    test_files = list(Path("tests").glob("test_*.py"))
    print(f"✅ 测试文件: {len(test_files)} 个")
    
    for test_file in test_files:
        print(f"   - {test_file.name}")
    
    return len(test_files) >= 3

def check_documentation():
    """检查文档"""
    print("\n" + "=" * 60)
    print("📚 文档检查")
    print("=" * 60)
    
    docs = {
        "README": "README.md",
        "完成报告": "COMPLETION_REPORT.md",
        "API文档": "docs/api.md",
        "CLI文档": "docs/cli.md",
        "技能开发指南": "docs/skill-development.md",
        "AI工具集成": "docs/ai-tool-integration.md",
    }
    
    found = 0
    for name, path in docs.items():
        if Path(path).exists():
            print(f"✅ {name}")
            found += 1
        else:
            print(f"⚠️ {name}: 文件不存在")
    
    return found >= 3

def main():
    print("\n" + "🔍 Magic Skills 全局完成检查".center(60, "="))
    print()
    
    results = {
        "领域技能": check_skills(),
        "LLM提供商": check_llm_providers(),
        "核心模块": check_core_modules(),
        "接口层": check_interfaces(),
        "AI工具集成": check_ai_tool_integration(),
        "测试套件": check_tests(),
        "文档": check_documentation(),
    }
    
    print("\n" + "=" * 60)
    print("📋 检查结果汇总")
    print("=" * 60)
    
    all_passed = True
    for category, passed in results.items():
        status = "✅ 通过" if passed else "❌ 未通过"
        print(f"{status}: {category}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 所有检查通过！项目已完成！")
    else:
        print("⚠️ 部分检查未通过，请查看详情")
    print("=" * 60)
    
    return all_passed

if __name__ == "__main__":
    main()
