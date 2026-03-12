"""Linux Commands module - common system utilities."""

from tui.utils import (
    banner, clear_screen, get_choice, pause, run_cmd_safe,
    set_color,
)


def run():
    """Main Linux Commands menu."""
    while True:
        clear_screen()
        banner("Linux")
        set_color("green")
        print("""
        1)  Show calendar
        2)  Show date/time
        3)  View IP address
        4)  Create folder
        5)  Create file
        6)  Edit file
        7)  View running services
        8)  Open Firefox
        9)  Show running programs
        10) Show free RAM
        11) Install software
        12) Present working directory
        13) Remove software
        14) Return to main menu
        """)
        set_color("white")

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
            name = input("Enter folder name: ")
            run_cmd_safe(["mkdir", "-p", name])
        elif choice == 5:
            name = input("Enter file name: ")
            run_cmd_safe(["touch", name])
        elif choice == 6:
            name = input("Enter file name: ")
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
            name = input("Enter software name: ")
            run_cmd_safe(["sudo", "yum", "install", name])
        elif choice == 12:
            run_cmd_safe(["pwd"])
        elif choice == 13:
            name = input("Enter software name: ")
            run_cmd_safe(["sudo", "yum", "remove", name])
        elif choice == 14:
            break
        else:
            print("Invalid choice.")

        pause()
