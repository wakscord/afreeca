import asyncio
from traceback import print_exc
from typing import Awaitable, Callable, Optional

import orjson
from aiohttp import ClientSession, ClientWebSocketResponse, WSMessage, WSMsgType

from afreeca.credential import Credential

from .constants import CHAT_URL, FLAG, RETURN_CODE, ServiceCode
from .exceptions import NotStreamingError
from .interfaces import BJInfo, Chat
from .packet import create_packet
from .utils import Flag


class AfreecaTV:
    def __init__(self, credential: Credential):
        self.credential = credential

    async def get_bj_info(self, bj_id: str) -> BJInfo:
        return await self.fetch_bj_info(self.credential, bj_id)

    async def create_chat(self, bj_id: str) -> "AfreecaChat":
        return AfreecaChat(bj_id, self.credential)

    @staticmethod
    async def fetch_bj_info(credential: Credential, bj_id: str) -> BJInfo:
        session = await credential.get_session()
        response = await session.post(
            f"https://live.afreecatv.com/afreeca/player_live_api.php",
            data=f"bid={bj_id}&type=live&player_type=html5",
            headers=credential.headers,
        )

        data = await response.text()
        data = orjson.loads(data)

        if data["CHANNEL"]["RESULT"] != 1:
            raise NotStreamingError(bj_id)

        return BJInfo(
            bj_id=bj_id,
            bj_nick=data["CHANNEL"]["BJNICK"],
            bno=data["CHANNEL"]["BNO"],
            title=data["CHANNEL"]["TITLE"],
            chat_url=CHAT_URL.format(
                chdomain=data["CHANNEL"]["CHDOMAIN"],
                chpt=int(data["CHANNEL"]["CHPT"]) + 1,
                bj_id=bj_id,
            ),
            chatno=data["CHANNEL"]["CHATNO"],
            ftk=data["CHANNEL"]["FTK"],
        )


class AfreecaChat:
    def __init__(self, bj_id: str, credential: Credential):
        self.bj_id = bj_id
        self.credential = credential
        self.info: Optional[BJInfo] = None

        self.session: Optional[ClientSession] = None
        self.connection: Optional[ClientWebSocketResponse] = None

        self.callbacks: list[Callable[[Chat], Awaitable]] = []

        self.keepalive_task: Optional[asyncio.Task] = None

    def add_callback(self, callback: Callable[[Chat], Awaitable]):
        self.callbacks.append(callback)

    async def start(self):
        await self.connect()

        while True:
            try:
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
                    print("timeout")
                    continue
            except:
                print_exc()

    async def connect(self):
        if not self.info:
            self.info = await AfreecaTV.fetch_bj_info(self.credential, self.bj_id)

        self.session = ClientSession()
        self.connection = await self.session.ws_connect(self.info.chat_url)

        await self._send(
            ServiceCode.SVC_LOGIN,
            [
                self.credential.pdbox_ticket if self.credential.pdbox_ticket else "",
                "",
                Flag().add(FLAG["GUEST"]).flag1,
            ],
        )

        if not self.keepalive_task:
            self.keepalive_task = asyncio.create_task(self._keepalive())

    async def _send(self, svc: ServiceCode, data: list):
        await self.connection.send_bytes(create_packet(svc, data))

    async def _keepalive(self):
        while True:
            try:
                await self._send(ServiceCode.SVC_KEEPALIVE, [])
            except:
                pass

            await asyncio.sleep(20)

    async def _process_message(self, msg: WSMessage):
        if msg.type != WSMsgType.BINARY:
            return

        header = msg.data[:14]
        body = msg.data[14:]

        svc = int(header[2:6])
        ret_code = int(header[12:14])

        if ret_code > RETURN_CODE["SUCCESS"]:
            reversed_ret_code = {v: k for k, v in RETURN_CODE.items()}
            print(f"not success ret_code: {reversed_ret_code[ret_code]}")

            return

        if svc == ServiceCode.SVC_LOGIN:
            await self._send(
                ServiceCode.SVC_JOINCH,
                [
                    self.info.chatno,
                    self.info.ftk,
                    "0",
                    "",
                    "log&set_bps=8000&view_bps=1000&quality=normal&geo_cc=KR&geo_rc=11&acpt_lang=ko_KR&svc_lang=ko_KRpwdauth_infoNULLpver2access_systemhtml5",
                ],
            )

        packet = body.decode("utf-8").strip().split("\f")

        if svc == ServiceCode.SVC_CHATMESG:
            chat = Chat(packet)

            for callback in self.callbacks:
                asyncio.create_task(callback(chat))
