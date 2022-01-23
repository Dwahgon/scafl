import os
from os.path import dirname, abspath
from scafl.blacklist import Blacklist

from gi.repository import GLib  # type: ignore

SCAFL_DIR = dirname(abspath(__file__))

DATA_DIR = os.path.join(GLib.get_user_data_dir(), "scafl")
COOKIES_PATH = os.path.join(DATA_DIR, "cookies")

CONFIG_DIR = os.path.join(GLib.get_user_config_dir(), "scafl")
BLACKLIST_FILE = os.path.join(CONFIG_DIR, "blacklist.conf")

STEAM_IDLE_PROC_PATH = os.path.join(SCAFL_DIR, "steam_idle_proc.py")
LIB_DIR = os.path.join(SCAFL_DIR, "lib")
LIB64_DIR = os.path.join(SCAFL_DIR, "lib64")
STEAMAPI_PATH = os.path.join(LIB_DIR, "libsteam_api32.so")
STEAMAPI64_PATH = os.path.join(LIB64_DIR, "libsteam_api64.so")

blacklist = Blacklist(BLACKLIST_FILE)
