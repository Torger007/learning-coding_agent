---
name: /validate
description: 运行项目验证：lint、类型检查、测试。
---

# /validate

运行完整的项目验证管道。

## 执行步骤

1. **后端检查**
   ```bash
   cd backend
   ruff check .
   mypy src/
   pytest
   ```

2. **前端检查**
   ```bash
   cd src/renderer
   npx tsc --noEmit
   npx eslint .
   ```

3. **安全扫描**
   - 检查是否有硬编码 API Key（grep `sk-`, `Bearer ` 等模式）
   - 检查 `.env` 是否被 `.gitignore` 忽略

## 输出

报告每个步骤的通过/失败状态，以及失败文件列表。
