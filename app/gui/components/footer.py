from app import __version__

import tkinter as tk
from tkinter import ttk


def _generate_footer(container):
    footer = ttk.Label(
        container,
        text=__version__,
        font=("Helvetica", 8),
        foreground="gray",
    )
    footer.pack(side=tk.BOTTOM, pady=(10, 0))
