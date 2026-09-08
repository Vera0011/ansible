import tkinter as tk
import sv_ttk
from tkinter import ttk


def _generate_main_layout(container: tk.Tk) -> None:
    """
    Generates the initial layout

    Parameters
    ----------
    container: tk.Tk
        The container to modify
    """

    container = ttk.Frame(container, padding="20")
    container.pack(fill=tk.BOTH, expand=True)
