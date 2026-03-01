# Magic Skills 🪄

<div align="center">

**English** | [简体中文](#简体中文) | [繁體中文](#繁體中文)

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen)](tests/)

AI-powered skill platform for 6 professional domains with intelligent iteration and AI tool integration.

</div>

---

## 🌟 Features

- **6 Professional Domains**: Java Backend, Android OS, Digital Analytics, Mobile App, Multi-language Translation, Software Testing
- **160+ AI Skills**: Professionally designed for real-world development scenarios
- **Multi-LLM Support**: OpenAI, Anthropic, Google Gemini, and 8+ more providers
- **AI Tool Integration**: Native MCP support for Kiro, Cursor, Claude Desktop, VS Code
- **Self-Optimization**: Automatic skill improvement based on user feedback
- **Open Source**: MIT License, community-driven

## 🚀 Quick Start

### One-Click Installation (Recommended)

#### macOS / Linux

```bash
# Using curl
curl -fsSL https://raw.githubusercontent.com/magicskills/magic-skills/main/install.sh | bash

# Or using wget
wget -qO- https://raw.githubusercontent.com/magicskills/magic-skills/main/install.sh | bash
```

#### Windows (PowerShell)

```powershell
irm https://raw.githubusercontent.com/magicskills/magic-skills/main/install.ps1 | iex
```

#### Manual Installation

```bash
# Clone repository
git clone https://github.com/magicskills/magic-skills.git
cd magic-skills

# Run install script
chmod +x install.sh
./install.sh
```

### Usage

#### CLI

```bash
# List all skills
magic-skill list

# Execute a skill (using /mgc- command format)
magic-skill exec /mgc-java-backend-controller-gen -p '{"endpoint": "/api/users", "method": "GET", "description": "Get all users"}'

# Or use traditional format
magic-skill exec spring-boot-controller-gen -p '{"endpoint": "/api/users", "method": "GET", "description": "Get all users"}'

# Get skill info
magic-skill info spring-boot-controller-gen
```

#### REST API

```bash
# Start API server
python -m api.main

# List skills
curl http://localhost:3000/api/skills/list

# Execute skill
curl -X POST http://localhost:3000/api/skills/execute \
  -H "Content-Type: application/json" \
  -d '{
    "skill_name": "spring-boot-controller-gen",
    "params": {
      "endpoint": "/api/users",
      "method": "GET",
      "description": "Get all users"
    }
  }'
```

#### Kiro IDE (Built-in Support)

Kiro IDE has built-in support for Magic Skills. Just open the project:

```bash
kiro /path/to/magic-skills
```

Then use in Kiro with `/mgc-` commands:
```
/mgc-java-backend-controller-gen Create a user management API
```

Or with @kiro mention:
```
@kiro Use /mgc-java-backend-controller-gen to create a user API
```

Type `/mgc-` for auto-completion of available skills.

See [KIRO_INTEGRATION.md](KIRO_INTEGRATION.md) for details.

#### MCP Server (Cursor/Claude Desktop)

```bash
# Start MCP server
python -m src.mcp.server
```

## 📁 Project Structure

```
magic_skills/
├── skills/                    # Domain-specific skills
│   ├── java-backend/         # Java backend development (30 skills)
│   ├── android-os/           # Android OS development (25 skills)
│   ├── digital-analytics/    # Digital analytics (30 skills)
│   ├── mobile-app/           # Mobile app development (25 skills)
│   ├── multi-language/       # Multi-language translation (20 skills)
│   └── software-testing/     # Software testing (30 skills)
├── src/                       # Core source code
│   ├── core/                 # Skill management
│   ├── models/               # LLM providers (12 providers)
│   ├── optimization/         # Self-optimization engine
│   └── mcp/                  # MCP server
├── cli/                       # Command line interface
├── api/                       # REST API
├── tests/                     # Test suite
└── docs/                      # Documentation
```

## 🛠️ Development

### Run Tests

```bash
pytest
```

### Code Formatting

```bash
black src/ cli/ api/
flake8 src/ cli/ api/
mypy src/ cli/ api/
```

## 📚 Documentation

- [Installation Guide](docs/installation.md)
- [API Documentation](docs/api.md)
- [Skill Development Guide](docs/skill-development.md)
- [AI Tool Integration](docs/ai-tool-integration.md)

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

# 简体中文

<div align="center">

**简体中文** | [English](#magic-skills-) | [繁體中文](#繁體中文)

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen)](tests/)

面向6个专业领域的AI技能平台，具备智能迭代和AI工具集成能力。

</div>

---

## 🌟 功能特性

- **6大专业领域**：Java后端、Android OS、数字化分析、移动App、多语言翻译、软件测试
- **160+ AI技能**：针对真实开发场景专业设计
- **多LLM支持**：OpenAI、Anthropic、Google Gemini等12+提供商
- **AI工具集成**：原生MCP支持Kiro、Cursor、Claude Desktop、VS Code
- **自我优化**：基于用户反馈自动改进技能
- **开源**：MIT许可证，社区驱动

