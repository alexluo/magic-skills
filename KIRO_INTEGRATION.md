# Kiro IDE 集成指南

**English** | [简体中文](#简体中文) | [繁體中文](#繁體中文)

---

## English

### Overview

Magic Skills provides **built-in support** for Kiro IDE through MCP (Model Context Protocol). Kiro will automatically detect and use Magic Skills when you open the project.

### Quick Start

1. **Open Project in Kiro**
   ```bash
   kiro /path/to/magic-skills
   ```

2. **Set API Keys** (if not already set)
   ```bash
   export OPENAI_API_KEY="your-key"
   # Or other provider keys
   ```

3. **Start Using Skills**
   - Press `Cmd+Shift+P` → "Magic Skills: Execute Skill"
   - Or type `@kiro` in chat and mention a skill

### Configuration Files

The project includes pre-configured Kiro settings:

```
.kiro/
├── mcp.json          # MCP server configuration
├── spec.md           # Kiro spec for Magic Skills
└── settings.json     # Kiro IDE settings
```

### Usage Examples

#### Command Format (Recommended)

Use `/mgc-<category>-<skill-name>` format:

```
/mgc-java-backend-controller-gen Create a REST API for user management
```

#### Generate Spring Boot Controller

```
/mgc-java-backend-controller-gen Create a user management API with CRUD operations
```

Or with @kiro:
```
@kiro Use /mgc-java-backend-controller-gen to create a user API
```

#### Generate Unit Tests

```
/mgc-software-testing-unit-test-gen Generate tests for this function
```

#### Code Review

```
/mgc-java-backend-code-review-java Review this code and suggest improvements
```

#### Android Development

```
/mgc-android-os-aidl-interface-gen Create an AIDL interface for media player
```

#### Auto-Completion

Type `/mgc-` and Kiro will show available skills:
```
/mgc-[TAB]
  /mgc-java-backend-controller-gen
  /mgc-java-backend-service-gen
  /mgc-software-testing-unit-test-gen
  ...
```

### Kiro-specific Features

| Feature | Description |
|---------|-------------|
| Auto-suggestion | Kiro suggests relevant skills based on file type and context |
| Spec Integration | Skills work with Kiro's spec-driven development workflow |
| Cost Tracking | Real-time cost estimation for each skill execution |
| Multi-model | Choose from 12+ LLM providers |
| Context Awareness | Automatically passes file context, selected code, and project structure |

### Available Skills by Domain

#### Java Backend (30 skills)
- `spring-boot-controller-gen` - REST controllers
- `spring-boot-service-gen` - Service layer
- `jpa-entity-gen` - JPA entities
- `dto-gen` - DTOs
- `code-review-java` - Code review
- `junit-test-gen` - Unit tests

#### Android OS (25 skills)
- `android-bp-gen` - Android.bp files
- `aidl-interface-gen` - AIDL interfaces
- `hal-impl-gen` - HAL implementations
- `system-service-gen` - System services

#### Software Testing (30 skills)
- `unit-test-gen` - Unit tests
- `integration-test-gen` - Integration tests
- `test-plan-gen` - Test plans
- `bug-analyzer` - Bug analysis

### Troubleshooting

**Issue**: Skills not showing in Kiro

**Solution**: 
1. Check `.kiro/mcp.json` exists
2. Verify Python environment: `which python`
3. Check MCP server logs in Kiro output panel

**Issue**: API key errors

**Solution**: Set environment variables before starting Kiro:
```bash
export OPENAI_API_KEY="your-key"
kiro .
```

---

# 简体中文

**简体中文** | [English](#english) | [繁體中文](#繁體中文)

---

## 概述

Magic Skills 通过 MCP (Model Context Protocol) 为 Kiro IDE 提供**内置支持**。当你在 Kiro 中打开项目时，Kiro 会自动检测并使用 Magic Skills。

## 快速开始

1. **在 Kiro 中打开项目**
   ```bash
   kiro /path/to/magic-skills
   ```

2. **设置 API 密钥**（如果尚未设置）
   ```bash
   export OPENAI_API_KEY="your-key"
   # 或其他提供商的密钥
   ```

3. **开始使用技能**
   - 按 `Cmd+Shift+P` → "Magic Skills: 执行技能"
   - 或在聊天中输入 `@kiro` 并提及技能

## 配置文件

项目包含预配置的 Kiro 设置：

```
.kiro/
├── mcp.json          # MCP 服务器配置
├── spec.md           # Kiro 的 Magic Skills 规范
└── settings.json     # Kiro IDE 设置
```

## 使用示例

### 命令格式（推荐）

使用 `/mgc-<分类>-<技能名>` 格式：

```
/mgc-java-backend-controller-gen 创建一个用户管理的 REST API
```

### 生成 Spring Boot 控制器

```
/mgc-java-backend-controller-gen 创建用户管理 API，包含增删改查操作
```

或使用 @kiro：
```
@kiro 使用 /mgc-java-backend-controller-gen 创建用户 API
```

### 生成单元测试

```
/mgc-software-testing-unit-test-gen 为这个函数生成测试
```

### 代码审查

```
/mgc-java-backend-code-review-java 审查这段代码并提出改进建议
```

### Android 开发

```
/mgc-android-os-aidl-interface-gen 为媒体播放器创建 AIDL 接口
```

### 自动补全

输入 `/mgc-` 后，Kiro 会显示可用技能：
```
/mgc-[TAB]
  /mgc-java-backend-controller-gen
  /mgc-java-backend-service-gen
  /mgc-software-testing-unit-test-gen
  ...
```

## Kiro 专属功能

| 功能 | 描述 |
|------|------|
| 智能建议 | Kiro 根据文件类型和上下文推荐相关技能 |
| Spec 集成 | 技能与 Kiro 的规范驱动开发工作流集成 |
| 成本追踪 | 每次技能执行的实时成本估算 |
| 多模型 | 从 12+ LLM 提供商中选择 |
| 上下文感知 | 自动传递文件上下文、选中代码和项目结构 |

## 按领域分类的可用技能

### Java 后端 (30 个技能)
- `spring-boot-controller-gen` - REST 控制器
- `spring-boot-service-gen` - 服务层
- `jpa-entity-gen` - JPA 实体
- `dto-gen` - DTO
- `code-review-java` - 代码审查
- `junit-test-gen` - 单元测试

### Android OS (25 个技能)
- `android-bp-gen` - Android.bp 文件
- `aidl-interface-gen` - AIDL 接口
- `hal-impl-gen` - HAL 实现
- `system-service-gen` - 系统服务

### 软件测试 (30 个技能)
- `unit-test-gen` - 单元测试
- `integration-test-gen` - 集成测试
- `test-plan-gen` - 测试计划
- `bug-analyzer` - 缺陷分析

## 故障排除

**问题**: 技能在 Kiro 中不显示

**解决**: 
1. 检查 `.kiro/mcp.json` 是否存在
2. 验证 Python 环境：`which python`
3. 在 Kiro 输出面板中查看 MCP 服务器日志

**问题**: API 密钥错误

**解决**: 在启动 Kiro 前设置环境变量：
```bash
export OPENAI_API_KEY="your-key"
kiro .
```

---

# 繁體中文

**繁體中文** | [English](#english) | [简体中文](#简体中文)

---

## 概述

Magic Skills 透過 MCP (Model Context Protocol) 為 Kiro IDE 提供**內建支援**。當你在 Kiro 中開啟專案時，Kiro 會自動偵測並使用 Magic Skills。

## 快速開始

1. **在 Kiro 中開啟專案**
   ```bash
   kiro /path/to/magic-skills
   ```

2. **設定 API 金鑰**（如果尚未設定）
   ```bash
   export OPENAI_API_KEY="your-key"
   # 或其他提供商的金鑰
   ```

3. **開始使用技能**
   - 按 `Cmd+Shift+P` → "Magic Skills: 執行技能"
   - 或在聊天中輸入 `@kiro` 並提及技能

## 設定檔

專案包含預設定的 Kiro 設定：

```
.kiro/
├── mcp.json          # MCP 伺服器設定
├── spec.md           # Kiro 的 Magic Skills 規範
└── settings.json     # Kiro IDE 設定
```

## 使用範例

### 命令格式（推薦）

使用 `/mgc-<分類>-<技能名>` 格式：

```
/mgc-java-backend-controller-gen 建立一個使用者管理的 REST API
```

### 產生 Spring Boot 控制器

```
/mgc-java-backend-controller-gen 建立使用者管理 API，包含增刪改查操作
```

或使用 @kiro：
```
@kiro 使用 /mgc-java-backend-controller-gen 建立使用者 API
```

### 產生單元測試

```
/mgc-software-testing-unit-test-gen 為這個函式產生測試
```

### 程式碼審查

```
/mgc-java-backend-code-review-java 審查這段程式碼並提出改進建議
```

### Android 開發

```
/mgc-android-os-aidl-interface-gen 為媒體播放器建立 AIDL 介面
```

### 自動補全

輸入 `/mgc-` 後，Kiro 會顯示可用技能：
```
/mgc-[TAB]
  /mgc-java-backend-controller-gen
  /mgc-java-backend-service-gen
  /mgc-software-testing-unit-test-gen
  ...
```

## Kiro 專屬功能

| 功能 | 描述 |
|------|------|
| 智慧建議 | Kiro 根據檔案類型和上下文推薦相關技能 |
| Spec 整合 | 技能與 Kiro 的規範驅動開發工作流程整合 |
| 成本追蹤 | 每次技能執行的即時成本估算 |
| 多模型 | 從 12+ LLM 提供商中選擇 |
| 上下文感知 | 自動傳遞檔案上下文、選取程式碼和專案結構 |

## 按領域分類的可用技能

### Java 後端 (30 個技能)
- `spring-boot-controller-gen` - REST 控制器
- `spring-boot-service-gen` - 服務層
- `jpa-entity-gen` - JPA 實體
- `dto-gen` - DTO
- `code-review-java` - 程式碼審查
- `junit-test-gen` - 單元測試

### Android OS (25 個技能)
- `android-bp-gen` - Android.bp 檔案
- `aidl-interface-gen` - AIDL 介面
- `hal-impl-gen` - HAL 實作
- `system-service-gen` - 系統服務

### 軟體測試 (30 個技能)
- `unit-test-gen` - 單元測試
- `integration-test-gen` - 整合測試
- `test-plan-gen` - 測試計畫
- `bug-analyzer` - 缺陷分析

## 故障排除

**問題**: 技能在 Kiro 中不顯示

**解決**: 
1. 檢查 `.kiro/mcp.json` 是否存在
2. 驗證 Python 環境：`which python`
3. 在 Kiro 輸出面板中查看 MCP 伺服器日誌

**問題**: API 金鑰錯誤

**解決**: 在啟動 Kiro 前設定環境變數：
```bash
export OPENAI_API_KEY="your-key"
kiro .
```
