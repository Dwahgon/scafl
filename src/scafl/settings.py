import os
from os.path import dirname, abspath
from scafl import __version__
from scafl.blacklist import Blacklist
from configparser import ConfigParser, ParsingError, NoOptionError, NoSectionError

from gi.repository import GLib, Gtk  # type: ignore

APP_NAME = "ScafL"
VERSION = __version__
AUTHORS = ["Kawan Weege (Dragon Of War)"]
PROGRAM_DESCRIPTION = "A Steam game idler for trading card drops"
LICENSE_TYPE = Gtk.License.MIT_X11

SCAFL_DIR = dirname(abspath(__file__))

DATA_DIR = os.path.join(GLib.get_user_data_dir(), "scafl")
COOKIES_PATH = os.path.join(DATA_DIR, "cookies")

CONFIG_DIR = os.path.join(GLib.get_user_config_dir(), "scafl")
BLACKLIST_FILE = os.path.join(CONFIG_DIR, "blacklist.conf")
CONFIG_FILE = os.path.join(CONFIG_DIR, "scafl.conf")

STEAM_IDLE_PROC_PATH = os.path.join(SCAFL_DIR, "steam_idle_proc.py")
LIB_DIR = os.path.join(SCAFL_DIR, "lib")
LIB64_DIR = os.path.join(SCAFL_DIR, "lib64")
STEAMAPI_PATH = os.path.join(LIB_DIR, "libsteam_api32.so")
STEAMAPI64_PATH = os.path.join(LIB64_DIR, "libsteam_api64.so")

GITHUB_URL = "https://github.com/DragonOfWar/scafl"
BUG_REPORT_URL = "https://github.com/DragonOfWar/scafl/issues"
DONATION_URL = "https://www.paypal.com/donate/?hosted_button_id=TSARHWQFKSEBA"

blacklist = Blacklist(BLACKLIST_FILE)
_config_parser = ConfigParser()
if os.path.exists(CONFIG_FILE):
    try:
        _config_parser.read(CONFIG_FILE)
    except ParsingError as err:
        print(err)


def read_conf(option, section="scafl", default=None):
    try:
        return _config_parser.get(section, option, fallback=default)
    except (NoOptionError, NoSectionError) as err:
        return default


def write_conf(option, value, section="scafl"):
    if not _config_parser.has_section(section):
        _config_parser.add_section(section)
    _config_parser.set(section, option, str(value))

    with open(CONFIG_FILE, "w") as file:
        _config_parser.write(file)
