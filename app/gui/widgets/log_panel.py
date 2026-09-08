from __future__ import annotations

from textual.containers import Vertical
from textual.widgets import RichLog, Static


class LogPanel(Vertical):
    """
    Bottom panel showing live execution output (e.g. ansible-playbook).
    """

    def compose(self):
        yield Static("[bold]Execution log[/bold]")
        yield RichLog(id="exec-log", highlight=True, markup=True, wrap=True)

    def write(self, line: str) -> None:
        self.query_one("#exec-log", RichLog).write(line)

    def clear(self) -> None:
        self.query_one("#exec-log", RichLog).clear()