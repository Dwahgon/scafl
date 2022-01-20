from gi.repository import Gtk, WebKit2  # type: ignore


class SteamLoginWebview(Gtk.Dialog):
    _WEBVIEW_WIDTH = 390
    _WEBVIEW_HEIGHT = 500
    _LOGIN_URI = "https://steamcommunity.com/login/home/?goto=my/profile"
    _END_URI = "https://steamcommunity.com/id"

    def __init__(self, parent, cookie_storage_path) -> None:
        super().__init__(transient_for=parent, title="Steam Login")
        self.steam_cookies = {}
        self.set_border_width(0)
        self.set_default_size(
            SteamLoginWebview._WEBVIEW_WIDTH, SteamLoginWebview._WEBVIEW_HEIGHT
        )

        self.web_context = WebKit2.WebContext.new()
        self.cookie_manager = self.web_context.get_cookie_manager()
        WebKit2.CookieManager.set_persistent_storage(
            self.cookie_manager,
            cookie_storage_path,
            WebKit2.CookiePersistentStorage.TEXT,
        )

        self.web_view = WebKit2.WebView.new_with_context(self.web_context)
        self.web_view.load_uri(SteamLoginWebview._LOGIN_URI)
        self.web_view.connect("load-changed", self._on_web_view_load_changed)

        self.vbox.pack_start(self.web_view, True, True, 0)

    def _on_web_view_load_changed(self, web_view, load_event):
        uri = web_view.get_uri()
        if load_event == WebKit2.LoadEvent.COMMITTED and uri.startswith(self._END_URI):
            self.cookie_manager.get_cookies(
                self._END_URI, None, self._get_cookies_callback
            )

    def _get_cookies_callback(self, source, result, *userdata):
        cookies_result: list = self.cookie_manager.get_cookies_finish(result)
        for cookie in cookies_result:
            self.steam_cookies[cookie.name] = cookie.value
        self.destroy()
