import tkinter as tk
from tkinter import ttk

from app.gui.components.header import _generate_header
from app.gui.components.footer import _generate_footer


class EasySecApp(tk.Tk):
    """
    Main entry point for application
    """

    def __init__(self):
        super().__init__()

        self.title("Easysec")
        self.geometry("600x400+100+100")
        self.resizable(False, False)

        # Style layout
        self.style = ttk.Style(self)
        self.style.theme_use("clam")

        self.counter = 0

        self._build_ui()

    def _build_ui(self):
        # Main Container
        container = ttk.Frame(self, padding="20")
        container.pack(fill=tk.BOTH, expand=True)

        # Action Buttons
        btn_frame = ttk.Frame(container)
        btn_frame.pack(pady=10)

        increment_btn = ttk.Button(btn_frame, text="Increment", command=())
        increment_btn.pack(side=tk.LEFT, padx=5)

        # Info Footer
        _generate_footer(container)
