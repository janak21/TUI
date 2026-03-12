"""Shared utilities for TUI modules."""

import shlex
import subprocess
import sys
from platform import system as detect_platform

import pyfiglet


COLORS = {
    "red": 1,
    "green": 2,
    "yellow": 3,
    "blue": 4,
    "magenta": 5,
    "cyan": 6,
    "white": 7,
    "grey": 8,
}


def set_color(color: str) -> None:
    code = COLORS.get(color, 7)
    subprocess.run(["tput", "setaf", str(code)], check=False)


def clear_screen() -> None:
    cmd = "cls" if detect_platform() == "Windows" else "clear"
    subprocess.run([cmd], check=False)


def banner(text: str, color: str = "yellow") -> None:
    set_color(color)
    print(pyfiglet.figlet_format(text, font="slant"))


def separator() -> None:
    print("-" * 100)


def pause(msg: str = "Press Enter to continue...") -> None:
    input(msg)


def get_choice(prompt: str = "Enter your choice: ") -> int | None:
    raw = input(prompt).strip()
    try:
        return int(raw)
    except ValueError:
        print("Please enter a valid number.")
        return None


def run_cmd(cmd: str, **kwargs) -> int:
    """Run a shell command string. Use only for simple, hardcoded commands."""
    result = subprocess.run(cmd, shell=True, check=False, **kwargs)
    return result.returncode


def run_cmd_safe(args: list[str], **kwargs) -> int:
    """Run a command with a list of arguments (no shell injection risk)."""
    result = subprocess.run(args, check=False, **kwargs)
    return result.returncode


def safe_quote(value: str) -> str:
    """Shell-quote a user-provided value to prevent injection."""
    return shlex.quote(value)


def check_root() -> None:
    """Check if the script is running with root/sudo privileges."""
    import os
    if os.geteuid() != 0:
        set_color("red")
        print(
            "You need root privileges to run this script as some commands require root permission.\n"
            "Please try again using 'sudo'."
        )
        sys.exit(1)
