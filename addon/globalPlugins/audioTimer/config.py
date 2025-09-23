from pathlib import Path

from configobj import ConfigObj
from configobj.validate import Validator

from .config_spec import CONFIG_SPEC, TimerSchema


class Config:
    def __init__(self, config_path: Path):
        self._config_path = config_path
        validator = Validator()
        self._config = ConfigObj(
            self._config_path, configspec=CONFIG_SPEC, encoding="utf-8"
        )
        self._config.validate(validator)
        import builtins

        builtins.debug = self

    def save(self):
        with self._config_path.open("wb") as f:
            self._config.write(f)

    @property
    def timers(self):
        return [v for k, v in self._config["timers"].items()]

    def add_timer(self, timer: TimerSchema):
        if timer["id"] is None:
            timer["id"] = self._config["next_timer_id"]
            self._config["next_timer_id"] += 1
        self._config["timers"][str(timer["id"])] = timer

    def remove_timer(self, timer_id: int):
        del self._config["timers"][str(timer_id)]
