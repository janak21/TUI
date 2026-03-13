"""Linux Commands module — common system utilities."""

from tui.utils import (
    banner, clear_screen, error, get_choice, pause,
    print_menu, run_cmd_safe, separator,
)


def run() -> None:
    while True:
        clear_screen()
        banner("Linux")
        separator()
        print_menu("Linux Commands", [
            "Show calendar",
            "Show date/time",
            "View IP address",
            "Create folder",
            "Create file",
            "Edit file (nano)",
            "View running services",
            "Open Firefox",
            "Show running processes",
            "Show free RAM",
            "Install software",
            "Present working directory",
            "Remove software",
            "Return to main menu",
        ])

        choice = get_choice()
        if choice is None:
            continue

        if choice == 1:
            run_cmd_safe(["cal"])
        elif choice == 2:
            run_cmd_safe(["date"])
        elif choice == 3:
            run_cmd_safe(["ifconfig"])
        elif choice == 4:
            name = input("  Folder name: ")
            run_cmd_safe(["mkdir", "-p", name])
        elif choice == 5:
            name = input("  File name: ")
            run_cmd_safe(["touch", name])
        elif choice == 6:
            name = input("  File name: ")
            run_cmd_safe(["nano", name])
        elif choice == 7:
            run_cmd_safe(["netstat", "-tnlp"])
        elif choice == 8:
            run_cmd_safe(["firefox"])
        elif choice == 9:
            run_cmd_safe(["ps", "aux"])
        elif choice == 10:
            run_cmd_safe(["free", "-m"])
        elif choice == 11:
            name = input("  Software name: ")
            run_cmd_safe(["sudo", "yum", "install", name])
        elif choice == 12:
            run_cmd_safe(["pwd"])
        elif choice == 13:
            name = input("  Software name: ")
            run_cmd_safe(["sudo", "yum", "remove", name])
        elif choice == 14:
            break
        else:
            error("Invalid choice.")

        pause()
