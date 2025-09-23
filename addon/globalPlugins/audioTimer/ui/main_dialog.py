import gui
import wx
from gui.guiHelper import BoxSizerHelper

from ..timer_manager import TimerManager
from .new_timer_dialog import NewTimerDialog
from .timer_menu import TimerMenu


class MainDialog(wx.Dialog):
    _dialog = None

    def __init__(self, timer_manager: TimerManager):
        super().__init__(parent=gui.mainFrame, title="Audio Timer", style=wx.CLOSE_BOX)
        self.timer_manager = timer_manager
        self.main_sizer = BoxSizerHelper(self, wx.VERTICAL)
        self.timer_list = self.main_sizer.addLabeledControl(
            _("Timers"),
            wx.ListCtrl,
            style=wx.LC_REPORT | wx.LC_NO_HEADER | wx.LC_SINGLE_SEL,
        )
        self.timer_list.AppendColumn("Timer")
        self.timer_list.Bind(wx.EVT_CONTEXT_MENU, self.on_context_menu)
        self.button_sizer = BoxSizerHelper(self, wx.HORIZONTAL)
        self.add_btn = self.button_sizer.addItem(wx.Button(self, label=_("Add")))
        self.add_btn.Bind(wx.EVT_BUTTON, self.on_add_btn)
        self.main_sizer.addItem(self.button_sizer)
        self.close_btn = self.button_sizer.addItem(
            wx.Button(self, id=wx.ID_CLOSE, label=_("Close"))
        )
        self.close_btn.Bind(wx.EVT_BUTTON, self.on_close_btn)
        self.main_sizer.sizer.Fit(self)
        self.SetSizer(self.main_sizer.sizer)
        self.SetEscapeId(wx.ID_CLOSE)
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.refresh_timer_list()

    @classmethod
    def show_main_dialog(cls, timer_manager):
        if cls._dialog is None:
            cls._dialog = MainDialog(timer_manager)
            cls._dialog.Show()
        gui.mainFrame.Raise()
        cls._dialog.SetFocus()

    @classmethod
    def _clear_main_dialog(cls):
        cls._dialog = None

    def on_close_btn(self, event):
        self.Close()

    def on_close(self, event):
        self._clear_main_dialog()
        self.Destroy()

    def refresh_timer_list(self):
        self.timer_list.DeleteAllItems()
        for timer in self.timer_manager.timers:
            index = self.timer_list.Append([timer.config["name"]])
            self.timer_list.SetItemData(index, timer.config["id"])
        if self.timer_list.GetItemCount() > 0:
            self.timer_list.Focus(0)
            self.timer_list.Select(0)

    def on_context_menu(self, event):
        first_selected_index = self.timer_list.GetFirstSelected()
        if first_selected_index < 0:
            return
        if event.GetPosition() == wx.DefaultPosition:
            # Applications key
            position = self.timer_list.GetItemRect(first_selected_index).GetBottomLeft()
        else:
            # Mouse right click
            position = wx.DefaultPosition
        timer_id = self.timer_list.GetItemData(first_selected_index)
        timer = self.timer_manager.get_timer(timer_id)
        menu = TimerMenu(self.timer_manager, timer)
        menu.popup_timer_menu(self.timer_list, position)

    def on_add_btn(self, event):
        new_timer_dialog = NewTimerDialog(self, self.timer_manager)
        new_timer_dialog.ShowModal()
