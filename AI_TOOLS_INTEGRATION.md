# Magic Skills AI 工具集成指南

**English** | [简体中文](#简体中文) | [繁體中文](#繁體中文)

---

## English

### Supported AI Tools

- ✅ **Kiro** - Via MCP (Built-in)
- ✅ **Cursor** - Via MCP
- ✅ **Claude Desktop** - Via MCP
- ✅ **VS Code** - Via Extension
- ✅ **Trae** - Via MCP
- ✅ **OpenCode** - Via API
- ✅ **Codex** - Via API

### Command Format

Magic Skills uses a unified command format across all AI tools:

```
/mgc-<category>-<skill-name>
```

**Examples:**
- `/mgc-java-backend-controller-gen` - Generate Spring Boot controller
- `/mgc-software-testing-unit-test-gen` - Generate unit tests
- `/mgc-android-os-aidl-interface-gen` - Generate AIDL interface

### Special Commands

- `/mgc-list` - List all available skills
- `/mgc-help` - Show help information
- `/mgc-models` - List available LLM models
- `/mgc-version` - Show version

### Auto-Completion

When you type `/` in supported AI tools, Magic Skills will automatically show available commands and skills.

### Kiro IDE Integration

Kiro IDE has built-in support for Magic Skills via MCP.

#### 1. Configuration (Auto-detected)

The `.kiro/mcp.json` file is already included in the project:

```json
{
  "mcpServers": {
    "magic-skills": {
      "command": "python",
      "args": ["-m", "src.mcp.server"],
      "env": {
        "PYTHONPATH": "${workspaceFolder}",
        "OPENAI_API_KEY": "${env:OPENAI_API_KEY}"
      }
    }
  }
}
```

#### 2. Use in Kiro

Kiro will automatically detect and use Magic Skills. You can:

**Via Command Palette:**
```
Cmd+Shift+P → "Magic Skills: Execute Skill"
```

**Via Command (Recommended):**
```
/mgc-java-backend-controller-gen Create a user management API with CRUD operations
```

**Via Inline Chat:**
```
@kiro Use /mgc-java-backend-controller-gen to create a user API
```

**Via Spec Mode:**
```
@kiro Generate unit tests using /mgc-software-testing-unit-test-gen
```

**Auto-Completion:**
Type `/mgc-` and Kiro will show available skills:
```
/mgc-[TAB]
  /mgc-java-backend-controller-gen
  /mgc-java-backend-service-gen
  /mgc-software-testing-unit-test-gen
  ...
```

#### 3. Kiro-specific Features

- **Auto-suggestion**: Kiro suggests relevant skills based on context
- **Spec Integration**: Skills integrate with Kiro's spec-driven development
- **Cost Tracking**: Built-in cost estimation and tracking
- **Multi-model Support**: Choose from 12+ LLM providers

### Cursor Integration

#### 1. Configure MCP

Create `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "magic-skills": {
      "command": "python",
      "args": ["-m", "src.mcp.server"],
      "env": {
        "OPENAI_API_KEY": "your-key"
      }
    }
  }
}
```

#### 2. Use in Cursor

Open Cursor Command Palette (`Cmd+Shift+P`) and type:

```
Use spring-boot-controller-gen to create a user API
```

### Claude Desktop Integration

#### 1. Configure MCP

Create `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "magic-skills": {
      "command": "python",
      "args": ["-m", "src.mcp.server"],
      "env": {
        "OPENAI_API_KEY": "your-key"
      }
    }
  }
}
```

#### 2. Use in Claude Desktop

```
Use unit-test-gen to create tests for this function
```

### VS Code Integration

#### 1. Install Extension

```bash
cd extensions/vscode
npm install
npm run package
```

Then install the `.vsix` file in VS Code.

#### 2. Use in VS Code

- Open Command Palette: `Cmd+Shift+P`
- Type: `Magic Skills: Execute Skill`
- Select a skill and provide parameters

### Custom Integration

Use the REST API:

```python
import requests

response = requests.post(
    "http://localhost:3000/api/skills/execute",
    headers={"X-API-Key": "your-key"},
    json={
        "skill_name": "unit-test-gen",
        "params": {"input": "def add(a,b): return a+b"}
    }
)

result = response.json()
```

---

# 简体中文

**简体中文** | [English](#english) | [繁體中文](#繁體中文)

---

## 支持的 AI 工具

- ✅ **Kiro** - 通过 MCP (内置支持)
- ✅ **Cursor** - 通过 MCP
- ✅ **Claude Desktop** - 通过 MCP
- ✅ **VS Code** - 通过扩展
- ✅ **Trae** - 通过 MCP
- ✅ **OpenCode** - 通过 API
- ✅ **Codex** - 通过 API

## 命令格式

Magic Skills 在所有 AI 工具中使用统一的命令格式：

```
/mgc-<分类>-<技能名>
```

**示例：**
- `/mgc-java-backend-controller-gen` - 生成 Spring Boot 控制器
- `/mgc-software-testing-unit-test-gen` - 生成单元测试
- `/mgc-android-os-aidl-interface-gen` - 生成 AIDL 接口

## 特殊命令

- `/mgc-list` - 列出所有可用技能
- `/mgc-help` - 显示帮助信息
- `/mgc-models` - 列出可用的 LLM 模型
- `/mgc-version` - 显示版本

## 自动补全

在支持的 AI 工具中输入 `/` 后，Magic Skills 会自动显示可用的命令和技能。

## Kiro IDE 集成

Kiro IDE 通过 MCP 内置支持 Magic Skills。

### 1. 配置（自动检测）

项目已包含 `.kiro/mcp.json` 文件：

```json
{
  "mcpServers": {
    "magic-skills": {
      "command": "python",
      "args": ["-m", "src.mcp.server"],
      "env": {
        "PYTHONPATH": "${workspaceFolder}",
        "OPENAI_API_KEY": "${env:OPENAI_API_KEY}"
      }
    }
  }
}
```

### 2. 在 Kiro 中使用

Kiro 会自动检测并使用 Magic Skills。你可以：

**通过命令面板：**
```
Cmd+Shift+P → "Magic Skills: 执行技能"
```

**通过命令（推荐）：**
```
/mgc-java-backend-controller-gen 创建一个用户管理 API，包含增删改查操作
```

**通过内联聊天：**
```
@kiro 使用 /mgc-java-backend-controller-gen 创建用户 API
```

**通过 Spec 模式：**
```
@kiro 使用 /mgc-software-testing-unit-test-gen 为这个函数生成单元测试
```

**自动补全：**
输入 `/mgc-` 后，Kiro 会显示可用技能：
```
/mgc-[TAB]
  /mgc-java-backend-controller-gen
  /mgc-java-backend-service-gen
  /mgc-software-testing-unit-test-gen
  ...
```

### 3. Kiro 专属功能

- **智能建议**：Kiro 根据上下文推荐相关技能
- **Spec 集成**：技能与 Kiro 的规范驱动开发集成
- **成本追踪**：内置成本估算和追踪
- **多模型支持**：从 12+ LLM 提供商中选择

## Cursor 集成

### 1. 配置 MCP

创建 `.cursor/mcp.json`：

```json
{
  "mcpServers": {
    "magic-skills": {
      "command": "python",
      "args": ["-m", "src.mcp.server"],
      "env": {
        "OPENAI_API_KEY": "your-key"
      }
    }
  }
}
```

### 2. 在 Cursor 中使用

打开 Cursor 命令面板 (`Cmd+Shift+P`)，输入：

```
使用 spring-boot-controller-gen 创建用户 API
```

## Claude Desktop 集成

### 1. 配置 MCP

创建 `claude_desktop_config.json`：

```json
{
  "mcpServers": {
    "magic-skills": {
      "command": "python",
      "args": ["-m", "src.mcp.server"],
      "env": {
        "OPENAI_API_KEY": "your-key"
      }
    }
  }
}
```

### 2. 在 Claude Desktop 中使用

```
使用 unit-test-gen 为这个函数创建测试
```

## VS Code 集成

### 1. 安装扩展

```bash
cd extensions/vscode
npm install
npm run package
```

然后在 VS Code 中安装生成的 `.vsix` 文件。

### 2. 在 VS Code 中使用

- 打开命令面板：`Cmd+Shift+P`
- 输入：`Magic Skills: 执行技能`
- 选择技能并提供参数

## 自定义集成

使用 REST API：

```python
import requests

response = requests.post(
    "http://localhost:3000/api/skills/execute",
    headers={"X-API-Key": "your-key"},
    json={
        "skill_name": "unit-test-gen",
        "params": {"input": "def add(a,b): return a+b"}
    }
)

result = response.json()
```

## 上下文传递

Magic Skills 支持多种上下文传递方式：

### 1. 选中的文本

```python
{
  "params": {
    "selected_text": "选中的代码",
    "language": "python"
  }
}
```

### 2. 当前文件

```python
{
  "params": {
    "file_path": "/path/to/file.py",
    "file_content": "整个文件内容"
  }
}
```

### 3. 项目结构

```python
{
  "params": {
    "project_structure": "目录树",
    "relevant_files": ["file1.py", "file2.py"]
  }
}
```

---

# 繁體中文

**繁體中文** | [English](#english) | [简体中文](#简体中文)

---

## 支援的 AI 工具

- ✅ **Kiro** - 透過 MCP (內建支援)
- ✅ **Cursor** - 透過 MCP
- ✅ **Claude Desktop** - 透過 MCP
- ✅ **VS Code** - 透過擴充功能
- ✅ **Trae** - 透過 MCP
- ✅ **OpenCode** - 透過 API
- ✅ **Codex** - 透過 API

## 命令格式

Magic Skills 在所有 AI 工具中使用統一的命令格式：

```
/mgc-<分類>-<技能名>
```

**範例：**
- `/mgc-java-backend-controller-gen` - 產生 Spring Boot 控制器
- `/mgc-software-testing-unit-test-gen` - 產生單元測試
- `/mgc-android-os-aidl-interface-gen` - 產生 AIDL 介面

## 特殊命令

- `/mgc-list` - 列出所有可用技能
- `/mgc-help` - 顯示說明資訊
- `/mgc-models` - 列出可用的 LLM 模型
- `/mgc-version` - 顯示版本

## 自動補全

在支援的 AI 工具中輸入 `/` 後，Magic Skills 會自動顯示可用的命令和技能。

## Kiro IDE 整合

Kiro IDE 透過 MCP 內建支援 Magic Skills。

### 1. 設定（自動偵測）

專案已包含 `.kiro/mcp.json` 檔案：

```json
{
  "mcpServers": {
    "magic-skills": {
      "command": "python",
      "args": ["-m", "src.mcp.server"],
      "env": {
        "PYTHONPATH": "${workspaceFolder}",
        "OPENAI_API_KEY": "${env:OPENAI_API_KEY}"
      }
    }
  }
}
```

### 2. 在 Kiro 中使用

Kiro 會自動偵測並使用 Magic Skills。你可以：

**透過命令面板：**
```
Cmd+Shift+P → "Magic Skills: 執行技能"
```

**透過命令（推薦）：**
```
/mgc-java-backend-controller-gen 建立一個使用者管理 API，包含增刪改查操作
```

**透過內嵌聊天：**
```
@kiro 使用 /mgc-java-backend-controller-gen 建立使用者 API
```

**透過 Spec 模式：**
```
@kiro 使用 /mgc-software-testing-unit-test-gen 為這個函式產生單元測試
```

**自動補全：**
輸入 `/mgc-` 後，Kiro 會顯示可用技能：
```
/mgc-[TAB]
  /mgc-java-backend-controller-gen
  /mgc-java-backend-service-gen
  /mgc-software-testing-unit-test-gen
  ...
```

### 3. Kiro 專屬功能

- **智慧建議**：Kiro 根據上下文推薦相關技能
- **Spec 整合**：技能與 Kiro 的規範驅動開發整合
- **成本追蹤**：內建成本估算和追蹤
- **多模型支援**：從 12+ LLM 提供商中選擇

## Cursor 整合

### 1. 設定 MCP

建立 `.cursor/mcp.json`：

```json
{
  "mcpServers": {
    "magic-skills": {
      "command": "python",
      "args": ["-m", "src.mcp.server"],
      "env": {
        "OPENAI_API_KEY": "your-key"
      }
    }
  }
}
```

### 2. 在 Cursor 中使用

開啟 Cursor 命令面板 (`Cmd+Shift+P`)，輸入：

```
使用 spring-boot-controller-gen 建立使用者 API
```

## Claude Desktop 整合

### 1. 設定 MCP

建立 `claude_desktop_config.json`：

```json
{
  "mcpServers": {
    "magic-skills": {
      "command": "python",
      "args": ["-m", "src.mcp.server"],
      "env": {
        "OPENAI_API_KEY": "your-key"
      }
    }
  }
}
```

### 2. 在 Claude Desktop 中使用

```
使用 unit-test-gen 為這個函式建立測試
```

## VS Code 整合

### 1. 安裝擴充功能

```bash
cd extensions/vscode
npm install
npm run package
```

然後在 VS Code 中安裝產生的 `.vsix` 檔案。

### 2. 在 VS Code 中使用

- 開啟命令面板：`Cmd+Shift+P`
- 輸入：`Magic Skills: 執行技能`
- 選擇技能並提供參數

## 自訂整合

使用 REST API：

```python
import requests

response = requests.post(
    "http://localhost:3000/api/skills/execute",
    headers={"X-API-Key": "your-key"},
    json={
        "skill_name": "unit-test-gen",
        "params": {"input": "def add(a,b): return a+b"}
    }
)

result = response.json()
```

## 上下文傳遞

Magic Skills 支援多種上下文傳遞方式：

### 1. 選取的文字

```python
{
  "params": {
    "selected_text": "選取的程式碼",
    "language": "python"
  }
}
```

### 2. 目前檔案

```python
{
  "params": {
    "file_path": "/path/to/file.py",
    "file_content": "整個檔案內容"
  }
}
```

### 3. 專案結構

```python
{
  "params": {
    "project_structure": "目錄樹",
    "relevant_files": ["file1.py", "file2.py"]
  }
}
```
