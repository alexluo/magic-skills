# Magic Skills 安装指南

**English** | [简体中文](#简体中文) | [繁體中文](#繁體中文)

---

## English

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Git (optional, for cloning)

### Installation Steps

#### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/magic-skills.git
cd magic-skills
```

#### 2. Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Required: At least one LLM provider API key
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
GOOGLE_API_KEY=your_google_api_key

# Optional: Other providers
QWEN_API_KEY=your_qwen_api_key
ERNIE_API_KEY=your_ernie_api_key
SPARK_API_KEY=your_spark_api_key
KIMI_API_KEY=your_kimi_api_key
DEEPSEEK_API_KEY=your_deepseek_api_key
META_API_KEY=your_meta_api_key
MISTRAL_API_KEY=your_mistral_api_key
COHERE_API_KEY=your_cohere_api_key

# Optional: Server configuration
API_HOST=0.0.0.0
API_PORT=3000
LOG_LEVEL=INFO
```

#### 5. Verify Installation

```bash
# Run verification script
python verify_all.py

# Or run quick verification
./quick_verify.sh
```

### Usage

#### CLI

```bash
# List all skills
magic-skill list

# Execute a skill
magic-skill exec spring-boot-controller-gen -p '{"endpoint": "/api/users", "method": "GET"}'
```

#### REST API

```bash
# Start API server
python -m api.main

# Test API
curl http://localhost:3000/health
```

#### Python

```python
from src.core.skill_manager import SkillManager

sm = SkillManager()
sm.load_all_skills()
result = sm.execute_skill("unit-test-gen", {"input": "def add(a,b): return a+b"})
```

### Troubleshooting

**Issue**: `ModuleNotFoundError: No module named 'src'`

**Solution**: Ensure you're in the project root directory and virtual environment is activated.

**Issue**: `API key not found`

**Solution**: Check your `.env` file and ensure API keys are set correctly.

---

# 简体中文

**简体中文** | [English](#english) | [繁體中文](#繁體中文)

---

## 系统要求

- Python 3.9 或更高版本
- pip (Python 包管理器)
- Git (可选，用于克隆仓库)

## 安装步骤

### 1. 克隆仓库

```bash
git clone https://github.com/yourusername/magic-skills.git
cd magic-skills
```

### 2. 创建虚拟环境

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

在项目根目录创建 `.env` 文件：

```bash
# 必需：至少一个 LLM 提供商的 API 密钥
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
GOOGLE_API_KEY=your_google_api_key

# 可选：其他提供商
QWEN_API_KEY=your_qwen_api_key
ERNIE_API_KEY=your_ernie_api_key
SPARK_API_KEY=your_spark_api_key
KIMI_API_KEY=your_kimi_api_key
DEEPSEEK_API_KEY=your_deepseek_api_key
META_API_KEY=your_meta_api_key
MISTRAL_API_KEY=your_mistral_api_key
COHERE_API_KEY=your_cohere_api_key

# 可选：服务器配置
API_HOST=0.0.0.0
API_PORT=3000
LOG_LEVEL=INFO
```

### 5. 验证安装

```bash
# 运行完整验证脚本
python verify_all.py

# 或运行快速验证
./quick_verify.sh
```

## 使用方法

### 命令行工具 (CLI)

```bash
# 列出所有技能
magic-skill list

# 执行技能
magic-skill exec spring-boot-controller-gen -p '{"endpoint": "/api/users", "method": "GET"}'
```

### REST API

```bash
# 启动 API 服务器
python -m api.main

# 测试 API
curl http://localhost:3000/health
```

### Python

```python
from src.core.skill_manager import SkillManager

sm = SkillManager()
sm.load_all_skills()
result = sm.execute_skill("unit-test-gen", {"input": "def add(a,b): return a+b"})
```

## 常见问题

**问题**: `ModuleNotFoundError: No module named 'src'`

**解决**: 确保你在项目根目录，并且虚拟环境已激活。

**问题**: `API key not found`

**解决**: 检查 `.env` 文件，确保 API 密钥设置正确。

---

# 繁體中文

**繁體中文** | [English](#english) | [简体中文](#简体中文)

---

## 系統要求

- Python 3.9 或更高版本
- pip (Python 套件管理器)
- Git (可選，用於複製倉庫)

## 安裝步驟

### 1. 複製倉庫

```bash
git clone https://github.com/yourusername/magic-skills.git
cd magic-skills
```

### 2. 建立虛擬環境

```bash
# 建立虛擬環境
python3 -m venv venv

# 啟動虛擬環境
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

### 3. 安裝相依套件

```bash
pip install -r requirements.txt
```

### 4. 設定環境變數

在專案根目錄建立 `.env` 檔案：

```bash
# 必要：至少一個 LLM 提供商的 API 金鑰
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
GOOGLE_API_KEY=your_google_api_key

# 可選：其他提供商
QWEN_API_KEY=your_qwen_api_key
ERNIE_API_KEY=your_ernie_api_key
SPARK_API_KEY=your_spark_api_key
KIMI_API_KEY=your_kimi_api_key
DEEPSEEK_API_KEY=your_deepseek_api_key
META_API_KEY=your_meta_api_key
MISTRAL_API_KEY=your_mistral_api_key
COHERE_API_KEY=your_cohere_api_key

# 可選：伺服器設定
API_HOST=0.0.0.0
API_PORT=3000
LOG_LEVEL=INFO
```

### 5. 驗證安裝

```bash
# 執行完整驗證腳本
python verify_all.py

# 或執行快速驗證
./quick_verify.sh
```

## 使用方法

### 命令列工具 (CLI)

```bash
# 列出所有技能
magic-skill list

# 執行技能
magic-skill exec spring-boot-controller-gen -p '{"endpoint": "/api/users", "method": "GET"}'
```

### REST API

```bash
# 啟動 API 伺服器
python -m api.main

# 測試 API
curl http://localhost:3000/health
```

### Python

```python
from src.core.skill_manager import SkillManager

sm = SkillManager()
sm.load_all_skills()
result = sm.execute_skill("unit-test-gen", {"input": "def add(a,b): return a+b"})
```

## 常見問題

**問題**: `ModuleNotFoundError: No module named 'src'`

**解決**: 確保你在專案根目錄，並且虛擬環境已啟動。

**問題**: `API key not found`

**解決**: 檢查 `.env` 檔案，確保 API 金鑰設定正確。
