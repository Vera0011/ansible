from __future__ import annotations
import os
from nicegui import ui

# Set QT to be used by pywebview (instead of the default GTK)
os.environ["PYWEBVIEW_GUI"] = "qt"

from app.gui.app import EasySecApp

if __name__ in {"__main__", "__mp_main__"}:
    EasySecApp()
    ui.run(title="EasySec Desktop", native=True, window_size=(700, 600), reload=True)
