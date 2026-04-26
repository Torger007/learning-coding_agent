# AI API Key 配置指南

项目现在使用通用 OpenAI-compatible 配置项，不再绑定到 Kimi 命名。你可以把火山引擎 Coding Plan 的 API Key 接入到同一套后端适配器。

## 推荐配置

在 `backend/.env` 中填写：

```env
AI_API_KEY=你的火山引擎CodingPlan API Key
AI_BASE_URL=https://ark.cn-beijing.volces.com/api/coding/v3
AI_MODEL=doubao-seed-code
```

注意：`AI_BASE_URL` 只写到 `/api/coding/v3`，不要加 `/chat/completions`。后端会自动拼接：

```text
{AI_BASE_URL}/chat/completions
```

## 前端临时输入方式

如果你不想把 API Key 写入后端 `.env`，也可以在前端右上角「设置 API Key」弹窗中临时粘贴。

这种方式只会把 key 保存在当前页面内存中：

- 刷新页面后需要重新输入。
- 不会写入浏览器本地存储。
- 不会提交到代码仓库。

前端输入的 API Key 优先级高于后端环境变量。

## 获取火山 API Key

1. 打开火山方舟控制台：https://console.volcengine.com/ark
2. 登录账号。
3. 进入 API Key 或访问密钥管理页面。
4. 创建 Coding Plan 可用的 API Key。
5. 复制 Key，填入 `AI_API_KEY` 或前端设置弹窗。

## 兼容说明

后端仍保留旧变量作为过渡兼容：

```env
KIMI_API_KEY=
KIMI_BASE_URL=
KIMI_MODEL=
```

新变量 `AI_*` 优先级更高，后续建议只使用：

```env
AI_API_KEY=
AI_BASE_URL=
AI_MODEL=
```
