from nicegui import ui
from typing import Callable, Optional


class ToggleButton(ui.button):
    """
    This class represents a generic button
    """

    def __init__(
        self,
        text: str,
        checked: bool = False,
        on_change: Optional[Callable[[bool], None]] = None,
        **kwargs,
    ):
        super().__init__(text, **kwargs)
        self.is_checked = checked
        self.on_change_callback = on_change

        self.on("click", self.toggle)
        self.update_style()

    def toggle(self) -> None:
        """
        Handler for state change
        """

        self.is_checked = not self.is_checked
        self.update_style()

        if self.on_change_callback:
            self.on_change_callback(self.is_checked)

    def update_style(self) -> None:
        """
        Updates the style - checked / unchecked
        """

        if self.is_checked:
            self.props("icon=check_box color=positive")
        else:
            self.props("icon=check_box_outline_blank color=grey-7")

        self.update()
