"""Shared utilities for TUI — display (Rich), command execution, and auth."""

import shlex
import subprocess
import sys
from platform import system as detect_platform

import pyfiglet
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table
from rich.text import Text

console = Console()


# ---------------------------------------------------------------------------
# Display helpers
# ---------------------------------------------------------------------------

def banner(text: str, subtitle: str = "") -> None:
    """Render an ASCII-art banner inside a styled panel."""
    fig = pyfiglet.figlet_format(text, font="slant").rstrip()
    content = Text(fig, style="bold yellow", justify="center")
    console.print(Panel(content, border_style="blue", subtitle=f"[dim]{subtitle}[/dim]" if subtitle else ""))


def print_menu(title: str, options: list[str]) -> None:
    """Render a numbered menu inside a styled panel."""
    table = Table(show_header=False, box=box.SIMPLE, padding=(0, 1), show_edge=False)
    table.add_column("num", style="bold cyan", no_wrap=True, width=5)
    table.add_column("option", style="white")
    for i, opt in enumerate(options, 1):
        table.add_row(f"[{i}]", opt)
    console.print(Panel(table, title=f"[bold yellow]{title}[/bold yellow]", border_style="blue"))


def separator(title: str = "") -> None:
    """Print a horizontal rule."""
    console.print(Rule(title=f"[dim]{title}[/dim]" if title else "", style="blue"))


def success(msg: str) -> None:
    console.print(f"[bold green]✓[/bold green]  {msg}")


def error(msg: str) -> None:
    console.print(f"[bold red]✗[/bold red]  {msg}")


def info(msg: str) -> None:
    console.print(f"[bold cyan]ℹ[/bold cyan]  {msg}")


def warn(msg: str) -> None:
    console.print(f"[bold yellow]⚠[/bold yellow]  {msg}")


# ---------------------------------------------------------------------------
# Input helpers
# ---------------------------------------------------------------------------

def get_choice(prompt: str = "Enter your choice") -> int | None:
    try:
        console.print(f"\n[bold cyan]{prompt}:[/bold cyan] ", end="")
        raw = input()
        return int(raw.strip())
    except ValueError:
        error("Please enter a valid number.")
        return None
    except EOFError:
        raise  # propagate so while-True loops terminate cleanly


def pause(msg: str = "Press Enter to continue...") -> None:
    console.input(f"[dim]{msg}[/dim]")


def clear_screen() -> None:
    cmd = "cls" if detect_platform() == "Windows" else "clear"
    subprocess.run([cmd], check=False)


# ---------------------------------------------------------------------------
# Command execution
# ---------------------------------------------------------------------------

def run_cmd_safe(args: list[str], **kwargs) -> int:
    """Run a command with a list of args — safe from shell injection."""
    result = subprocess.run(args, check=False, **kwargs)
    return result.returncode


def run_cmd(cmd: str, **kwargs) -> int:
    """Run a hardcoded shell command string."""
    result = subprocess.run(cmd, shell=True, check=False, **kwargs)
    return result.returncode


def safe_quote(value: str) -> str:
    return shlex.quote(value)


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

def check_root() -> None:
    import os
    if os.geteuid() != 0:
        console.print(Panel(
            "[bold red]Root privileges required.[/bold red]\n"
            "Please re-run with [bold]sudo[/bold].",
            border_style="red",
            title="[red]Permission Denied[/red]",
        ))
        sys.exit(1)
