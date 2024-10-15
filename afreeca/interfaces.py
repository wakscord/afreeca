from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .types.packet import ChatPacket
from .utils import get_color, get_flags


@dataclass
class BroadcastInfo:
    bno: int
    title: str
    viewer: int
    is_password: bool
    is_subscription: bool


@dataclass
class BJInfo:
    bj_id: str
    bj_nick: str

    bno: str
    title: str

    chat_url: str
    chatno: str
    ftk: str
    tk: Optional[str]

    pcon: dict[int, str]
    bpwd: bool


@dataclass
class Chat:
    sender_id: str
    nickname: str
    message: str

    chat_lang: int
    subscription_month: Optional[int]
    flags: list[str]

    def __init__(self, packet: list[str]) -> None:
        data = self._parse_packet(packet)["data"]

        self.sender_id = data["senderID"]
        self.nickname = data["nickname"]
        self.message = data["message"]
        self.chat_lang = data["chatLang"]
        self.subscription_month = data["subscription_month"]
        self.flags = data["flags"]

    def _parse_packet(self, packet: list[str]) -> ChatPacket:
        message = packet[0].replace("\r", "")
        senderID = packet[1]
        permission = int(packet[3])
        chatLang = int(packet[4])
        nickname = packet[5]
        flag = packet[6]
        subscription_month = None if packet[7] == "-1" else int(packet[7])

        color = None

        if len(packet) > 8:
            color = get_color(packet[8])

        # if permission == 1:
        #     return {"cmd": "staff", "data": {"message": message, "nickname": nickname}}
        # elif permission == 2:
        #     return {"cmd": "police", "data": {"message": message, "nickname": nickname}}

        if permission == 3 or permission == 0:
            flag1, flag2 = flag.split("|")

            return {
                "cmd": "msg",
                "data": {
                    "senderID": senderID,
                    "nickname": nickname,
                    "message": message,
                    "chatLang": chatLang,
                    "color": color,
                    "subscription_month": subscription_month,
                    "flags": get_flags(flag1, flag2),
                },
            }

        return {"cmd": "unknown", "data": {}}
