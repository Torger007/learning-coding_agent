---
name: testing-rules
description: L2 测试规范。定义测试结构、命名、覆盖要求。
version: "2.0"
---

# 测试规范

## 1. 测试结构

```
tests/
├── conftest.py           # pytest fixtures
├── unit/                 # 单元测试
│   ├── services/
│   └── utils/
├── integration/          # 集成测试
│   ├── api/
│   └── db/
└── e2e/                  # 端到端（MVP 可延后）
```

## 2. 命名规范

```python
# 文件: test_<module>.py
# 类: Test<Feature>
# 函数: test_<action>_<condition>_<expected>

class TestUserCreation:
    def test_create_user_with_valid_email_returns_user(self):
        ...

    def test_create_user_with_duplicate_email_raises_error(self):
        ...
```

## 3. 覆盖要求

| 阶段 | 要求 |
|------|------|
| MVP | 核心逻辑 >60%，UI 可延后 |
| 正式版 | >80%，含集成和 e2e |

## 4. 不可妥协

- 沙箱执行逻辑必须有测试
- AI 服务接口（适配器层）必须有测试
- 数据库操作层必须有测试

## 5. 允许妥协（MVP）

- React 组件测试可用手动代替
- 复杂边界条件可延后
- 性能测试延后到正式版
