from gi.repository import Gtk  # type: ignore
from scafl import settings


class AboutDialog(Gtk.AboutDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_program_name(settings.APP_NAME)
        self.set_version(settings.VERSION)
        self.set_authors(settings.AUTHORS)
        self.set_website(settings.GITHUB_URL)
        self.set_website_label("Github")
        self.set_comments(settings.PROGRAM_DESCRIPTION)
        self.set_license_type(settings.LICENSE_TYPE)
