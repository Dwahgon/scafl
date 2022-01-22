import sys
import platform
from scafl import settings
from ctypes import CDLL


def load_steam_api():
    if sys.platform.startswith("linux"):
        if platform.architecture()[0].startswith("32bit"):
            return CDLL(settings.STEAMAPI_PATH)
        elif platform.architecture()[0].startswith("64bit"):
            return CDLL(settings.STEAMAPI64_PATH)

        raise OSError("Unsupported architecture")

    raise OSError("Unsupported operating system")


def format_snake_case(string):
    return " ".join([word.capitalize() for word in string.split("_")])
