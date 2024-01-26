from .constants import ServiceCode


def _build_packet_array(arr: list) -> list:
    return ["\f" + i for i in arr] + ["\f"]


def _make_bytes(arr: list) -> bytes:
    return bytes("".join(arr), "utf-8")


def _make_header(svc: ServiceCode, body_length: int) -> list:
    return [
        "\u001b",
        "\t",
        str(svc).zfill(4),
        str(body_length).zfill(6),
        "00",
    ]


def create_packet(svc: ServiceCode, data: list):
    body = _make_bytes(_build_packet_array(data))
    header = _make_bytes(_make_header(svc, len(body)))

    return header + body
