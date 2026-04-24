"""Repository 模式示例（后端）。

数据访问抽象，隔离 SQLAlchemy 与业务逻辑。
"""
from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.conversation import Conversation


class ConversationRepository:
    """对话数据仓库。"""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, conversation_id: str) -> Conversation | None:
        """根据 ID 获取对话。"""
        result = await self._session.execute(
            select(Conversation).where(Conversation.id == conversation_id)
        )
        return result.scalar_one_or_none()

    async def create(self, conversation: Conversation) -> Conversation:
        """创建对话。"""
        self._session.add(conversation)
        await self._session.commit()
        await self._session.refresh(conversation)
        return conversation

    async def list_by_channel(
        self, channel: str, limit: int = 20, offset: int = 0
    ) -> list[Conversation]:
        """分页获取某通道的对话列表。"""
        result = await self._session.execute(
            select(Conversation)
            .where(Conversation.channel == channel)
            .order_by(Conversation.updated_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())
