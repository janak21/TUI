"""Main CLI entry point — renders the main menu and dispatches to modules."""

from platform import system as detect_platform

import pyfiglet

from tui.utils import banner, clear_screen, console, error, get_choice, pause, print_menu, separator
from tui.modules import aws, docker, hadoop, kubernetes, linux, lvm, webserver


def detect_os() -> None:
    os_name = detect_platform()
    banner(os_name, subtitle="Detected OS")
    pause()
    clear_screen()


def main_menu() -> None:
    while True:
        clear_screen()
        banner("TUI", subtitle="Cloud & DevOps Terminal Interface")
        separator()
        print_menu("Main Menu", [
            "Detect Operating System",
            "Hadoop",
            "AWS",
            "Docker",
            "Kubernetes",
            "Webserver",
            "Linux Partitions (LVM)",
            "Linux Commands",
            "Exit",
        ])

        choice = get_choice()
        if choice is None:
            continue

        if choice == 1:
            detect_os()
        elif choice == 2:
            hadoop.run()
        elif choice == 3:
            aws.run()
        elif choice == 4:
            docker.run()
        elif choice == 5:
            kubernetes.run()
        elif choice == 6:
            webserver.run()
        elif choice == 7:
            lvm.run()
        elif choice == 8:
            linux.run()
        elif choice == 9:
            console.print("\n[bold yellow]Goodbye![/bold yellow]\n")
            break
        else:
            error("Invalid option.")
