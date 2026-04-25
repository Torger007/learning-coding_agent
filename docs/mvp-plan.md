# learning-coding-agent MVP 规划（3天）

## Context

项目目标：面向编程新手小白的智能编程学习助手 Web 应用。核心交互为**双栏并行**：左栏「编程通道」（多轮对话生成代码）、右栏「理解通道」（选中代码块提问解答，或全局提问）。

MVP 约束：3 天内可运行；P0 必须完成，P1 可简化，P2 延后。技术栈遵循 Harness 框架：React + TypeScript 前端，FastAPI + Python 3.12 后端，Kimi K2.5 单模型，纯内存会话。

## MVP 范围定义

### P0 — 必须完成（3天内）
- **前端**：双栏布局（编程通道 + 理解通道），Tailwind + shadcn/ui
- **编程通道**：多轮对话生成代码，Monaco Editor 展示代码，支持代码高亮
- **代码选中 Ask**：用户鼠标选中代码块，自动弹出 "Ask" 按钮，点击后携带代码片段到理解通道
- **理解通道**：默认开启，未选中代码时回答全局会话问题；选中代码时针对代码解答
- **后端**：FastAPI 提供 REST API 和 WebSocket 流式响应
- **AI 接入**：Kimi K2.5 单模型适配器，支持流式输出
- **API Key 配置**：前端提供输入框 + 详细获取指引文档
- **代码执行**：后端 Docker 沙箱执行 Python 代码（框架 C5 强制安全参数）
- **测试**：沙箱执行逻辑、AI 服务适配器层至少各有一个测试

### P1 — 可简化
- UI 动画、精细化样式
- 错误处理完善度
- 代码执行结果显示优化（仅返回正确/错误 + 简要输出）

### P2 — 延后
- 对话历史持久化（SQLite）
- 多模型切换
- Electron 桌面版迁移
- 用户认证

## 技术架构

### 前端（Web）
- **框架**：React 18 + TypeScript + Vite
- **样式**：Tailwind CSS + shadcn/ui
- **编辑器**：@monaco-editor/react（Monaco Editor React 封装）
- **状态管理**：Zustand（按功能拆分：chatStore, codeStore, uiStore）
- **HTTP 客户端**：Axios
- **WebSocket**：原生 WebSocket API

### 后端
- **框架**：FastAPI + Uvicorn
- **AI 适配器**：`app/services/ai_service.py`，封装 Kimi K2.5 HTTP SSE 调用
- **代码执行**：`app/services/code_execution.py` + Docker 沙箱（python:3.12-slim）
- **危险代码检测**：`DangerousCodeDetector` 类（框架 security.md 强制要求）
- **会话存储**：纯内存（Python dict），重启丢失

### 部署
- **前端**：Vercel（免费，GitHub 自动部署）
- **后端**：Render 免费 tier（支持 Docker，15分钟休眠，唤醒稍慢）
- **环境变量**：API Key 通过前端界面输入（内存存储，刷新需重填）

## 3天详细排期

### Day 1 — 骨架搭建 + 后端核心
**上午（4h）**
1. 初始化前端项目：`npm create vite@latest frontend -- --template react-ts`
2. 配置 Tailwind + shadcn/ui
3. 初始化后端项目：`mkdir backend`，pip 安装 FastAPI/Uvicorn/httpx
4. 创建 FastAPI 入口 `app/main.py`，配置 CORS

**下午（4h）**
5. 实现 Kimi K2.5 AI 服务适配器 `app/services/ai_service.py`（支持流式 SSE）
6. 实现危险代码检测 `app/services/code_execution.py` 的 `DangerousCodeDetector`
7. 实现 Docker 沙箱执行逻辑（Python 专用）
8. 编写 API 路由：`/api/v1/chat/code`（生成代码）、`/api/v1/chat/explain`（解释代码）、`/api/v1/code/execute`（执行代码）
9. WebSocket 路由 `/api/v1/ws/chat` 流式对话
10. 编写 AI 服务适配器 + 沙箱执行各至少 1 个单元测试

**Day 1 产出**：后端可独立运行，Postman 能调通生成代码和执行代码接口。

### Day 2 — 前端双栏 + 核心交互
**上午（4h）**
1. 搭建双栏布局组件：`src/components/layout/DualPanelLayout.tsx`
2. 实现编程通道：`src/components/chat/CodeChatPanel.tsx`（消息列表 + 输入框）
3. 集成 Monaco Editor 展示 AI 生成的代码：`src/components/code/CodeEditor.tsx`

**下午（4h）**
4. 实现理解通道：`src/components/chat/ExplainPanel.tsx`
5. 实现代码选中检测 + "Ask" 浮层：`src/components/code/CodeSelectionOverlay.tsx`
   - Monaco Editor `onMouseUp` 事件获取选中内容
   - 选中文本非空时在鼠标位置显示 Ask 按钮
   - 点击后将 `{code, language}` 写入全局状态并滚动到理解通道
6. 全局状态管理（Zustand）：`chatStore` 管理双栏消息，`uiStore` 管理选中状态
7. 前端 API 服务层：`src/services/api.ts`、`src/services/websocket.ts`

**Day 2 产出**：前端可运行，能看到双栏界面，编程通道能发消息（mock 数据也能看到效果），选代码能弹出 Ask。

