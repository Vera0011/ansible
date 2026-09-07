from __future__ import annotations
import typer

from pathlib import Path
from typing import Annotated
from rich.panel import Panel
from rich.table import Table

from cli.ansible.runner import AnsibleWrapper
from cli.core.context import Context
from cli.core.models.audit.AnsibleResult import AnsibleResult
from cli.core.models.audit.AuditResult import AuditResult
from cli.output.io import _render_success, _write_result
from cli.core.exceptions import EasySecError


def hardening(
    ctx: typer.Context,
    ssh_key: Annotated[
        str,
        typer.Option(
            "--key",
            "-k",
            help="Uses a custom SSH key",
        ),
    ] = "",
    ssh_user: Annotated[
        str,
        typer.Option(
            "--user",
            "-u",
            help="Uses a custom SSH user",
        ),
    ] = "",
    check: Annotated[
        bool,
        typer.Option(
            "--check",
            "-c",
            help="Run Ansible in check mode. This means that the playbook will be executed but will not perform changes",
        ),
    ] = False,
    diff: Annotated[
        bool,
        typer.Option(
            "--diff",
            "-d",
            help="Run Ansible in diff mode. This means that it will display changes on the system without executing it",
        ),
    ] = False,
    json: Annotated[
        bool,
        typer.Option(
            "--json",
            "-j",
            help="Display output in JSON format",
        ),
    ] = False,
) -> None:
    """
    Runs a security audit
    """

    ctx: Context = ctx.obj
    console = ctx.console

    try:
        exit_code: int = run_hardening(
            ctx,
            inventory=inventory,
            ssh_key=ssh_key,
            ssh_user=ssh_user,
            check=check,
            json=json,
            diff=diff,
        )

    except EasySecError as exc:
        console.print(f"[red]Error:[/red] {exc}")
        raise typer.Exit(code=2) from exc

    raise typer.Exit(code=exit_code)


def run_hardening(
    ctx: Context,
    *,
    inventory: Path,
    ssh_key: str,
    ssh_user: str,
    check: bool,
    json: bool,
    diff: bool,
) -> int:
    """
    Executes an auditory

    Parameters
    ----------
    ctx: Context
        Context of the application
    inventory: Path
        The selected inventory
    ssh_key: str
        If an access key must be used
    ssh_user: str
        If an access user must be used
    check: bool
        The parameter 'check' for the Ansible runner
    json: bool
        If output must be written in JSON (automatically sends it to a new file)
    diff: bool
        The parameter 'diff' for the Ansible runner


    Returns
    -------
    int
        The result as int depending Ansible result
    """

    if not ctx.audit_playbook.is_file():
        ctx.console.print(f"[red]Playbook not found:[/red] {ctx.audit_playbook}")
        return 2

    inventory_value: str = str(inventory)
    result: AuditResult = AuditResult.create(inventory_value)

    ctx.console.print()
    table = Table.grid(padding=(0, 2))
    table.add_column(style="bold", no_wrap=True)
    table.add_column(style="spring_green1")

    table.add_row("Repository", str(ctx.root))
    table.add_row("Inventory", str(inventory_value))
    table.add_row("Check enabled", str(check))
    table.add_row("Diff enabled", str(diff))
    table.add_row("JSON output", str(json))

    ctx.console.print(
        Panel(
            table,
            title="[bold cyan]Starting security audit[/bold cyan]",
            width=100,
            border_style="cyan",
        )
    )

    runner: AnsibleWrapper = AnsibleWrapper(ctx)

    ctx.console.print("[bold]Running audit...[/bold]\n")

    ansible_result: AnsibleResult = runner.run(
        ctx.audit_playbook,
        inventory=inventory_value,
        ssh_key=ssh_key,
        ssh_user=ssh_user,
        check=check,
        diff=diff,
    )

    ctx.console.print(ansible_result.stdout)

    if ansible_result.stderr:
        ctx.console.print(f"[yellow]{ansible_result.stderr}[/yellow]")

    result.success = ansible_result.success

    if ansible_result.success:
        result.finished_at = result.started_at
        _render_success(ctx, result)
    else:
        ctx.console.print(
            Panel(
                f"Ansible exited with code {ansible_result.returncode}",
                title="Audit failed",
                border_style="red",
            )
        )

        result.finished_at = result.started_at

    if json:
        _write_result(ctx, result, "json")

    return 0 if ansible_result.success else ansible_result.returncode
