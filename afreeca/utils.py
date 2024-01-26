from .constants import FLAG


def get_color(raw_color):
    if not raw_color or not raw_color.isdigit() or int(raw_color) == 0:
        return None

    c = format(int(raw_color), "06X")
    return f"#{c[4:6]}{c[2:4]}{c[0:2]}"


def get_flags(flag1, flag2):
    flags = []

    for flag, data in FLAG.items():
        where, value = data["where"], data["value"]
        flag_binary = int(flag1) if where == 1 else int(flag2)

        if flag_binary & value:
            flags.append(flag)

    return flags


class Flag:
    def __init__(self):
        self._flag1 = 0
        self._flag2 = 0

    @property
    def flag1(self):
        return str(self._flag1)

    @property
    def flag2(self):
        return str(self._flag2)

    def add(self, flag):
        value, where = flag["value"], flag["where"]

        if where == 1:
            self._flag1 |= value
        else:
            self._flag2 |= value

        return self

    def sub(self, flag):
        value, where = flag["value"], flag["where"]

        if where == 1:
            self._flag1 &= ~value
        else:
            self._flag2 &= ~value

        return self
