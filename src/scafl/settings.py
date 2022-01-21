import os
from os.path import dirname, abspath

from gi.repository import GLib  # type: ignore

PROJECT_DIR = dirname(dirname(dirname(abspath(__file__))))
SRC_DIR = os.path.join(PROJECT_DIR, "src")
SCAFL_DIR = os.path.join(SRC_DIR, "scafl")

DATA_DIR = os.path.join(GLib.get_user_data_dir(), "scafl")
COOKIES_PATH = os.path.join(DATA_DIR, "cookies")

STEAM_IDLE_PROC_PATH = os.path.join(SCAFL_DIR, "steam_idle_proc.py")
