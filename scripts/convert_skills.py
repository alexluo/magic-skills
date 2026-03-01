#!/usr/bin/env python3
"""
Skill 转换器：将 skill.yaml + prompt.txt + handler.py 转换为 SKILL.md
遵循 Anthropic Skills 标准格式，支持自优化
"""

import yaml
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


class SkillConverter:
    """Skill 转换器"""
    
    def __init__(self, skills_root: Path, output_root: Path):
        self.skills_root = Path(skills_root)
        self.output_root = Path(output_root)
        self.converted_count = 0
        
    def convert_all(self):
        """批量转换所有 skills"""
        print("🚀 开始转换 Skills...")
        print(f"📁 源目录: {self.skills_root}")
        print(f"📁 目标目录: {self.output_root}")
        print()
        
        # 查找所有 skill.yaml
        skill_files = list(self.skills_root.rglob("skill.yaml"))
        total = len(skill_files)
        
        print(f"🔍 发现 {total} 个 Skills")
        print()
        
        for i, skill_yaml_path in enumerate(skill_files, 1):
            skill_dir = skill_yaml_path.parent
            category = skill_dir.parent.name
            skill_name = skill_dir.name
            
            try:
                self._convert_single(skill_dir, category, skill_name)
                print(f"✅ [{i}/{total}] {category}/{skill_name}")
                self.converted_count += 1
            except Exception as e:
                print(f"❌ [{i}/{total}] {category}/{skill_name}: {e}")
        
        print()
        print(f"🎉 转换完成！成功: {self.converted_count}/{total}")
        
    def _convert_single(self, skill_dir: Path, category: str, skill_name: str):
        """转换单个 skill"""
        # 读取源文件
        skill_yaml = self._load_yaml(skill_dir / "skill.yaml")
        prompt_txt = self._load_text(skill_dir / "prompt.txt")
        handler_py = self._load_text(skill_dir / "handler.py", optional=True)
        
        # 生成 SKILL.md 内容
        skill_md = self._generate_skill_md(
            skill_yaml=skill_yaml,
            prompt_txt=prompt_txt,
            handler_py=handler_py,
            category=category,
            skill_name=skill_name
        )
        
        # 创建输出目录（.magic-skills/skills）
        output_dir = self.output_root / category / skill_name
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 写入 SKILL.md 到 .magic-skills/skills
        (output_dir / "SKILL.md").write_text(skill_md, encoding='utf-8')
        
        # 同时写入到原始 skills 目录（供 magic-skill init 使用）
        (skill_dir / "SKILL.md").write_text(skill_md, encoding='utf-8')
        
    def _load_yaml(self, path: Path) -> Dict:
        """加载 YAML 文件"""
        if not path.exists():
            raise FileNotFoundError(f"找不到文件: {path}")
        return yaml.safe_load(path.read_text(encoding='utf-8'))
    
    def _load_text(self, path: Path, optional: bool = False) -> str:
        """加载文本文件"""
        if not path.exists():
            if optional:
                return ""
            raise FileNotFoundError(f"找不到文件: {path}")
        return path.read_text(encoding='utf-8')
    
    def _generate_skill_md(
        self,
        skill_yaml: Dict,
        prompt_txt: str,
        handler_py: str,
        category: str,
        skill_name: str
    ) -> str:
        """生成 SKILL.md 内容"""
        
        # 提取基础信息
        name = skill_yaml.get('name', skill_name)
        description = skill_yaml.get('description', '')
        version = skill_yaml.get('version', '1.0.0')
        tags = skill_yaml.get('tags', [category])
        author = skill_yaml.get('author', 'Magic Skills Team')
        
        # 生成触发条件
        triggers = self._generate_triggers(name, description, category)
        
        # 生成执行逻辑
        execution_logic = self._generate_execution_logic(
            name, description, prompt_txt, handler_py, category
        )
        
        # 生成下一步建议
        next_steps = self._generate_next_steps(category, name)
        
        # 组装 SKILL.md
        skill_md = f"""---
name: mgc-{category}-{name}
description: {description}
category: {category}
version: {version}
tags: {tags}
author: {author}
usage_count: 0
success_rate: 0
last_optimized: null
---

# {description}

## 触发条件

{triggers}

## 执行逻辑

{execution_logic}

## 学习记录（运行时更新）

```yaml
# 成功模式记录
successful_patterns: []
  # - pattern: "具体模式描述"
  #   context: "适用场景"
  #   generated: "生成的内容类型"
  #   user_accepted: true
  #   count: 0

# 失败/调整记录
adjustment_history: []
  # - issue: "发现的问题"
  #   first_seen: "YYYY-MM-DD"
  #   frequency: "出现频率"
  #   solution: "解决方案"
  #   implemented: "版本号"
  #   resolved: false

# 用户反馈
user_feedback: []
  # - suggestion: "用户建议"
  #   votes: 1
  #   status: "pending"  # pending/implemented/rejected
```

## 下一步建议

{next_steps}

---

*本 Skill 由 Magic Skills 自动生成，会根据使用数据自动优化*
"""
        
        return skill_md
    
    def _generate_triggers(self, name: str, description: str, category: str) -> str:
        """生成触发条件"""
        
        # 根据 category 生成特定的触发条件
        triggers_by_category = {
            'java-backend': """**自然语言：**
- "创建 {name}"
- "生成 {name}"
- "写个 {name}"
- "添加 {name}"

**代码上下文：**
- 文件类型: `.java`
- 项目类型: Spring Boot (检测到 `pom.xml` 或 `build.gradle` 包含 `spring-boot`)
- 输入模式: 类定义、接口声明""",
            
            'software-testing': """**自然语言：**
- "生成测试"
- "写单元测试"
- "测试 {name}"
- "添加测试用例"

**代码上下文：**
- 文件类型: `.java`, `.kt`, `.swift`
- 选中方法或类
- 光标位于测试类中""",
            
            'android-os': """**自然语言：**
- "创建 {name}"
- "生成 Android {name}"
- "AOSP {name}"

**代码上下文：**
- 文件类型: `.java`, `.cpp`, `.h`, `.aidl`, `.hal`
- 项目类型: AOSP (检测到 `Android.bp` 或 `Android.mk`)
- 文件路径包含 `frameworks/`, `hardware/`, `system/`""",
            
            'mobile-app': """**自然语言：**
- "创建 {name}"
- "生成 {name}"
- "iOS/Android {name}"

**代码上下文：**
- 文件类型: `.swift`, `.kt`, `.dart`
- 项目类型: iOS (`.xcodeproj`), Android (`build.gradle`), Flutter (`pubspec.yaml`)""",
            
            'digital-analytics': """**自然语言：**
- "分析 {name}"
- "生成 {name} 报告"
- "创建 {name}"

**代码上下文：**
- 文件类型: `.sql`, `.py`, `.ipynb`
- 数据文件: `.csv`, `.json`, `.parquet`""",
            
            'multi-language': """**自然语言：**
- "翻译 {name}"
- "本地化 {name}"
- "生成多语言 {name}"

**代码上下文：**
- 文件类型: `.json`, `.xml`, `.strings`, `.arb`
- 资源文件: `res/values/`, `Localizable.strings`"""
        }
        
        default_trigger = f"""**自然语言：**
- "创建 {name}"
- "生成 {name}"
- "{description}"

**代码上下文：**
- 根据具体场景自动识别"""
        
        trigger_template = triggers_by_category.get(category, default_trigger)
        return trigger_template.format(name=name, description=description)
    
    def _generate_execution_logic(
        self,
        name: str,
        description: str,
        prompt_txt: str,
        handler_py: str,
        category: str
    ) -> str:
        """生成执行逻辑"""
        
        # 提取 prompt 中的关键信息
        prompt_summary = self._extract_prompt_summary(prompt_txt)
        
        # 根据 category 生成特定的执行步骤
        if category == 'java-backend':
            return f"""### 步骤 1: 分析意图
从用户输入提取关键信息：
- 类名（如 UserController）
- 端点路径（如 /api/users）
- HTTP 方法（GET/POST/PUT/DELETE）
- 需要的依赖（Service/DAO）

### 步骤 2: 检测项目上下文
自动检测项目配置：
- 是否使用 Swagger/OpenAPI（添加 @Tag, @Operation）
- 是否使用 Spring Security（添加 @PreAuthorize）
- 是否使用 Lombok（使用 @RequiredArgsConstructor）
- 是否使用 Validation（添加 @Valid）

### 步骤 3: 生成代码
基于检测到的上下文生成代码：
```java
@RestController
@RequestMapping("{{endpoint}}")
@Tag(name = "{{resourceName}}")  // 如果使用 Swagger
public class {{className}} {{
    
    private final {{serviceName}} {{serviceVar}};
    
    // 根据意图生成 CRUD 方法
    @GetMapping
    @Operation(summary = "列表查询")
    public List<{{entity}}> list() {{
        return {{serviceVar}}.list();
    }}
    
    // ... 其他方法
}}
```

### 步骤 4: 插入代码
- 自动定位到正确的包目录
- 添加必要的 import 语句
- 格式化代码"""
        
        elif category == 'software-testing':
            return f"""### 步骤 1: 分析测试目标
- 识别要测试的类/方法
- 分析方法签名和依赖
- 确定测试类型（单元测试/集成测试）

### 步骤 2: 生成测试代码
```java
@Test
void {{testMethodName}}() {{
    // Arrange
    {{arrangeCode}}
    
    // Act
    {{actCode}}
    
    // Assert
    {{assertCode}}
}}
```

### 步骤 3: 添加依赖
- 自动添加 Mockito/MockBean
- 生成 Mock 数据
- 添加必要的 import"""
        
        else:
            return f"""### 步骤 1: 理解需求
{prompt_summary}

### 步骤 2: 分析上下文
- 检测项目类型和配置
- 识别相关文件和依赖
- 分析代码风格

### 步骤 3: 生成内容
根据分析结果生成符合项目规范的输出

### 步骤 4: 应用结果
- 插入到正确位置
- 格式化代码
- 添加必要的引用"""
    
    def _extract_prompt_summary(self, prompt_txt: str) -> str:
        """从 prompt.txt 提取摘要"""
        # 提取第一行或关键描述
        lines = prompt_txt.strip().split('\n')
        for line in lines:
            line = line.strip()
            if line and not line.startswith('Input:'):
                return line
        return "根据用户输入生成相应内容"
    
    def _generate_next_steps(self, category: str, skill_name: str) -> str:
        """生成下一步建议"""
        
        next_steps_by_category = {
            'java-backend': """执行后根据上下文智能推荐：

- **Controller 生成后** → "生成对应的 Service 层？" (`mgc-java-backend-service-gen`)
- **Service 生成后** → "生成 DAO/Repository 层？" (`mgc-java-backend-dao-gen`)
- **DAO 生成后** → "生成 Entity/Model？" (`mgc-java-backend-jpa-entity-gen`)
- **完整分层后** → "生成单元测试？" (`mgc-unit-test-gen`)
- **API 完成后** → "生成 Swagger 文档？" (`mgc-java-backend-rest-api-doc-gen`)
- **代码生成后** → "进行代码审查？" (`mgc-code-review-java`)""",
            
            'software-testing': """执行后根据上下文智能推荐：

- **单元测试生成后** → "生成集成测试？" (`mgc-integration-test-gen`)
- **测试生成后** → "生成 Mock 数据？" (`mgc-mock-server-gen`)
- **测试完成后** → "分析测试覆盖率？" (`mgc-code-coverage-analysis`)
- **发现 Bug 后** → "分析根本原因？" (`mgc-bug-root-cause`)""",
            
            'android-os': """执行后根据上下文智能推荐：

- **HAL 接口生成后** → "生成 Binder 存根？" (`mgc-android-os-binder-stub-gen`)
- **AIDL 生成后** → "实现 Service？" (`mgc-android-os-android-service-gen`)
- **Native 代码后** → "配置 SELinux 策略？" (`mgc-android-os-selinux-policy-gen`)
- **系统服务后** → "生成 init.rc 配置？" (`mgc-android-os-init-rc-gen`)""",
            
            'mobile-app': """执行后根据上下文智能推荐：

- **UI 生成后** → "添加状态管理？" (`mgc-mobile-app-state-management-gen`)
- **功能实现后** → "添加单元测试？" (`mgc-mobile-app-unit-test-gen-mobile`)
- **页面完成后** → "添加导航？" (`mgc-mobile-app-navigation-setup-gen`)
- **功能完成后** → "添加分析追踪？" (`mgc-mobile-app-analytics-integration`)""",
            
            'digital-analytics': """执行后根据上下文智能推荐：

- **SQL 生成后** → "优化查询性能？" (`mgc-digital-analytics-sql-query-gen`)
- **报表生成后** → "设置自动化？" (`mgc-digital-analytics-report-automation`)
- **分析完成后** → "创建可视化仪表板？" (`mgc-digital-analytics-kpi-dashboard-gen`)
- **数据清洗后** → "设计数据模型？" (`mgc-digital-analytics-data-model-design`)""",
            
            'multi-language': """执行后根据上下文智能推荐：

- **翻译生成后** → "检查翻译质量？" (`mgc-multi-language-translation-quality-check`)
- **资源生成后** → "设置翻译工作流？" (`mgc-multi-language-translation-workflow`)
- **本地化后** → "检查文化适应性？" (`mgc-multi-language-cultural-adaptation`)
- **多语言后** → "生成翻译报告？" (`mgc-multi-language-translation-coverage-report`)"""
        }
        
        return next_steps_by_category.get(
            category, 
            "- 根据执行结果智能推荐下一步操作"
        )


def main():
    """主函数"""
    import sys
    
    # 默认路径
    skills_root = Path(__file__).parent.parent / "skills"
    output_root = Path(__file__).parent.parent / ".magic-skills" / "skills"
    
    # 支持命令行参数
    if len(sys.argv) > 1:
        skills_root = Path(sys.argv[1])
    if len(sys.argv) > 2:
        output_root = Path(sys.argv[2])
    
    # 执行转换
    converter = SkillConverter(skills_root, output_root)
    converter.convert_all()


if __name__ == "__main__":
    main()
