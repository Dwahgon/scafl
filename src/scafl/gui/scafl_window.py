from gi.repository import Gio, Gtk  # type: ignore

from scafl.gui.components.badge_box import BadgeBox


class ScaflWindow(Gtk.ApplicationWindow):
    DEFAULT_WIDTH = 800
    DEFAULT_HEIGHT = 600

    def __init__(self, *args, **kwargs):
        super().__init__(
            default_width=self.DEFAULT_WIDTH,
            default_height=self.DEFAULT_HEIGHT,
            name="scafl",
            window_position=Gtk.WindowPosition.CENTER,
            *args,
            **kwargs,
        )

        self._init_widgets()
        self.set_not_idling()

    def _init_widgets(self):
        self._create_header_bar()

        main_box = Gtk.VBox()
        self.add(main_box)

        self.badges_screen = self._create_badges_screen()
        self.loading_screen = self._create_loading_screen()
        self.connect_steam_screen = self._create_connect_steam_screen()

        separater = Gtk.Separator()

        self.idle_button = Gtk.Button.new_with_label("")
        self.idle_button.props.margin = 4
        self.idle_button.connect("clicked", self._on_idle_clicked)

        main_box.pack_start(self.badges_screen, True, True, 0)
        main_box.pack_start(self.loading_screen, True, False, 0)
        main_box.pack_start(self.connect_steam_screen, True, False, 0)
        main_box.pack_start(separater, False, False, 6)
        main_box.pack_start(self._create_status_section(), False, False, 0)
        main_box.pack_start(self.idle_button, False, False, 6)

    def _create_header_bar(self):
        headerbar = Gtk.HeaderBar()
        headerbar.set_show_close_button(True)
        headerbar.props.title = "ScafL"
        self.set_titlebar(headerbar)

        refresh_button = Gtk.Button()
        refresh_icon = Gio.ThemedIcon(name="view-refresh")
        refresh_button.connect("clicked", self._on_refresh_clicked)
        refresh_image = Gtk.Image.new_from_gicon(refresh_icon, Gtk.IconSize.BUTTON)
        refresh_button.add(refresh_image)

        # TODO: Create menu button
        # hamburger_button = Gtk.Button()
        # hamburger_icon = Gio.ThemedIcon(name="open-menu-symbolic")
        # hamburger_image = Gtk.Image.new_from_gicon(hamburger_icon, Gtk.IconSize.BUTTON)
        # hamburger_button.add(hamburger_image)

        headerbar.pack_start(refresh_button)
        # headerbar.pack_end(hamburger_button)

    def _create_status_section(self):
        status_hbox = Gtk.HBox(margin=4)

        self.idle_status_label = Gtk.Label()
        self.idle_status_label.props.xalign = 0

        self.status_spinner = Gtk.Spinner()
        self.status_spinner.stop()

        status_hbox.pack_start(self.idle_status_label, True, True, 0)
        status_hbox.pack_start(self.status_spinner, False, False, 0)

        return status_hbox

    def _create_loading_screen(self):
        loading_box = Gtk.VBox()
        loading_box.set_vexpand(True)

        loading_spinner = Gtk.Spinner()
        loading_spinner.start()

        loading_text = Gtk.Label()
        loading_text.set_text("Loading your Steam badges.")

        loading_box.pack_start(loading_spinner, True, False, 0)
        loading_box.pack_start(loading_text, True, False, 0)

        return loading_box

    def _create_connect_steam_screen(self):
        connect_steam_box = Gtk.HBox()
        vbox = Gtk.VBox()

        connect_steam_label = Gtk.Label()
        connect_steam_label.set_text("You are currently not connected to Steam.")

        connect_steam_button = Gtk.Button.new_with_label("Connect to Steam")
        connect_steam_button.connect("clicked", self._on_connect_clicked)

        vbox.pack_start(connect_steam_label, False, False, 8)
        vbox.pack_start(connect_steam_button, False, False, 8)
        connect_steam_box.pack_start(vbox, True, False, 0)
        return connect_steam_box

    def _create_badges_screen(self):
        scroll_window = Gtk.ScrolledWindow()
        self.badges_screen_viewport = Gtk.VBox()
        scroll_window.add_with_viewport(self.badges_screen_viewport)
        return scroll_window

    def set_idle_button_active(self, active=True):
        self.idle_button.set_sensitive(active)

    def set_idling(self, game):
        self._update_idle_status_label(f'{game["name"]} ({game["id"]})')
        self._set_idle_button_as_idling()
        self.status_spinner.start()

    def set_badge_list(self, badges):
        for badge_widget in self.badges_screen_viewport.get_children():
            badge_widget.destroy()
        for badge in badges:
            badgebox = BadgeBox(badge)
            self.badges_screen_viewport.pack_start(badgebox, False, False, 0)

    def set_not_idling(self):
        self._update_idle_status_label()
        self._set_idle_button_as_idling(False)
        self.status_spinner.stop()

    def show_loading_screen(self):
        self.loading_screen.show()
        self.badges_screen.hide()
        self.connect_steam_screen.hide()

    def show_badges_screen(self):
        self.badges_screen.show_all()
        self.loading_screen.hide()
        self.connect_steam_screen.hide()

    def show_connect_steam_screen(self):
        self.connect_steam_screen.show()
        self.badges_screen.hide()
        self.loading_screen.hide()

    def _update_idle_status_label(self, status="Nothing"):
        self.idle_status_label.set_markup(f"<big>Currently idling: {status}</big>")

    def _set_idle_button_as_idling(self, is_idling=True):
        self.idle_button.set_label("Stop Idling" if is_idling else "Idle")

    def _on_connect_clicked(self, _):
        self.get_application().show_login_webview()

    def _on_refresh_clicked(self, _):
        self.get_application().load_badges()

    def _on_idle_clicked(self, _):
        self.get_application().toggle_idling()
