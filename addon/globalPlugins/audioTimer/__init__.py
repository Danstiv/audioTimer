import globalPluginHandler
import addonHandler
import ui
import gui
from . import dialog
from threading import Thread
import time
import winsound
from datetime import datetime
import os.path
from scriptHandler import script
addonHandler.initTranslation()
path_to_sound=os.path.join(os.path.dirname(dialog.__file__), 'sound.wav')
class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self, *args, **kwargs):
		globalPluginHandler.GlobalPlugin.__init__(self, *args, **kwargs)
		self.time=0
		self.offset=0
		self.last_value=(0, 0, 0)
		dialog.Dialog.callback=self.set_time
		self.thread=Thread(target=self.timer)
		self.status=1
		self.thread.start()
	@script(
		gesture = 'kb:nvda+alt+t',
		description = _('Configure / disable a timer'),
	)
	def script_set_timer(self, gesture):
		if self.offset:
			ui.message(_('Timer off.'))
			self.offset=0
			return
		gui.mainFrame._popupSettingsDialog(dialog.Dialog, self.last_value)
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
		description = _('Get information about timer'),
	)
	def script_check_timer(self, gesture):
		if not self.offset:
			ui.message(_('Timer not started.'))
			return
		result=self.time_from_seconds(self.time-time.time())
		ui.message(result)
	@script(
		gesture = 'kb:nvda+control+f12',
		description = _('Get the current second in a minute'),
	)
	def script_current_second(self, gesture):
		ui.message(str(datetime.now().second))
	def set_time(self, new_value):
		self.last_value=new_value
		new_time=new_value[0]*3600+new_value[1]*60+new_value[2]
		self.time=time.time()+new_time
		self.offset=new_time
	def timer(self):
		while True:
			if not self.status:
				break
			if self.offset==0 or time.time()<self.time:
				time.sleep(1)
			else:
				self.play()
				self.time=time.time()+self.offset
	def play(self):
		try:
			winsound.PlaySound(path_to_sound, winsound.SND_ASYNC)
		except RuntimeError:
			pass
	def terminate(self):
		self.status=0
