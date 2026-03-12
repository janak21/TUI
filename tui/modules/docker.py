"""Docker module - installation, image, and container management."""

from tui.utils import (
    banner, clear_screen, get_choice, pause, run_cmd_safe,
    separator, set_color,
)


def _docker_service():
    print("""
    Press 1: Start Docker service (permanently)
    Press 2: Stop Docker service
    Press 3: Show Docker service status
    Press 4: Back
    """)
    while True:
        choice = get_choice()
        if choice is None:
            continue
        if choice == 1:
            run_cmd_safe(["sudo", "systemctl", "start", "docker"])
            run_cmd_safe(["sudo", "systemctl", "enable", "docker"])
        elif choice == 2:
            run_cmd_safe(["sudo", "systemctl", "stop", "docker"])
        elif choice == 3:
            run_cmd_safe(["sudo", "systemctl", "status", "docker"])
        elif choice == 4:
            break
        else:
            print("Invalid choice.")
        pause()
        clear_screen()


def _delete_images():
    while True:
        print("""
        Press 1: Delete single image
        Press 2: Delete all images
        Press 3: Back
        """)
        choice = get_choice()
        if choice is None:
            continue
        if choice == 1:
            img = input("Enter image name: ")
            version = input("Enter version/tag: ")
            run_cmd_safe(["docker", "rmi", "-f", f"{img}:{version}"])
        elif choice == 2:
            print("Deleting all images...")
            run_cmd_safe(["docker", "image", "prune", "-a", "-f"])
            print("All images deleted.")
        elif choice == 3:
            break
        else:
            print("Invalid choice.")
        pause()
        clear_screen()


def _delete_containers():
    while True:
        print("""
        Press 1: Delete single container
        Press 2: Delete all containers
        Press 3: Back
        """)
        choice = get_choice()
        if choice is None:
            continue
        if choice == 1:
            container_id = input("Enter container name/ID: ")
            run_cmd_safe(["docker", "rm", "-f", container_id])
        elif choice == 2:
            print("Deleting all containers...")
            run_cmd_safe(["docker", "container", "prune", "-f"])
            print("All containers deleted.")
        elif choice == 3:
            break
        else:
            print("Invalid choice.")
        pause()
        clear_screen()


def _stop_containers():
    while True:
        print("""
        Press 1: Stop single container
        Press 2: Stop all containers
        Press 3: Back
        """)
        choice = get_choice()
        if choice is None:
            continue
        if choice == 1:
            container_id = input("Enter container name: ")
            run_cmd_safe(["docker", "stop", container_id])
        elif choice == 2:
            print("Stopping all containers...")
            run_cmd_safe(["docker", "stop", "$(docker ps -q)"])
            print("All containers stopped.")
        elif choice == 3:
            break
        else:
            print("Invalid choice.")
        pause()
        clear_screen()


def run():
    """Main Docker menu."""
    while True:
        clear_screen()
        banner("Docker")
        set_color("green")
        separator()
        print("""
        Press 1 : Install/Update Docker
        Press 2 : Docker service management
        Press 3 : Check Docker version
        Press 4 : Search images on Docker Hub
        Press 5 : Pull (download) image
        Press 6 : List downloaded images
        Press 7 : Run new container
        Press 8 : View running containers
        Press 9 : View all containers (including stopped)
        Press 10: Start existing container
        Press 11: Delete images
        Press 12: Delete containers
        Press 13: Stop containers
        Press 14: Docker system info
        Press 15: Return to main menu
        """)
        separator()
        set_color("white")

        choice = get_choice()
        if choice is None:
            continue

        if choice == 1:
            run_cmd_safe(["sudo", "yum", "install", "docker", "--nobest"])
        elif choice == 2:
            _docker_service()
        elif choice == 3:
            run_cmd_safe(["docker", "-v"])
        elif choice == 4:
            name = input("Enter image/distro name to search: ")
            run_cmd_safe(["docker", "search", name])
        elif choice == 5:
            name = input("Enter image name to pull: ")
            run_cmd_safe(["docker", "pull", name])
        elif choice == 6:
            run_cmd_safe(["docker", "images"])
        elif choice == 7:
            name = input("Enter container name: ")
            img = input("Enter image name: ")
            run_cmd_safe(["docker", "run", "-it", "--name", name, img])
        elif choice == 8:
            run_cmd_safe(["docker", "ps"])
        elif choice == 9:
            run_cmd_safe(["docker", "ps", "-a"])
        elif choice == 10:
            name = input("Enter container name: ")
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
            print("Invalid choice.")

        pause()
        clear_screen()
