## Why

构建一个功能完整、可用于开源的 AI 技能平台，解决当前 AI 应用开发中 LLM 集成碎片化、技能复用困难、缺乏智能优化机制的问题。**特别针对主流 AI 编程工具（Cursor、Claude Desktop、VS Code Copilot、Trae、OpenCode、Codex）提供深度集成**，让开发者能够在熟悉的编程环境中直接调用 Magic Skills，实现"AI 工具 + 技能"的无缝工作流。**聚焦 6 个专业领域**：
1. **Java 后端开发**：Spring Boot、微服务、数据库相关的 AI 编程技能
2. **Android 手机 OS 源码开发**：AOSP、HAL、驱动、系统服务相关的 AI 编程技能  
3. **软件公司数字化分析**：数据分析、商业智能、机器学习相关的 AI 分析技能
4. **移动 App 开发**：Android/iOS App 开发相关的 AI 编程技能
5. **软件多语言翻译**：国际化、本地化、翻译相关的 AI 处理技能
6. **软件测试与问题分析**：自动化测试、问题诊断、质量保证相关的 AI 分析技能

通过统一的抽象层支持国内外主流 LLM（10+ 个），提供基于文件系统的技能管理系统，并引入自我优化引擎实现 Prompt 和参数的自动调优，降低 AI 应用开发门槛，建立技术影响力并吸引社区共建。

## What Changes

- **新增技能管理平台核心架构**
  - 基于文件系统的技能存储和管理
  - 统一的 LLM 抽象层（Level 2 集成）
  - CLI 命令行工具和 REST API 双接口
  - 自我优化引擎（反馈收集、Prompt 优化、参数调优）

- **新增 AI 编程工具集成（MVP 核心功能）**
  - **MCP Server**：实现 Model Context Protocol，支持 Cursor、Claude Desktop 原生集成
  - **VS Code 扩展**：专用插件，支持代码审查、重构、测试生成等场景
  - **上下文管理**：读取编辑器选中代码、文件内容、项目结构作为技能输入
  - **Trae/OpenCode 适配器**：为其他 AI 工具提供集成支持
  - **智能工作流**：AI 助手自动推荐和调用技能

- **新增 LLM 提供商集成**
  - 国际主流 LLM：OpenAI GPT、Anthropic Claude、Google Gemini、Meta Llama、Mistral AI、Cohere
  - 国内主流 LLM：通义千问、文心一言、讯飞星火、Kimi、DeepSeek
  - 统一的 `generate()` 和 `stream()` 接口

- **新增智能迭代功能**
  - 用户反馈收集系统（点赞/点踩）
  - Prompt 版本管理和 A/B 测试
  - 基于执行日志的性能分析
  - 自动参数调优（temperature、top_p 等）
  - 模型选择推荐系统

- **新增开源基础设施**
  - 完整的文档系统（README、API 文档、贡献指南）
  - 测试套件（目标覆盖率 > 80%）
  - CI/CD 管道和自动化测试
  - 示例技能库（10+ 个示例）

## Capabilities

### New Capabilities
- `skill-management`: 技能加载、注册、执行、版本控制的核心能力
- `llm-integration`: 统一 LLM 抽象层，支持 10+ 个主流模型的接入和调用
- `self-optimization`: 基于反馈和日志的自我优化引擎，包括 Prompt 优化和参数调优
- `cli-interface`: 命令行工具，提供技能执行、管理、配置的 CLI 命令
- `rest-api`: RESTful API 服务，支持本地调用的 HTTP 接口
- `feedback-system`: 用户反馈收集和分析系统，支持点赞/点踩和日志记录
- `documentation`: 完整的开源文档体系，包括安装指南、API 文档、贡献指南
- `ai-tool-integration`: **MVP 核心** - 与主流 AI 编程工具（Cursor、Claude Desktop、VS Code 等）的深度集成能力，包括 MCP Server、VS Code 扩展、上下文管理
- `domain-specific-skills`: **MVP 核心** - 聚焦 6 个专业领域的 AI 编程技能集：
  - `java-backend`: Java 后端开发相关的 30+ 个 AI 编程技能
  - `android-os`: Android 手机 OS 源码开发相关的 25+ 个 AI 编程技能
  - `digital-analytics`: 软件公司数字化分析相关的 30+ 个 AI 分析技能
  - `mobile-app`: Android/iOS App 开发相关的 25+ 个 AI 编程技能
  - `multi-language`: 软件多语言翻译相关的 20+ 个 AI 处理技能
  - `software-testing`: 软件测试与问题分析相关的 30+ 个 AI 分析技能

### Modified Capabilities
<!-- 无修改的现有能力，这是全新项目 -->

## Impact

- **代码影响**
  - 新增 `skills/` 目录用于存放技能定义（YAML 配置 + Prompt 模板 + Python 处理逻辑）
  - 新增 `src/core/` 核心模块（SkillManager、ModelManager、OptimizationEngine）
  - 新增 `src/models/` LLM 提供商集成模块（10+ 个提供商）
  - 新增 `src/optimization/` 自我优化模块（PromptOptimizer、ParameterTuner、ModelSelector）
  - 新增 `src/mcp/` **MVP 核心** - MCP Server 实现（与 AI 工具集成）
  - 新增 `extensions/vscode/` VS Code 专用插件
  - 新增 `cli/` 命令行工具
  - 新增 `api/` REST API 服务

- **依赖影响**
  - Python 3.10+
  - LLM SDK：openai、anthropic、google-generativeai 等
  - Web 框架：FastAPI（REST API）
  - CLI 框架：Typer 或 Click
  - 数据库：SQLite（反馈存储，可选）
  - 测试：pytest、pytest-asyncio

- **部署影响**
  - 本地运行模式（localhost API 服务 + CLI 工具）
  - 支持 Docker 容器化（可选）
  - 环境变量配置（API 密钥管理）

- **用户影响**
  - 开发者：通过 API/SDK 集成技能到应用
  - 最终用户：通过 CLI 工具直接使用技能
  - 贡献者：通过文件系统轻松添加新技能

- **时间框架**
  - 开发周期：**4 周（MVP 包含 AI 工具集成）**
  - 发布计划：
    - v1.0.0（MVP）：核心技能管理 + LLM 集成 + **AI 工具集成（MCP Server + VS Code 扩展）**
    - v1.1.0（自我优化增强）：完整自我优化引擎 + Trae/OpenCode 集成
    - v2.0.0（生态系统）：技能市场、工作流、多语言 SDK
