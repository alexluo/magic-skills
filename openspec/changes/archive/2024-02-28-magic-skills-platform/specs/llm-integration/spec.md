## ADDED Requirements

### Requirement: 统一 LLM 接口
系统 SHALL 提供统一的抽象接口用于调用所有支持的 LLM 模型。

#### Scenario: 调用 generate 方法
- **WHEN** 调用 `provider.generate(prompt, options)`
- **THEN** 返回 LLM 生成的文本响应

#### Scenario: 调用 stream 方法
- **WHEN** 调用 `provider.stream(prompt, options)`
- **THEN** 返回异步迭代器，逐步生成响应文本

#### Scenario: 设置模型参数
- **WHEN** 调用 `generate` 时传入 `options={"temperature": 0.7, "max_tokens": 1000}`
- **THEN** 使用指定参数调用 LLM

---

### Requirement: OpenAI GPT 集成
系统 SHALL 支持 OpenAI GPT 系列模型（GPT-3.5、GPT-4、GPT-4o）。

#### Scenario: 使用 GPT-3.5 生成文本
- **WHEN** 调用 OpenAI 提供商并指定 `model="gpt-3.5-turbo"`
- **THEN** 使用 GPT-3.5 模型生成响应

#### Scenario: 使用 GPT-4 生成文本
- **WHEN** 调用 OpenAI 提供商并指定 `model="gpt-4"`
- **THEN** 使用 GPT-4 模型生成响应

#### Scenario: OpenAI API 密钥缺失
- **WHEN** 未配置 OPENAI_API_KEY 环境变量
- **THEN** 初始化时抛出 `ConfigurationError` 异常

#### Scenario: OpenAI API 调用失败
- **WHEN** OpenAI API 返回错误（如配额超限）
- **THEN** 抛出 `LLMProviderError` 并包含详细错误信息

---

### Requirement: Anthropic Claude 集成
系统 SHALL 支持 Anthropic Claude 系列模型（Claude 3、Claude 3.5）。

#### Scenario: 使用 Claude 3 Opus 生成文本
- **WHEN** 调用 Anthropic 提供商并指定 `model="claude-3-opus-20240229"`
- **THEN** 使用 Claude 3 Opus 模型生成响应

#### Scenario: Anthropic API 密钥缺失
- **WHEN** 未配置 ANTHROPIC_API_KEY 环境变量
- **THEN** 初始化时抛出 `ConfigurationError` 异常

---

### Requirement: Google Gemini 集成
系统 SHALL 支持 Google Gemini 系列模型（Gemini Pro、Gemini 1.5）。

#### Scenario: 使用 Gemini Pro 生成文本
- **WHEN** 调用 Google 提供商并指定 `model="gemini-pro"`
- **THEN** 使用 Gemini Pro 模型生成响应

#### Scenario: Google 凭证配置
- **WHEN** 配置 GOOGLE_APPLICATION_CREDENTIALS 环境变量
- **THEN** 使用指定凭证文件初始化 Google Vertex AI 客户端

---

### Requirement: 国内 LLM 集成
系统 SHALL 支持国内主流 LLM（通义千问、文心一言、讯飞星火、Kimi、DeepSeek）。

#### Scenario: 使用通义千问生成文本
- **WHEN** 调用 Qwen 提供商并传入 prompt
- **THEN** 使用通义千问模型生成响应

#### Scenario: 使用 Kimi 生成文本
- **WHEN** 调用 Kimi 提供商并传入 prompt
- **THEN** 使用 Kimi 模型生成响应

#### Scenario: 国内 LLM API 密钥配置
- **WHEN** 配置对应 LLM 的 API 密钥环境变量
- **THEN** 成功初始化该 LLM 提供商

---

### Requirement: LLM 模型列表查询
系统 SHALL 提供获取所有可用 LLM 模型列表的功能。

#### Scenario: 获取可用模型列表
- **WHEN** 调用 `get_available_models()`
- **THEN** 返回所有已配置且可用的 LLM 名称列表

#### Scenario: 查询模型详细信息
- **WHEN** 调用 `get_model_info(model_name)`
- **THEN** 返回模型的详细信息（提供商、上下文窗口、成本等）

---

### Requirement: LLM 降级策略
系统 SHALL 在主 LLM 不可用时提供降级到备用 LLM 的能力。

#### Scenario: 主 LLM 调用失败自动降级
- **WHEN** 主 LLM 调用失败且配置了备用 LLM
- **THEN** 自动尝试使用备用 LLM 执行

#### Scenario: 所有 LLM 都不可用
- **WHEN** 所有配置的 LLM 都调用失败
- **THEN** 抛出 `AllProvidersUnavailableError` 异常

---

### Requirement: Token 计数和成本估算
系统 SHALL 提供 token 计数和 API 调用成本估算功能。

#### Scenario: 计算请求 token 数
- **WHEN** 调用 `count_tokens(text, model)`
- **THEN** 返回文本在指定模型下的 token 数量

#### Scenario: 估算 API 调用成本
- **WHEN** 调用 `estimate_cost(tokens, model)`
- **THEN** 返回基于模型定价的成本估算（美元）

---

### Requirement: LLM 响应缓存
系统 SHALL 支持缓存 LLM 响应以减少重复调用和成本。

#### Scenario: 缓存命中
- **WHEN** 相同的 prompt 和参数被再次调用
- **THEN** 返回缓存的响应而不调用 LLM API

#### Scenario: 缓存失效
- **WHEN** 缓存超过 TTL（默认 24 小时）
- **THEN** 清除旧缓存并重新调用 LLM API

#### Scenario: 禁用缓存
- **WHEN** 调用时设置 `options={"cache": False}`
- **THEN** 不使用缓存，始终调用 LLM API
