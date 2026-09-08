from __future__ import annotations
import typer

from typing import Annotated
from rich.panel import Panel
from rich.table import Table

from cli.ansible.runner import AnsibleWrapper
from cli.core.context import Context
from cli.core.exceptions import EasySecError


def audit(
    ctx: typer.Context,
    environment: Annotated[
        str,
        typer.Option(
            "--environment",
            "-e",
            help="Determines if the inventory to use. Available options are 'vagrant', 'production' and 'staging'",
        ),
    ] = "vagrant",
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
    ] = True,
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
        if environment not in ["staging", "production", "vagrant"]:
            console.print(f"[red]Error:[/red] {environment} is not a valid option")
            raise typer.Exit(code=2)

        exit_code: int = run_audit(
            ctx,
            environment=environment,
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


def run_audit(
    ctx: Context,
    environment: bool,
    *,
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
    environment: str
        The environment to use
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

    available_envs: dict = {
        "vagrant": "/vagrant",
        "production": "/production",
        "staging": "/staging",
    }

    custom_inventory = str(ctx.inventory_dir) + available_envs[environment]

    ctx.console.print()
    table = Table.grid(padding=(0, 2))
    table.add_column(style="bold", no_wrap=True)
    table.add_column(style="spring_green1")

    table.add_row("Repository", str(ctx.root))
    table.add_row("Option", "Audit")
    table.add_row("Inventory", available_envs[environment])
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

    # Does not check if the key is correct when Vagrant environment is selected
    insecure: bool = True if environment in ["vagrant"] else False

    ansible_result: int = runner.run(
        ctx.audit_playbook,
        ssh_key=ssh_key,
        inventory=custom_inventory,
        ssh_user=ssh_user,
        check=check,
        diff=diff,
        insecure=insecure,
    )

    return ansible_result
