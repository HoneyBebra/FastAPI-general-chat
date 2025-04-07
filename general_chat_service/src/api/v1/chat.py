import asyncio

from fastapi import APIRouter, Depends, Request, WebSocket
from fastapi.responses import HTMLResponse
from starlette.websockets import WebSocketDisconnect

from ...dao.chat import MessagesDAO
from ...dependensies.chat import send_message_on_websocket
from ...dependensies.users import get_current_user
from ...models.users import Users
from ...schemas.v1.chat import SMessage
from ..v1 import templates

router = APIRouter()

active_websockets: list[WebSocket] = []


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    global active_websockets

    await websocket.accept()
    active_websockets.append(websocket)
    try:
        while True:
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        active_websockets.remove(websocket)


# TODO: Add auth check and redirect to /auth
@router.get(
    "/",
    response_class=HTMLResponse,
    summary="Chat page",
    description="A page where you can send and read messages",
    response_description="Return html template",
)
async def get_chat_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("chat.html", {"request": request})


@router.get(
    "/messages",
    response_model=list[SMessage],
    summary="All chat messages",
    description="Return all chat messages",
    response_description="Return a list of all chat messages",
)
async def get_messages(messages_dao: MessagesDAO = Depends()) -> list[SMessage]:
    return await messages_dao.get_all() or []  # type: ignore[return-value]


@router.post(
    "/messages",
    response_model=SMessage,
    summary="Create a new chat message",
    description="Create a new chat message",
    response_description="Return a new chat message",
)
async def send_message(
    message: SMessage,
    current_user: Users = Depends(get_current_user),
    messages_dao: MessagesDAO = Depends(),
) -> SMessage:
    global active_websockets

    await messages_dao.add(sender_id=current_user.id, content=message.content)
    await send_message_on_websocket(active_websockets, message)

    return message
