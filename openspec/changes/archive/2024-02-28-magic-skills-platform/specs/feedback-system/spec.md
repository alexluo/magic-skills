## ADDED Requirements

### Requirement: 反馈数据存储
系统 SHALL 使用 SQLite 数据库持久化存储用户反馈数据。

#### Scenario: 初始化反馈数据库
- **WHEN** 系统首次启动
- **THEN** 自动创建 feedback 表和相关索引

#### Scenario: 存储反馈记录
- **WHEN** 用户提交反馈
- **THEN** 反馈记录被存储到 feedback 表

#### Scenario: 反馈数据迁移
- **WHEN** 数据库 schema 升级
- **THEN** 自动执行数据迁移脚本

---

### Requirement: 反馈提交接口
系统 SHALL 提供多种反馈提交方式。

#### Scenario: 通过 CLI 提交反馈
- **WHEN** 用户运行 `magic-skill feedback submit <execution_id> --rating 1`
- **THEN** 反馈被存储到数据库

#### Scenario: 通过 API 提交反馈
- **WHEN** 客户端 POST 请求 `/api/feedback/submit`
- **THEN** 反馈被存储到数据库

#### Scenario: 批量导入反馈
- **WHEN** 调用 `import_feedback_from_file(filepath)`
- **THEN** 批量导入反馈数据

---

### Requirement: 反馈查询和过滤
系统 SHALL 提供灵活的反馈查询和过滤功能。

#### Scenario: 按技能查询反馈
- **WHEN** 查询 `skill_name="hello_world"` 的反馈
- **THEN** 返回该技能的所有反馈记录

#### Scenario: 按时间范围查询反馈
- **WHEN** 查询过去 7 天的反馈
- **THEN** 返回指定时间范围内的反馈记录

#### Scenario: 按评分过滤反馈
- **WHEN** 查询所有点踩反馈（rating=-1）
- **THEN** 返回所有负反馈记录

#### Scenario: 组合条件查询
- **WHEN** 查询过去 7 天 hello_world 技能的负反馈
- **THEN** 返回满足所有条件的反馈记录

---

### Requirement: 反馈统计分析
系统 SHALL 提供反馈统计分析功能。

#### Scenario: 计算满意度评分
- **WHEN** 调用 `get_satisfaction_score(skill_name)`
- **THEN** 返回该技能的满意度百分比（点赞数/总反馈数）

#### Scenario: 反馈趋势分析
- **WHEN** 调用 `get_feedback_trend(skill_name, days=30)`
- **THEN** 返回每天反馈数量的时间序列数据

#### Scenario: 反馈分布统计
- **WHEN** 调用 `get_feedback_distribution(skill_name)`
- **THEN** 返回评分分布（1 星到 5 星的数量）

---

### Requirement: 反馈驱动告警
系统 SHALL 基于反馈数据触发告警和通知。

#### Scenario: 连续负反馈告警
- **WHEN** 技能收到连续 5 个点踩反馈
- **THEN** 系统记录警告日志并标记该技能需要审查

#### Scenario: 满意度下降告警
- **WHEN** 技能满意度从 90% 下降到 60% 以下
- **THEN** 系统发送告警通知

#### Scenario: 反馈量异常告警
- **WHEN** 技能反馈量突然增加 300%
- **THEN** 系统记录异常并提示可能的质量问题

---

### Requirement: 反馈导出
系统 SHALL 支持导出反馈数据用于进一步分析。

#### Scenario: 导出为 CSV
- **WHEN** 调用 `export_feedback_csv(filepath)`
- **THEN** 导出所有反馈数据为 CSV 文件

#### Scenario: 导出为 JSON
- **WHEN** 调用 `export_feedback_json(filepath)`
- **THEN** 导出所有反馈数据为 JSON 文件

#### Scenario: 选择性导出
- **WHEN** 导出指定技能的反馈
- **THEN** 仅导出该技能的反馈数据

---

### Requirement: 反馈清理和归档
系统 SHALL 提供反馈数据清理和归档功能。

#### Scenario: 删除过期反馈
- **WHEN** 调用 `cleanup_feedback(retention_days=365)`
- **THEN** 删除超过 365 天的反馈数据

#### Scenario: 归档反馈数据
- **WHEN** 调用 `archive_feedback(before_date)`
- **THEN** 将指定日期前的反馈数据归档到压缩文件

#### Scenario: 恢复归档数据
- **WHEN** 调用 `restore_feedback_from_archive(filepath)`
- **THEN** 从归档文件恢复反馈数据

---

### Requirement: 反馈隐私保护
系统 SHALL 保护用户反馈隐私。

#### Scenario: 匿名化反馈
- **WHEN** 存储反馈时
- **THEN** 移除或匿名化所有个人身份信息

#### Scenario: 用户请求删除反馈
- **WHEN** 用户请求删除其提交的反馈
- **THEN** 删除该用户的所有反馈记录

#### Scenario: 数据脱敏导出
- **WHEN** 导出反馈数据用于公开分享
- **THEN** 自动脱敏敏感信息

---

### Requirement: 反馈可视化
系统 SHALL 提供反馈数据的可视化展示。

#### Scenario: 生成满意度趋势图
- **WHEN** 调用 `generate_satisfaction_chart(skill_name, days=30)`
- **THEN** 生成满意度趋势图（PNG 或 HTML）

#### Scenario: 生成反馈分布饼图
- **WHEN** 调用 `generate_distribution_chart(skill_name)`
- **THEN** 生成评分分布饼图

#### Scenario: 导出可视化报告
- **WHEN** 调用 `export_feedback_report(skill_name)`
- **THEN** 生成包含图表和统计的 PDF 报告

---

### Requirement: 反馈与日志关联
系统 SHALL 将反馈与执行日志关联以进行深度分析。

#### Scenario: 关联反馈和执行记录
- **WHEN** 查询某次执行的反馈
- **THEN** 可以同时获取该次执行的详细日志

#### Scenario: 基于反馈分析性能
- **WHEN** 分析负反馈对应的执行日志
- **THEN** 识别性能瓶颈或错误模式

#### Scenario: 反馈驱动日志级别调整
- **WHEN** 技能收到大量负反馈
- **THEN** 自动提升该技能的日志级别以收集更多调试信息
