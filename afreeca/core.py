from __future__ import annotations

import asyncio
from typing import Callable, Coroutine, Optional, cast

import orjson
from aiohttp import ClientSession, ClientWebSocketResponse, WSMessage, WSMsgType

from .constants import CHAT_URL, FLAG, RETURN_CODE, ServiceCode
from .credential import Credential
from .exceptions import NotStreamingError, PasswordError
from .interfaces import BJInfo, BroadcastInfo, Chat
from .packet import create_packet
from .types.bj_info import BJInfo as BJInfoDict
from .utils import Flag, callback

Callback = Coroutine[None, None, None]


class AfreecaTV:
    def __init__(self, credential: Credential) -> None:
        self.credential = credential

    async def get_bj_info(self, bj_id: str) -> BJInfo:
        return await self.fetch_bj_info(self.credential, bj_id)

    async def get_broadcast_info(self, bj_id: str) -> BroadcastInfo | None:
        return await self.fetch_broadcast_info(self.credential, bj_id)

    async def create_chat(self, bj_id: str) -> AfreecaChat:
        return AfreecaChat(bj_id, self.credential)

    @staticmethod
    async def fetch_bj_info(credential: Credential, bj_id: str) -> BJInfo:
        session = await credential.get_session()
        response = await session.post(
            f"https://live.sooplive.co.kr/afreeca/player_live_api.php?bjid={bj_id}",
            data=f"bid={bj_id}&type=live&player_type=html5",
            headers=credential.headers,
        )

        raw_data = await response.text()
        data = orjson.loads(raw_data)
        data = cast(BJInfoDict, data)

        if data["CHANNEL"]["RESULT"] != 1:
            raise NotStreamingError(bj_id)

        pcon = {}

        pcon_object = data["CHANNEL"].get("PCON_OBJECT")

        if isinstance(pcon_object, dict):
            pcon = {
                obj["MONTH"]: obj["FILENAME"]
                for obj in data["CHANNEL"]["PCON_OBJECT"]["tier1"]
            }
        elif isinstance(pcon_object, list):
            pcon = {
                obj["MONTH"]: obj["FILENAME"] for obj in data["CHANNEL"]["PCON_OBJECT"]
            }

        return BJInfo(
            bj_id=bj_id,
            bj_nick=data["CHANNEL"]["BJNICK"],
            bno=data["CHANNEL"]["BNO"],
            title=data["CHANNEL"]["TITLE"],
            chat_url=CHAT_URL.format(
                chdomain=data["CHANNEL"]["CHDOMAIN"],
                chpt=int(data["CHANNEL"]["CHPT"]),  # wss 프로토콜 사용시 +1
                bj_id=bj_id,
            ),
            chatno=data["CHANNEL"]["CHATNO"],
            ftk=data["CHANNEL"]["FTK"],
            tk=data["CHANNEL"]["TK"] if "TK" in data["CHANNEL"] else None,
            pcon=pcon,
            bpwd=data["CHANNEL"]["BPWD"] == "Y",
        )

    @staticmethod
    async def fetch_broadcast_info(
        credential: Credential, bj_id: str
    ) -> BroadcastInfo | None:
        session = await credential.get_session()
        response = await session.get(
            f"https://chapi.sooplive.co.kr/api/{bj_id}/station",
            headers=credential.headers,
        )

        raw_data = await response.text()
        data = orjson.loads(raw_data)

        if "broad" not in data:
            return None

        return BroadcastInfo(
            bno=data["broad"]["broad_no"],
            title=data["broad"]["broad_title"],
            viewer=data["broad"]["current_sum_viewer"],
            is_password=data["broad"]["is_password"],
        )


