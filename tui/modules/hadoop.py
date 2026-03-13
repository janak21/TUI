"""Hadoop module — installation, configuration, and cluster management."""

from tui.utils import (
    banner, clear_screen, error, get_choice, info, pause,
    print_menu, run_cmd_safe, separator, success,
)


def _install_hadoop() -> None:
    info("Installing Hadoop (and Java dependency)...")
    run_cmd_safe([
        "curl",
        "https://archive.apache.org/dist/hadoop/core/hadoop-1.2.1/hadoop-1.2.1-1.x86_64.rpm",
        "--output", "hadoop-1.2.1-1.x86_64.rpm",
    ])
    run_cmd_safe(["sudo", "rpm", "-i", "hadoop-1.2.1-1.x86_64.rpm", "--force"])
    success("Hadoop installed.")


def _configure_node() -> None:
    while True:
        print_menu("Configure Node", [
            "Master node",
            "Slave node",
            "Back",
        ])
        choice = get_choice()
        if choice is None:
            continue
        if choice == 1:
            ip = input("  Master IP: ")
            fn = input("  Data folder name: ")
            run_cmd_safe(["mkdir", "-p", f"/{fn}"])
            hdfs = f"<configuration><property><name>dfs.name.dir</name><value>/{fn}</value></property></configuration>"
            core = f"<configuration><property><name>fs.default.name</name><value>hdfs://{ip}:9001</value></property></configuration>"
            with open("/etc/hadoop/hdfs-site.xml", "w") as f:
                f.write(hdfs)
            with open("/etc/hadoop/core-site.xml", "w") as f:
                f.write(core)
            info("Starting Hadoop master node...")
            run_cmd_safe(["hadoop", "namenode", "-format"])
            run_cmd_safe(["hadoop-daemon.sh", "start", "namenode"])
            run_cmd_safe(["jps"])
            success("Master node configured.")
        elif choice == 2:
            ip = input("  Master IP: ")
            fn = input("  Data folder name: ")
            run_cmd_safe(["mkdir", "-p", f"/{fn}"])
            hdfs = f"<configuration><property><name>dfs.data.dir</name><value>/{fn}</value></property></configuration>"
            core = f"<configuration><property><name>fs.default.name</name><value>hdfs://{ip}:9001</value></property></configuration>"
            with open("/etc/hadoop/hdfs-site.xml", "w") as f:
                f.write(hdfs)
            with open("/etc/hadoop/core-site.xml", "w") as f:
                f.write(core)
            info("Starting Hadoop slave node...")
            run_cmd_safe(["hadoop-daemon.sh", "start", "datanode"])
            run_cmd_safe(["jps"])
            success("Slave node configured.")
        else:
            break


def _system_info() -> None:
    while True:
        print_menu("System Info", [
            "Disk space",
            "RAM usage",
            "CPU info",
            "Back",
        ])
        choice = get_choice()
        if choice is None:
            continue
        if choice == 1:
            clear_screen()
            run_cmd_safe(["df", "-hT"])
        elif choice == 2:
            clear_screen()
            run_cmd_safe(["free", "-m"])
        elif choice == 3:
            clear_screen()
            run_cmd_safe(["lscpu"])
        else:
            break


def _cluster_status() -> None:
    while True:
        print_menu("Cluster Status", [
            "Detailed cluster report",
            "Summary cluster report",
            "Back",
        ])
        choice = get_choice()
        if choice is None:
            continue
        if choice == 1:
            clear_screen()
            run_cmd_safe(["hadoop", "dfsadmin", "-report"])
        elif choice == 2:
            clear_screen()
            run_cmd_safe(["hadoop", "dfsadmin", "-report"])
        else:
            break


def _cluster_operations() -> None:
    while True:
        print_menu("Cluster File Operations", [
            "Upload file to cluster",
            "Create file in cluster",
            "Remove file from cluster",
            "Upload with custom block size",
            "Hadoop filesystem help",
            "Back",
        ])
        choice = get_choice()
        if choice is None:
            continue
        if choice == 1:
            fn = input("  File path to upload: ")
            run_cmd_safe(["hadoop", "fs", "-put", fn, "/"])
            run_cmd_safe(["hadoop", "fs", "-ls", "/"])
            success("File uploaded.")
        elif choice == 2:
            fn = input("  Filename to create: ")
            run_cmd_safe(["hadoop", "fs", "-touchz", f"/{fn}"])
            run_cmd_safe(["hadoop", "fs", "-ls", "/"])
            success("File created.")
        elif choice == 3:
            fn = input("  Filename to remove: ")
            run_cmd_safe(["hadoop", "fs", "-rm", f"/{fn}"])
            run_cmd_safe(["hadoop", "fs", "-ls", "/"])
            success("File removed.")
        elif choice == 4:
            bs = input("  Block size (bytes): ")
            fn = input("  File path: ")
            run_cmd_safe(["hadoop", "fs", f"-Ddfs.block.size={bs}", "-put", fn, "/"])
            run_cmd_safe(["hadoop", "fs", "-ls", "/"])
            success(f"File uploaded with block size {bs}.")
        elif choice == 5:
            run_cmd_safe(["hadoop", "fs"])
        else:
            break


def run() -> None:
    while True:
        clear_screen()
        banner("Hadoop")
        separator()
        print_menu("Hadoop", [
            "Install Hadoop",
            "Check Hadoop version",
            "Configure Master/Slave node",
            "Test network connectivity",
            "System info (disk, RAM, CPU)",
            "Start Hadoop",
            "Cluster status",
            "Cluster file operations",
            "About Hadoop",
            "Return to main menu",
        ])

        choice = get_choice()
        if choice is None:
            continue

        if choice == 1:
            _install_hadoop()
        elif choice == 2:
            run_cmd_safe(["hadoop", "version"])
        elif choice == 3:
            _configure_node()
        elif choice == 4:
            run_cmd_safe(["ping", "-c", "5", "8.8.8.8"])
        elif choice == 5:
            _system_info()
        elif choice == 6:
            run_cmd_safe(["hadoop", "namenode", "-format"])
            run_cmd_safe(["hadoop-daemon.sh", "start", "namenode"])
            run_cmd_safe(["jps"])
        elif choice == 7:
            _cluster_status()
        elif choice == 8:
            _cluster_operations()
        elif choice == 9:
            from tui.utils import console
            console.print("""
[bold]Apache Hadoop[/bold] is an open-source framework for distributed processing of
large data sets across clusters of computers.

[bold cyan]Core Components:[/bold cyan]
  • [cyan]HDFS[/cyan]       — Distributed file system
  • [cyan]YARN[/cyan]       — Job scheduling & cluster resource management
  • [cyan]MapReduce[/cyan]  — Parallel processing of large data sets
  • [cyan]Ozone[/cyan]      — Object store

[bold cyan]Key Benefits:[/bold cyan]
  • [green]Scalable[/green]        — Add nodes without changing application logic
  • [green]Fault-tolerant[/green]  — Data replicated across nodes for resilience
""")
        elif choice == 10:
            break
        else:
            error("Invalid choice.")

        pause()
