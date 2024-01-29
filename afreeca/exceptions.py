class NotStreamingError(Exception):
    def __init__(self, bj_id: str) -> None:
        self.bj_id = bj_id

    def __str__(self) -> str:
        return f"{self.bj_id}님은 방송 중이 아닙니다."


class LoginError(Exception):
    def __str__(self) -> str:
        return "로그인에 실패했습니다."
