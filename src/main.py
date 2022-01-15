#!/usr/bin/env python3

import sys
sys.path.insert(0, '..')

from application import Application


def main():
    app = Application()
    sys.exit(app.run(sys.argv))


if __name__ == "__main__":
    main()
