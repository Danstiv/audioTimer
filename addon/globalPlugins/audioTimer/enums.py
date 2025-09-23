from enum import StrEnum, auto


class TimerState(StrEnum):
    DISABLED = auto()
    ACTIVE = auto()
    PENDING = auto()


class TimerFinishAction(StrEnum):
    REMOVE = auto()
    DISABLE = auto()


class NotificationType(StrEnum):
    ONETIME = auto()
    RECURRENT = auto()


class RestartPolicy(StrEnum):
    IMMEDIATE = auto()
    ON_USER_ACTION = auto()
