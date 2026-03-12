"""Hadoop module - installation, configuration, and cluster management."""

from tui.utils import (
    banner, clear_screen, get_choice, pause, run_cmd_safe,
    safe_quote, separator, set_color,
)


def _install_hadoop():
    print("Hadoop has a dependency on Java... installing it too.")
    run_cmd_safe([
        "curl",
        "https://archive.apache.org/dist/hadoop/core/hadoop-1.2.1/hadoop-1.2.1-1.x86_64.rpm",
        "--output", "hadoop-1.2.1-1.x86_64.rpm",
    ])
    run_cmd_safe(["sudo", "rpm", "-i", "hadoop-1.2.1-1.x86_64.rpm", "--force"])


def _check_version():
    set_color("grey")
    print("If installed, you can check the version:")
    run_cmd_safe(["hadoop", "version"])
    pause()


def _configure_node():
    print(
        "\n    Press 1: Master node"
        "\n    Press 2: Slave node"
        "\n    Press 3: Back to Hadoop menu\n"
    )
    while True:
        choice = get_choice()
        if choice is None:
            continue
        if choice == 1:
            set_color("grey")
            ip = input("Enter your Master IP: ")
            fn = input("Name of the folder (to store shared data): ")
            safe_fn = safe_quote(fn)
            safe_ip = safe_quote(ip)
            run_cmd_safe(["mkdir", "-p", f"/{fn}"])
            hdfs_config = f"<configuration><property><name>dfs.name.dir</name><value>/{fn}</value></property></configuration>"
            core_config = f"<configuration><property><name>fs.default.name</name><value>hdfs://{ip}:9001</value></property></configuration>"
            with open("/etc/hadoop/hdfs-site.xml", "w") as f:
                f.write(hdfs_config)
            with open("/etc/hadoop/core-site.xml", "w") as f:
                f.write(core_config)
            print("Please wait... Hadoop Master is getting ready...")
            run_cmd_safe(["hadoop", "namenode", "-format"])
            run_cmd_safe(["hadoop-daemon.sh", "start", "namenode"])
            run_cmd_safe(["jps"])
        elif choice == 2:
            set_color("grey")
            ip = input("Enter your Master IP: ")
            fn = input("Name of the folder (to store shared data): ")
            run_cmd_safe(["mkdir", "-p", f"/{fn}"])
            hdfs_config = f"<configuration><property><name>dfs.data.dir</name><value>/{fn}</value></property></configuration>"
            core_config = f"<configuration><property><name>fs.default.name</name><value>hdfs://{ip}:9001</value></property></configuration>"
            with open("/etc/hadoop/hdfs-site.xml", "w") as f:
                f.write(hdfs_config)
            with open("/etc/hadoop/core-site.xml", "w") as f:
                f.write(core_config)
            print("Please wait... Hadoop Slave node is getting ready...")
            run_cmd_safe(["hadoop-daemon.sh", "start", "datanode"])
            run_cmd_safe(["jps"])
        else:
            break


def _test_network():
    set_color("cyan")
    run_cmd_safe(["ping", "-c", "5", "8.8.8.8"])


def _system_info():
    while True:
        print(
            "\n    Press 1: Disk Space"
            "\n    Press 2: RAM Usage"
            "\n    Press 3: CPU Info"
            "\n    Press 4: Back\n"
        )
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


def _start_hadoop():
    set_color("grey")
    run_cmd_safe(["hadoop", "namenode", "-format"])
    run_cmd_safe(["hadoop-daemon.sh", "start", "namenode"])
    set_color("white")
    print("Hadoop STATUS:")
    run_cmd_safe(["jps"])


def _cluster_status():
    while True:
        print(
            "\n    Press 1: Detailed cluster view"
            "\n    Press 2: Summary cluster view"
            "\n    Press 3: Back\n"
        )
        choice = get_choice()
        if choice is None:
            continue
        if choice == 1:
            clear_screen()
            set_color("grey")
            run_cmd_safe(["hadoop", "dfsadmin", "-report"])
        elif choice == 2:
            set_color("magenta")
            clear_screen()
            run_cmd_safe(["hadoop", "dfsadmin", "-report"])
        else:
            break


