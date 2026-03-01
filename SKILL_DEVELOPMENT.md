# Magic Skills 技能开发指南

**English** | [简体中文](#简体中文) | [繁體中文](#繁體中文)

---

## English

### Skill Structure

Each skill is a folder containing:

```
skills/my-skill/
├── skill.yaml      # Metadata and schemas
├── prompt.txt      # Prompt template
└── handler.py      # Python implementation
```

### 1. Create skill.yaml

```yaml
name: my-skill
description: What this skill does
version: "1.0.0"
category: java-backend
author: "Your Name"

input_schema:
  type: object
  properties:
    code:
      type: string
      description: Input code to process
  required: ["code"]

output_schema:
  type: object
  properties:
    result:
      type: string
      description: Processed result
```

### 2. Create prompt.txt

```
You are an expert programmer. Analyze the following code:

{{code}}

Provide suggestions for improvement.
```

### 3. Create handler.py

```python
from typing import Dict, Any
from src.core.base_skill import BaseSkill

class MySkill(BaseSkill):
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        code = params["code"]
        
        # Load prompt template
        prompt = self.load_prompt()
        
        # Generate with LLM
        result = self.llm.generate(
            prompt.format(code=code)
        )
        
        return {"result": result}
```

### Advanced Features

#### Access Multiple LLM Providers

```python
# Use specific provider
result = self.llm.generate_with_provider(
    prompt,
    provider="anthropic",
    model="claude-3-sonnet"
)
```

#### Collect Feedback

```python
def execute(self, params):
    result = self.llm.generate(...)
    
    # Record for optimization
    self.record_execution(params, result)
    
    return result
```

#### Cost Tracking

```python
cost = self.llm.estimate_cost(
    input_tokens=1000,
    output_tokens=500,
    provider="openai"
)
```

---

# 简体中文

**简体中文** | [English](#english) | [繁體中文](#繁體中文)

---

## 技能结构

每个技能是一个包含以下文件的文件夹：

```
skills/my-skill/
├── skill.yaml      # 元数据和结构定义
├── prompt.txt      # 提示词模板
└── handler.py      # Python 实现
```

## 1. 创建 skill.yaml

```yaml
name: my-skill
description: 这个技能的功能描述
version: "1.0.0"
category: java-backend
author: "你的名字"

input_schema:
  type: object
  properties:
    code:
      type: string
      description: 要处理的输入代码
  required: ["code"]

output_schema:
  type: object
  properties:
    result:
      type: string
      description: 处理结果
```

## 2. 创建 prompt.txt

```
你是一位专家级程序员。分析以下代码：

{{code}}

提供改进建议。
```

## 3. 创建 handler.py

```python
from typing import Dict, Any
from src.core.base_skill import BaseSkill

class MySkill(BaseSkill):
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        code = params["code"]
        
        # 加载提示词模板
        prompt = self.load_prompt()
        
        # 使用 LLM 生成结果
        result = self.llm.generate(
            prompt.format(code=code)
        )
        
        return {"result": result}
```

## 高级功能

### 使用多个 LLM 提供商

```python
# 使用特定提供商
result = self.llm.generate_with_provider(
    prompt,
    provider="anthropic",
    model="claude-3-sonnet"
)
```

### 收集反馈

```python
def execute(self, params):
    result = self.llm.generate(...)
    
    # 记录执行用于优化
    self.record_execution(params, result)
    
    return result
```

### 成本追踪

```python
cost = self.llm.estimate_cost(
    input_tokens=1000,
    output_tokens=500,
    provider="openai"
)
```

## 完整示例

```python
from typing import Dict, Any
from src.core.base_skill import BaseSkill

class CodeReviewerSkill(BaseSkill):
    """代码审查技能示例"""
    
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        code = params["code"]
        language = params.get("language", "python")
        
        # 加载提示词
        prompt_template = self.load_prompt()
        
        # 构建完整提示词
        full_prompt = f"""{prompt_template}

编程语言: {language}
代码行数: {len(code.split(chr(10)))}

待审查代码:
```{language}
{code}
```
"""
        
        # 生成审查结果
        review = self.llm.generate(full_prompt)
        
        # 提取问题
        issues = self._extract_issues(review)
        
        # 计算评分
        score = self._calculate_score(review, len(issues))
        
        return {
            "review": review,
            "issues": issues,
            "score": score,
            "language": language
        }
    
    def _extract_issues(self, review: str) -> list:
        """从审查文本中提取问题"""
        issues = []
        for line in review.split("\n"):
            if any(marker in line for marker in ["问题", "错误", "建议"]):
                issues.append(line.strip())
        return issues
    
    def _calculate_score(self, review: str, issue_count: int) -> float:
        """计算代码质量评分"""
        base_score = 10.0
        deductions = min(issue_count * 0.5, 5.0)
        return round(max(1.0, base_score - deductions), 1)
```

---

# 繁體中文

**繁體中文** | [English](#english) | [简体中文](#简体中文)

---

## 技能結構

每個技能是一個包含以下檔案的資料夾：

```
skills/my-skill/
├── skill.yaml      # 元資料和結構定義
├── prompt.txt      # 提示詞模板
└── handler.py      # Python 實作
```

## 1. 建立 skill.yaml

```yaml
name: my-skill
description: 這個技能的功能描述
version: "1.0.0"
category: java-backend
author: "你的名字"

input_schema:
  type: object
  properties:
    code:
      type: string
      description: 要處理的輸入程式碼
  required: ["code"]

output_schema:
  type: object
  properties:
    result:
      type: string
      description: 處理結果
```

## 2. 建立 prompt.txt

```
你是一位專家級程式設計師。分析以下程式碼：

{{code}}

提供改進建議。
```

## 3. 建立 handler.py

```python
from typing import Dict, Any
from src.core.base_skill import BaseSkill

class MySkill(BaseSkill):
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        code = params["code"]
        
        # 載入提示詞模板
        prompt = self.load_prompt()
        
        # 使用 LLM 產生結果
        result = self.llm.generate(
            prompt.format(code=code)
        )
        
        return {"result": result}
```

## 進階功能

### 使用多個 LLM 提供商

```python
# 使用特定提供商
result = self.llm.generate_with_provider(
    prompt,
    provider="anthropic",
    model="claude-3-sonnet"
)
```

### 收集回饋

```python
def execute(self, params):
    result = self.llm.generate(...)
    
    # 記錄執行用於優化
    self.record_execution(params, result)
    
    return result
```

### 成本追蹤

```python
cost = self.llm.estimate_cost(
    input_tokens=1000,
    output_tokens=500,
    provider="openai"
)
```

## 完整範例

```python
from typing import Dict, Any
from src.core.base_skill import BaseSkill

class CodeReviewerSkill(BaseSkill):
    """程式碼審查技能範例"""
    
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        code = params["code"]
        language = params.get("language", "python")
        
        # 載入提示詞
        prompt_template = self.load_prompt()
        
        # 建構完整提示詞
        full_prompt = f"""{prompt_template}

程式語言: {language}
程式碼行數: {len(code.split(chr(10)))}

待審查程式碼:
```{language}
{code}
```
"""
        
        # 產生審查結果
        review = self.llm.generate(full_prompt)
        
        # 提取問題
        issues = self._extract_issues(review)
        
        # 計算評分
        score = self._calculate_score(review, len(issues))
        
        return {
            "review": review,
            "issues": issues,
            "score": score,
            "language": language
        }
    
    def _extract_issues(self, review: str) -> list:
        """從審查文字中提取問題"""
        issues = []
        for line in review.split("\n"):
            if any(marker in line for marker in ["問題", "錯誤", "建議"]):
                issues.append(line.strip())
        return issues
    
    def _calculate_score(self, review: str, issue_count: int) -> float:
        """計算程式碼品質評分"""
        base_score = 10.0
        deductions = min(issue_count * 0.5, 5.0)
        return round(max(1.0, base_score - deductions), 1)
```
