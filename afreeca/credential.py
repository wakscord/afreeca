from __future__ import annotations

from typing import Optional

from aiohttp import ClientSession

from .exceptions import LoginError


class Credential:
    headers: dict[str, str] = {"Content-Type": "application/x-www-form-urlencoded"}
    pdbox_ticket: Optional[str] = None
    _session: Optional[ClientSession] = None

    async def get_session(self) -> ClientSession:
        if self._session is None:
            self._session = ClientSession()

        self._session.headers.update(self.headers)

        return self._session


class GuestCredential(Credential):
    ...


class UserCredential(Credential):
    @classmethod
    async def login(cls, id: str, pw: str) -> UserCredential:
        credential = cls()

        session = await credential.get_session()
        response = await session.post(
            "https://login.afreecatv.com/app/LoginAction.php",
            data=f"szUid={id}&szPassword={pw}&szWork=login",
        )

        cookies = {key: value.value for key, value in response.cookies.items()}

        if not cookies.get("PdboxTicket"):
            raise LoginError()

        credential.pdbox_ticket = cookies.get("PdboxTicket")
        credential.headers["Cookie"] = "; ".join(
            [f"{key}={value}" for key, value in cookies.items()]
        )

        return credential
