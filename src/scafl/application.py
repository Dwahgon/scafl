# fmt: off
import gi
gi.require_version("Gtk", "3.0")
gi.require_version("WebKit2", "4.0")
from gi.repository import Gtk, Gio, GLib # type: ignore
# fmt: on

from scafl import settings, startup, utils
from scafl.steam_user_badges import SteamUserBadges
from scafl.gui.steam_login_webview import SteamLoginWebview
from scafl.gui.scafl_window import ScaflWindow
from threading import Timer
import time
import os
import threading
import subprocess


class Application(Gtk.Application):
    IDLE_TIMEOUT = 5 * 60.0
    CYCLES_FOR_IDLE_RESTART = 3

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.steam_cookies = {}
        self.is_loading = True
        self.is_idling = False
        self.steam_user_badges = None
        self.steam_idle_proc = None
        self.badges_to_idle = []
        self._steam_api = None
        self._cycles_without_card_drops = 0
        self._idling_badge_id = 0
        self._badge_loading_thread = None
        self.window = None
        self._new_timer()

        try:
            self._steam_api = utils.load_steam_api()
        except OSError as err:
            print(f"OS Error: {err}")
            self.quit()
        # TODO: Add command line support

    def do_startup(self):
        Gtk.Application.do_startup(self)

        action = Gio.SimpleAction.new("quit")
        action.connect("activate", lambda *_: self.quit())
        self.add_action(action)

        startup.init_app()

    def do_activate(self):
        self._create_window()

    def show_login_webview(self):
        steam_login_webview = SteamLoginWebview(self.window, settings.COOKIES_PATH)
        steam_login_webview.connect("destroy", self._on_steam_login_webview_close)
        steam_login_webview.show_all()
        if self.window is not None:
            self.window.show_loading_screen()

    def _create_window(self):
        if self.window is not None:
            return

        if not self.window:
            self.window = ScaflWindow(application=self, title="Idle Master")

        self.window.present()
        self.window.show_all()
        if not self.steam_cookies:
            self.window.show_connect_steam_screen()
            self.window.set_idle_button_active(False)
        elif self.steam_user_badges is None:
            self.window.show_loading_screen()
        else:
            self.window.show_badges_screen()

    def toggle_idling(self):
        if not self.is_idling:
            self._start_idling()
        else:
            self._stop_idling()
            self.load_badges()

    def sort_games(self, sort_method, ascending=True):
        sort_func = lambda e: e["name"]
        if sort_method == "drop_count":
            sort_func = lambda e: e["drop_count"]
        elif sort_method != "name":
            # TODO: Throw exception here
            pass
        self.badges_to_idle.sort(reverse=not ascending, key=sort_func)

        if self.window is not None:
            self.window.set_badge_list(self.badges_to_idle)

    def _start_steam_idle_proc(self, game_id):
        if self.steam_idle_proc is not None:
            print("Steam idle process is already running. Terminating it...")
            self._stop_steam_idle_proc()

        self.steam_idle_proc = subprocess.Popen(
            ["python", settings.STEAM_IDLE_PROC_PATH, game_id]
        )

    def _stop_steam_idle_proc(self):
        if self.steam_idle_proc is not None:
            self.steam_idle_proc.terminate()
            self.steam_idle_proc = None

    def _start_idling(self):
        if (
            self.window is None
            or self.badges_to_idle is None
            or len(self.badges_to_idle) == 0
        ):
            return

        if (
            self._steam_api is not None
            and not self._steam_api.SteamAPI_IsSteamRunning()
            and self.window is not None
        ):
            self.window.show_steam_not_running_dialog()
            return

        self.idling_badge = self._get_next_badge_to_idle()
        if self.idling_badge is None:
            return

        self.is_idling = True
        self.window.set_idling(self.idling_badge)

        self._start_steam_idle_proc(self.idling_badge["id"])
        self._cycles_without_card_drops = 0

        self._idle_timer.start()

    def _stop_idling(self):
        if self.window is None:
            return
        self.is_idling = False
        self.idling_badge = None
        self.window.set_not_idling()
        self._stop_steam_idle_proc()
        self._idle_timer.cancel()
        self._new_timer()

    def _get_next_badge_to_idle(self):
        for badge in self.badges_to_idle:
            if badge["id"] not in settings.blacklist:
                return badge
        return None

    def _new_timer(self):
        self._idle_timer = Timer(self.IDLE_TIMEOUT, self._on_idle_timeout)

    def update_badge(self, badge):
        self.badges_to_idle[self.badges_to_idle.index(self.idling_badge)] = badge

    def _on_idle_timeout(self):
        if self.idling_badge is None or self.steam_user_badges is None:
            return

        if self._cycles_without_card_drops == self.CYCLES_FOR_IDLE_RESTART:
            print(
                f"We have made {self._cycles_without_card_drops} idling cycles and still haven't gotten a card drop. Restarting steam idle process"
            )
            self._stop_steam_idle_proc()
            time.sleep(2)
            self._start_steam_idle_proc(self.idling_badge["id"])
            print("Steam idle process restarted")
            self._cycles_without_card_drops = 0

        old_drop_count = self.idling_badge["drop_count"]
        self.idling_badge = self.steam_user_badges.get_badge_data(
            self.idling_badge["id"]
        )
        self.update_badge(self.idling_badge)
        if old_drop_count != self.idling_badge["drop_count"]:
            self._cycles_without_card_drops = 0

        if self.idling_badge["drop_count"] == 0:
            self._stop_steam_idle_proc()

            self.badges_to_idle.remove(self.idling_badge)
            if self.window is not None:
                self.window.set_badge_list(self.badges_to_idle)

            self._new_timer()
            self._start_idling()
            return

        if self.window is not None:
            self.window.set_badge_list(self.badges_to_idle)

        self._cycles_without_card_drops += 1
        self._new_timer()
        self._idle_timer.start()

    def _thread_load_badges_func(self):
        if self.steam_user_badges is None or self.window is None:
            return

        self.badges_to_idle = self.steam_user_badges.get_badges_with_remaining_drops()
        GLib.idle_add(self.window.set_badge_list, self.badges_to_idle)
        GLib.idle_add(self.window.show_badges_screen)
        GLib.idle_add(self.window.set_idle_button_active, len(self.badges_to_idle) > 0)
        self._badge_loading_thread = None

    def load_badges(self):
        if (
            self.steam_user_badges is None
            or self.window is None
            or self._badge_loading_thread is not None
        ):
            return

        self.window.show_loading_screen()
        self.window.set_idle_button_active(False)
        self._badge_loading_thread = threading.Thread(
            target=self._thread_load_badges_func
        )
        self._badge_loading_thread.start()

    def set_game_blacklisted(self, game_id, is_blacklisted):
        if is_blacklisted:
            settings.blacklist.add_game(game_id)
        else:
            settings.blacklist.remove_game(game_id)

    def _on_steam_login_webview_close(self, widget):
        if self.window is None:
            return

        self.steam_cookies = widget.steam_cookies
        if not self.steam_cookies:
            print("Error: no cookies")

        if "sessionid" not in self.steam_cookies:
            print("Error: sessionid is not set")
            self.window.show_connect_steam_screen()
            return

        if "steamLoginSecure" not in self.steam_cookies:
            print("Error: steamLoginSecure is not set")
            self.window.show_connect_steam_screen()
            return

        self.steam_user_badges = SteamUserBadges(self.steam_cookies)
        self.load_badges()

    @property
    def idling_badge(self):
        badge_search = [
            x for x in self.badges_to_idle if x["id"] == self.idling_badge_id
        ]
        return None if len(badge_search) == 0 else badge_search[0]

    @idling_badge.setter
    def idling_badge(self, value):
        self.idling_badge_id = "0" if value is None else value["id"]
