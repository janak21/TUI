"""Webserver (httpd) module — installation and service management."""

from tui.utils import (
    banner, clear_screen, error, get_choice, info, pause,
    print_menu, run_cmd_safe, separator, success,
)


def run() -> None:
    while True:
        clear_screen()
        banner("Webserver")
        separator()
        print_menu("Apache httpd", [
            "Install webserver (httpd)",
            "Start webserver",
            "Check webserver status",
            "Stop webserver",
            "Return to main menu",
        ])

        choice = get_choice()
        if choice is None:
            continue

        if choice == 1:
            info("Installing Apache httpd...")
            run_cmd_safe(["sudo", "yum", "install", "-y", "httpd"])
            success("httpd installed.")
        elif choice == 2:
            run_cmd_safe(["sudo", "systemctl", "start", "httpd"])
            success("httpd started.")
        elif choice == 3:
            run_cmd_safe(["sudo", "systemctl", "status", "httpd"])
        elif choice == 4:
            run_cmd_safe(["sudo", "systemctl", "stop", "httpd"])
            success("httpd stopped.")
        elif choice == 5:
            break
        else:
            error("Invalid choice.")

        pause()
        clear_screen()
