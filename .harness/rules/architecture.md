---
name: architecture-rules
description: L2 架构详细规则。定义技术栈、目录结构、模块边界。
version: "2.0"
---

# 架构规则

## 1. 技术栈（强制）

| 层级 | 技术 | 用途 |
|------|------|------|
| 前端 | React + TypeScript + Electron | UI 与桌面壳 |
| 后端 | FastAPI + Python 3.12 | REST API + WebSocket |
| AI 接口 | 多模型适配器 | GPT-4.5 / Kimi K2.5 |
| 沙箱 | Docker | 代码隔离执行 |
| 数据(MVP) | SQLite | 本地存储 |
| 数据(正式) | PostgreSQL | 云端数据库 |

## 2. 项目目录结构

### 前端 (Electron)
```
src/
├── main/                    # Electron 主进程
│   ├── index.ts
│   ├── ipc-handlers/
│   └── window-manager.ts
├── renderer/                # React 渲染进程
│   ├── components/
│   │   ├── common/         # 通用组件
│   │   ├── code/           # 代码相关
│   │   └── chat/           # 聊天相关
│   ├── hooks/
│   ├── pages/
│   ├── services/           # API 服务
│   ├── stores/             # Zustand 状态（按功能拆分）
│   ├── types/
│   └── utils/
└── shared/                 # 共享类型/常量
    ├── constants.ts
    └── types.ts
```

### 后端 (FastAPI)
```
backend/
├── app/
│   ├── main.py              # FastAPI 入口
│   ├── config.py
│   ├── dependencies.py      # 依赖注入
│   ├── api/v1/              # 路由
│   │   ├── chat.py
│   │   ├── code.py
│   │   ├── users.py
│   │   └── ws.py            # WebSocket
│   ├── core/                # 安全、异常、日志
│   ├── models/              # SQLAlchemy 模型
│   ├── schemas/             # Pydantic Schema
│   ├── services/            # 业务逻辑
│   │   ├── ai_service.py
│   │   ├── code_execution.py
│   │   └── chat_service.py
│   └── db/                  # 数据库会话 + 迁移
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
└── docker/
```

## 3. 通信协议

- **HTTP REST**: 常规请求（代码生成、用户管理）
- **WebSocket**: AI 流式响应（`ws://localhost:8000/api/v1/ws/chat`）
- **Electron IPC**: 主进程 ↔ 渲染进程（`ipcMain` / `ipcRenderer`）

## 4. 模块边界

- `api/` 层只负责路由和参数校验，不直接调用外部服务
- `services/` 层封装业务逻辑，可调用多个模型/外部接口
- `models/` 只定义数据结构，不包含业务逻辑
- `core/` 提供跨模块基础设施（配置、安全、日志）
