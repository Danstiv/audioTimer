import time
from pathlib import Path

from .enums import NotificationType, RestartPolicy, TimerFinishAction, TimerState
from .schema import TimerSchema
from .utils import play_sound

DEFAULT_NOTIFICATION_SOUND = Path(__file__).parent / "sound.wav"


class Timer:
    def __init__(self, config: TimerSchema):
        self.config = config

    @property
    def enabled(self):
        return self.config.state is not TimerState.DISABLED

    @property
    def repeat_limit_reached(self):
        return (
            self.config.repeat_limit > 0
            and self.config.repeat_count == self.config.repeat_limit
        )

    @property
    def should_be_removed(self):
        return (
            self.config.finish_action is TimerFinishAction.REMOVE
            and not self.enabled
            and self.repeat_limit_reached
        )

    @property
    def recurrent_notification_active(self):
        return self.config.recurrent_notification_time > 0

    def check_enabled(self):
        if not self.enabled:
            raise ValueError("Timer is disabled")

    @property
    def next_action_time(self) -> int:
        self.check_enabled()
        if self.config.state is TimerState.PENDING:
            return self.config.recurrent_notification_time
        elif self.config.state is TimerState.ACTIVE:
            if not self.recurrent_notification_active:
                return self.config.finish_time
            return min(self.config.finish_time, self.config.recurrent_notification_time)

    def do_next_action(self):
        self.check_enabled()
        timestamp = time.time()
        self._finish(timestamp)
        self._notify_recurrent(timestamp)

    def reset(self):
        timestamp = time.time()
        self.config.finish_time = timestamp + self.config.interval
        self.config.repeat_count = 0
        self.config.recurrent_notification_time = 0
        self.config.state = TimerState.ACTIVE

    def disable(self):
        if self.config.state is TimerState.DISABLED:
            raise ValueError("Timer is already disabled")
        self.config.state = TimerState.DISABLED

    def enable(self):
        if self.enabled:
            raise ValueError("Timer is already enabled")
        self.reset()

    def _finish(self, timestamp):
        if not (
            self.config.state is TimerState.ACTIVE
            and timestamp >= self.config.finish_time
        ):
            return
        self.config.repeat_count += 1
        if self.repeat_limit_reached:
            new_state = TimerState.DISABLED
        else:
            if self.config.restart_policy is RestartPolicy.IMMEDIATE:
                new_state = TimerState.ACTIVE
                self.config.finish_time = timestamp + self.config.interval
            elif self.config.restart_policy is RestartPolicy.ON_USER_ACTION:
                new_state = TimerState.PENDING
            else:
                raise ValueError("Unknown restart policy")
        if self.config.notification_type is NotificationType.ONETIME:
            self._notify_once(timestamp)
        elif self.config.notification_type is NotificationType.RECURRENT:
            # Recurrent notification could be already active,
            # but we should notify about timer round explicitly.
            self._notify_once(timestamp)
            if new_state is TimerState.DISABLED:
                new_state = TimerState.PENDING
            if not self.recurrent_notification_active:
                self.config.recurrent_notification_time = (
                    timestamp + self.config.recurrent_notification_interval
                )
        else:
            raise ValueError("Unknown notification type")
        self.config.state = new_state

    @property
    def _notification_sound_path(self) -> Path:
        if not self.config.notification_sound:
            return DEFAULT_NOTIFICATION_SOUND
        notification_sound = Path(self.config.notification_sound)
        if not notification_sound.is_file():
            notification_sound = DEFAULT_NOTIFICATION_SOUND
        return notification_sound

    def _notify(self):
        play_sound(self._notification_sound_path)

    def _notify_once(self, timestamp):
        self._notify()

    def _notify_recurrent(self, timestamp):
        if not (
            self.config.notification_type is NotificationType.RECURRENT
            and timestamp >= self.config.recurrent_notification_time
        ):
            return
        self._notify()
        self.config.recurrent_notification_time = (
            timestamp + self.config.recurrent_notification_interval
        )
