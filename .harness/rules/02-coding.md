---
name: coding-standards
description: 编码规范，定义代码风格、文档、测试要求
version: "1.0"
---

# 编码规范

## 1. 代码风格

### 1.1 Python 风格（遵循 PEP 8 + Ruff 规则）

#### 基础格式
```python
# 使用 4 空格缩进，非 Tab
# 最大行长度 88 字符（Black 默认）
# 使用双引号字符串（除单引号更方便的情况）

# ✅ 正确
class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    async def get_user(self, user_id: UUID) -> User | None:
        return await self._repository.get_by_id(user_id)

# ❌ 错误
class user_service:  # 类名小写
    def __init__(self,repo):  # 缺少空格，类型注解
        self.repo=repo  # 操作符周围缺少空格
```

#### 导入排序
```python
# 导入顺序：标准库 → 第三方库 → 本地模块
# 每组之间空一行
# 使用绝对导入，避免相对导入（..module）

# ✅ 正确
import asyncio
from datetime import datetime
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import select

from myproject.domain.models import User
from myproject.infrastructure.database import get_db

# ❌ 错误
from ..models import User  # 避免相对导入
import os,sys  # 多个导入放一行
from fastapi import FastAPI
import asyncio  # 顺序错误（标准库应在最前）
```

#### 类型注解
```python
# 所有函数参数和返回值必须标注类型
# 使用 | 替代 Union（Python 3.10+）
# 使用 ... 表示可变参数类型

# ✅ 正确
def process_items(
    items: list[dict[str, Any]],
    callback: Callable[[int], str] | None = None,
    **kwargs: Any,
) -> tuple[int, list[str]]:
    ...

# 复杂类型使用 TypeAlias
from typing import TypeAlias

UserDict: TypeAlias = dict[str, str | int | list[str]]

# ❌ 错误
def process(items, callback=None):  # 缺少类型注解
    ...
```

### 1.2 命名规范

| 类型 | 命名风格 | 示例 |
|------|----------|------|
| 包/模块 | 小写，无下划线 | `auth`, `user_service` |
| 类/异常 | 大驼峰 | `UserService`, `ValidationError` |
| 函数/方法 | 小写下划线 | `get_user`, `process_payment` |
| 常量 | 大写下划线 | `MAX_RETRY`, `DEFAULT_TIMEOUT` |
| 私有 | 前导下划线 | `_internal_helper`, `_cache` |
| 保护 | 单前导下划线 | `_protected_method` |

## 2. 文档规范

### 2.1 文件头注释
```python
"""用户服务模块。

该模块提供用户管理的核心业务逻辑，包括：
- 用户 CRUD 操作
- 用户认证和授权
- 用户数据验证

示例:
    >>> service = UserService(repository)
    >>> user = await service.create_user(
    ...     CreateUserRequest(email="user@example.com", name="张三")
    ... )

作者: AI Agent
创建日期: 2024-01-15
"""
```

### 2.2 函数/方法文档字符串
```python
async def get_user_by_email(
    self,
    email: str,
    include_inactive: bool = False,
) -> User | None:
    """根据邮箱查找用户。

    参数:
        email: 用户邮箱地址，必须符合 RFC 5322 标准。
        include_inactive: 是否包含已注销用户。默认为 False，
            只返回活跃用户。

    返回:
        找到的用户对象，如果未找到返回 None。

    抛出:
        ValueError: 如果 email 格式无效。
        DatabaseError: 如果数据库查询失败。

    示例:
        >>> user = await service.get_user_by_email("user@example.com")
        >>> if user:
        ...     print(f"找到用户: {user.name}")
        ... else:
        ...     print("用户不存在")
    """
    if not validate_email(email):
        raise ValueError(f"无效的邮箱格式: {email}")
    # ... 实现代码
```

