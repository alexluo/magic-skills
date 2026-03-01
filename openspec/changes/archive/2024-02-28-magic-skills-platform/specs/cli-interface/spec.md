## ADDED Requirements

### Requirement: CLI 命令结构
系统 SHALL 提供统一的命令行接口，所有命令遵循 `magic-skill <command> [options]` 格式。

#### Scenario: 查看帮助信息
- **WHEN** 用户运行 `magic-skill --help`
- **THEN** 显示所有可用命令和全局选项的帮助信息

#### Scenario: 查看命令帮助
- **WHEN** 用户运行 `magic-skill exec --help`
- **THEN** 显示 exec 命令的详细用法和选项

#### Scenario: 命令自动补全
- **WHEN** 用户在 zsh/bash 中启用自动补全
- **THEN** 支持命令和选项的 Tab 补全

---

### Requirement: 技能执行命令
系统 SHALL 提供 `exec` 命令用于执行技能。

#### Scenario: 执行技能（基本用法）
- **WHEN** 用户运行 `magic-skill exec hello_world --name World`
- **THEN** 执行 hello_world 技能并输出结果

#### Scenario: 执行技能并指定模型
- **WHEN** 用户运行 `magic-skill exec hello_world --name World --model claude`
- **THEN** 使用 Claude 模型执行技能

#### Scenario: 执行技能并传递 JSON 参数
- **WHEN** 用户运行 `magic-skill exec my_skill --params '{"key": "value"}'`
- **THEN** 解析 JSON 参数并传递给技能

#### Scenario: 执行不存在的技能
- **WHEN** 用户运行 `magic-skill exec nonexistent`
- **THEN** 显示错误信息"Skill 'nonexistent' not found"并返回非零退出码

---

### Requirement: 技能列表命令
系统 SHALL 提供 `list` 命令用于查看所有可用技能。

#### Scenario: 列出所有技能
- **WHEN** 用户运行 `magic-skill list`
- **THEN** 以表格形式显示所有技能的名称、描述和版本

#### Scenario: 按标签过滤技能列表
- **WHEN** 用户运行 `magic-skill list --tag nlp`
- **THEN** 仅显示包含 "nlp" 标签的技能

#### Scenario: 显示技能详细信息
- **WHEN** 用户运行 `magic-skill list --verbose`
- **THEN** 显示技能的详细信息（作者、创建时间、使用次数等）

---

### Requirement: 模型管理命令
系统 SHALL 提供 `models` 命令用于管理 LLM 模型。

#### Scenario: 列出可用模型
- **WHEN** 用户运行 `magic-skill models list`
- **THEN** 显示所有已配置且可用的 LLM 模型列表

#### Scenario: 测试模型连接
- **WHEN** 用户运行 `magic-skill models test openai`
- **THEN** 测试 OpenAI API 连接并显示结果（延迟、状态）

#### Scenario: 设置默认模型
- **WHEN** 用户运行 `magic-skill models default claude`
- **THEN** 设置默认模型为 Claude，后续执行默认使用该模型

---

### Requirement: 优化命令
系统 SHALL 提供 `optimize` 命令用于触发技能优化。

#### Scenario: 查看优化建议
- **WHEN** 用户运行 `magic-skill optimize hello_world --suggest`
- **THEN** 显示该技能的优化建议（Prompt 改进、参数调整等）

#### Scenario: 应用推荐参数
- **WHEN** 用户运行 `magic-skill optimize hello_world --apply-params`
- **THEN** 自动应用推荐的参数配置

#### Scenario: 查看执行统计
- **WHEN** 用户运行 `magic-skill optimize hello_world --stats --days 7`
- **THEN** 显示过去 7 天的执行统计（平均延迟、满意度等）

---

### Requirement: 反馈命令
系统 SHALL 提供 `feedback` 命令用于管理用户反馈。

#### Scenario: 提交反馈
- **WHEN** 用户运行 `magic-skill feedback submit <execution_id> --rating 1`
- **THEN** 提交点赞反馈

#### Scenario: 查看反馈历史
- **WHEN** 用户运行 `magic-skill feedback list --skill hello_world`
- **THEN** 显示该技能的所有反馈记录

#### Scenario: 导出反馈数据
- **WHEN** 用户运行 `magic-skill feedback export --format csv`
- **THEN** 导出所有反馈数据为 CSV 文件

---

### Requirement: 配置命令
系统 SHALL 提供 `config` 命令用于管理系统配置。

#### Scenario: 查看当前配置
- **WHEN** 用户运行 `magic-skill config show`
- **THEN** 显示当前所有配置项（默认模型、日志级别等）

#### Scenario: 设置配置项
- **WHEN** 用户运行 `magic-skill config set default_model gpt-4`
- **THEN** 更新默认模型配置

#### Scenario: 重置配置
- **WHEN** 用户运行 `magic-skill config reset`
- **THEN** 恢复所有配置到默认值

---

### Requirement: 初始化命令
系统 SHALL 提供 `init` 命令用于初始化新项目。

#### Scenario: 初始化新项目
- **WHEN** 用户在新目录运行 `magic-skill init`
- **THEN** 创建项目结构（skills/目录、配置文件、示例技能）

#### Scenario: 初始化时选择模板
- **WHEN** 用户运行 `magic-skill init --template advanced`
- **THEN** 使用高级模板初始化（包含更多示例和配置）

---

### Requirement: 错误处理
系统 SHALL 提供友好的错误提示和调试信息。

#### Scenario: API 密钥缺失错误
- **WHEN** 用户执行技能但未配置 API 密钥
- **THEN** 显示详细错误信息和配置指南链接

#### Scenario: 网络错误
- **WHEN** LLM API 调用因网络问题失败
- **THEN** 显示错误详情并建议重试或使用离线模式

#### Scenario: 详细错误模式
- **WHEN** 用户运行 `magic-skill exec hello_world --debug`
- **THEN** 显示详细的调试信息（完整堆栈、HTTP 请求等）

---

### Requirement: 输出格式化
系统 SHALL 支持多种输出格式以适应不同场景。

#### Scenario: 默认文本输出
- **WHEN** 用户运行命令未指定格式
- **THEN** 使用人类可读的文本格式输出

#### Scenario: JSON 格式输出
- **WHEN** 用户运行 `magic-skill list --format json`
- **THEN** 以 JSON 格式输出结果（便于脚本处理）

#### Scenario: 静默模式
- **WHEN** 用户运行 `magic-skill exec hello_world --quiet`
- **THEN** 仅输出技能执行结果，不显示额外信息
