"""Webserver (httpd) module - installation and service management."""

from tui.utils import (
    banner, clear_screen, get_choice, pause, run_cmd_safe,
    separator, set_color,
)


def run():
    """Main Webserver menu."""
    while True:
        clear_screen()
        banner("Webserver")
        set_color("green")
        separator()
        print("""
        Press 1: Install webserver (httpd)
        Press 2: Start webserver
        Press 3: Check webserver status
        Press 4: Stop webserver
        Press 5: Return to main menu
        """)
        separator()
        set_color("white")

        choice = get_choice()
        if choice is None:
            continue

        if choice == 1:
            run_cmd_safe(["sudo", "yum", "install", "-y", "httpd"])
        elif choice == 2:
            run_cmd_safe(["sudo", "systemctl", "start", "httpd"])
        elif choice == 3:
            run_cmd_safe(["sudo", "systemctl", "status", "httpd"])
        elif choice == 4:
            run_cmd_safe(["sudo", "systemctl", "stop", "httpd"])
        elif choice == 5:
            break
        else:
            print("Invalid choice.")

        pause()
        clear_screen()
