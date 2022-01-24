from gi.repository import Gio, Gtk  # type: ignore

from scafl.gui.components.badge_box import BadgeBox
from scafl import utils, settings


class ScaflWindow(Gtk.ApplicationWindow):
    DEFAULT_WIDTH = 800
    DEFAULT_HEIGHT = 600
    SORT_METHODS = ["name", "drop_count"]

    def __init__(self, *args, **kwargs):
        super().__init__(
            default_width=self.DEFAULT_WIDTH,
            default_height=self.DEFAULT_HEIGHT,
            name="scafl",
            window_position=Gtk.WindowPosition.CENTER,
            *args,
            **kwargs,
        )

        self._badges = []
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
        # headerbar.pack_end(hamburger_button)

        headerbar.pack_start(refresh_button)

    def _create_sort_button(self):
        sort_popover = Gtk.Popover()
        sort_popover_vbox = Gtk.VBox(margin=4)
        self._sort_ascending_check = Gtk.CheckButton(label="Sort ascending")
        self._sort_ascending_check.set_active(True)
        sort_popover_vbox.pack_start(self._sort_ascending_check, False, True, 4)
        for method in self.SORT_METHODS:
            button = Gtk.ModelButton(label=utils.format_snake_case(method))
            button.connect("clicked", self._on_sort_method_button_clicked, method)
            sort_popover_vbox.pack_start(button, False, True, 0)
        sort_popover_vbox.show_all()
        sort_popover.add(sort_popover_vbox)
        sort_popover.set_position(Gtk.PositionType.BOTTOM)
        sorting_dropdown_button = Gtk.MenuButton(popover=sort_popover)
        return sorting_dropdown_button

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
        badges_screen_vbox = Gtk.VBox()

        options_vbox = Gtk.VBox(margin=6)
        first_options_row = Gtk.HBox()
        sort_hbox = Gtk.HBox()
        sort_hbox.pack_start(Gtk.Label(label="Sort games: "), False, False, 0)
        sort_hbox.pack_start(self._create_sort_button(), False, False, 0)
        self._hide_blacklisted = Gtk.CheckButton(label="Hide blacklisted badges")
        self._hide_blacklisted.set_active(
            bool(settings.read_conf("hide_blacklisted", default=False))
        )
        self._hide_blacklisted.connect("toggled", self._on_hide_blacklisted_toggled)

        scroll_window = Gtk.ScrolledWindow()
        self.badges_screen_viewport = Gtk.VBox()
        scroll_window.add_with_viewport(self.badges_screen_viewport)

        first_options_row.pack_start(sort_hbox, False, False, 0)
        first_options_row.pack_end(self._hide_blacklisted, False, False, 0)
        options_vbox.pack_start(first_options_row, False, False, 0)
        badges_screen_vbox.pack_start(options_vbox, False, False, 0)
        badges_screen_vbox.pack_start(
            Gtk.Separator(margin_start=6, margin_end=6), False, False, 0
        )
        badges_screen_vbox.pack_start(scroll_window, True, True, 0)

        return badges_screen_vbox

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
            if (
                not self._hide_blacklisted.get_active()
                or not badge["id"] in settings.blacklist
            ):
                badgebox = BadgeBox(badge)
                badgebox.blacklist_checkbox.connect(
                    "toggled", self._on_set_blacklist_toggle, badge["id"]
                )
                self.badges_screen_viewport.pack_start(badgebox, False, False, 0)
                badgebox.show_all()
        self._badges = badges

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

    def show_steam_not_running_dialog(self):
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.WARNING,
            buttons=Gtk.ButtonsType.OK,
            text="Steam is not running",
        )
        dialog.format_secondary_text(
            "ScafL is unable to idle Steam games while Steam is not running. Please start Steam, then try again."
        )
        dialog.run()
        dialog.destroy()

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

    def _on_sort_method_button_clicked(self, _, *data):
        self.get_application().sort_games(
            data[0], self._sort_ascending_check.get_active()
        )

    def _on_hide_blacklisted_toggled(self, widget):
        settings.write_conf("hide_blacklisted", widget.get_active())
        self.set_badge_list(self._badges)

    def _on_set_blacklist_toggle(self, widget, game_id):
        self.get_application().set_game_blacklisted(game_id, widget.get_active())
        self.set_badge_list(self._badges)
