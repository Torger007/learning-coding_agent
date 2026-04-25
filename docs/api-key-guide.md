# 如何获取 Kimi API Key

本项目 MVP 使用 Kimi K2.5 作为 AI 模型适配目标。API Key 可以在前端设置弹窗中临时输入，也可以配置为后端环境变量 `KIMI_API_KEY`。

## 获取步骤

1. 打开 Kimi 开放平台：https://platform.moonshot.cn
2. 注册或登录账号。
3. 进入「API Key 管理」页面。
4. 点击「创建 API Key」。
5. 复制生成的 Key，粘贴到应用右上角「设置 API Key」弹窗中。
6. 保存后即可在编程通道和理解通道中发起请求。

## MVP 存储方式

- 前端输入的 API Key 只保存在当前页面内存中。
- 刷新页面后需要重新输入。
- 不会写入代码仓库、浏览器本地存储或日志。

## 后端环境变量方式

如果要在部署环境中由后端统一管理 API Key，可以设置：

```bash
KIMI_API_KEY=sk-xxxxxxxxxxxxxxxx
```

前端请求携带的 API Key 优先级高于后端环境变量，便于本地调试和多用户试用。
