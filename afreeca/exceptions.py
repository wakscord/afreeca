class NotStreamingError(Exception):
    def __init__(self, bj_id: str):
        self.bj_id = bj_id

    def __str__(self):
        return f"{self.bj_id}님은 방송 중이 아닙니다."
