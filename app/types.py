import enum


class Role(enum.Enum):
    admin = "admin"
    dispatcher = "dispatcher"


class Status(enum.Enum):
    pending = "pending"
    in_progress = "in progress"
    done = "done"
    canceled = "canceled"


class Category(enum.Enum):
    lightweight = "lightweight"
    heavy = "heavy"


class Transport(enum.Enum):
    auto = "auto"
    mt = "mt"
    pd = "pd"
    bc = "bc"
    sc = "sc"
