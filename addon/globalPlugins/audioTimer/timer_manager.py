import threading
import time

from .config import Config, TimerSchema
from .enums import TimerState
from .timer import Timer


def _with_lock(func):
    def wrapper(self, *args, **kwargs):
        with self._lock:
            return func(self, *args, **kwargs)

    return wrapper


class TimerManager:
    TIMER_NAME_TEMPLATE = "Timer {n}"

    def __init__(self, config: Config):
        self._config = config
        self.timers = [Timer(config) for config in config.timers]
        self._run_thread = None
        self._event = threading.Event()
        self._lock = threading.Lock()
        self._terminate = False

    def start(self):
        if self._run_thread is not None:
            raise RuntimeError("Timer manager is already running")
        self._terminate = False
        self._run_thread = threading.Thread(target=self._run)
        self._run_thread.start()

    def stop(self):
        if self._run_thread is None:
            raise RuntimeError("Timer manager is not running")
        self._terminate = True
        self._event.set()
        self._run_thread.join()
        self._run_thread = None

    @property
    def enabled_timers(self):
        return [t for t in self.timers if t.enabled]

    def _run(self):
        delay = 0
        while True:
            if self._event.wait(delay):
                self._event.clear()
            if self._terminate:
                return
            delay = self._update()

    @_with_lock
    def _update(self) -> int | None:
        next_timer = None
        next_timer_action_timestamp = None
        for timer in self.enabled_timers:
            if (
                next_timer is None
                or timer.next_action_time < next_timer_action_timestamp
            ):
                next_timer = timer
                next_timer_action_timestamp = next_timer.next_action_time
        if next_timer is None:
            return
        timestamp = time.time()
        delay = next_timer_action_timestamp - timestamp
        if delay is None:
            return
        if delay > 0:
            delay = min(delay, 30)
            return delay
        next_timer.do_next_action()
        if next_timer.should_be_removed:
            self.timers.remove(next_timer)
            self._config.remove_timer(next_timer.config["id"])
        self._config.save()
        return 0

    @_with_lock
    def add_timer(self, timer: TimerSchema):
        timer = timer | {
            "state": TimerState.ACTIVE.value,
            "finish_time": 0,
            "repeat_count": 0,
            "recurrent_notification_time": 0,
        }
        self._config.add_timer(timer)
        new_timer = Timer(timer)
        new_timer.reset()
        self.timers.append(new_timer)
        self._config.save()
        self.trigger_update()

    @_with_lock
    def remove_timer(self, timer_id: int):
        removed = False
        for i, timer in enumerate(self.timers):
            if timer.config["id"] == timer_id:
                del self.timers[i]
                removed = True
                break
        if not removed:
            raise ValueError(f"Timer with id {timer_id} not found")
        self._config.remove_timer(timer_id)
        self._config.save()
        self.trigger_update()

    def get_timer(self, timer_id: int) -> Timer | None:
        for timer in self.timers:
            if timer.config["id"] == timer_id:
                return timer

    def trigger_update(self):
        self._event.set()

    def generate_timer_name(self):
        names = set(t.config["name"] for t in self.timers)
        n = 1
        while True:
            name = self.TIMER_NAME_TEMPLATE.format(n=n)
            if name not in names:
                return name
            n += 1
