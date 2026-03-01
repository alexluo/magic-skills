#!/usr/bin/env python3
"""
Magic Skills 完整验证脚本
运行所有验证检查并生成报告
"""

import sys
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

# 颜色输出
class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RESET = "\033[0m"

def print_success(msg: str):
    print(f"{Colors.GREEN}✅ {msg}{Colors.RESET}")

def print_error(msg: str):
    print(f"{Colors.RED}❌ {msg}{Colors.RESET}")

def print_warning(msg: str):
    print(f"{Colors.YELLOW}⚠️ {msg}{Colors.RESET}")

def print_info(msg: str):
    print(f"{Colors.BLUE}ℹ️ {msg}{Colors.RESET}")

class Verifier:
    def __init__(self):
        self.results: Dict[str, Tuple[bool, str]] = {}
        self.errors: List[str] = []

    def check_environment(self) -> bool:
        """检查环境"""
        print_info("检查环境...")
        try:
            import sys
            if sys.version_info < (3, 9):
                self.errors.append("Python 版本需要 3.9+")
                return False
            
            # 检查关键依赖
            required = ["fastapi", "typer", "httpx", "pydantic", "yaml"]
            missing = []
            for pkg in required:
                try:
                    __import__(pkg)
                except ImportError:
                    missing.append(pkg)
            
            if missing:
                self.errors.append(f"缺少依赖: {', '.join(missing)}")
                return False
            
            print_success(f"Python {sys.version_info.major}.{sys.version_info.minor}")
            return True
        except Exception as e:
            self.errors.append(f"环境检查失败: {e}")
            return False

    def check_skills(self) -> bool:
        """检查技能"""
        print_info("检查技能...")
        try:
            from src.core.skill_manager import SkillManager
            
            sm = SkillManager()
            count = sm.load_all_skills()
            
            if count < 160:
                self.errors.append(f"技能数量不足: {count}/160")
                return False
            
            # 检查各领域的技能数量
            expected = {
                "java-backend": 30,
                "android-os": 25,
                "digital-analytics": 30,
                "mobile-app": 25,
                "multi-language": 20,
                "software-testing": 30,
            }
            
            skills = sm.list_skills()
            domain_counts = {}
            for skill in skills:
                cat = skill["category"]
                domain_counts[cat] = domain_counts.get(cat, 0) + 1
            
            for domain, expected_count in expected.items():
                actual = domain_counts.get(domain, 0)
                if actual < expected_count:
                    print_warning(f"{domain}: {actual}/{expected_count}")
                else:
                    print_success(f"{domain}: {actual} 个技能")
            
            print_success(f"总计 {count} 个技能")
            return True
        except Exception as e:
            self.errors.append(f"技能检查失败: {e}")
            return False

    def check_providers(self) -> bool:
        """检查 LLM 提供商"""
        print_info("检查 LLM 提供商...")
        try:
            from src.models import ModelManager
            
            mm = ModelManager()
            providers = mm.list_providers()
            
            expected = ["openai", "anthropic", "google", "qwen", "ernie", 
                       "spark", "kimi", "deepseek", "meta", "mistral", "cohere"]
            
            missing = [p for p in expected if p not in providers]
            if missing:
                self.errors.append(f"缺少提供商: {', '.join(missing)}")
                return False
            
            for provider in expected:
                print_success(f"{provider}")
            
            print_success(f"共 {len(providers)} 个提供商")
            return True
        except Exception as e:
            self.errors.append(f"提供商检查失败: {e}")
            return False

    def check_core_modules(self) -> bool:
        """检查核心模块"""
        print_info("检查核心模块...")
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
                print_success(name)
            else:
                print_error(f"{name} 不存在")
                all_exist = False
        
        return all_exist

    def check_interfaces(self) -> bool:
        """检查接口层"""
        print_info("检查接口层...")
        interfaces = {
            "CLI": "cli/main.py",
            "REST API": "api/main.py",
            "MCP Server": "src/mcp/server.py",
        }
        
        all_exist = True
        for name, path in interfaces.items():
            if Path(path).exists():
                print_success(name)
            else:
                print_error(f"{name} 不存在")
                all_exist = False
        
        return all_exist

    def check_ai_integration(self) -> bool:
        """检查 AI 工具集成"""
        print_info("检查 AI 工具集成...")
        configs = {
            "Cursor MCP": ".cursor/mcp.json",
            "Claude Desktop": "claude_desktop_config.json",
            "VS Code Extension": "extensions/vscode/package.json",
        }
        
        all_exist = True
        for name, path in configs.items():
            if Path(path).exists():
                print_success(name)
            else:
                print_error(f"{name} 不存在")
                all_exist = False
        
        return all_exist

    def check_tests(self) -> bool:
        """检查测试"""
        print_info("检查测试...")
        try:
            import subprocess
            result = subprocess.run(
                ["python", "-m", "pytest", "tests/", "-v", "--tb=short"],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                # 统计通过数量
                lines = result.stdout.split("\n")
                for line in lines:
                    if "passed" in line:
                        print_success(f"测试通过: {line.strip()}")
                        break
                return True
            else:
                self.errors.append("测试运行失败")
                print_error("测试运行失败")
                return False
        except Exception as e:
            self.errors.append(f"测试检查失败: {e}")
            return False

    def check_documentation(self) -> bool:
        """检查文档"""
        print_info("检查文档...")
        docs = {
            "README": "README.md",
            "完成报告": "COMPLETION_REPORT.md",
            "验证指南": "VERIFICATION_GUIDE.md",
        }
        
        all_exist = True
        for name, path in docs.items():
            if Path(path).exists():
                print_success(name)
            else:
                print_error(f"{name} 不存在")
                all_exist = False
        
        return all_exist

    def run_all_checks(self) -> Dict:
        """运行所有检查"""
        print("\n" + "=" * 60)
        print("🔍 Magic Skills 完整验证".center(60))
        print("=" * 60 + "\n")
        
        start_time = time.time()
        
        checks = [
            ("环境", self.check_environment),
            ("技能", self.check_skills),
            ("LLM提供商", self.check_providers),
            ("核心模块", self.check_core_modules),
            ("接口层", self.check_interfaces),
            ("AI工具集成", self.check_ai_integration),
            ("测试", self.check_tests),
            ("文档", self.check_documentation),
        ]
        
        for name, check_func in checks:
            print(f"\n{'─' * 60}")
            try:
                passed = check_func()
                self.results[name] = (passed, "")
            except Exception as e:
                self.results[name] = (False, str(e))
                self.errors.append(f"{name}: {e}")
        
        elapsed = time.time() - start_time
        
        # 生成报告
        return self.generate_report(elapsed)

    def generate_report(self, elapsed: float) -> Dict:
        """生成验证报告"""
        print("\n" + "=" * 60)
        print("📋 验证报告".center(60))
        print("=" * 60)
        
        passed = sum(1 for r in self.results.values() if r[0])
        total = len(self.results)
        
        for name, (result, msg) in self.results.items():
            status = "✅ 通过" if result else "❌ 失败"
            print(f"{status}: {name}")
            if msg:
                print(f"   {msg}")
        
        print("\n" + "─" * 60)
        print(f"总计: {passed}/{total} 项检查通过")
        print(f"耗时: {elapsed:.2f} 秒")
        
        if self.errors:
            print("\n❌ 发现的问题:")
            for error in self.errors[:10]:
                print(f"  - {error}")
            if len(self.errors) > 10:
                print(f"  ... 还有 {len(self.errors) - 10} 个问题")
        
        all_passed = passed == total
        
        print("\n" + "=" * 60)
        if all_passed:
            print("🎉 所有验证通过！项目已就绪！".center(60))
        else:
            print("⚠️ 部分验证未通过，请查看详情".center(60))
        print("=" * 60 + "\n")
        
        return {
            "timestamp": datetime.now().isoformat(),
            "total_checks": total,
            "passed": passed,
            "failed": total - passed,
            "elapsed_seconds": elapsed,
            "results": {k: v[0] for k, v in self.results.items()},
            "errors": self.errors,
            "all_passed": all_passed
        }

def main():
    verifier = Verifier()
    report = verifier.run_all_checks()
    
    # 保存报告
    report_file = Path("verification_report.json")
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"📄 详细报告已保存: {report_file}")
    
    # 返回退出码
    sys.exit(0 if report["all_passed"] else 1)

if __name__ == "__main__":
    main()