### 2.3 类文档字符串
```python
class UserService:
    """用户服务类，处理用户相关的业务逻辑。

    该类是用户领域的核心服务，负责协调用户数据的持久化、
    验证和业务规则执行。

    属性:
        repository: 用户数据访问对象。
        validator: 用户数据验证器。
        event_publisher: 领域事件发布器。

    方法:
        create_user: 创建新用户。
        get_user: 根据 ID 获取用户。
        update_user: 更新用户信息。
        delete_user: 删除用户。

    线程安全:
        该类的实例是线程安全的，可以在多个协程中共享。

    示例:
        >>> repository = UserRepository(db_session)
        >>> service = UserService(repository)
        >>> user = await service.create_user(
        ...     CreateUserRequest(email="test@example.com", name="测试")
        ... )
    """
```

## 3. 测试规范

### 3.1 测试结构
```
tests/
├── conftest.py           # pytest 配置和 fixtures
├── unit/                 # 单元测试
│   ├── domain/           # 领域层测试
│   ├── application/      # 应用层测试
│   └── infrastructure/   # 基础设施层测试
├── integration/          # 集成测试
│   ├── api/              # API 测试
│   └── database/         # 数据库测试
└── e2e/                  # 端到端测试
    └── scenarios/        # 业务场景测试
```

### 3.2 测试命名规范
```python
# 测试文件: test_<module_name>.py
# 测试类: Test<FeatureName>
# 测试函数: test_<action>_<condition>_<expected>

# ✅ 正确
class TestUserCreation:
    def test_create_user_with_valid_email_returns_user(self):
        ...

    def test_create_user_with_duplicate_email_raises_error(self):
        ...

    async def test_async_create_user_persists_to_database(self):
        ...

# ❌ 错误
def test1():  # 无意义名称
    ...

def user_test():  # 不清晰
    ...
```

### 3.3 单元测试示例
```python
import pytest
from unittest.mock import Mock, AsyncMock
from myproject.domain.models import User
from myproject.application.services import UserService


@pytest.fixture
def mock_repository():
    """创建模拟的用户仓库。"""
    repo = Mock()
    repo.get_by_email = AsyncMock()
    repo.create = AsyncMock()
    return repo


@pytest.fixture
def user_service(mock_repository):
    """创建用户服务实例。"""
    return UserService(repository=mock_repository)


class TestUserServiceCreateUser:
    """测试用户创建功能。"""

    async def test_create_user_with_valid_data_returns_user(
        self, user_service, mock_repository
    ):
        """使用有效数据创建用户应返回用户对象。"""
        # Arrange
        email = "test@example.com"
        name = "测试用户"
        mock_repository.get_by_email.return_value = None
        mock_repository.create.return_value = User(
            id="123", email=email, name=name
        )

        # Act
        result = await user_service.create_user(email=email, name=name)

        # Assert
        assert result is not None
        assert result.email == email
        assert result.name == name
        mock_repository.create.assert_called_once()

    async def test_create_user_with_existing_email_raises_error(
        self, user_service, mock_repository
    ):
        """使用已存在的邮箱创建用户应抛出错误。"""
        # Arrange
        email = "existing@example.com"
        mock_repository.get_by_email.return_value = User(
            id="456", email=email, name="现有用户"
        )

        # Act & Assert
        with pytest.raises(ValueError, match="邮箱已存在"):
            await user_service.create_user(email=email, name="新用户")

        mock_repository.create.assert_not_called()

    @pytest.mark.parametrize("invalid_email", [
        "not-an-email",
        "@example.com",
        "user@",
        "",
    ])
    async def test_create_user_with_invalid_email_raises_error(
        self, user_service, invalid_email
    ):
        """使用无效邮箱格式应抛出错误。"""
        with pytest.raises(ValueError, match="无效的邮箱格式"):
            await user_service.create_user(email=invalid_email, name="测试")
```

