"""单元测试模式示例（后端 pytest）。

参考此风格编写测试。
"""
import pytest
from unittest.mock import Mock, AsyncMock

from app.services.chat_service import ChatService
from app.models.conversation import Conversation


@pytest.fixture
def mock_repo():
    repo = Mock(spec=ConversationRepository)
    repo.get_by_id = AsyncMock()
    repo.create = AsyncMock()
    return repo


@pytest.fixture
def mock_ai():
    service = Mock(spec=AIService)
    service.chat = AsyncMock(return_value="AI 响应")
    return service


@pytest.fixture
def chat_service(mock_repo, mock_ai):
    return ChatService(conversation_repo=mock_repo, ai_service=mock_ai)


class TestChatService:
    """测试对话服务。"""

    async def test_send_message_with_valid_conversation_returns_response(
        self, chat_service, mock_repo, mock_ai
    ):
        """有效对话应返回 AI 响应。"""
        # Arrange
        conv = Conversation(id="123", title="测试", channel="coding")
        mock_repo.get_by_id.return_value = conv

        # Act
        result = await chat_service.send_message("123", "你好", "gpt-4.5")

        # Assert
        assert result == "AI 响应"
        mock_ai.chat.assert_called_once()

    async def test_send_message_with_missing_conversation_raises_error(
        self, chat_service, mock_repo
    ):
        """对话不存在时应抛出错误。"""
        mock_repo.get_by_id.return_value = None

        with pytest.raises(ValueError, match="对话不存在"):
            await chat_service.send_message("999", "你好", "gpt-4.5")
