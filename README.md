# Harness Engineering Framework

AI-native 工程化框架，支持稳定、自主、可控的 AI 任务执行。

## 核心组件

| 组件 | 描述 | 状态 |
|------|------|------|
| **Agent Harness** | AI 运行底座（环境、工具、沙箱）| ✅ 已完成 |
| **Context Manager** | 结构化项目知识，防止失忆/幻觉 | 🔄 进行中 |
| **Architectural Constraints** | 自动化规则执行，防止架构腐化 | 🔄 进行中 |
| **Verification Hooks** | 质量门禁，行动前自我验证 | 🔄 进行中 |
| **Feedback Loop** | 从错误学习，正向循环 | 🔄 进行中 |

## 项目结构

```
.
├── .harness/                  # Harness 框架配置（核心）
│   ├── context/               # Context Manager 配置
│   ├── constraints/           # Architectural Constraints 配置
│   ├── verification/          # Verification Hooks 配置
│   └── feedback/              # Feedback Loop 配置
├── docs/                      # 项目知识库
├── src/                       # 源代码
├── tests/                     # 测试代码
└── scripts/                   # 工具脚本
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

# 安装依赖
pip install -r requirements.txt
```

### 3. 运行验证

```bash
# 运行项目验证
python .harness/verification/validate.py
```

## 核心文档

- **AI 项目地图**: [.harness/context/AGENTS.md](.harness/context/AGENTS.md) - 阅读此文档了解项目规则和导航
- **记忆索引**: [.harness/context/memory.yaml](.harness/context/memory.yaml) - 快速查找规则和知识
- **核心规则**: [.harness/rules/01-core.md](.harness/rules/01-core.md) - AI 行为规则
- **编码规范**: [.harness/rules/02-coding.md](.harness/rules/02-coding.md) - 代码风格指南

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
