"""In-memory chat session management."""

from app.schemas.chat import ChatMessage


class ChatService:
    """Manages chat sessions in memory."""

    def __init__(self) -> None:
        self._sessions: dict[str, list[dict]] = {}

    def get_history(self, session_id: str) -> list[dict]:
        """Retrieve message history for a session."""
        return self._sessions.get(session_id, [])

    def append_message(self, session_id: str, message: ChatMessage | dict) -> None:
        """Append a message to session history."""
        if session_id not in self._sessions:
            self._sessions[session_id] = []
        msg = message.model_dump() if isinstance(message, ChatMessage) else message
        self._sessions[session_id].append(msg)

    def clear_session(self, session_id: str) -> None:
        """Clear a session's history."""
        self._sessions.pop(session_id, None)


chat_service = ChatService()
