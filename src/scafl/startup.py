from scafl import settings
import os

DIRECTORIES = [
    settings.DATA_DIR,
    settings.CONFIG_DIR,
]


def _init_dirs():
    for dir in DIRECTORIES:
        os.makedirs(dir, exist_ok=True)


def init_app():
    _init_dirs()