def _cluster_operations():
    while True:
        print(
            "\n    Press 1: Upload file to cluster"
            "\n    Press 2: Create file in cluster"
            "\n    Press 3: Remove file from cluster"
            "\n    Press 4: Upload file with custom block size"
            "\n    Press 5: Hadoop filesystem help"
            "\n    Press 6: Back\n"
        )
        choice = get_choice()
        if choice is None:
            continue
        if choice == 1:
            clear_screen()
            set_color("yellow")
            fn = input("Enter your filename (include path): ")
            run_cmd_safe(["hadoop", "fs", "-put", fn, "/"])
            print("File uploaded. Current files:")
            run_cmd_safe(["hadoop", "fs", "-ls", "/"])
        elif choice == 2:
            set_color("magenta")
            clear_screen()
            fn = input("Enter filename to create: ")
            run_cmd_safe(["hadoop", "fs", "-touchz", f"/{fn}"])
            print("File created.")
            run_cmd_safe(["hadoop", "fs", "-ls", "/"])
        elif choice == 3:
            set_color("white")
            clear_screen()
            fn = input("Enter filename to remove: ")
            run_cmd_safe(["hadoop", "fs", "-rm", f"/{fn}"])
            print("File removed.")
            run_cmd_safe(["hadoop", "fs", "-ls", "/"])
        elif choice == 4:
            set_color("green")
            clear_screen()
            bs = input("Enter block size (in bytes): ")
            fn = input("Enter filename (with path): ")
            run_cmd_safe(["hadoop", "fs", f"-Ddfs.block.size={bs}", "-put", fn, "/"])
            print(f"File uploaded with block size {bs}.")
            run_cmd_safe(["hadoop", "fs", "-ls", "/"])
        elif choice == 5:
            clear_screen()
            run_cmd_safe(["hadoop", "fs"])
        else:
            break


def _hadoop_info():
    print("""
    Apache Hadoop develops open-source software for reliable, scalable, distributed computing.

    The Apache Hadoop software library is a framework that allows for the distributed
    processing of large data sets across clusters of computers using simple programming
    models. It is designed to scale up from single servers to thousands of machines.

    Key Components:
      - Hadoop Common: Common utilities that support other Hadoop modules
      - HDFS: Distributed file system for high-throughput data access
      - YARN: Framework for job scheduling and cluster resource management
      - MapReduce: YARN-based system for parallel processing of large data sets
      - Ozone: Object store for Hadoop

    Key Benefits:
      - Scalability: Clusters can be scaled by adding nodes without application changes
      - Fault Tolerance: Data is replicated across nodes for resilience
    """)


def run():
    """Main Hadoop menu."""
    while True:
        clear_screen()
        separator()
        banner("Hadoop")
        set_color("green")
        print("""
        Press 1 : Install Hadoop
        Press 2 : Check Hadoop version
        Press 3 : Configure Master/Slave node
        Press 4 : Test network connectivity
        Press 5 : System info (disk, RAM, CPU)
        Press 6 : Start Hadoop
        Press 7 : Cluster status
        Press 8 : Cluster file operations
        Press 9 : About Hadoop
        Press 10: Return to main menu
        """)
        separator()
        set_color("white")

        choice = get_choice()
        if choice is None:
            continue

        if choice == 1:
            _install_hadoop()
        elif choice == 2:
            _check_version()
        elif choice == 3:
            _configure_node()
        elif choice == 4:
            _test_network()
        elif choice == 5:
            _system_info()
        elif choice == 6:
            _start_hadoop()
        elif choice == 7:
            _cluster_status()
        elif choice == 8:
            _cluster_operations()
        elif choice == 9:
            _hadoop_info()
        elif choice == 10:
            break
        else:
            print("Invalid choice.")

        pause()
