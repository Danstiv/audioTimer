import wx

from ..timer import Timer
from ..timer_manager import TimerManager


class TimerMenu:
    def __init__(self, timer_manager: TimerManager, timer: Timer):
        self.timer_manager = timer_manager
        self.timer = timer
        self.menu = wx.Menu()
        if self.timer.enabled:
            if self.timer.waiting_for_user_action:
                self.start_next_round_item = self._add_menu_item(
                    _("Start next round"), self.on_start_next_round
                )
            if self.timer.recurrent_notification_active:
                self.dismiss_recurrent_notification_item = self._add_menu_item(
                    _("Dismiss recurrent notification"),
                    self.on_dismiss_recurrent_notification,
                )
            self.disable_item = self._add_menu_item(_("Disable"), self.on_disable)
        else:
            self.enable_item = self._add_menu_item(_("Enable"), self.on_enable)
        self.remove_item = self._add_menu_item(_("Remove"), self.on_remove)

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

    def on_dismiss_recurrent_notification(self, event):
        if self.timer.recurrent_notification_active:
            self.timer.dismiss_recurrent_notification()
            self._update_timer()

    def on_start_next_round(self, event):
        if self.timer.waiting_for_user_action:
            self.timer.start_next_round()
            self._update_timer()

    def popup_timer_menu(self, parent, position):
        parent.PopupMenu(self.menu, pos=position)
