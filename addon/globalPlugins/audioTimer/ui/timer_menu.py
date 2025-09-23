import wx

from ..timer import Timer
from ..timer_manager import TimerManager


class TimerMenu:
    def __init__(self, timer_manager: TimerManager, timer: Timer):
        self.timer_manager = timer_manager
        self.timer = timer
        self.menu = wx.Menu()
        self.remove_item = wx.MenuItem(self.menu, wx.ID_ANY, _("Remove"))
        self.menu.Bind(wx.EVT_MENU, self.on_remove, self.remove_item)
        self.menu.Append(self.remove_item)
        self.disable_item = wx.MenuItem(self.menu, wx.ID_ANY, _("Disable"))
        self.menu.Bind(wx.EVT_MENU, self.on_disable, self.disable_item)
        self.menu.Append(self.disable_item)
        self.enable_item = wx.MenuItem(self.menu, wx.ID_ANY, _("Enable"))
        self.menu.Bind(wx.EVT_MENU, self.on_enable, self.enable_item)
        self.menu.Append(self.enable_item)
        (self.enable_item if self.timer.enabled else self.disable_item).Enable(False)

    def on_remove(self, event):
        self.timer_manager.remove_timer(self.timer.config.id)

    def on_disable(self, event):
        if self.timer.enabled:
            self.timer.disable()

    def on_enable(self, event):
        if not self.timer.enabled:
            self.timer.enable()

    def popup_timer_menu(self, parent, position):
        parent.PopupMenu(self.menu, pos=position)
