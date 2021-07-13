import wx
from gui.guiHelper import BoxSizerHelper
import addonHandler
addonHandler.initTranslation()
class Dialog(wx.Dialog):
	def __init__(self, parent=None, value=60):
		wx.Dialog.__init__(self, parent, title=_(_('Timer setting')))
		self.Bind(wx.EVT_TEXT_ENTER, self.on_enter)
		self.main_sizer=BoxSizerHelper(self, wx.VERTICAL)
		self.hours_field=self.main_sizer.addLabeledControl(_('Hours'), wx.SpinCtrl, min=0, max=8760, initial=value[0], style=wx.SP_ARROW_KEYS|wx.TE_PROCESS_ENTER)
		self.minutes_field=self.main_sizer.addLabeledControl(_('Minutes'), wx.SpinCtrl, min=0, max=59, initial=value[1], style=wx.SP_ARROW_KEYS|wx.TE_PROCESS_ENTER)
		self.seconds_field=self.main_sizer.addLabeledControl(_('Seconds'), wx.SpinCtrl, min=0, max=59, initial=value[2], style=wx.SP_ARROW_KEYS|wx.TE_PROCESS_ENTER)
		self.btn_sizer=BoxSizerHelper(self, wx.HORIZONTAL)
		self.ok_btn=wx.Button(self, wx.ID_OK)
		self.btn_sizer.addItem(self.ok_btn)
		self.Bind(wx.EVT_BUTTON, self.on_ok, self.ok_btn)
		self.cancel_btn=wx.Button(self, wx.ID_CANCEL)
		self.btn_sizer.addItem(self.cancel_btn)
		self.main_sizer.addItem(self.btn_sizer)
		self.SetSizer(self.main_sizer.sizer)
		self.Bind(wx.EVT_SHOW, self.on_show)
	def on_show(self, event):
		self.hours_field.SetSelection(0, -1)
		self.minutes_field.SetSelection(0, -1)
		self.seconds_field.SetSelection(0, -1)
		event.Skip()
	def on_enter(self, event):
		self.set()
		self.Close()
	def on_ok(self, event):
		self.set()
		event.Skip()
	def set(self):
		self.callback((self.hours_field.GetValue(), self.minutes_field.GetValue(), self.seconds_field.GetValue()))
