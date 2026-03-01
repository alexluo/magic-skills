---
name: mgc-java-backend-k8s-deployment-gen
description: Generate Kubernetes deployment files
category: java-backend
version: 1.0.0
tags: ['java-backend', 'config-generation']
author: Magic Skills Team
usage_count: 0
success_rate: 0
last_optimized: null
---

# Generate Kubernetes deployment files

## 触发条件

**自然语言：**
- "创建 k8s-deployment-gen"
- "生成 k8s-deployment-gen"
- "写个 k8s-deployment-gen"
- "添加 k8s-deployment-gen"

**代码上下文：**
- 文件类型: `.java`
- 项目类型: Spring Boot (检测到 `pom.xml` 或 `build.gradle` 包含 `spring-boot`)
- 输入模式: 类定义、接口声明

## 执行逻辑

### 步骤 1: 分析意图
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
@RequestMapping("{endpoint}")
@Tag(name = "{resourceName}")  // 如果使用 Swagger
public class {className} {
    
    private final {serviceName} {serviceVar};
    
    // 根据意图生成 CRUD 方法
    @GetMapping
    @Operation(summary = "列表查询")
    public List<{entity}> list() {
        return {serviceVar}.list();
    }
    
    // ... 其他方法
}
```

### 步骤 4: 插入代码
- 自动定位到正确的包目录
- 添加必要的 import 语句
- 格式化代码

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

- **Controller 生成后** → "生成对应的 Service 层？" (`mgc-java-backend-service-gen`)
- **Service 生成后** → "生成 DAO/Repository 层？" (`mgc-java-backend-dao-gen`)
- **DAO 生成后** → "生成 Entity/Model？" (`mgc-java-backend-jpa-entity-gen`)
- **完整分层后** → "生成单元测试？" (`mgc-unit-test-gen`)
- **API 完成后** → "生成 Swagger 文档？" (`mgc-java-backend-rest-api-doc-gen`)
- **代码生成后** → "进行代码审查？" (`mgc-code-review-java`)

---

*本 Skill 由 Magic Skills 自动生成，会根据使用数据自动优化*
