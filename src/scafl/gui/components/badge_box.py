# fmt: off
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, GdkPixbuf # type: ignore
# fmt: on
import urllib.request
from scafl import settings


class BadgeBox(Gtk.Frame):
    def __init__(self, game, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.game = game
        self.props.margin = 6
        self.props.margin_right = 14

        main_hbox = Gtk.Box()
        self.add(main_hbox)

        url = f'http://cdn.akamai.steamstatic.com/steam/apps/{game["id"]}/header_292x136.jpg'
        response = urllib.request.urlopen(url)
        input_stream = Gio.MemoryInputStream.new_from_data(response.read(), None)
        pixbuf = GdkPixbuf.Pixbuf.new_from_stream(input_stream, None)
        image = Gtk.Image(margin=4)
        image.set_from_pixbuf(pixbuf)
        main_hbox.pack_start(image, False, False, 0)

        vsep = Gtk.VSeparator()
        main_hbox.pack_start(vsep, False, False, 0)

        data_wrapper = Gtk.VBox(margin=6)
        data_wrapper.set_homogeneous(False)
        game_title_label = Gtk.Label()
        game_title_label.set_markup(f'<b><big>{game["name"]} ({game["id"]})</big></b>')
        game_title_label.props.xalign = 0
        drops_left = Gtk.Label()
        drops_left.set_text(f'{game["drop_count"]} cards left')
        drops_left.props.xalign = 0

        self.blacklist_checkbox = Gtk.CheckButton(label="Blacklist game")
        self.blacklist_checkbox.set_active(self.game["id"] in settings.blacklist)

        data_wrapper.pack_start(game_title_label, True, True, 0)
        data_wrapper.pack_start(drops_left, True, True, 0)
        data_wrapper.pack_start(self.blacklist_checkbox, True, True, 0)
        main_hbox.pack_start(data_wrapper, False, False, 0)
