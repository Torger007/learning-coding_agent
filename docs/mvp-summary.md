# MVP 总结

## 当前完成范围

learning-coding_agent 已完成 MVP P0 主流程：

- React + TypeScript + Vite 前端骨架。
- 双栏并行界面：编程助手与理解助手。
- 编程通道支持 WebSocket 流式生成代码。
- AI 返回的代码块通过 Monaco Editor 展示。
- 用户选中代码后显示 Ask 浮层，并把片段带入理解通道。
- 理解通道支持围绕选中代码片段继续提问。
- FastAPI 后端提供 REST API、WebSocket 和健康检查。
- OpenAI-compatible AI 适配器支持普通响应与流式响应。
- API Key 支持前端内存输入，也支持后端环境变量兜底。
- Python 代码执行使用 Docker 沙箱，并在执行前做危险代码静态扫描。
- AI 适配器和沙箱检测已有单元测试。

## 已实现的 P0 验收点

| 验收项 | 状态 |
|------|------|
| 双栏布局 | 已完成 |
| 编程通道多轮会话 | 已完成，内存会话 |
| Monaco 代码展示 | 已完成 |
| 代码选中 Ask | 已完成 |
| 理解通道代码问答 | 已完成 |
| REST API | 已完成 |
| WebSocket 流式响应 | 已完成 |
| AI 适配器 | 已完成 |
| API Key 设置 | 已完成 |
| Docker 沙箱执行 | 已完成 |
| 核心单元测试 | 已完成 |

## 已知妥协

- 前端 API Key 只保存在页面内存中，刷新后需要重新输入。
- UI 动画和错误提示保持 MVP 级别。
- 端到端自动化测试尚未加入，当前以单元测试和手动联调为主。
- Electron 桌面壳、SQLite 持久化、多模型切换和用户认证延后到 P2。

## 本地验证

后端：

```bash
cd backend
pytest tests/unit
uvicorn app.main:app --reload
```

前端：

```bash
cd frontend
npm install
npm run dev
npm run build
```

手动主流程：

1. 打开前端页面。
2. 点击右上角「设置 API Key」并填入 AI API Key。
3. 在编程通道输入「写一个冒泡排序」。
4. 等待 AI 返回代码块。
5. 在代码块中选中一段代码并点击 Ask。
6. 在理解通道继续输入问题并发送。

## 部署说明

- 后端可使用 `backend/Dockerfile` 和 `backend/render.yaml` 部署到 Render。
- 前端可部署到 Vercel。
- 前端生产环境需要设置：
  - `VITE_API_BASE_URL`
  - `VITE_WS_BASE_URL`
