import wx

from ..timer import Timer
from ..timer_manager import TimerManager


class TimerMenu:
    def __init__(self, timer_manager: TimerManager, timer: Timer):
        self.timer_manager = timer_manager
        self.timer = timer
        self.menu = wx.Menu()
        self.remove_item = self._add_menu_item(_("Remove"), self.on_remove)
        if self.timer.enabled:
            self.disable_item = self._add_menu_item(_("Disable"), self.on_disable)
        else:
            self.enable_item = self._add_menu_item(_("Enable"), self.on_enable)

    def _add_menu_item(self, name, handler):
        item = wx.MenuItem(self.menu, wx.ID_ANY, name)
        self.menu.Bind(wx.EVT_MENU, handler, item)
        self.menu.Append(item)
        return item

    def _update_timer(self):
        self.timer_manager.update_timer(self.timer)

    def on_remove(self, event):
        self.timer_manager.remove_timer(self.timer.config.id)

    def on_disable(self, event):
        if self.timer.enabled:
            self.timer.disable()
            self._update_timer()

    def on_enable(self, event):
        if not self.timer.enabled:
            self.timer.enable()
            self._update_timer()

    def popup_timer_menu(self, parent, position):
        parent.PopupMenu(self.menu, pos=position)
