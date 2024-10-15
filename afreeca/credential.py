from __future__ import annotations

from typing import Optional

from aiohttp import ClientSession

from .exceptions import LoginError


class Credential:
    headers: dict[str, str] = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    pdbox_ticket: Optional[str] = None
    au: Optional[str] = None
    _session: Optional[ClientSession] = None

    async def get_session(self) -> ClientSession:
        if self._session is None:
            self._session = ClientSession()

        self._session.headers.update(self.headers)

        return self._session


class GuestCredential(Credential): ...


class UserCredential(Credential):
    @classmethod
    async def login(cls, id: str, pw: str) -> UserCredential:
        credential = cls()

        session = await credential.get_session()
        response = await session.post(
            "https://login.sooplive.co.kr/app/LoginAction.php",
            data=f"szUid={id}&szPassword={pw}&szWork=login",
        )

        cookies = {key: value.value for key, value in response.cookies.items()}

        if not cookies.get("AuthTicket"):
            raise LoginError()

        credential.pdbox_ticket = cookies.get("PdboxTicket")
        credential.au = cookies.get("_au")
        credential.headers["Cookie"] = "; ".join(
            [f"{key}={value}" for key, value in cookies.items()]
        )

        return credential

    async def logout(self) -> None:
        session = await self.get_session()

        await session.get("https://login.sooplive.co.kr/app/LogOut.php")

        await session.close()

        self._session = None
