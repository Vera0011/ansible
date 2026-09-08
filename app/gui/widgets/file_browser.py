from __future__ import annotations

from pathlib import Path

from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import DirectoryTree, TextArea, Static


class ScopedDirectoryTree(DirectoryTree):
    """
    A DirectoryTree that only shows .yml/.yaml files (and directories,
    so users can navigate into them).
    """

    def filter_paths(self, paths):
        return [
            p for p in paths
            if p.is_dir() or p.suffix in (".yml", ".yaml")
        ]


class FileBrowser(Horizontal):
    """
    File browser + editor for inventory/ and playbooks/ .yml files.
    """

    def __init__(self, root_dirs: list[Path], **kwargs) -> None:
        super().__init__(**kwargs)
        self.root_dirs = root_dirs
        self.current_path: Path | None = None

    def compose(self) -> ComposeResult:
        with Vertical(id="file-tree-container"):
            yield Static("[bold]inventory/ & playbooks/[/bold]")
            for root in self.root_dirs:
                if root.is_dir():
                    yield ScopedDirectoryTree(str(root), id=f"tree-{root.name}")
        with Vertical(id="editor-container"):
            yield Static("No file selected", id="editor-title")
            yield TextArea.code_editor("", language="yaml", id="yaml-editor")

    @on(DirectoryTree.FileSelected)
    def load_file(self, event: DirectoryTree.FileSelected) -> None:
        path = Path(event.path)
        self.current_path = path
        editor = self.query_one("#yaml-editor", TextArea)
        editor.load_text(path.read_text())
        self.query_one("#editor-title", Static).update(f"[bold]{path}[/bold]")

    def save_current_file(self) -> str | None:
        if self.current_path is None:
            return None

        editor = self.query_one("#yaml-editor", TextArea)
        self.current_path.write_text(editor.text)
        return str(self.current_path)