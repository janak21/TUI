"""AWS module — CLI installation and service management."""

from tui.utils import (
    banner, clear_screen, error, get_choice, info, pause,
    print_menu, run_cmd_safe, separator, success, warn,
)


def _install_cli() -> None:
    while True:
        print_menu("Install AWS CLI", ["Windows", "Mac", "Linux", "Back"])
        choice = get_choice("Enter your OS")
        if choice is None:
            continue
        if choice == 1:
            run_cmd_safe(["pip3", "install", "awscli", "--upgrade", "--user"])
        elif choice == 2:
            run_cmd_safe(["curl", "https://s3.amazonaws.com/aws-cli/awscli-bundle.zip", "-o", "awscli-bundle.zip"])
            run_cmd_safe(["unzip", "awscli-bundle.zip"])
            run_cmd_safe(["sudo", "./awscli-bundle/install", "-i", "/usr/local/aws", "-b", "/usr/local/bin/aws"])
        elif choice == 3:
            run_cmd_safe(["curl", "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip", "-o", "awscliv2.zip"])
            run_cmd_safe(["unzip", "awscliv2.zip"])
            run_cmd_safe(["sudo", "./aws/install"])
            success("AWS CLI installed.")
        elif choice == 4:
            break
        else:
            error("Invalid option.")
        pause()
        clear_screen()


def _ec2_instances() -> None:
    print_menu("EC2 Instances", [
        "Launch new instance",
        "View instances",
        "Start instance",
        "Stop instance",
        "Terminate instance",
        "Reboot instance",
        "Back",
    ])
    choice = get_choice()
    if choice is None:
        return
    if choice == 1:
        img_id   = input("  Image ID: ")
        ins_type = input("  Instance type: ")
        key_name = input("  Key name: ")
        sg_id    = input("  Security group ID: ")
        count    = input("  Number of instances: ")
        subnet   = input("  Subnet ID: ")
        run_cmd_safe(["aws", "ec2", "run-instances",
            "--image-id", img_id, "--instance-type", ins_type,
            "--key-name", key_name, "--security-group-ids", sg_id,
            "--count", count, "--subnet-id", subnet])
    elif choice == 2:
        run_cmd_safe(["aws", "ec2", "describe-instances"])
    elif choice == 3:
        run_cmd_safe(["aws", "ec2", "start-instances", "--instance-ids", input("  Instance ID: ")])
    elif choice == 4:
        run_cmd_safe(["aws", "ec2", "stop-instances", "--instance-ids", input("  Instance ID: ")])
    elif choice == 5:
        run_cmd_safe(["aws", "ec2", "terminate-instances", "--instance-ids", input("  Instance ID: ")])
    elif choice == 6:
        run_cmd_safe(["aws", "ec2", "reboot-instances", "--instance-ids", input("  Instance ID: ")])
    pause()
    clear_screen()


def _ec2_volumes() -> None:
    while True:
        print_menu("EBS Volumes", [
            "Create volume", "View volumes", "Attach volume",
            "Detach volume", "Force detach volume", "Delete volume", "Back",
        ])
        choice = get_choice()
        if choice is None:
            continue
        if choice == 1:
            zone  = input("  Availability zone (e.g. ap-south-1a): ")
            vtype = input("  Volume type (e.g. gp2): ")
            size  = input("  Size (GiB): ")
            run_cmd_safe(["aws", "ec2", "create-volume",
                "--availability-zone", zone, "--volume-type", vtype, "--size", size])
        elif choice == 2:
            run_cmd_safe(["aws", "ec2", "describe-volumes"])
        elif choice == 3:
            iid = input("  Instance ID: ")
            vid = input("  Volume ID: ")
            run_cmd_safe(["aws", "ec2", "attach-volume", "--instance-id", iid, "--volume-id", vid])
        elif choice == 4:
            iid = input("  Instance ID: ")
            vid = input("  Volume ID: ")
            run_cmd_safe(["aws", "ec2", "detach-volume", "--instance-id", iid, "--volume-id", vid])
        elif choice == 5:
            iid = input("  Instance ID: ")
            vid = input("  Volume ID: ")
            run_cmd_safe(["aws", "ec2", "detach-volume", "--force", "--instance-id", iid, "--volume-id", vid])
        elif choice == 6:
            run_cmd_safe(["aws", "ec2", "delete-volume", "--volume-id", input("  Volume ID: ")])
        elif choice == 7:
            break
        else:
            error("Invalid choice.")
        pause()
        clear_screen()


def _ec2_security_groups() -> None:
    while True:
        print_menu("Security Groups", [
            "Create security group", "View all security groups",
            "View single security group", "Delete security group", "Back",
        ])
        choice = get_choice()
        if choice is None:
            continue
        if choice == 1:
            name = input("  Group name: ")
            desc = input("  Description: ")
            run_cmd_safe(["aws", "ec2", "create-security-group", "--group-name", name, "--description", desc])
        elif choice == 2:
            run_cmd_safe(["aws", "ec2", "describe-security-groups"])
        elif choice == 3:
            run_cmd_safe(["aws", "ec2", "describe-security-groups", "--group-name", input("  Group name: ")])
        elif choice == 4:
            run_cmd_safe(["aws", "ec2", "delete-security-group", "--group-name", input("  Group name: ")])
        else:
            break
        pause()
        clear_screen()


