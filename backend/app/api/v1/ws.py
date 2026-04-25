"""WebSocket routes for streaming chat."""

import json
import uuid

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.services.ai_service import ai_service
from app.services.chat_service import chat_service

router = APIRouter(tags=["websocket"])


@router.websocket("/ws/chat")
async def chat_websocket(websocket: WebSocket) -> None:
    """WebSocket endpoint for streaming chat."""
    await websocket.accept()
    session_id: str | None = None

    try:
        while True:
            raw = await websocket.receive_text()
            msg = json.loads(raw)

            msg_type = msg.get("type")
            payload = msg.get("payload", {})

            if msg_type == "chat.init":
                session_id = payload.get("session_id") or str(uuid.uuid4())
                await websocket.send_json({
                    "type": "chat.init_ack",
                    "payload": {"session_id": session_id},
                })
                continue

            if msg_type == "chat.message":
                session_id = payload.get("session_id") or session_id or str(uuid.uuid4())
                content = payload.get("content", "")
                mode = payload.get("mode", "code")  # 'code' or 'explain'
                code_snippet = payload.get("code_snippet")
                api_key = payload.get("api_key")

                history = chat_service.get_history(session_id)

                if mode == "code":
                    stream_gen = await ai_service.generate_code(
                        prompt=content, history=history, stream=True, api_key=api_key
                    )
                else:
                    stream_gen = await ai_service.explain(
                        prompt=content,
                        code_snippet=code_snippet,
                        history=history,
                        stream=True,
                        api_key=api_key,
                    )

                full_response = ""
                async for chunk in stream_gen:
                    full_response += chunk
                    await websocket.send_json({
                        "type": "chat.chunk",
                        "payload": {"content": chunk, "session_id": session_id, "mode": mode},
                    })

                chat_service.append_message(session_id, {"role": "user", "content": content})
                chat_service.append_message(session_id, {"role": "assistant", "content": full_response})

                await websocket.send_json({"type": "chat.done", "payload": {"session_id": session_id, "mode": mode}})
                continue

            await websocket.send_json({
                "type": "error",
                "payload": {"message": f"Unknown message type: {msg_type}"},
            })

    except WebSocketDisconnect:
        pass
    except Exception as e:
        await websocket.send_json({
            "type": "error",
            "payload": {"message": str(e)},
        })
