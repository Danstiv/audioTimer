import os
import threading
import time
import winsound
from datetime import datetime

import addonHandler
import globalPluginHandler
import gui
import ui
from scriptHandler import script

from . import dialog

addonHandler.initTranslation()
path_to_sound=os.path.join(os.path.dirname(dialog.__file__), 'sound.wav')


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    scriptCategory = 'Audio timer'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.activation_time = None
        self.timer_amount = 0
        self.last_settings = (0, 0, 0)
        dialog.Dialog.callback=self.set_settings
        self.thread_termination_event = threading.Event()
        self.thread = threading.Thread(target=self.timer)
        self.thread.start()

    @script(
        gesture = 'kb:nvda+alt+t',
        description = _('Configure / disable a timer'),
    )
    def script_set_timer(self, gesture):
        if self.activation_time is None:
            gui.mainFrame._popupSettingsDialog(dialog.Dialog, self.last_settings)
            return
        self.activation_time = None
        ui.message(_('Timer off.'))

    def time_from_seconds(self, seconds):
        days=int(seconds//86400)
        hours=int(seconds//3600%24)
        minutes=int(seconds//60%60)
        seconds=round(seconds%60, 2)
        time_list=[]
        if days:
            time_list.append(_('{days} days').format(days=days))
        if hours:
            time_list.append(_('{hours} hours').format(hours=hours))
        if minutes:
            time_list.append(_('{minutes} minutes').format(minutes=minutes))
        if seconds:
            if len(time_list):
                seconds=int(seconds)
            if seconds:
                time_list.append(_('{seconds} seconds').format(seconds=seconds))
        if len(time_list):
            result=', '.join(time_list[:-1])+(_(' and ') if len(time_list)>1 else '')+time_list[-1]
        else:
            result=_('0 seconds')
        return result+'.'

    @script(
        gesture = 'kb:nvda+alt+r',
        description = _('Get information about the timer'),
    )
    def script_check_timer(self, gesture):
        if self.activation_time is None:
            ui.message(_('Timer not started.'))
            return
        result = self.time_from_seconds(self.activation_time-time.time())
        ui.message(result)

    @script(
        gesture = 'kb:nvda+control+f12',
        description = _('Get the current second in a minute'),
    )
    def script_current_second(self, gesture):
        ui.message(str(datetime.now().second))

    def set_settings(self, new_settings):
        self.last_settings = new_settings
        self.timer_amount = new_settings[0]*3600 + new_settings[1]*60 + new_settings[2]
        self.activation_time = time.time() + self.timer_amount if self.timer_amount > 0 else None

    def timer(self):
        while True:
            delay = 1
            if self.activation_time is not None:
                offset = self.activation_time-time.time()
                delay = offset if offset < 1 else delay
            if self.thread_termination_event.wait(delay):
                break
            if self.activation_time is not None and  self.activation_time <= time.time():
                self.activation_time += self.timer_amount
                self.play()

    def play(self):
        try:
            winsound.PlaySound(path_to_sound, winsound.SND_ASYNC)
        except RuntimeError:
            pass

    def terminate(self):
        self.thread_termination_event.set()
