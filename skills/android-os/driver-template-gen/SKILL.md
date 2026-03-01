---
name: mgc-android-os-driver-template-gen
description: Generate driver templates
category: android-os
version: 1.0.0
tags: ['android-os', 'driver-development']
author: Magic Skills Team
usage_count: 0
success_rate: 0
last_optimized: null
---

# Generate driver templates

## 触发条件

**自然语言：**
- "创建 driver-template-gen"
- "生成 Android driver-template-gen"
- "AOSP driver-template-gen"

**代码上下文：**
- 文件类型: `.java`, `.cpp`, `.h`, `.aidl`, `.hal`
- 项目类型: AOSP (检测到 `Android.bp` 或 `Android.mk`)
- 文件路径包含 `frameworks/`, `hardware/`, `system/`

## 执行逻辑

### 步骤 1: 理解需求
You are an expert in android-os. Help with: Generate driver templates

### 步骤 2: 分析上下文
- 检测项目类型和配置
- 识别相关文件和依赖
- 分析代码风格

### 步骤 3: 生成内容
根据分析结果生成符合项目规范的输出

### 步骤 4: 应用结果
- 插入到正确位置
- 格式化代码
- 添加必要的引用

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

- **HAL 接口生成后** → "生成 Binder 存根？" (`mgc-android-os-binder-stub-gen`)
- **AIDL 生成后** → "实现 Service？" (`mgc-android-os-android-service-gen`)
- **Native 代码后** → "配置 SELinux 策略？" (`mgc-android-os-selinux-policy-gen`)
- **系统服务后** → "生成 init.rc 配置？" (`mgc-android-os-init-rc-gen`)

---

*本 Skill 由 Magic Skills 自动生成，会根据使用数据自动优化*
