import os
import sys
import platform
import settings
from ctypes import CDLL


def load_steam_api():
    if sys.platform.startswith("linux"):
        if platform.architecture()[0].startswith("32bit"):
            return CDLL(settings.STEAMAPI_PATH)
        elif platform.architecture()[0].startswith("64bit"):
            return CDLL(settings.STEAMAPI64_PATH)

        print("Architecture not supported")
        sys.exit()

    print("OS not supported")
    sys.exit()


def main():
    os.environ["SteamAppId"] = sys.argv[1]
    try:
        steam_api = load_steam_api()
        steam_api.SteamAPI_Init()
    except:
        print("Error")
        sys.exit()


if __name__ == "__main__":
    main()
