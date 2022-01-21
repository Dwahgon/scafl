#!/usr/bin/env python3

import sys
from os.path import dirname, abspath

module_dir = dirname(dirname(abspath(__file__)))
if sys.path[0] != module_dir:
    sys.path.insert(0, module_dir)

from scafl.application import Application


def main():
    app = Application()
    sys.exit(app.run(sys.argv))


if __name__ == "__main__":
    main()
