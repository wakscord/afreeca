def _build_packet_array(arr: list[str]) -> list[str]:
    return ["\f" + i for i in arr] + ["\f"]


def _make_bytes(arr: list[str]) -> bytes:
    return bytes("".join(arr), "utf-8")


def _make_header(svc: int, body_length: int) -> list[str]:
    return [
        "\u001b",
        "\t",
        str(svc).zfill(4),
        str(body_length).zfill(6),
        "00",
    ]


def create_packet(svc: int, data: list[str]) -> bytes:
    body = _make_bytes(_build_packet_array(data))
    header = _make_bytes(_make_header(svc, len(body)))

    return header + body
