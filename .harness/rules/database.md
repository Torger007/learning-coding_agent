---
name: database-rules
description: L2 数据库规范。定义存储策略、表结构、数据位置。
version: "2.0"
---

# 数据库规范

## 1. MVP 存储策略（本地优先）

```
Windows:   %APPDATA%/CodeMentor/
macOS:     ~/Library/Application Support/CodeMentor/
Linux:     ~/.config/CodeMentor/
```

文件:
- `database.sqlite` — SQLite 主数据库
- `cache/` — AI 响应缓存
- `exports/` — 导出文件

## 2. 核心表结构（MVP）

```sql
-- conversations: 对话历史
CREATE TABLE conversations (
    id TEXT PRIMARY KEY,
    title TEXT,
    channel TEXT CHECK(channel IN ('coding', 'understanding')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- messages: 消息记录
CREATE TABLE messages (
    id TEXT PRIMARY KEY,
    conversation_id TEXT REFERENCES conversations(id),
    role TEXT CHECK(role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    metadata TEXT, -- JSON: model, tokens, etc.
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- code_snippets: 保存的代码片段
CREATE TABLE code_snippets (
    id TEXT PRIMARY KEY,
    title TEXT,
    language TEXT,
    code TEXT NOT NULL,
    conversation_id TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- concept_mastery: 用户概念掌握度
CREATE TABLE concept_mastery (
    id TEXT PRIMARY KEY,
    concept TEXT UNIQUE NOT NULL,
    familiarity INTEGER CHECK(familiarity BETWEEN 0 AND 100),
    last_reviewed TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- settings: 用户设置
CREATE TABLE settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
```

## 3. 数据迁移

- MVP 使用 SQLite，迁移脚本放在 `backend/app/db/migrations/`
- 使用 Alembic 管理迁移
- 任何 schema 变更必须经过人工确认

## 4. 正式版策略（预留）

- PostgreSQL 替代 SQLite
- JWT 认证 + 多设备同步
- 保留 MVP 的 SQLite 路径逻辑作为离线降级