### 3.4 集成测试示例
```python
import pytest
from httpx import AsyncClient
from myproject.main import app


@pytest.fixture
async def client():
    """创建测试客户端。"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


class TestUserAPI:
    """测试用户 API 端点。"""

    async def test_create_user_endpoint(self, client):
        """测试创建用户端点。"""
        response = await client.post(
            "/api/v1/users",
            json={"email": "test@example.com", "name": "测试用户"}
        )

        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "test@example.com"
        assert "id" in data

    async def test_get_user_endpoint(self, client):
        """测试获取用户端点。"""
        # 先创建用户
        create_response = await client.post(
            "/api/v1/users",
            json={"email": "get@example.com", "name": "获取测试"}
        )
        user_id = create_response.json()["id"]

        # 再获取用户
        get_response = await client.get(f"/api/v1/users/{user_id}")

        assert get_response.status_code == 200
        data = get_response.json()
        assert data["id"] == user_id
        assert data["email"] == "get@example.com"
```

## 4. 类型注解规范

### 4.1 基本类型注解
```python
from typing import Any, TypeVar, Generic

# 基础类型
name: str = "Alice"
age: int = 30
height: float = 1.75
is_active: bool = True

# 容器类型
items: list[str] = ["a", "b", "c"]
mapping: dict[str, int] = {"a": 1, "b": 2}
unique: set[str] = {"a", "b"}
pair: tuple[str, int] = ("age", 30)

# Optional 和 Union
from typing import Optional, Union

def find_user(user_id: str) -> Optional[User]:
    ...

def parse_value(value: str) -> Union[int, float, str]:
    ...

# Python 3.10+ 推荐使用 | 操作符
def find_user(user_id: str) -> User | None:
    ...

def parse_value(value: str) -> int | float | str:
    ...
```

### 4.2 函数类型注解
```python
from collections.abc import Callable, Iterable, Iterator, AsyncIterator
from typing import ParamSpec, TypeVar

# 回调函数类型
Callback = Callable[[int], None]
Processor = Callable[[str], list[str]]

# 泛型函数
T = TypeVar('T')
U = TypeVar('U')

def first(items: list[T]) -> T | None:
    return items[0] if items else None

def map_items(items: list[T], func: Callable[[T], U]) -> list[U]:
    return [func(item) for item in items]

# 参数规范（保留调用签名）
P = ParamSpec('P')

def with_logging(func: Callable[P, T]) -> Callable[P, T]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

# 异步类型
from collections.abc import Coroutine

async def fetch_data(url: str) -> dict[str, Any]:
    ...

# 协程类型注解
CoroutineFunc = Callable[[str], Coroutine[None, None, dict[str, Any]]]

# 迭代器类型
def process_stream(data: Iterable[bytes]) -> Iterator[ProcessedChunk]:
    for chunk in data:
        yield process_chunk(chunk)

# 异步迭代器
async def async_fetch(urls: list[str]) -> AsyncIterator[Response]:
    for url in urls:
        yield await fetch(url)
```

### 4.3 类类型注解
```python
from typing import Self, override

class Container(Generic[T]):
    """泛型容器类。"""

    def __init__(self, item: T) -> None:
        self._item: T = item

    def get(self) -> T:
        return self._item

    def set(self, item: T) -> Self:
        """返回 self 支持链式调用。"""
        self._item = item
        return self

# 抽象基类
from abc import ABC, abstractmethod

class DataSource(ABC):
    """数据源抽象基类。"""

    @abstractmethod
    async def connect(self) -> None:
        """建立连接。"""
        ...

    @abstractmethod
    async def fetch(self, query: str) -> list[dict[str, Any]]:
        """执行查询。"""
        ...

class PostgresSource(DataSource):
    """PostgreSQL 数据源实现。"""

    def __init__(self, dsn: str) -> None:
        self._dsn = dsn
        self._pool: asyncpg.Pool | None = None

    @override
    async def connect(self) -> None:
        self._pool = await asyncpg.create_pool(self._dsn)

    @override
    async def fetch(self, query: str) -> list[dict[str, Any]]:
        if not self._pool:
            raise RuntimeError("未建立连接")
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(query)
            return [dict(row) for row in rows]
```

