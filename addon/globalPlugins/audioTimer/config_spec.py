from typing import TypedDict

from .enums import NotificationType, RestartPolicy, TimerFinishAction, TimerState

CONFIG_SPEC = {
    "next_timer_id": "integer(default=1)",
    "timers": {
        "__many__": {
            "id": "integer",
            "name": "string",
            "state": "integer",
            "finish_time": "float",
            "interval": "integer",
            "repeat_count": "integer",
            "repeat_limit": "integer",
            "finish_action": "integer",
            "notification_type": "integer",
            "restart_policy": "integer",
            "recurrent_notification_interval": "integer",
            "recurrent_notification_time": "float",
            "notification_sound": "string",
        }
    },
}


class TimerSchema(TypedDict):
    id: int | None
    name: str
    state: TimerState
    finish_time: float
    interval: int
    repeat_count: int
    repeat_limit: int
    finish_action: TimerFinishAction
    notification_type: NotificationType
    restart_policy: RestartPolicy
    recurrent_notification_interval: int
    recurrent_notification_time: float
    notification_sound: str
