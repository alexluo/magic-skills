# Magic Skills API 文档

**English** | [简体中文](#简体中文) | [繁體中文](#繁體中文)

---

## English

### Base URL

```
http://localhost:3000
```

### Authentication

All API endpoints (except `/health`) require an API key in the header:

```
X-API-Key: your-api-key
```

### Endpoints

#### Health Check

```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-02-28T10:00:00Z",
  "version": "1.0.0"
}
```

#### List Skills

```http
GET /api/skills/list
```

**Response:**
```json
[
  {
    "name": "spring-boot-controller-gen",
    "description": "Generate Spring Boot REST controllers",
    "version": "1.0.0",
    "category": "java-backend"
  }
]
```

#### Get Skill Info

```http
GET /api/skills/info/{skill_name}
```

**Response:**
```json
{
  "name": "spring-boot-controller-gen",
  "description": "Generate Spring Boot REST controllers",
  "version": "1.0.0",
  "input_schema": {...},
  "output_schema": {...}
}
```

#### Execute Skill

```http
POST /api/skills/execute
Content-Type: application/json

{
  "skill_name": "unit-test-gen",
  "params": {
    "input": "def add(a,b): return a+b"
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "test_code": "...",
    "explanation": "..."
  },
  "execution_time": 1.23
}
```

#### List Models

```http
GET /api/models/list
```

**Response:**
```json
{
  "providers": ["openai", "anthropic", "google"],
  "models": {
    "openai": ["gpt-4o", "gpt-4o-mini"]
  }
}
```

### Error Responses

```json
{
  "detail": "Skill not found: unknown-skill"
}
```

---

# 简体中文

**简体中文** | [English](#english) | [繁體中文](#繁體中文)

---

## 基础 URL

```
http://localhost:3000
```

## 认证

所有 API 端点（除 `/health` 外）都需要在请求头中提供 API 密钥：

```
X-API-Key: your-api-key
```

## 接口列表

### 健康检查

```http
GET /health
```

**响应：**
```json
{
  "status": "healthy",
  "timestamp": "2026-02-28T10:00:00Z",
  "version": "1.0.0"
}
```

### 列出技能

```http
GET /api/skills/list
```

**响应：**
```json
[
  {
    "name": "spring-boot-controller-gen",
    "description": "生成 Spring Boot REST 控制器",
    "version": "1.0.0",
    "category": "java-backend"
  }
]
```

### 获取技能信息

```http
GET /api/skills/info/{skill_name}
```

**响应：**
```json
{
  "name": "spring-boot-controller-gen",
  "description": "生成 Spring Boot REST 控制器",
  "version": "1.0.0",
  "input_schema": {...},
  "output_schema": {...}
}
```

### 执行技能

```http
POST /api/skills/execute
Content-Type: application/json

{
  "skill_name": "unit-test-gen",
  "params": {
    "input": "def add(a,b): return a+b"
  }
}
```

**响应：**
```json
{
  "success": true,
  "data": {
    "test_code": "...",
    "explanation": "..."
  },
  "execution_time": 1.23
}
```

### 列出模型

```http
GET /api/models/list
```

**响应：**
```json
{
  "providers": ["openai", "anthropic", "google"],
  "models": {
    "openai": ["gpt-4o", "gpt-4o-mini"]
  }
}
```

## 错误响应

```json
{
  "detail": "技能未找到: unknown-skill"
}
```

---

# 繁體中文

**繁體中文** | [English](#english) | [简体中文](#简体中文)

---

## 基礎 URL

```
http://localhost:3000
```

## 認證

所有 API 端點（除 `/health` 外）都需要在請求標頭中提供 API 金鑰：

```
X-API-Key: your-api-key
```

## 介面列表

### 健康檢查

```http
GET /health
```

**回應：**
```json
{
  "status": "healthy",
  "timestamp": "2026-02-28T10:00:00Z",
  "version": "1.0.0"
}
```

### 列出技能

```http
GET /api/skills/list
```

**回應：**
```json
[
  {
    "name": "spring-boot-controller-gen",
    "description": "產生 Spring Boot REST 控制器",
    "version": "1.0.0",
    "category": "java-backend"
  }
]
```

### 取得技能資訊

```http
GET /api/skills/info/{skill_name}
```

**回應：**
```json
{
  "name": "spring-boot-controller-gen",
  "description": "產生 Spring Boot REST 控制器",
  "version": "1.0.0",
  "input_schema": {...},
  "output_schema": {...}
}
```

### 執行技能

```http
POST /api/skills/execute
Content-Type: application/json

{
  "skill_name": "unit-test-gen",
  "params": {
    "input": "def add(a,b): return a+b"
  }
}
```

**回應：**
```json
{
  "success": true,
  "data": {
    "test_code": "...",
    "explanation": "..."
  },
  "execution_time": 1.23
}
```

### 列出模型

```http
GET /api/models/list
```

**回應：**
```json
{
  "providers": ["openai", "anthropic", "google"],
  "models": {
    "openai": ["gpt-4o", "gpt-4o-mini"]
  }
}
```

## 錯誤回應

```json
{
  "detail": "技能未找到: unknown-skill"
}
```
