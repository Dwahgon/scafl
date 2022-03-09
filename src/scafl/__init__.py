__version__ = "0.4.1"


def main():
    import sys
    from scafl.application import Application

    app = Application()
    sys.exit(app.run(sys.argv))
