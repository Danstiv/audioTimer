from enum import IntEnum


class TimerState(IntEnum):
    DISABLED = 0
    ACTIVE = 1
    PENDING = 2


class TimerFinishAction(IntEnum):
    REMOVE = 0
    DISABLE = 1


class NotificationType(IntEnum):
    ONETIME = 0
    RECURRENT = 1


class RestartPolicy(IntEnum):
    IMMEDIATE = 0
    ON_USER_ACTION = 1
