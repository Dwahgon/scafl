import os


class Blacklist:
    def __init__(self, blacklist_file):
        self.blacklisted_games = set()
        self._blacklist_file = blacklist_file
        if os.path.exists(blacklist_file):
            with open(blacklist_file, "r") as file:
                self.blacklisted_games = set([x.strip() for x in file])

    def __contains__(self, item):
        return item in self.blacklisted_games

    def add_game(self, game_id):
        self.blacklisted_games.add(game_id)
        self._update_file()

    def remove_game(self, game_id):
        try:
            self.blacklisted_games.remove(game_id)
            self._update_file()
        except ValueError:
            pass

    def _update_file(self):
        with open(self._blacklist_file, "w") as file:
            for id in self.blacklisted_games:
                file.write(f"{id}\n")
