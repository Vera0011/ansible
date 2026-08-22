from __future__ import annotations
from datetime import datetime, timezone
from rich.table import Table

from cli.core.context import Context
from cli.core.models.audit.AuditResult import AuditResult


def _render_success(context: Context, result: AuditResult) -> None:
    table = Table(title=f"Audit Summary - {datetime.now(timezone.utc)}")

    table.add_column("Status")
    table.add_column("Count", justify="right")

    table.add_row("[green]Passed[/green]", str(result.summary.passed))
    table.add_row("[red]Failed[/red]", str(result.summary.failed))
    table.add_row("[yellow]Skipped[/yellow]", str(result.summary.skipped))
    table.add_row("[red]Errors[/red]", str(result.summary.errors))

    context.console.print(table)
    context.console.print("\n[green]Audit completed successfully.[/green]")


def _write_result(
    context: Context,
    result: AuditResult,
    output_format: str,
) -> None:
    if output_format != "json":
        raise ValueError(f"Unsupported output format: {output_format}")

    context.reports_dir.mkdir(parents=True, exist_ok=True)
    file_to_write = (context.reports_dir / f"{result.id}.json").resolve()

    file_to_write.write_text(
        result.model_dump_json(indent=2),
        encoding="utf-8",
    )

    context.console.print(f"\n[dim]Result written to {file_to_write}[/dim]")