class AfreecaChat:
    def __init__(self, bj_id: str, credential: Credential):
        self.bj_id = bj_id
        self.credential = credential
        self.info: Optional[BJInfo] = None

        self.session: Optional[ClientSession] = None
        self.connection: Optional[ClientWebSocketResponse] = None

        self.callbacks: dict[str, list[Callable[[Chat], Callback]]] = {}
        self.process_callbacks: dict[
            int, list[Callable[[AfreecaChat, list[str]], None]]
        ] = {}

        self.keepalive_task: Optional[asyncio.Task[None]] = None

        self.room_password: Optional[str] = None

    def add_callback(self, event: str, callback: Callable[[Chat], Callback]) -> None:
        if self.callbacks.get(event) is None:
            self.callbacks[event] = []

        self.callbacks[event].append(callback)

    def remove_callback(self, callback: Callable[[Chat], Callback]) -> None:
        for event, callbacks in self.callbacks.items():
            if callback in callbacks:
                self.callbacks[event].remove(callback)

    def set_password(self, password: str) -> None:
        self.room_password = password

    async def loop(self) -> None:
        while self.connection is not None:
            if self.connection.closed:
                await self.connect()
                return

            try:
                msg = await self.connection.receive(timeout=10)

                if msg.type == WSMsgType.CLOSED:
                    await self.connect()
                    continue

                await self._process_message(msg)
            except asyncio.TimeoutError:
                continue

    async def start(self) -> None:
        await self.connect()
        await self.loop()

    async def connect(self, sub: bool = False) -> None:
        if not self.info:
            self.info = await AfreecaTV.fetch_bj_info(self.credential, self.bj_id)

        self.session = ClientSession()
        self.connection = await self.session.ws_connect(self.info.chat_url)

        await self.send(
            ServiceCode.SVC_LOGIN,
            [
                self.info.tk if self.info.tk else "",
                "",
                Flag().add(FLAG["FOLLOWER" if sub else "GUEST"]).flag1,
            ],
        )

        if not self.keepalive_task:
            self.keepalive_task = asyncio.create_task(self._keepalive())

    async def send(self, svc: int, data: list[str]) -> None:
        if self.connection is not None:
            await self.connection.send_bytes(create_packet(svc, data))

    async def _keepalive(self) -> None:
        while True:
            try:
                await self.send(ServiceCode.SVC_KEEPALIVE, [])
            except:
                pass

            await asyncio.sleep(20)

    async def _process_message(self, msg: WSMessage) -> None:
        if msg.type != WSMsgType.BINARY:
            return

        header = msg.data[:14]
        body = msg.data[14:]

        svc = int(header[2:6])
        ret_code = int(header[12:14])

        if ret_code == RETURN_CODE["PASSWORD_ERROR"]:
            raise PasswordError()

        if ret_code > RETURN_CODE["SUCCESS"]:
            reversed_ret_code = {v: k for k, v in RETURN_CODE.items()}
            print(f"not success ret_code: {reversed_ret_code[ret_code]}")

            return

        if svc == ServiceCode.SVC_LOGIN and self.info is not None:
            content = [
                self.info.chatno,
                self.info.ftk,
                "0",
                "",
                "",
            ]

            if self.room_password:
                content[4] = f"pwd\x11{self.room_password}"

            await self.send(ServiceCode.SVC_JOINCH, content)

        packet: list[str] = []

        try:
            packet = body.decode("utf-8").strip().split("\f")
        except UnicodeDecodeError:
            packet_raw: list[bytes] = body.split()

            for packet_part in packet_raw:
                try:
                    packet.append(packet_part.decode("utf-8"))
                except UnicodeDecodeError:
                    packet.append(packet_part.decode("euc-kr"))

        for name in self.__dir__():
            if name.startswith("_process_"):
                func = getattr(self, name)

                if callable(func) and hasattr(func, "svc"):
                    if func.svc == svc:
                        await func(packet)

        for callback in self.callbacks.get("all", []):
            asyncio.create_task(callback(svc, packet))

    @callback(ServiceCode.SVC_CHATMESG)
    async def _process_chat(self, packet: list[str]) -> None:
        if len(packet) < 11:
            return

        chat = Chat(packet)

        for callback in self.callbacks.get("chat", []):
            asyncio.create_task(callback(chat))