## 🚀 快速开始

### 一键安装（推荐）

#### macOS / Linux

```bash
# 使用 curl
curl -fsSL https://raw.githubusercontent.com/magicskills/magic-skills/main/install.sh | bash

# 或使用 wget
wget -qO- https://raw.githubusercontent.com/magicskills/magic-skills/main/install.sh | bash
```

#### Windows (PowerShell)

```powershell
irm https://raw.githubusercontent.com/magicskills/magic-skills/main/install.ps1 | iex
```

#### 手动安装

```bash
# 克隆仓库
git clone https://github.com/magicskills/magic-skills.git
cd magic-skills

# 运行安装脚本
chmod +x install.sh
./install.sh
```

### 传统安装方式

```bash
# 克隆仓库
git clone https://github.com/magicskills/magic-skills.git
cd magic-skills

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -e ".[dev]"
```

### 使用方法

#### 命令行工具 (CLI)

```bash
# 列出所有技能
magic-skill list

# 执行技能（使用 /mgc- 命令格式）
magic-skill exec /mgc-java-backend-controller-gen -p '{"endpoint": "/api/users", "method": "GET", "description": "获取所有用户"}'

# 或使用传统格式
magic-skill exec spring-boot-controller-gen -p '{"endpoint": "/api/users", "method": "GET", "description": "获取所有用户"}'

# 获取技能信息
magic-skill info spring-boot-controller-gen
```

#### REST API

```bash
# 启动API服务器
python -m api.main

# 列出技能
curl http://localhost:3000/api/skills/list

# 执行技能
curl -X POST http://localhost:3000/api/skills/execute \
  -H "Content-Type: application/json" \
  -d '{
    "skill_name": "spring-boot-controller-gen",
    "params": {
      "endpoint": "/api/users",
      "method": "GET",
      "description": "获取所有用户"
    }
  }'
```

#### Kiro IDE (内置支持)

Kiro IDE 内置支持 Magic Skills。只需在 Kiro 中打开项目：

```bash
kiro /path/to/magic-skills
```

然后在 Kiro 中使用 `/mgc-` 命令：
```
/mgc-java-backend-controller-gen 创建一个用户管理 API
```

或使用 @kiro 提及：
```
@kiro 使用 /mgc-java-backend-controller-gen 创建用户 API
```

输入 `/mgc-` 查看可用技能的自动补全。

详见 [KIRO_INTEGRATION.md](KIRO_INTEGRATION.md)。

#### MCP服务器 (Cursor/Claude Desktop)

```bash
# 启动MCP服务器
python -m src.mcp.server
```

## 📁 项目结构

```
magic_skills/
├── skills/                    # 领域特定技能
│   ├── java-backend/         # Java后端开发 (30个技能)
│   ├── android-os/           # Android OS开发 (25个技能)
│   ├── digital-analytics/    # 数字化分析 (30个技能)
│   ├── mobile-app/           # 移动App开发 (25个技能)
│   ├── multi-language/       # 多语言翻译 (20个技能)
│   └── software-testing/     # 软件测试 (30个技能)
├── src/                       # 核心源代码
│   ├── core/                 # 技能管理
│   ├── models/               # LLM提供商 (12个提供商)
│   ├── optimization/         # 自我优化引擎
│   └── mcp/                  # MCP服务器
├── cli/                       # 命令行界面
├── api/                       # REST API
├── tests/                     # 测试套件
└── docs/                      # 文档
```

## 🛠️ 开发

### 运行测试

```bash
pytest
```

### 代码格式化

```bash
black src/ cli/ api/
flake8 src/ cli/ api/
mypy src/ cli/ api/
```

## 📚 文档

- [安装指南](docs/installation.md)
- [API文档](docs/api.md)
- [技能开发指南](docs/skill-development.md)
- [AI工具集成](docs/ai-tool-integration.md)

## 🤝 贡献

我们欢迎贡献！请参阅 [CONTRIBUTING.md](CONTRIBUTING.md) 了解指南。

## 📄 许可证

MIT许可证 - 详情请参见 [LICENSE](LICENSE) 文件。

---

# 繁體中文

<div align="center">

**繁體中文** | [English](#magic-skills-) | [简体中文](#简体中文)

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen)](tests/)

面向6個專業領域的AI技能平台，具備智能迭代和AI工具整合能力。

</div>

---

## 🌟 功能特性

- **6大專業領域**：Java後端、Android OS、數位化分析、行動App、多語言翻譯、軟體測試
- **160+ AI技能**：針對真實開發場景專業設計
- **多LLM支援**：OpenAI、Anthropic、Google Gemini等12+提供商
- **AI工具整合**：原生MCP支援Kiro、Cursor、Claude Desktop、VS Code
- **自我優化**：基於用戶回饋自動改進技能
- **開源**：MIT授權條款，社群驅動

