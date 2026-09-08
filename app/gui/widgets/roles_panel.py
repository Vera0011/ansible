from __future__ import annotations

from pathlib import Path

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Label, ListItem, ListView, Static


class RoleItem(ListItem):
    def __init__(self, role_path: Path) -> None:
        super().__init__(Label(role_path.name, classes="role-item"))
        self.role_path = role_path


class RolesPanel(Vertical):
    """
    Left panel listing every available role in the roles directory.
    """

    def __init__(self, roles_dir: Path, **kwargs) -> None:
        super().__init__(id="roles-panel", **kwargs)
        self.roles_dir = roles_dir

    def compose(self) -> ComposeResult:
        yield Static("[bold]Roles[/bold]", classes="panel-title")
        yield ListView(*self._load_roles())

    def _load_roles(self) -> list[RoleItem]:
        if not self.roles_dir.is_dir():
            return []

        return [
            RoleItem(path)
            for path in sorted(self.roles_dir.iterdir())
            if path.is_dir() and not path.name.startswith(".")
        ]

    def refresh_roles(self) -> None:
        list_view = self.query_one(ListView)
        list_view.clear()
        for item in self._load_roles():
            list_view.append(item)