### 4.4 高级类型特性
```python
from typing import Literal, TypedDict, Required, NotRequired, ReadOnly

# 字面量类型
Status = Literal["pending", "processing", "completed", "failed"]
Priority = Literal[1, 2, 3, 4, 5]

def update_status(task_id: str, status: Status) -> None:
    ...

# TypedDict（结构化字典）
class Movie(TypedDict):
    name: str
    year: int
    rating: NotRequired[float]  # Python 3.11+
    tags: list[str]

movie: Movie = {
    "name": "Inception",
    "year": 2010,
    "tags": ["sci-fi", "thriller"],
}

# 或传统方式（Python < 3.11）
from typing import TypedDict, total_ordering

class MovieLegacy(TypedDict, total=False):
    name: str
    year: int
    rating: float

# Required/NotRequired（Python 3.10+）
class Config(TypedDict):
    host: Required[str]  # 必须提供
    port: Required[int]
    debug: NotRequired[bool]  # 可选，默认为 False
    workers: NotRequired[int]

# 泛型 TypedDict
from typing import Generic, TypeVar

T = TypeVar('T')

class PaginatedResponse(TypedDict, Generic[T]):
    items: list[T]
    total: int
    page: int
    per_page: int

# 使用
users_response: PaginatedResponse[User] = {
    "items": [user1, user2],
    "total": 100,
    "page": 1,
    "per_page": 20,
}

# Protocol（结构子类型）
from typing import Protocol

class Drawable(Protocol):
    """可绘制对象的协议。"""

    def draw(self, canvas: Canvas) -> None:
        """在画布上绘制。"""
        ...

    @property
    def bounds(self) -> Rect:
        """返回边界矩形。"""
        ...

# 任何实现了 draw 和 bounds 的对象都是 Drawable
class Circle:
    def __init__(self, x: float, y: float, r: float) -> None:
        self.x = x
        self.y = y
        self.r = r

    def draw(self, canvas: Canvas) -> None:
        canvas.draw_circle(self.x, self.y, self.r)

    @property
    def bounds(self) -> Rect:
        return Rect(
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r,
        )

def render_all(items: list[Drawable], canvas: Canvas) -> None:
    """渲染所有可绘制对象。"""
    for item in items:
        item.draw(canvas)

# 使用
circles = [Circle(0, 0, 10), Circle(100, 100, 20)]
render_all(circles, canvas)  # 类型检查通过
```

### 4.5 类型检查配置
```toml
# pyproject.toml 中的 mypy 配置
[tool.mypy]
python_version = "3.12"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
warn_unreachable = true
strict_equality = true
show_error_codes = true
show_column_numbers = true

# 忽略某些第三方库的类型检查
[[tool.mypy.overrides]]
module = ["thirdparty.*", "legacy.*"]
ignore_missing_imports = true

# 允许测试文件有一定灵活性
[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false
```

## 5. 代码审查清单

### 5.1 提交前自查
- [ ] 代码通过 ruff 检查（无格式错误）
- [ ] 代码通过 mypy 检查（无类型错误）
- [ ] 所有函数都有类型注解
- [ ] 公共 API 有文档字符串
- [ ] 新增代码有对应的测试
- [ ] 所有测试通过
- [ ] 没有打印调试代码（print/debugger）
- [ ] 没有硬编码的敏感信息

### 5.2 PR 审查要点
- [ ] 代码符合项目架构设计
- [ ] 没有重复代码（DRY 原则）
- [ ] 错误处理完善
- [ ] 性能考虑（无 N+1 查询、适当缓存）
- [ ] 安全性（输入验证、SQL 注入防护、XSS 防护）
- [ ] 向后兼容（API 版本控制）
- [ ] 文档更新（README、API 文档、CHANGELOG）

---

*本规范遵循 PEP 8、PEP 257 和 Google Python Style Guide，结合项目实际需求制定。*
