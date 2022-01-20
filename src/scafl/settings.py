import os

from gi.repository import GLib  # type: ignore

DATA_DIR = os.path.join(GLib.get_user_data_dir(), "scafl")
COOKIES_PATH = os.path.join(DATA_DIR, "cookies")
