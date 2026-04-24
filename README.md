# learning-coding_agent

智能编程学习助手（CodeMentor），面向编程初学者的 AI 桌面应用。

- **核心交互**: 双栏并行模式（编程通道 + 理解通道）
- **技术栈**: React + TypeScript + Electron（前端），FastAPI + Python 3.12（后端）
- **AI 模型**: GPT-5.4 / Kimi K2.5 多模型切换
- **代码执行**: Docker 沙箱隔离运行

## 项目结构

```
.
├── AGENTS.md                  # 根入口（符号链接 → .harness/AGENTS.md）
├── .harness/                  # Harness 规则框架
│   ├── AGENTS.md              # L1 核心约束（始终加载）
│   ├── rules/                 # L2 领域规则（按需加载）
│   │   ├── architecture.md
│   │   ├── api-design.md
│   │   ├── database.md
│   │   ├── security.md
│   │   └── testing.md
│   ├── guides/                # L3 指南与示例（手动参考）
│   │   ├── error-handling.md
│   │   ├── performance.md
│   │   └── patterns/
│   ├── commands/              # Claude Code 斜杠命令定义
│   │   ├── plan.md
│   │   ├── review.md
│   │   └── validate.md
│   ├── scripts/               # 验证脚本
│   │   ├── pre-validate
│   │   ├── validate.py
│   │   └── lint-deps.py
│   ├── hooks/                 # Git hooks
│   ├── context/               # 动态上下文（AI 可写入）
│   │   ├── memory.yaml
│   │   └── decisions.md
│   └── CHANGELOG.md           # 规则变更日志
├── src/                       # 源代码
│   ├── main/                  # Electron 主进程
│   ├── renderer/              # React 渲染进程
│   └── shared/                # 共享类型/常量
├── backend/                   # FastAPI 后端
│   ├── app/
│   ├── tests/
│   └── docker/
└── tests/                     # 端到端测试
```

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/Torger007/learning-coding_agent.git
cd learning-coding_agent
```

### 2. 配置环境

```bash
# 使用 conda 虚拟环境 LC
conda activate LC

# 安装后端依赖
cd backend
pip install -r requirements.txt

# 安装前端依赖
cd ../src/renderer
npm install
```

### 3. 运行验证

```bash
# 运行完整项目验证
python .harness/scripts/validate.py

# 检查模块依赖方向
python .harness/scripts/lint-deps.py
```

## 核心文档

| 层级 | 文件 | 说明 |
|------|------|------|
| L1 | [`.harness/AGENTS.md`](.harness/AGENTS.md) | 核心约束（≤10条），AI 始终加载 |
| L2 | [`.harness/rules/architecture.md`](.harness/rules/architecture.md) | 技术栈与目录结构 |
| L2 | [`.harness/rules/api-design.md`](.harness/rules/api-design.md) | REST / WebSocket / 响应格式 |
| L2 | [`.harness/rules/security.md`](.harness/rules/security.md) | 沙箱参数与安全约束 |
| 索引 | [`.harness/context/memory.yaml`](.harness/context/memory.yaml) | 规则索引与快捷命令 |
| ADR | [`.harness/context/decisions.md`](.harness/context/decisions.md) | 架构决策记录 |
| 变更 | [`.harness/CHANGELOG.md`](.harness/CHANGELOG.md) | 规则框架变更日志 |

## MVP 目标（1周）

| 优先级 | 功能 |
|--------|------|
| P0 | 双栏基础 UI、代码选中 Ask 流程、AI 流式响应、多模型切换 |
| P1 | Python 代码执行（Docker 沙箱）、术语表基础版、对话历史（SQLite） |
| P2 | 多语言执行、可视化图示（Mermaid）、术语表高级功能 |

## 贡献指南

1. Fork 仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 许可证

[MIT](LICENSE)

## 联系方式

- 项目链接: https://github.com/Torger007/learning-coding_agent
- 问题反馈: https://github.com/Torger007/learning-coding_agent/issues
