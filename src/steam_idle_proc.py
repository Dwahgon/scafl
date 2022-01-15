import os
import sys
import platform
from ctypes import CDLL


def load_steam_api():
    if sys.platform.startswith("linux"):
        if platform.architecture()[0].startswith("32bit"):
            return CDLL("lib/libsteam_api32.so")
        elif platform.architecture()[0].startswith("64bit"):
            return CDLL("lib64/libsteam_api64.so")

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