## 🚀 快速開始

### 一鍵安裝（推薦）

#### macOS / Linux

```bash
# 使用 curl
curl -fsSL https://raw.githubusercontent.com/magicskills/magic-skills/main/install.sh | bash

# 或使用 wget
wget -qO- https://raw.githubusercontent.com/magicskills/magic-skills/main/install.sh | bash
```

#### Windows (PowerShell)

```powershell
irm https://raw.githubusercontent.com/magicskills/magic-skills/main/install.ps1 | iex
```

#### 手動安裝

```bash
# 克隆倉庫
git clone https://github.com/magicskills/magic-skills.git
cd magic-skills

# 執行安裝腳本
chmod +x install.sh
./install.sh
```

### 傳統安裝方式

```bash
# 克隆倉庫
git clone https://github.com/magicskills/magic-skills.git
cd magic-skills

# 建立虛擬環境
python3 -m venv venv
source venv/bin/activate

# 安裝依賴
pip install -e ".[dev]"
```

### 使用方法

#### 命令列工具 (CLI)

```bash
# 列出所有技能
magic-skill list

# 執行技能（使用 /mgc- 命令格式）
magic-skill exec /mgc-java-backend-controller-gen -p '{"endpoint": "/api/users", "method": "GET", "description": "獲取所有使用者"}'

# 或使用傳統格式
magic-skill exec spring-boot-controller-gen -p '{"endpoint": "/api/users", "method": "GET", "description": "獲取所有使用者"}'

# 獲取技能資訊
magic-skill info spring-boot-controller-gen
```

#### REST API

```bash
# 啟動API伺服器
python -m api.main

# 列出技能
curl http://localhost:3000/api/skills/list

# 執行技能
curl -X POST http://localhost:3000/api/skills/execute \
  -H "Content-Type: application/json" \
  -d '{
    "skill_name": "spring-boot-controller-gen",
    "params": {
      "endpoint": "/api/users",
      "method": "GET",
      "description": "獲取所有使用者"
    }
  }'
```

#### Kiro IDE (內建支援)

Kiro IDE 內建支援 Magic Skills。只需在 Kiro 中開啟專案：

```bash
kiro /path/to/magic-skills
```

然後在 Kiro 中使用 `/mgc-` 命令：
```
/mgc-java-backend-controller-gen 建立一個使用者管理 API
```

或使用 @kiro 提及：
```
@kiro 使用 /mgc-java-backend-controller-gen 建立使用者 API
```

輸入 `/mgc-` 查看可用技能的自動補全。

詳見 [KIRO_INTEGRATION.md](KIRO_INTEGRATION.md)。

#### MCP伺服器 (Cursor/Claude Desktop)

```bash
# 啟動MCP伺服器
python -m src.mcp.server
```

## 📁 專案結構

```
magic_skills/
├── skills/                    # 領域特定技能
│   ├── java-backend/         # Java後端開發 (30個技能)
│   ├── android-os/           # Android OS開發 (25個技能)
│   ├── digital-analytics/    # 數位化分析 (30個技能)
│   ├── mobile-app/           # 行動App開發 (25個技能)
│   ├── multi-language/       # 多語言翻譯 (20個技能)
│   └── software-testing/     # 軟體測試 (30個技能)
├── src/                       # 核心原始碼
│   ├── core/                 # 技能管理
│   ├── models/               # LLM提供商 (12個提供商)
│   ├── optimization/         # 自我優化引擎
│   └── mcp/                  # MCP伺服器
├── cli/                       # 命令列介面
├── api/                       # REST API
├── tests/                     # 測試套件
└── docs/                      # 文件
```

## 🛠️ 開發

### 執行測試

```bash
pytest
```

### 程式碼格式化

```bash
black src/ cli/ api/
flake8 src/ cli/ api/
mypy src/ cli/ api/
```

## 📚 文件

- [安裝指南](docs/installation.md)
- [API文件](docs/api.md)
- [技能開發指南](docs/skill-development.md)
- [AI工具整合](docs/ai-tool-integration.md)

## 🤝 貢獻

我們歡迎貢獻！請參閱 [CONTRIBUTING.md](CONTRIBUTING.md) 了解指南。

## 📄 授權條款

MIT授權條款 - 詳情請參見 [LICENSE](LICENSE) 檔案。

## 🙏 致謝

- 使用 [FastAPI](https://fastapi.tiangolo.com/) 建置
- LLM整合由 [OpenAI](https://openai.com/)、[Anthropic](https://anthropic.com/)、[Google](https://ai.google.dev/) 提供支援
- MCP協議由 [Anthropic](https://modelcontextprotocol.io/) 提供
