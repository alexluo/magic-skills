---
name: mgc-software-testing-code-coverage-analysis
description: Analyze code coverage
category: software-testing
version: 1.0.0
tags: ['software-testing', 'coverage']
author: Magic Skills Team
usage_count: 0
success_rate: 0
last_optimized: null
---

# Analyze code coverage

## 触发条件

**自然语言：**
- "生成测试"
- "写单元测试"
- "测试 code-coverage-analysis"
- "添加测试用例"

**代码上下文：**
- 文件类型: `.java`, `.kt`, `.swift`
- 选中方法或类
- 光标位于测试类中

## 执行逻辑

### 步骤 1: 分析测试目标
- 识别要测试的类/方法
- 分析方法签名和依赖
- 确定测试类型（单元测试/集成测试）

### 步骤 2: 生成测试代码
```java
@Test
void {testMethodName}() {
    // Arrange
    {arrangeCode}
    
    // Act
    {actCode}
    
    // Assert
    {assertCode}
}
```

### 步骤 3: 添加依赖
- 自动添加 Mockito/MockBean
- 生成 Mock 数据
- 添加必要的 import

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

执行后根据上下文智能推荐：

- **单元测试生成后** → "生成集成测试？" (`mgc-integration-test-gen`)
- **测试生成后** → "生成 Mock 数据？" (`mgc-mock-server-gen`)
- **测试完成后** → "分析测试覆盖率？" (`mgc-code-coverage-analysis`)
- **发现 Bug 后** → "分析根本原因？" (`mgc-bug-root-cause`)

---

*本 Skill 由 Magic Skills 自动生成，会根据使用数据自动优化*
