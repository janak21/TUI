"""Webserver (httpd) module — installation and service management."""

from tui.utils import (
    banner, clear_screen, detect_pkg_manager, error, get_choice, info, pause,
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

        # apt uses 'apache2', yum/dnf uses 'httpd'
        pm  = detect_pkg_manager()
        svc = "apache2" if pm == "apt-get" else "httpd"

        if choice == 1:
            info(f"Installing Apache ({svc}) via {pm}...")
            run_cmd_safe(["sudo", pm, "install", "-y", svc])
            success(f"{svc} installed.")
        elif choice == 2:
            run_cmd_safe(["sudo", "systemctl", "start", svc])
            success(f"{svc} started.")
        elif choice == 3:
            run_cmd_safe(["sudo", "systemctl", "status", svc])
        elif choice == 4:
            run_cmd_safe(["sudo", "systemctl", "stop", svc])
            success(f"{svc} stopped.")
        elif choice == 5:
            break
        else:
            error("Invalid choice.")

        pause()
        clear_screen()
