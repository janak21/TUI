"""Linux Partitions (LVM) module - physical volumes, volume groups, and logical volumes."""

from tui.utils import (
    banner, clear_screen, get_choice, pause, run_cmd_safe,
    separator, set_color,
)


def _mount_volume():
    while True:
        print(
            "\n    Press 1: Mount on new folder"
            "\n    Press 2: Mount on existing folder"
            "\n    Press 3: Back\n"
        )
        choice = get_choice()
        if choice is None:
            continue
        if choice in (1, 2):
            set_color("white")
            if choice == 1:
                mount_point = input("Enter new folder name: ")
                run_cmd_safe(["mkdir", "-p", mount_point])
            else:
                mount_point = input("Enter existing folder path: ")
            vg_name = input("Enter volume group name: ")
            lv_name = input("Enter logical volume name: ")
            run_cmd_safe(["mount", f"/dev/{vg_name}/{lv_name}", mount_point])
            run_cmd_safe(["df", "-h"])
            set_color("yellow")
            print("\n\t\t\tLogical volume mounted successfully.")
        elif choice == 3:
            break
        else:
            print("Invalid option.")
        pause()
        clear_screen()


def run():
    """Main Linux Partitions menu."""
    while True:
        clear_screen()
        banner("LVM")
        set_color("green")
        separator()
        print("""
        Press 1 : Check available disks
        Press 2 : Create physical volume
        Press 3 : View all physical volumes
        Press 4 : View physical volume by name
        Press 5 : Create volume group
        Press 6 : View all volume groups
        Press 7 : View volume group by name
        Press 8 : Create logical volume
        Press 9 : View all logical volumes
        Press 10: View logical volume by name
        Press 11: Format logical volume
        Press 12: Mount logical volume
        Press 13: Extend logical volume
        Press 14: Resize extended partition
        Press 15: Extend volume group
        Press 16: Return to main menu
        """)
        separator()
        set_color("white")

        choice = get_choice()
        if choice is None:
            continue

        if choice == 1:
            run_cmd_safe(["fdisk", "-l"])

        elif choice == 2:
            disk = input("Enter disk name: ")
            run_cmd_safe(["pvcreate", disk])
            set_color("yellow")
            print("\n\t\t\tPhysical volume created successfully.")

        elif choice == 3:
            run_cmd_safe(["pvdisplay"])

        elif choice == 4:
            disk = input("Enter disk name: ")
            run_cmd_safe(["pvdisplay", disk])

        elif choice == 5:
            disk1 = input("Enter first PV name: ")
            disk2 = input("Enter second PV name: ")
            vg_name = input("Enter volume group name: ")
            run_cmd_safe(["vgcreate", vg_name, disk1, disk2])
            run_cmd_safe(["vgdisplay", vg_name])
            set_color("yellow")
            print("\n\t\t\tVolume group created successfully.")

        elif choice == 6:
            run_cmd_safe(["vgdisplay"])

        elif choice == 7:
            vg_name = input("Enter volume group name: ")
            run_cmd_safe(["vgdisplay", vg_name])

        elif choice == 8:
            vg_name = input("Enter volume group name: ")
            lv_name = input("Enter logical volume name: ")
            size = input("Enter size in GB: ")
            run_cmd_safe(["lvcreate", "--size", f"{size}G", "--name", lv_name, vg_name])
            run_cmd_safe(["lvdisplay", f"{vg_name}/{lv_name}"])
            set_color("yellow")
            print("\n\t\t\tLogical volume created successfully.")

        elif choice == 9:
            run_cmd_safe(["lvdisplay"])

        elif choice == 10:
            vg_name = input("Enter volume group name: ")
            lv_name = input("Enter logical volume name: ")
            run_cmd_safe(["lvdisplay", f"{vg_name}/{lv_name}"])

        elif choice == 11:
            vg_name = input("Enter volume group name: ")
            lv_name = input("Enter logical volume name: ")
            run_cmd_safe(["mkfs.ext4", f"/dev/{vg_name}/{lv_name}"])
            set_color("yellow")
            print("\n\t\t\tLogical volume formatted successfully.")

        elif choice == 12:
            _mount_volume()

        elif choice == 13:
            size = input("Enter size in GB to extend: ")
            vg_name = input("Enter volume group name: ")
            lv_name = input("Enter logical volume name: ")
            run_cmd_safe(["lvextend", "--size", f"+{size}G", f"/dev/{vg_name}/{lv_name}"])
            set_color("yellow")
            print("\n\t\t\tLogical volume extended. Resize the volume to use extended storage.")

        elif choice == 14:
            vg_name = input("Enter volume group name: ")
            lv_name = input("Enter logical volume name: ")
            run_cmd_safe(["resize2fs", f"/dev/{vg_name}/{lv_name}"])
            set_color("yellow")
            print("\n\t\t\tPartition resized successfully.")

        elif choice == 15:
            vg_name = input("Enter volume group name: ")
            disk = input("Enter disk name: ")
            run_cmd_safe(["vgextend", vg_name, disk])

        elif choice == 16:
            break
        else:
            print("Invalid choice.")

        set_color("white")
        pause()
        clear_screen()
