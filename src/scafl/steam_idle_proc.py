import os
import sys
from scafl import utils


def main():
    os.environ["SteamAppId"] = sys.argv[1]
    try:
        steam_api = utils.load_steam_api()
        steam_api.SteamAPI_Init()
    except OSError as err:
        print(f"OS error: {err}")
        sys.exit()


if __name__ == "__main__":
    main()