### Day 3 — 前后端联调 + 部署 + 文档
**上午（4h）**
1. 前后端联调：前端真实调用后端 API
2. 流式响应接入：WebSocket 打字机效果
3. API Key 输入界面：`src/components/settings/ApiKeySettings.tsx`
4. 编写《如何获取 Kimi API Key》用户指引文档（docs/api-key-guide.md）

**下午（4h）**
5. 部署后端到 Render（Dockerfile + render.yaml）
6. 部署前端到 Vercel（配置 API_BASE_URL 环境变量指向 Render）
7. 端到端测试：完整走通「编程通道提问 → AI 生成代码 → 选中代码 Ask → 理解通道解答」
8. 编写 MVP 总结文档 docs/mvp-summary.md
9. 清理 TODO，确保 P0 无遗漏

**Day 3 产出**：公网可访问的 MVP，README 有访问链接和快速开始说明。

## 核心交互设计

### 1. 编程通道（左栏）
- 顶部：标题 "编程助手"
- 中部：消息气泡列表（用户右对齐，AI 左对齐）
- AI 消息中包含 Monaco Editor 只读代码块
- 底部：输入框 + 发送按钮，支持 Shift+Enter 换行
- 多轮对话：同一 session_id 上下文关联（内存 dict）

### 2. 代码选中 Ask
- 用户在 Monaco Editor 中鼠标拖动选中任意代码片段
- `onMouseUp` 时检测 `editor.getSelection()` 是否非空
- 若非空，在选区右下角（或鼠标位置）显示小浮层按钮 "Ask"
- 点击 "Ask" 后：
  - 将 `{ selectedCode, language }` 存入 `uiStore.selectedSnippet`
  - 理解通道输入框自动填充："我对这段代码有疑问：[代码片段]\n\n"
  - 光标定位到输入框末尾，用户继续输入具体问题
- 如果用户不点击 Ask，浮层 3 秒后自动消失，或在别处点击消失

### 3. 理解通道（右栏）
- 顶部：标题 "理解助手"
- 中部：消息气泡列表
- 底部：输入框 + 发送按钮
- 当 `uiStore.selectedSnippet` 存在时，理解通道顶部显示一个小的代码片段引用卡片（可删除），表示本次回答的上下文
- 用户可直接在输入框提问（不选中代码时），回答基于全局对话上下文

### 4. API Key 配置
- 首次访问或刷新后，如果本地内存没有 API Key，前端显示一个非阻塞的顶部提示条
- 提供 "设置 API Key" 按钮，打开设置弹窗
- 弹窗内包含：
  - 输入框（type=password，可切换可见）
  - "如何获取 API Key？" 折叠面板，内含图文步骤：
    1. 访问 Kimi 开放平台 (platform.moonshot.cn)
    2. 注册/登录账号
    3. 进入「API Key 管理」页面
    4. 点击「创建 API Key」
    5. 复制生成的 Key，粘贴到上方输入框
  - "保存" 按钮（仅保存在内存，刷新需重填）

## API 路由设计

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/v1/health | 健康检查 |
| POST | /api/v1/chat/code | 编程通道：生成代码（流式 WebSocket） |
| POST | /api/v1/chat/explain | 理解通道：解释代码/全局问题 |
| POST | /api/v1/code/execute | 执行 Python 代码（返回正确/错误+输出） |
| WS | /api/v1/ws/chat | WebSocket 流式对话（统一入口） |

请求/响应格式遵循 `.harness/rules/api-design.md` 统一响应格式。

## 关键文件清单

### 前端
```
frontend/src/
├── components/
│   ├── layout/DualPanelLayout.tsx
│   ├── chat/CodeChatPanel.tsx
│   ├── chat/ExplainPanel.tsx
│   ├── code/CodeEditor.tsx
│   ├── code/CodeSelectionOverlay.tsx
│   └── settings/ApiKeySettings.tsx
├── stores/
│   ├── chatStore.ts
│   └── uiStore.ts
├── services/
│   ├── api.ts
│   └── websocket.ts
└── types/
    └── index.ts
```

### 后端
```
backend/app/
├── main.py
├── config.py
├── api/v1/
│   ├── chat.py
│   ├── code.py
│   └── ws.py
├── services/
│   ├── ai_service.py
│   ├── chat_service.py
│   └── code_execution.py
├── core/
│   └── exceptions.py
└── schemas/
    └── chat.py
```

## 风险与妥协

| 风险 | 缓解措施 |
|------|----------|
| Render 免费 tier 休眠导致首次请求慢 | 文档中说明；MVP 可接受 |
| Docker 沙箱在 Render 上资源受限 | 严格限制 1CPU/512MB，超时报错友好提示 |
| 用户每次刷新需重填 API Key | MVP 已知妥协，P2 持久化解决 |
| Monaco Editor 体积大影响首屏 | Vite 动态导入 `monaco-editor` 的 loader，按需加载 |
| 3 天排期紧张 | Day 1 后端必须完成；若 Day 2 前端进度滞后，简化 UI 动画和样式细节 |

## 验证计划

1. **单元测试**：运行 `pytest backend/tests/unit`，AI 适配器和沙箱检测必须通过
2. **集成测试**：前后端同时运行，Postman/浏览器调通所有 P0 API
3. **端到端测试**：
   - 打开前端页面 → 输入 API Key → 在编程通道提问 "写一个冒泡排序" → 看到 AI 返回代码
   - 选中代码中的 `for` 循环 → 弹出 Ask → 点击 Ask → 理解通道出现代码片段 → 提问 "这里为什么用两层循环" → 看到解释
4. **部署验证**：公网 URL 能访问，走通上述流程
