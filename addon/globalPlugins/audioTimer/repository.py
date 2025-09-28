import dataclasses
import json
from copy import deepcopy
from pathlib import Path

from .schema import TimerSchema

INITIAL_CONFIG = {"schema_version": 1, "next_timer_id": 1, "timers": []}


class TimerRepository:
    def __init__(self, config_path: Path):
        self._config_path = config_path
        if self._config_path.is_file():
            with self._config_path.open("rb") as f:
                self._config = json.load(f)
        else:
            self._config = deepcopy(INITIAL_CONFIG)

    def save(self):
        data = json.dumps(self._config, indent=2, ensure_ascii=False).encode()
        self._config_path.write_bytes(data)

    def get_timers(self):
        return [TimerSchema(**t) for t in self._config["timers"]]

    def add_timer(self, timer: TimerSchema):
        if timer.id is None:
            timer.id = self._config["next_timer_id"]
            self._config["next_timer_id"] += 1
        self._config["timers"].append(dataclasses.asdict(timer))

    def remove_timer(self, timer_id: int):
        for i, timer in enumerate(self._config["timers"]):
            if timer["id"] == timer_id:
                del self._config["timers"][i]
                break

    def update_timer(self, timer: TimerSchema):
        for i, t in enumerate(self._config["timers"]):
            if t["id"] == timer.id:
                self._config["timers"][i] = dataclasses.asdict(timer)
                return
        raise ValueError(f"Timer with id {timer.id} not found")
