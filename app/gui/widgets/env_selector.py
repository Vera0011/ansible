from __future__ import annotations

from pathlib import Path

from textual.widgets import Select


class EnvSelector(Select):
    """
    Dropdown listing available inventories (environments) found under
    inventory/, e.g. inventory/production, inventory/staging.
    """

    def __init__(self, inventory_dir: Path, **kwargs) -> None:
        self.inventory_dir = inventory_dir
        options = self._discover_environments()
        super().__init__(options, id="env-select", prompt="Environment", **kwargs)

    def _discover_environments(self) -> list[tuple[str, str]]:
        if not self.inventory_dir.is_dir():
            return []

        envs: list[tuple[str, str]] = []
        for entry in sorted(self.inventory_dir.iterdir()):
            if entry.name.startswith("."):
                continue
            if entry.is_dir() or entry.suffix in (".yml", ".yaml", ".ini"):
                envs.append((entry.name, str(entry)))

        return envs