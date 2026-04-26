# learning-coding_agent

面向编程初学者的智能编程学习助手 MVP。当前版本以 Web 形态交付，核心交互是双栏并行：左侧「编程助手」用于多轮生成代码，右侧「理解助手」用于解释选中的代码片段或回答全局问题。

## 功能

- 双栏学习界面：编程通道 + 理解通道
- Monaco Editor 展示 AI 生成代码，支持选中代码后点击 Ask
- WebSocket 流式响应，提供接近打字机的反馈体验
- OpenAI-compatible AI 适配器，支持火山 Coding Plan、前端输入 API Key 或后端环境变量
- Python 代码执行接口，使用 Docker 沙箱隔离
- 后端单元测试覆盖 AI 适配器和沙箱危险代码检测

## 技术栈

- 前端：React + TypeScript + Vite + Tailwind CSS + shadcn 风格组件 + Zustand
- 后端：FastAPI + Python 3.12 + httpx + WebSocket
- 沙箱：Docker `python:3.12-slim`
- 部署建议：前端 Vercel，后端 Render Docker Web Service

## 项目结构

```text
.
├── .harness/                 # 项目规则、架构约束、验证脚本
├── backend/                  # FastAPI 后端
│   ├── app/
│   ├── tests/
│   ├── Dockerfile
│   └── render.yaml
├── docs/
│   ├── api-key-guide.md
│   ├── mvp-plan.md
│   └── mvp-summary.md
└── frontend/                 # React + Vite 前端
    ├── src/
    └── package.json
```

## 快速开始

### 后端

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

后端默认运行在 `http://localhost:8000`，健康检查为：

- `GET /api/v1/health`
- `GET /health`

如果希望后端统一托管 API Key，可设置环境变量：

```bash
AI_API_KEY=your-api-key
AI_BASE_URL=https://ark.cn-beijing.volces.com/api/coding/v3
AI_MODEL=doubao-seed-code
```

也可以不设置 `AI_API_KEY`，直接在前端设置弹窗中输入 API Key。

### 前端

```bash
cd frontend
npm install
npm run dev
```

前端默认运行在 `http://localhost:5173`。如需连接远端后端，可配置：

```bash
VITE_API_BASE_URL=https://your-api.example.com
VITE_WS_BASE_URL=wss://your-api.example.com
```

## 测试与构建

```bash
cd backend
pytest tests/unit
```

```bash
cd frontend
npm run build
```

## API

| 方法 | 路径 | 用途 |
|------|------|------|
| GET | `/api/v1/health` | 健康检查 |
| POST | `/api/v1/chat/code` | 编程通道代码生成 |
| POST | `/api/v1/chat/explain` | 理解通道代码解释/问答 |
| POST | `/api/v1/code/execute` | Docker 沙箱执行 Python 代码 |
| WS | `/api/v1/ws/chat` | 流式聊天 |

## 文档

- [MVP 规划](docs/mvp-plan.md)
- [AI API Key 配置指南](docs/api-key-guide.md)
- [MVP 总结](docs/mvp-summary.md)
- [核心规则](.harness/AGENTS.md)
