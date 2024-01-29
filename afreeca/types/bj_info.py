from __future__ import annotations

from typing import TypedDict


class BJInfo(TypedDict):
    CHANNEL: BJChannel


class BJChannel(TypedDict):
    RESULT: int
    BJNICK: str
    BNO: str
    TITLE: str
    CHDOMAIN: str
    CHPT: str
    CHATNO: str
    FTK: str
