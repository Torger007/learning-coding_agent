---
name: core-rules
description: L1 核心约束，始终加载。≤10条，定义不可违反的底线。
version: "2.0"
---

# AGENTS — 核心约束

> 本文档始终加载。所有 AI 任务执行前必须阅读。

## 1. 项目身份

- **产品**: learning-coding-agent — 智能编程学习助手（Electron 桌面应用）
- **核心交互**: 双栏并行（编程通道 + 理解通道）
- **技术栈**: React + TypeScript + Electron 前端，FastAPI + Python 3.12 后端
- **AI 接口**: GPT-5.4 / Kimi K2.5，多模型可切换
- **代码执行**: Docker 沙箱隔离（Python 3.12 优先）

## 2. 十大不可违反约束

### C1 — 任务分解
超过 30 分钟、涉及 >3 个文件、或跨前后端的任务，必须分解为子任务。

### C2 — 自主决策边界
- **完全自主**: 代码格式、注释、变量重命名、补充测试用例（不改原逻辑）
- **必须确认**: 修改公共 API 签名、删除 >50 行代码、引入新依赖、改数据库 schema
- **禁止执行**: 提交到 main/master、执行 `rm -rf`/`DROP TABLE`、访问敏感配置、修改 CI/CD

### C3 — 类型与文档
- 所有公共函数必须有类型注解
- 所有公共 API 必须有一句文档字符串说明用途

### C4 — 测试底线
MVP 阶段核心逻辑必须至少有一个测试。不允许完全无测试的模块。

### C5 — 沙箱安全（不可妥协）
- 资源限制: 1 CPU / 512MB 内存 / 30 秒超时
- 网络隔离: 默认禁止外部网络
- 文件系统: 只读根目录，仅 `/tmp` 可写
- 危险代码执行前必须静态扫描

### C6 — 敏感信息
API Key、密码、Token 绝对禁止硬编码。必须使用环境变量或系统密钥管理。

### C7 — MVP 时间约束（1周）
- 每天结束时必须有可运行版本
- P0 必须完成，P1 可简化，P2 可延后
- P0 范围调整必须经过确认

### C8 — 技术栈锁定
UI 组件库、状态管理方案等允许自主选择。禁止引入新语言/运行时（不在既定范围）。

### C9 — 质量与速度平衡
- 不妥协: 沙箱安全、API Key 管理、双栏核心交互可用
- 可妥协: 测试覆盖率 >60% 即可、UI 精细度、错误处理完善度

### C10 — 规则分层读取
- L1（本文档）始终加载
- L2（`rules/`）按需读取: `@read .harness/rules/<领域>.md`
- L3（`guides/`）手动参考: 不确定时再读

## 3. 快速索引

| 需求 | 读取 |
|------|------|
| 架构约束 | `.harness/rules/architecture.md` |
| API 规范 | `.harness/rules/api-design.md` |
| 数据库规范 | `.harness/rules/database.md` |
| 测试规范 | `.harness/rules/testing.md` |
| 安全规范 | `.harness/rules/security.md` |
| 代码示例 | `.harness/guides/patterns/` |
| 决策记录 | `.harness/context/decisions.md` |
