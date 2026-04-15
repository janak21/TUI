"""Docker module — installation, image, and container management."""

from tui.utils import (
    banner, clear_screen, detect_pkg_manager, error, get_choice, info, pause,
    print_menu, require_tool, run_cmd, run_cmd_safe, separator, success,
)


def _docker_service() -> None:
    while True:
        print_menu("Docker Service", [
            "Start service (permanent)",
            "Stop service",
            "Show service status",
            "Back",
        ])
        choice = get_choice()
        if choice is None:
            continue
        if choice == 1:
            run_cmd_safe(["sudo", "systemctl", "start", "docker"])
            run_cmd_safe(["sudo", "systemctl", "enable", "docker"])
            success("Docker started and enabled.")
        elif choice == 2:
            run_cmd_safe(["sudo", "systemctl", "stop", "docker"])
            success("Docker stopped.")
        elif choice == 3:
            run_cmd_safe(["sudo", "systemctl", "status", "docker"])
        elif choice == 4:
            break
        else:
            error("Invalid choice.")
        pause()
        clear_screen()


def _delete_images() -> None:
    while True:
        print_menu("Delete Images", [
            "Delete single image",
            "Delete all images",
            "Back",
        ])
        choice = get_choice()
        if choice is None:
            continue
        if choice == 1:
            img = input("  Image name: ")
            tag = input("  Tag/version: ")
            run_cmd_safe(["docker", "rmi", "-f", f"{img}:{tag}"])
            success("Image deleted.")
        elif choice == 2:
            info("Deleting all images...")
            run_cmd_safe(["docker", "image", "prune", "-a", "-f"])
            success("All images deleted.")
        elif choice == 3:
            break
        else:
            error("Invalid choice.")
        pause()
        clear_screen()


def _delete_containers() -> None:
    while True:
        print_menu("Delete Containers", [
            "Delete single container",
            "Delete all containers",
            "Back",
        ])
        choice = get_choice()
        if choice is None:
            continue
        if choice == 1:
            cid = input("  Container name/ID: ")
            run_cmd_safe(["docker", "rm", "-f", cid])
            success("Container deleted.")
        elif choice == 2:
            info("Deleting all containers...")
            run_cmd_safe(["docker", "container", "prune", "-f"])
            success("All containers deleted.")
        elif choice == 3:
            break
        else:
            error("Invalid choice.")
        pause()
        clear_screen()


def _stop_containers() -> None:
    while True:
        print_menu("Stop Containers", [
            "Stop single container",
            "Stop all containers",
            "Back",
        ])
        choice = get_choice()
        if choice is None:
            continue
        if choice == 1:
            cid = input("  Container name: ")
            run_cmd_safe(["docker", "stop", cid])
            success("Container stopped.")
        elif choice == 2:
            info("Stopping all containers...")
            run_cmd("docker stop $(docker ps -q)")  # shell substitution required
            success("All containers stopped.")
        elif choice == 3:
            break
        else:
            error("Invalid choice.")
        pause()
        clear_screen()


def run() -> None:
    while True:
        clear_screen()
        banner("Docker")
        separator()
        print_menu("Docker", [
            "Install / Update Docker",
            "Docker service management",
            "Check Docker version",
            "Search images on Docker Hub",
            "Pull (download) image",
            "List downloaded images",
            "Run new container",
            "View running containers",
            "View all containers (including stopped)",
            "Start existing container",
            "Delete images",
            "Delete containers",
            "Stop containers",
            "Docker system info",
            "Return to main menu",
        ])

        choice = get_choice()
        if choice is None:
            continue

        if choice == 1:
            pm = detect_pkg_manager()
            if pm == "apt-get":
                run_cmd("curl -fsSL https://get.docker.com | sudo sh")
            else:
                run_cmd_safe(["sudo", pm, "install", "-y", "docker"])
        elif choice == 2:
            _docker_service()
        elif choice == 3:
            if require_tool("docker"):
                run_cmd_safe(["docker", "-v"])
        elif choice in range(4, 14):
            if not require_tool("docker"):
                pause()
                clear_screen()
                continue
            if choice == 4:
                name = input("  Image/distro name to search: ")
                run_cmd_safe(["docker", "search", name])
            elif choice == 5:
                name = input("  Image name to pull: ")
                run_cmd_safe(["docker", "pull", name])
            elif choice == 6:
                run_cmd_safe(["docker", "images"])
            elif choice == 7:
                name = input("  Container name: ")
                img = input("  Image name: ")
                run_cmd_safe(["docker", "run", "-it", "--name", name, img])
            elif choice == 8:
                run_cmd_safe(["docker", "ps"])
            elif choice == 9:
                run_cmd_safe(["docker", "ps", "-a"])
            elif choice == 10:
                name = input("  Container name: ")
                run_cmd_safe(["docker", "start", name])
                run_cmd_safe(["docker", "attach", name])
        elif choice == 11:
            _delete_images()
        elif choice == 12:
            _delete_containers()
        elif choice == 13:
            _stop_containers()
        elif choice == 14:
            run_cmd_safe(["docker", "info"])
        elif choice == 15:
            break
        else:
            error("Invalid choice.")

        pause()
        clear_screen()
