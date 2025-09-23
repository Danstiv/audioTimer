from pathlib import Path

import addonHandler
import globalPluginHandler
import NVDAState
from scriptHandler import script

from .repository import TimerRepository
from .timer_manager import TimerManager
from .ui.main_dialog import MainDialog

addonHandler.initTranslation()

CONFIG_PATH = Path(NVDAState.WritePaths.configDir) / "audioTimer.json"


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    scriptCategory = "Audio Timer"

    def __init__(self):
        super().__init__()
        self.config = TimerRepository(CONFIG_PATH)
        self.timer_manager = TimerManager(self.config)
        self.timer_manager.start()

    def terminate(self):
        self.timer_manager.stop()

    @script(description=_(""), gesture="kb:nvda+shift+a")
    def script_show_dialog(self, gesture):
        MainDialog.show_main_dialog(self.timer_manager)
