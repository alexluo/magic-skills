# Magic Skills 指令大全

**English** | [简体中文](#简体中文) | [繁體中文](#繁體中文)

---

## English

### CLI Commands

#### Basic Commands

| Command | Description | Example |
|---------|-------------|---------|
| `magic-skill --help` | Show help information | - |
| `magic-skill --version` | Show version | - |
| `magic-skill list` | List all skills | `magic-skill list` |
| `magic-skill list --category <category>` | List skills by category | `magic-skill list --category java-backend` |
| `magic-skill info <skill-name>` | Get skill information | `magic-skill info spring-boot-controller-gen` |
| `magic-skill exec <skill-name> -p '<params>'` | Execute a skill | `magic-skill exec spring-boot-controller-gen -p '{"endpoint":"/api/users"}'` |
| `magic-skill exec /mgc-<category>-<skill> -p '<params>'` | Execute with new format | `magic-skill exec /mgc-java-backend-controller-gen -p '{"endpoint":"/api/users"}'` |

#### Init Commands

| Command | Description | Example |
|---------|-------------|---------|
| `magic-skill init` | Initialize new skill project | `magic-skill init my-skill` |

### REST API Endpoints

#### Server Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `GET` | `/docs` | API documentation (Swagger UI) |

#### Skills API

| Method | Endpoint | Description | Example Request |
|--------|----------|-------------|-----------------|
| `GET` | `/api/skills/list` | List all skills | - |
| `GET` | `/api/skills/info/{name}` | Get skill info | `/api/skills/info/spring-boot-controller-gen` |
| `POST` | `/api/skills/execute` | Execute skill | `{"skill_name":"unit-test-gen","params":{"input":"code"}}` |

#### Models API

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/models/list` | List available LLM providers and models |
| `POST` | `/api/models/select` | Select default model | `{"provider":"openai","model":"gpt-4o"}` |

### MCP Server Commands (AI Tools)

When using Magic Skills through MCP (Cursor, Claude Desktop, Kiro, etc.):

#### Special Commands

| Command | Description |
|---------|-------------|
| `/mgc-list` | List all available skills with commands |
| `/mgc-help` | Show help information |
| `/mgc-models` | List available LLM models |
| `/mgc-version` | Show version |

#### Skill Execution Commands

| Command Format | Description | Example |
|----------------|-------------|---------|
| `/mgc-java-backend-<skill>` | Java backend skills | `/mgc-java-backend-controller-gen` |
| `/mgc-android-os-<skill>` | Android OS skills | `/mgc-android-os-aidl-interface-gen` |
| `/mgc-digital-analytics-<skill>` | Digital analytics skills | `/mgc-digital-analytics-funnel-analysis` |
| `/mgc-mobile-app-<skill>` | Mobile app skills | `/mgc-mobile-app-swiftui-view-gen` |
| `/mgc-multi-language-<skill>` | Translation skills | `/mgc-multi-language-i18n-key-extract` |
| `/mgc-software-testing-<skill>` | Testing skills | `/mgc-software-testing-unit-test-gen` |

### Python API

```python
from src.core.skill_manager import SkillManager
from src.models import ModelManager

# Skill Manager
sm = SkillManager()
sm.load_all_skills()
sm.list_skills()
sm.get_skill("skill-name")
sm.execute_skill("skill-name", params={})

# Model Manager
mm = ModelManager()
mm.list_providers()
mm.list_models("openai")
mm.set_default_provider("openai", "gpt-4o")
mm.generate(messages=[...])
mm.estimate_cost(input_tokens=1000, output_tokens=500)
```

### Verification Commands

| Command | Description |
|---------|-------------|
| `python verify_all.py` | Run full verification |
| `./quick_verify.sh` | Quick verification |
| `pytest` | Run all tests |
| `pytest tests/test_skill_manager.py -v` | Run specific tests |

---

# 简体中文

**简体中文** | [English](#english) | [繁體中文](#繁體中文)

---

## CLI 命令

### 基础命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `magic-skill --help` | 显示帮助信息 | - |
| `magic-skill --version` | 显示版本 | - |
| `magic-skill list` | 列出所有技能 | `magic-skill list` |
| `magic-skill list --category <category>` | 按分类列出技能 | `magic-skill list --category java-backend` |
| `magic-skill info <skill-name>` | 获取技能信息 | `magic-skill info spring-boot-controller-gen` |
| `magic-skill exec <skill-name> -p '<params>'` | 执行技能 | `magic-skill exec spring-boot-controller-gen -p '{"endpoint":"/api/users"}'` |
| `magic-skill exec /mgc-<category>-<skill> -p '<params>'` | 使用新格式执行 | `magic-skill exec /mgc-java-backend-controller-gen -p '{"endpoint":"/api/users"}'` |

### 初始化命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `magic-skill init` | 初始化新技能项目 | `magic-skill init my-skill` |

### REST API 端点

#### 服务器管理

| 方法 | 端点 | 说明 |
|------|------|------|
| `GET` | `/health` | 健康检查 |
| `GET` | `/docs` | API 文档 (Swagger UI) |

#### 技能 API

| 方法 | 端点 | 说明 | 示例请求 |
|------|------|------|----------|
| `GET` | `/api/skills/list` | 列出所有技能 | - |
| `GET` | `/api/skills/info/{name}` | 获取技能信息 | `/api/skills/info/spring-boot-controller-gen` |
| `POST` | `/api/skills/execute` | 执行技能 | `{"skill_name":"unit-test-gen","params":{"input":"code"}}` |

#### 模型 API

| 方法 | 端点 | 说明 |
|------|------|------|
| `GET` | `/api/models/list` | 列出可用的 LLM 提供商和模型 |
| `POST` | `/api/models/select` | 选择默认模型 | `{"provider":"openai","model":"gpt-4o"}` |

### MCP 服务器命令 (AI 工具)

通过 MCP 使用 Magic Skills 时 (Cursor, Claude Desktop, Kiro 等)：

#### 特殊命令

| 命令 | 说明 |
|------|------|
| `/mgc-list` | 列出所有可用技能及命令 |
| `/mgc-help` | 显示帮助信息 |
| `/mgc-models` | 列出可用的 LLM 模型 |
| `/mgc-version` | 显示版本 |

#### 技能执行命令

| 命令格式 | 说明 | 示例 |
|----------|------|------|
| `/mgc-java-backend-<skill>` | Java 后端技能 | `/mgc-java-backend-controller-gen` |
| `/mgc-android-os-<skill>` | Android OS 技能 | `/mgc-android-os-aidl-interface-gen` |
| `/mgc-digital-analytics-<skill>` | 数字化分析技能 | `/mgc-digital-analytics-funnel-analysis` |
| `/mgc-mobile-app-<skill>` | 移动应用技能 | `/mgc-mobile-app-swiftui-view-gen` |
| `/mgc-multi-language-<skill>` | 翻译技能 | `/mgc-multi-language-i18n-key-extract` |
| `/mgc-software-testing-<skill>` | 测试技能 | `/mgc-software-testing-unit-test-gen` |

### Python API

```python
from src.core.skill_manager import SkillManager
from src.models import ModelManager

# 技能管理器
sm = SkillManager()
sm.load_all_skills()           # 加载所有技能
sm.list_skills()               # 列出技能
sm.get_skill("skill-name")     # 获取技能
sm.execute_skill("skill-name", params={})  # 执行技能

# 模型管理器
mm = ModelManager()
mm.list_providers()            # 列出提供商
mm.list_models("openai")       # 列出模型
mm.set_default_provider("openai", "gpt-4o")  # 设置默认提供商
mm.generate(messages=[...])    # 生成内容
mm.estimate_cost(input_tokens=1000, output_tokens=500)  # 估算成本
```

### 验证命令

| 命令 | 说明 |
|------|------|
| `python verify_all.py` | 运行完整验证 |
| `./quick_verify.sh` | 快速验证 |
| `pytest` | 运行所有测试 |
| `pytest tests/test_skill_manager.py -v` | 运行特定测试 |

---

# 繁體中文

**繁體中文** | [English](#english) | [简体中文](#简体中文)

---

## CLI 命令

### 基礎命令

| 命令 | 說明 | 範例 |
|------|------|------|
| `magic-skill --help` | 顯示說明資訊 | - |
| `magic-skill --version` | 顯示版本 | - |
| `magic-skill list` | 列出所有技能 | `magic-skill list` |
| `magic-skill list --category <category>` | 按分類列出技能 | `magic-skill list --category java-backend` |
| `magic-skill info <skill-name>` | 取得技能資訊 | `magic-skill info spring-boot-controller-gen` |
| `magic-skill exec <skill-name> -p '<params>'` | 執行技能 | `magic-skill exec spring-boot-controller-gen -p '{"endpoint":"/api/users"}'` |
| `magic-skill exec /mgc-<category>-<skill> -p '<params>'` | 使用新格式執行 | `magic-skill exec /mgc-java-backend-controller-gen -p '{"endpoint":"/api/users"}'` |

### 初始化命令

| 命令 | 說明 | 範例 |
|------|------|------|
| `magic-skill init` | 初始化新技能專案 | `magic-skill init my-skill` |

### REST API 端點

#### 伺服器管理

| 方法 | 端點 | 說明 |
|------|------|------|
| `GET` | `/health` | 健康檢查 |
| `GET` | `/docs` | API 文件 (Swagger UI) |

#### 技能 API

| 方法 | 端點 | 說明 | 範例請求 |
|------|------|------|----------|
| `GET` | `/api/skills/list` | 列出所有技能 | - |
| `GET` | `/api/skills/info/{name}` | 取得技能資訊 | `/api/skills/info/spring-boot-controller-gen` |
| `POST` | `/api/skills/execute` | 執行技能 | `{"skill_name":"unit-test-gen","params":{"input":"code"}}` |

#### 模型 API

| 方法 | 端點 | 說明 |
|------|------|------|
| `GET` | `/api/models/list` | 列出可用的 LLM 提供商和模型 |
| `POST` | `/api/models/select` | 選擇預設模型 | `{"provider":"openai","model":"gpt-4o"}` |

### MCP 伺服器命令 (AI 工具)

透過 MCP 使用 Magic Skills 時 (Cursor, Claude Desktop, Kiro 等)：

#### 特殊命令

| 命令 | 說明 |
|------|------|
| `/mgc-list` | 列出所有可用技能及命令 |
| `/mgc-help` | 顯示說明資訊 |
| `/mgc-models` | 列出可用的 LLM 模型 |
| `/mgc-version` | 顯示版本 |

#### 技能執行命令

| 命令格式 | 說明 | 範例 |
|----------|------|------|
| `/mgc-java-backend-<skill>` | Java 後端技能 | `/mgc-java-backend-controller-gen` |
| `/mgc-android-os-<skill>` | Android OS 技能 | `/mgc-android-os-aidl-interface-gen` |
| `/mgc-digital-analytics-<skill>` | 數位化分析技能 | `/mgc-digital-analytics-funnel-analysis` |
| `/mgc-mobile-app-<skill>` | 行動應用技能 | `/mgc-mobile-app-swiftui-view-gen` |
| `/mgc-multi-language-<skill>` | 翻譯技能 | `/mgc-multi-language-i18n-key-extract` |
| `/mgc-software-testing-<skill>` | 測試技能 | `/mgc-software-testing-unit-test-gen` |

### Python API

```python
from src.core.skill_manager import SkillManager
from src.models import ModelManager

# 技能管理器
sm = SkillManager()
sm.load_all_skills()           # 載入所有技能
sm.list_skills()               # 列出技能
sm.get_skill("skill-name")     # 取得技能
sm.execute_skill("skill-name", params={})  # 執行技能

# 模型管理器
mm = ModelManager()
mm.list_providers()            # 列出提供商
mm.list_models("openai")       # 列出模型
mm.set_default_provider("openai", "gpt-4o")  # 設定預設提供商
mm.generate(messages=[...])    # 產生內容
mm.estimate_cost(input_tokens=1000, output_tokens=500)  # 估算成本
```

### 驗證命令

| 命令 | 說明 |
|------|------|
| `python verify_all.py` | 執行完整驗證 |
| `./quick_verify.sh` | 快速驗證 |
| `pytest` | 執行所有測試 |
| `pytest tests/test_skill_manager.py -v` | 執行特定測試 |
