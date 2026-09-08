from __future__ import annotations

import shlex
from pathlib import Path

from textual import on, work
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, TabbedContent, TabPane, Button

from app.cli.core.context import Context
from cli.gui.widgets.roles_panel import RolesPanel, RoleItem
from cli.gui.widgets.env_selector import EnvSelector
from cli.gui.widgets.file_browser import FileBrowser
from cli.gui.widgets.log_panel import LogPanel

try:
    from textual_terminal import Terminal
    HAS_TERMINAL = True
except ImportError:
    HAS_TERMINAL = False


class EasySecApp(App):
    """
    Visual interface for EasySec, built on top of the existing CLI context.
    """

    CSS_PATH = Path(__file__).parent / "styles" / "app.tcss"
    BINDINGS = [
        ("ctrl+s", "save_file", "Save file"),
        ("ctrl+r", "run_role", "Run selected role"),
        ("q", "quit", "Quit"),
    ]

    def __init__(self, context: Context) -> None:
        super().__init__()
        self.context = context
        self.selected_role: Path | None = None

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        with Horizontal(id="header"):
            yield EnvSelector(self.context.inventory_dir)
            yield Button("Run role", id="run-btn", variant="primary")

        yield RolesPanel(self.context.roles_dir)

        with Vertical(id="main-area"):
            with TabbedContent():
                with TabPane("Files", id="files-tab"):
                    yield FileBrowser([
                        self.context.inventory_dir,
                        self.context.playbooks_dir,
                    ])
                with TabPane("Terminal", id="terminal-tab"):
                    if HAS_TERMINAL:
                        yield Terminal(
                            command="/bin/bash",
                            default_directory=str(self.context.root),
                        )
                    else:
                        yield Vertical(
                            id="terminal-fallback"
                        )

        yield LogPanel(id="log-panel")
        yield Footer()

    def on_mount(self) -> None:
        if HAS_TERMINAL:
            self.query_one(Terminal).start()

    @on(RolesPanel.ListView.Highlighted := None)  # placeholder, replaced below
    def _unused(self) -> None:
        pass

    @on(RoleItem, "selected")
    def on_role_selected(self, event) -> None:
        self.selected_role = event.item.role_path
        self.query_one(LogPanel).write(f"[cyan]Selected role:[/cyan] {self.selected_role.name}")

    @on(Button.Pressed, "#run-btn")
    def on_run_pressed(self) -> None:
        self.action_run_role()

    def action_save_file(self) -> None:
        browser = self.query_one(FileBrowser)
        saved = browser.save_current_file()
        log = self.query_one(LogPanel)
        if saved:
            log.write(f"[green]Saved:[/green] {saved}")
        else:
            log.write("[yellow]No file open to save.[/yellow]")

    def action_run_role(self) -> None:
        if self.selected_role is None:
            self.query_one(LogPanel).write("[red]No role selected.[/red]")
            return

        env_select = self.query_one(EnvSelector)
        if env_select.value is None:
            self.query_one(LogPanel).write("[red]No environment selected.[/red]")
            return

        self._execute_role(self.selected_role, Path(env_select.value))

    @work(exclusive=True, thread=True)
    def _execute_role(self, role_path: Path, inventory_path: Path) -> None:
        import subprocess

        log = self.query_one(LogPanel)
        self.call_from_thread(log.write, f"[bold]Running role:[/bold] {role_path.name}")

        # Adjust this to however your project actually maps a role to a
        # playbook — this assumes a convention of playbooks/<role>.yml
        playbook = self.context.playbooks_dir / f"{role_path.name}.yml"

        if not playbook.is_file():
            self.call_from_thread(
                log.write,
                f"[red]No matching playbook found at {playbook}[/red]",
            )
            return

        command = [
            "ansible-playbook",
            "-i", str(inventory_path),
            str(playbook),
        ]

        process = subprocess.Popen(
            command,
            cwd=self.context.root,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )

        for line in process.stdout:
            self.call_from_thread(log.write, line.rstrip())

        process.wait()
        status = "green]Finished" if process.returncode == 0 else "red]Failed"
        self.call_from_thread(log.write, f"[{status} (exit code {process.returncode})[/]")


def run_app(context: Context) -> None:
    EasySecApp(context).run()