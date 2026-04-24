# Harness 规则变更日志

## [2.0] - 2026-04-24

### 重构
- 采用三层规则框架: L1(核心约束) + L2(领域规则) + L3(指南示例)
- 合并旧 5 个规则文件为新的分层结构:
  - `01-core.md` + `03-decision.md` → `.harness/AGENTS.md` (L1)
  - `05-project-coding-assistant.md` → `rules/architecture.md` + `rules/api-design.md` + `rules/database.md`
  - `02-coding.md` → `rules/testing.md` + `guides/patterns/`
  - `04-safety.md` → `rules/security.md`
- 删除教程式内容，保留约束性规则
- 新增 `commands/` 斜杠命令定义
- 新增 `scripts/` 验证脚本
- 新增 `guides/patterns/` 代码模式示例

### 保留
- 所有安全约束（沙箱参数、敏感信息规则）
- MVP 时间约束和功能优先级
- 技术栈锁定

### 删除
- 旧规则文件: `01-core.md`, `02-coding.md`, `03-decision.md`, `04-safety.md`, `05-project-coding-assistant.md`
