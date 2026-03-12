"""Main CLI entry point - renders the main menu and dispatches to modules."""

from platform import system as detect_platform

import pyfiglet

from tui.utils import banner, clear_screen, get_choice, pause, separator, set_color
from tui.modules import aws, docker, hadoop, kubernetes, linux, lvm, webserver


def detect_os():
    """Display detected OS with a banner."""
    os_name = detect_platform()
    set_color("magenta")
    print(pyfiglet.figlet_format(os_name, font="slant"))
    pause()
    clear_screen()


def main_menu():
    """Run the main TUI menu loop."""
    while True:
        clear_screen()
        separator()
        banner("Main Menu")
        set_color("green")
        print("""
        1) Detect Operating System
        2) Hadoop
        3) AWS
        4) Docker
        5) Kubernetes
        6) Webserver
        7) Linux Partitions (LVM)
        8) Linux Commands
        9) Exit
        """)
        separator()
        set_color("white")

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
            print("Goodbye!")
            break
        else:
            print("Invalid option.")
