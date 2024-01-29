from __future__ import annotations

from typing import Optional, TypedDict

from typing_extensions import NotRequired


class ChatPacket(TypedDict):
    cmd: str
    data: ChatPacketData


class ChatPacketData(TypedDict):
    message: NotRequired[str]
    senderID: NotRequired[str]
    permission: NotRequired[int]
    chatLang: NotRequired[int]
    nickname: NotRequired[str]
    flags: NotRequired[list[str]]
    subscription_month: NotRequired[Optional[int]]
    color: NotRequired[Optional[str]]
