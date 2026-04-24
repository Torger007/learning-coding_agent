"""Service 模式示例（后端）。

业务逻辑层，协调多个仓库/外部服务。
"""
from app.models.conversation import Conversation
from app.repositories.conversation import ConversationRepository
from app.services.ai_service import AIService


class ChatService:
    """对话业务服务。"""

    def __init__(
        self,
        conversation_repo: ConversationRepository,
        ai_service: AIService,
    ) -> None:
        self._conversation_repo = conversation_repo
        self._ai_service = ai_service

    async def create_conversation(
        self, title: str, channel: str
    ) -> Conversation:
        """创建新对话并返回。"""
        conversation = Conversation(title=title, channel=channel)
        return await self._conversation_repo.create(conversation)

    async def send_message(
        self, conversation_id: str, content: str, model: str
    ) -> str:
        """发送消息并获取 AI 响应。"""
        conversation = await self._conversation_repo.get_by_id(conversation_id)
        if not conversation:
            raise ValueError(f"对话不存在: {conversation_id}")

        # 调用 AI 服务
        response = await self._ai_service.chat(
            messages=conversation.messages,
            model=model,
        )
        return response
