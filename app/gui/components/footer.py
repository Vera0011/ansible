import sys
from nicegui import ui

from app import __version__


class Footer(ui.footer):
    """
    This class represents the general footer
    """

    def __init__(self) -> None:
        super().__init__()

        self.classes(
            "bg-slate-800 text-gray-300 text-xs py-2 px-4 flex justify-between items-center"
        )

        with self:
            ui.label(f"EasySec - {__version__}")
            ui.label(f"Python {sys.version_info.major}.{sys.version_info.minor}")
