from nicegui import app, ui

from app.gui.components.footer import Footer
from app.gui.components.toast import Toast


class EasySecApp:
    """
    Main entry point for application
    """

    footer_manager: Footer
    toast_manager: Toast

    def __init__(self):
        app.native.window_args["resizable"] = True
        app.native.start_args["debug"] = True

        self._build_ui()

    def _build_ui(self):
        """
        Creates the main UI
        """

        with ui.column().classes("w-full p-6 items-center"):
            ui.label("Main Interface Content").classes("text-xl font-bold")

        self.footer_manager = Footer()
        self.toast_manager = Toast()
