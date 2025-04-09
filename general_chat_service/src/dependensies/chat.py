from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect

from ..schemas.v1.chat import SMessage


async def send_message_on_websocket(active_websockets: list[WebSocket], message: SMessage) -> None:
    for websocket in active_websockets.copy():
        try:
            await websocket.send_json(dict(message))
        except (RuntimeError, WebSocketDisconnect):
            active_websockets.remove(websocket)