def _ec2_key_pairs() -> None:
    while True:
        print_menu("Key Pairs", [
            "Create key pair", "View all key pairs",
            "View single key pair", "Delete key pair", "Back",
        ])
        choice = get_choice()
        if choice is None:
            continue
        if choice == 1:
            run_cmd_safe(["aws", "ec2", "create-key-pair", "--key-name", input("  Key name: ")])
        elif choice == 2:
            run_cmd_safe(["aws", "ec2", "describe-key-pairs"])
        elif choice == 3:
            run_cmd_safe(["aws", "ec2", "describe-key-pairs", "--key-name", input("  Key name: ")])
        elif choice == 4:
            run_cmd_safe(["aws", "ec2", "delete-key-pair", "--key-name", input("  Key name: ")])
        elif choice == 5:
            break
        else:
            error("Invalid choice.")


def _ec2_services() -> None:
    while True:
        print_menu("EC2 Services", [
            "Instances", "Volumes (EBS)",
            "Security Groups", "Key Pairs", "Back",
        ])
        choice = get_choice()
        if choice is None:
            continue
        if choice == 1:
            _ec2_instances()
        elif choice == 2:
            _ec2_volumes()
        elif choice == 3:
            _ec2_security_groups()
        elif choice == 4:
            _ec2_key_pairs()
        elif choice == 5:
            break
        else:
            error("Invalid choice.")


def _s3_services() -> None:
    while True:
        print_menu("S3 Services", [
            "Create bucket", "List buckets", "Delete bucket",
            "Empty bucket", "Upload to bucket", "Back",
        ])
        choice = get_choice()
        if choice is None:
            continue
        if choice == 1:
            name   = input("  Bucket name: ")
            region = input("  Region (e.g. ap-south-1): ")
            acl    = input("  Access (e.g. public-read): ")
            run_cmd_safe(["aws", "s3api", "create-bucket",
                "--bucket", name, "--region", region, "--acl", acl,
                "--create-bucket-configuration", f"LocationConstraint={region}"])
        elif choice == 2:
            run_cmd_safe(["aws", "s3api", "list-buckets"])
        elif choice == 3:
            warn("Bucket must be empty before deletion. Use option 4 first.")
            run_cmd_safe(["aws", "s3api", "delete-bucket", "--bucket", input("  Bucket name: ")])
        elif choice == 4:
            warn("This will remove ALL objects from the bucket!")
            name = input("  Bucket name: ")
            run_cmd_safe(["aws", "s3", "rm", f"s3://{name}", "--recursive"])
        elif choice == 5:
            loc  = input("  Local file path: ")
            name = input("  Bucket name: ")
            acl  = input("  Access (e.g. public-read): ")
            run_cmd_safe(["aws", "s3", "cp", loc, f"s3://{name}", "--acl", acl])
        elif choice == 6:
            break
        else:
            error("Invalid choice.")
        pause()
        clear_screen()


def _cloudfront_services() -> None:
    while True:
        print_menu("CloudFront", [
            "Create distribution", "List distributions",
            "View single distribution", "Delete distribution", "Back",
        ])
        choice = get_choice()
        if choice is None:
            continue
        if choice == 1:
            origin = input("  S3 bucket name: ")
            run_cmd_safe(["aws", "cloudfront", "create-distribution",
                "--origin-domain-name", f"{origin}.s3.amazonaws.com"])
        elif choice == 2:
            run_cmd_safe(["aws", "cloudfront", "list-distributions"])
        elif choice == 3:
            run_cmd_safe(["aws", "cloudfront", "get-distribution", "--id", input("  Distribution ID: ")])
        elif choice == 4:
            warn("Distribution must be disabled before deletion.")
            dist_id = input("  Distribution ID: ")
            etag    = input("  ETag (from option 3): ")
            run_cmd_safe(["aws", "cloudfront", "delete-distribution", "--id", dist_id, "--if-match", etag])
        elif choice == 5:
            break
        else:
            error("Invalid choice.")
        clear_screen()


def run() -> None:
    while True:
        clear_screen()
        banner("AWS")
        separator()
        print_menu("AWS", [
            "Install AWS CLI",
            "Check AWS version",
            "Configure IAM credentials",
            "EC2 Services",
            "S3 Services",
            "CloudFront Services",
            "Return to main menu",
        ])

        choice = get_choice()
        if choice is None:
            continue

        if choice == 1:
            _install_cli()
        elif choice == 2:
            run_cmd_safe(["aws", "--version"])
        elif choice == 3:
            run_cmd_safe(["aws", "configure"])
        elif choice == 4:
            _ec2_services()
        elif choice == 5:
            _s3_services()
        elif choice == 6:
            _cloudfront_services()
        elif choice == 7:
            break
        else:
            error("Invalid choice.")

        pause()
        clear_screen()
