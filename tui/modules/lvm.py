"""Linux Partitions (LVM) module — PV, VG, and LV management."""

from tui.utils import (
    banner, clear_screen, error, get_choice, info, pause,
    print_menu, run_cmd_safe, separator, success,
)


def _mount_volume() -> None:
    while True:
        print_menu("Mount Logical Volume", [
            "Mount on new folder",
            "Mount on existing folder",
            "Back",
        ])
        choice = get_choice()
        if choice is None:
            continue
        if choice in (1, 2):
            if choice == 1:
                mount_point = input("  New folder name: ")
                run_cmd_safe(["mkdir", "-p", mount_point])
            else:
                mount_point = input("  Existing folder path: ")
            vg = input("  Volume group name: ")
            lv = input("  Logical volume name: ")
            run_cmd_safe(["mount", f"/dev/{vg}/{lv}", mount_point])
            run_cmd_safe(["df", "-h"])
            success("Logical volume mounted.")
        elif choice == 3:
            break
        else:
            error("Invalid option.")
        pause()
        clear_screen()


def run() -> None:
    while True:
        clear_screen()
        banner("LVM")
        separator()
        print_menu("Linux Partitions", [
            "Check available disks",
            "Create physical volume",
            "View all physical volumes",
            "View physical volume by name",
            "Create volume group",
            "View all volume groups",
            "View volume group by name",
            "Create logical volume",
            "View all logical volumes",
            "View logical volume by name",
            "Format logical volume",
            "Mount logical volume",
            "Extend logical volume",
            "Resize extended partition",
            "Extend volume group",
            "Return to main menu",
        ])

        choice = get_choice()
        if choice is None:
            continue

        if choice == 1:
            run_cmd_safe(["fdisk", "-l"])

        elif choice == 2:
            disk = input("  Disk name: ")
            run_cmd_safe(["pvcreate", disk])
            success("Physical volume created.")

        elif choice == 3:
            run_cmd_safe(["pvdisplay"])

        elif choice == 4:
            disk = input("  Disk name: ")
            run_cmd_safe(["pvdisplay", disk])

        elif choice == 5:
            disk1 = input("  First PV name: ")
            disk2 = input("  Second PV name: ")
            vg = input("  Volume group name: ")
            run_cmd_safe(["vgcreate", vg, disk1, disk2])
            run_cmd_safe(["vgdisplay", vg])
            success("Volume group created.")

        elif choice == 6:
            run_cmd_safe(["vgdisplay"])

        elif choice == 7:
            vg = input("  Volume group name: ")
            run_cmd_safe(["vgdisplay", vg])

        elif choice == 8:
            vg = input("  Volume group name: ")
            lv = input("  Logical volume name: ")
            size = input("  Size in GB: ")
            run_cmd_safe(["lvcreate", "--size", f"{size}G", "--name", lv, vg])
            run_cmd_safe(["lvdisplay", f"{vg}/{lv}"])
            success("Logical volume created.")

        elif choice == 9:
            run_cmd_safe(["lvdisplay"])

        elif choice == 10:
            vg = input("  Volume group name: ")
            lv = input("  Logical volume name: ")
            run_cmd_safe(["lvdisplay", f"{vg}/{lv}"])

        elif choice == 11:
            vg = input("  Volume group name: ")
            lv = input("  Logical volume name: ")
            run_cmd_safe(["mkfs.ext4", f"/dev/{vg}/{lv}"])
            success("Logical volume formatted.")

        elif choice == 12:
            _mount_volume()

        elif choice == 13:
            size = input("  GB to extend: ")
            vg = input("  Volume group name: ")
            lv = input("  Logical volume name: ")
            run_cmd_safe(["lvextend", "--size", f"+{size}G", f"/dev/{vg}/{lv}"])
            success("Logical volume extended. Run option 14 to resize the filesystem.")

        elif choice == 14:
            vg = input("  Volume group name: ")
            lv = input("  Logical volume name: ")
            run_cmd_safe(["resize2fs", f"/dev/{vg}/{lv}"])
            success("Partition resized.")

        elif choice == 15:
            vg = input("  Volume group name: ")
            disk = input("  Disk name: ")
            run_cmd_safe(["vgextend", vg, disk])
            success("Volume group extended.")

        elif choice == 16:
            break
        else:
            error("Invalid choice.")

        pause()
        clear_screen()
