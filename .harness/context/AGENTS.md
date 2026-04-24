# AI 项目地图

> 这是 AI Agent 的导航地图。阅读本文档以理解项目结构、规则和最佳实践。

## 项目概述

- **项目名称**: Harness Engineering Framework
- **技术栈**: Python 3.12, FastAPI, SQLAlchemy, Pydantic v2
- **架构**: 分层架构（Domain → Application → Infrastructure → Interface）
- **目标**: AI-native 工程化框架，支持稳定、自主、可控的 AI 任务执行

## 快速导航

| 需求 | 位置 |
|------|------|
| 查看核心规则 | `.harness/rules/01-core.md` |
| 查看编码规范 | `.harness/rules/02-coding.md` |
| 查看架构约束 | `.harness/constraints/architecture.yaml` |
| 查看验证流程 | `.harness/process/task-lifecycle.yaml` |
| 项目文档 | `docs/` |
| 源代码 | `src/` |
| 测试代码 | `tests/` |

## 关键规则（TL;DR）

### 必须遵守
1. **任务分解**: 超过 30 分钟、涉及多个文件的任务必须分解
2. **类型注解**: 所有函数必须添加类型注解
3. **文档字符串**: 所有公共 API 必须有文档字符串
4. **测试覆盖**: 新代码必须伴随测试

### 需要确认
- 修改公共 API 签名
- 删除代码（>50 行）
- 引入新依赖
- 修改数据库 schema
- 涉及安全的改动

### 禁止自主执行
- 提交到生产分支
- 破坏性命令（`rm -rf`, `DROP TABLE`）
- 访问敏感配置
- 执行外部 API 请求
- 修改 CI/CD 管道

## 任务执行流程

```
开始任务
    ↓
Phase 1: Analyze（分析）
  - 理解任务目标
  - 识别相关代码
  - 评估影响范围
    ↓
Phase 2: Plan（规划）
  - 制定执行计划
  - 标记需确认的点
  - 确定验证方法
    ↓
Phase 3: Execute（执行）
  - 执行子任务
  - 每步后验证
  - 保留中间状态
    ↓
Phase 4: Review（审查）
  - 代码自审
  - 运行自动化检查
  - 生成变更摘要
    ↓
Phase 5: Finalize（完成）
  - 整理提交信息
  - 清理临时文件
  - 任务总结
```

## 代码审查清单

### 提交前自查
- [ ] 代码通过 ruff 检查
- [ ] 代码通过 mypy 检查
- [ ] 所有函数有类型注解
- [ ] 公共 API 有文档字符串
- [ ] 新代码有对应测试
- [ ] 所有测试通过
- [ ] 无调试代码（print/debugger）
- [ ] 无硬编码敏感信息

### PR 审查要点
- [ ] 符合项目架构设计
- [ ] 无重复代码（DRY 原则）
- [ ] 错误处理完善
- [ ] 性能考虑
- [ ] 安全性
- [ ] 向后兼容
- [ ] 文档更新

## 常见问题

### Q: 如何添加新的 lint 规则？
A: 编辑 `.harness/constraints/lint-rules/` 目录下的规则文件。

### Q: 如何修改验证流程？
A: 编辑 `.harness/process/task-lifecycle.yaml` 文件。

### Q: 遇到验证失败怎么办？
A: 查看 `.harness/verification/logs/` 目录下的日志文件，根据错误信息修复。

## 参考链接

- 项目文档: `docs/`
- 架构文档: `docs/02-architecture/`
- API 文档: `docs/04-api/`
- 决策记录: `docs/05-decisions/`

---

*最后更新: 2024-01-15*
*维护者: AI Agent*
