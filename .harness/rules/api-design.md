---
name: api-design-rules
description: L2 API 设计规范。定义路由命名、请求响应格式、版本控制。
version: "2.0"
---

# API 设计规范

## 1. REST 路由命名

- 使用资源名词，避免动词开头
- 统一前缀 `/api/v1/`
- HTTP 方法表达操作语义

```
✅ GET    /api/v1/health          # 健康检查
✅ POST   /api/v1/chat/code       # 生成代码
✅ POST   /api/v1/code/execute    # 执行代码
✅ GET    /api/v1/conversations   # 获取对话列表
✅ GET    /api/v1/conversations/{id}/messages

❌ POST   /createCode             # 动词开头
❌ GET    /api/v1/getUsers        # 动词冗余
```

## 2. WebSocket 规范

- 路径: `/api/v1/ws/chat`
- 消息格式（JSON）:
  ```json
  {
    "type": "chat.message",
    "payload": {
      "conversation_id": "uuid",
      "content": "用户问题",
      "model": "gpt-4.5"
    }
  }
  ```
- 流式响应分块发送，最后发送 `{"type": "chat.done"}`

## 3. 统一响应格式

```json
{
  "success": true,
  "data": { ... },
  "error": null,
  "meta": {
    "request_id": "uuid",
    "timestamp": "2026-04-24T10:00:00Z"
  }
}
```

错误时:
```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "字段验证失败",
    "details": [{ "field": "email", "message": "格式不正确" }]
  }
}
```

## 4. 版本控制

- URL 路径包含版本号（`/api/v1/`）
- 破坏性变更必须升级版本号
- 非破坏性变更（新增字段）保持当前版本
