"""AWS module - CLI installation and service management."""

from tui.utils import (
    banner, clear_screen, get_choice, pause, run_cmd_safe,
    separator, set_color,
)


def _install_cli():
    while True:
        print(
            "\n    Press 1: Windows"
            "\n    Press 2: Mac"
            "\n    Press 3: Linux"
            "\n    Press 4: Back\n"
        )
        choice = get_choice("Enter your OS: ")
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
        elif choice == 4:
            break
        else:
            print("Invalid option.")
        pause()
        clear_screen()


def _ec2_instances():
    print("""
    --- Instances ---
    Press 1: Launch new instance
    Press 2: View instances
    Press 3: Start instance
    Press 4: Stop instance
    Press 5: Terminate instance
    Press 6: Reboot instance
    Press 7: Back
    """)
    choice = get_choice()
    if choice is None:
        return
    if choice == 1:
        img_id = input("Enter image ID: ")
        ins_type = input("Enter instance type: ")
        key_name = input("Enter key name: ")
        sg_id = input("Enter security group ID: ")
        count = input("Enter number of instances: ")
        subnet_id = input("Enter subnet ID: ")
        run_cmd_safe([
            "aws", "ec2", "run-instances",
            "--image-id", img_id,
            "--instance-type", ins_type,
            "--key-name", key_name,
            "--security-group-ids", sg_id,
            "--count", count,
            "--subnet-id", subnet_id,
        ])
    elif choice == 2:
        run_cmd_safe(["aws", "ec2", "describe-instances"])
    elif choice == 3:
        inst = input("Enter Instance ID: ")
        run_cmd_safe(["aws", "ec2", "start-instances", "--instance-ids", inst])
    elif choice == 4:
        inst = input("Enter Instance ID: ")
        run_cmd_safe(["aws", "ec2", "stop-instances", "--instance-ids", inst])
    elif choice == 5:
        inst = input("Enter Instance ID: ")
        run_cmd_safe(["aws", "ec2", "terminate-instances", "--instance-ids", inst])
    elif choice == 6:
        inst = input("Enter Instance ID: ")
        run_cmd_safe(["aws", "ec2", "reboot-instances", "--instance-ids", inst])
    elif choice == 7:
        return
    pause()
    clear_screen()


def _ec2_volumes():
    print("""
    --- Volumes (EBS) ---
    Press 1: Create volume
    Press 2: View volumes
    Press 3: Attach volume
    Press 4: Detach volume
    Press 5: Force detach volume
    Press 6: Delete volume
    Press 7: Back
    """)
    while True:
        choice = get_choice()
        if choice is None:
            continue
        if choice == 1:
            zone = input("Enter availability zone (e.g. ap-south-1a): ")
            vtype = input("Enter volume type (e.g. gp2): ")
            size = input("Enter EBS volume size: ")
            run_cmd_safe([
                "aws", "ec2", "create-volume",
                "--availability-zone", zone,
                "--volume-type", vtype,
                "--size", size,
            ])
        elif choice == 2:
            run_cmd_safe(["aws", "ec2", "describe-volumes"])
        elif choice == 3:
            iid = input("Enter Instance ID: ")
            vid = input("Enter Volume ID: ")
            run_cmd_safe(["aws", "ec2", "attach-volume", "--instance-id", iid, "--volume-id", vid])
        elif choice == 4:
            iid = input("Enter Instance ID: ")
            vid = input("Enter Volume ID: ")
            run_cmd_safe(["aws", "ec2", "detach-volume", "--instance-id", iid, "--volume-id", vid])
        elif choice == 5:
            iid = input("Enter Instance ID: ")
            vid = input("Enter Volume ID: ")
            run_cmd_safe(["aws", "ec2", "detach-volume", "--force", "--instance-id", iid, "--volume-id", vid])
        elif choice == 6:
            vid = input("Enter Volume ID: ")
            run_cmd_safe(["aws", "ec2", "delete-volume", "--volume-id", vid])
        elif choice == 7:
            break
        else:
            print("Invalid choice.")
        pause()
        clear_screen()


def _ec2_security_groups():
    print("""
    --- Security Groups ---
    Press 1: Create security group
    Press 2: View all security groups
    Press 3: View single security group
    Press 4: Delete security group
    Press 5: Back
    """)
    while True:
        choice = get_choice()
        if choice is None:
            continue
        if choice == 1:
            name = input("Enter security group name: ")
            desc = input("Enter description: ")
            run_cmd_safe(["aws", "ec2", "create-security-group", "--group-name", name, "--description", desc])
        elif choice == 2:
            run_cmd_safe(["aws", "ec2", "describe-security-groups"])
        elif choice == 3:
            name = input("Enter security group name: ")
            run_cmd_safe(["aws", "ec2", "describe-security-groups", "--group-name", name])
        elif choice == 4:
            name = input("Enter security group name: ")
            run_cmd_safe(["aws", "ec2", "delete-security-group", "--group-name", name])
        else:
            break
        pause()
        clear_screen()


def _ec2_key_pairs():
    print("""
    --- Key Pairs ---
    Press 1: Create key pair
    Press 2: View all key pairs
    Press 3: View single key pair
    Press 4: Delete key pair
    Press 5: Back
    """)
    while True:
        choice = get_choice()
        if choice is None:
            continue
        if choice == 1:
            name = input("Enter key name: ")
            run_cmd_safe(["aws", "ec2", "create-key-pair", "--key-name", name])
        elif choice == 2:
            run_cmd_safe(["aws", "ec2", "describe-key-pairs"])
        elif choice == 3:
            name = input("Enter key name: ")
            run_cmd_safe(["aws", "ec2", "describe-key-pairs", "--key-name", name])
        elif choice == 4:
            name = input("Enter key name: ")
            run_cmd_safe(["aws", "ec2", "delete-key-pair", "--key-name", name])
        else:
            break


def _ec2_services():
    print("""
    --- EC2 Services ---
    Press 1: Instances
    Press 2: Volumes (EBS)
    Press 3: Security Groups
    Press 4: Key Pairs
    Press 5: Back
    """)
    choice = get_choice()
    if choice is None:
        return
    if choice == 1:
        _ec2_instances()
    elif choice == 2:
        _ec2_volumes()
    elif choice == 3:
        _ec2_security_groups()
    elif choice == 4:
        _ec2_key_pairs()


def _s3_services():
    print("""
    --- S3 Services ---
    Press 1: Create bucket
    Press 2: List buckets
    Press 3: Delete bucket
    Press 4: Empty bucket
    Press 5: Upload to bucket
    Press 6: Back
    """)
    while True:
        choice = get_choice()
        if choice is None:
            continue
        if choice == 1:
            name = input("Enter unique bucket name: ")
            region = input("Enter region (e.g. ap-south-1): ")
            acl = input("Enter access (e.g. public-read): ")
            run_cmd_safe([
                "aws", "s3api", "create-bucket",
                "--bucket", name,
                "--region", region,
                "--acl", acl,
                "--create-bucket-configuration", f"LocationConstraint={region}",
            ])
        elif choice == 2:
            run_cmd_safe(["aws", "s3api", "list-buckets"])
        elif choice == 3:
            print("Note: Bucket must be empty before deletion. Use option 4 to empty it first.")
            name = input("Enter bucket name: ")
            run_cmd_safe(["aws", "s3api", "delete-bucket", "--bucket", name])
        elif choice == 4:
            print("Warning: This will remove ALL objects from the bucket!")
            name = input("Enter bucket name: ")
            run_cmd_safe(["aws", "s3", "rm", f"s3://{name}", "--recursive"])
        elif choice == 5:
            location = input("Enter local file path: ")
            name = input("Enter bucket name: ")
            acl = input("Enter access (e.g. public-read): ")
            run_cmd_safe(["aws", "s3", "cp", location, f"s3://{name}", "--acl", acl])
        elif choice == 6:
            break
        else:
            print("Invalid choice.")
        pause()
        clear_screen()


def _cloudfront_services():
    print("""
    --- CloudFront Services ---
    Press 1: Create distribution
    Press 2: List distributions
    Press 3: View single distribution
    Press 4: Delete distribution
    Press 5: Back
    """)
    while True:
        choice = get_choice()
        if choice is None:
            continue
        if choice == 1:
            origin = input("Enter bucket name for distribution (e.g. mybucket): ")
            run_cmd_safe([
                "aws", "cloudfront", "create-distribution",
                "--origin-domain-name", f"{origin}.s3.amazonaws.com",
            ])
        elif choice == 2:
            run_cmd_safe(["aws", "cloudfront", "list-distributions"])
        elif choice == 3:
            dist_id = input("Enter distribution ID: ")
            run_cmd_safe(["aws", "cloudfront", "get-distribution", "--id", dist_id])
        elif choice == 4:
            print("Note: Distribution must be disabled before deletion.")
            dist_id = input("Enter distribution ID: ")
            etag = input("Enter ETag (find via option 3): ")
            run_cmd_safe(["aws", "cloudfront", "delete-distribution", "--id", dist_id, "--if-match", etag])
        elif choice == 5:
            break
        else:
            print("Invalid choice.")
        clear_screen()


def run():
    """Main AWS menu."""
    while True:
        clear_screen()
        banner("AWS")
        set_color("green")
        separator()
        print("""
        Press 1: Install AWS CLI
        Press 2: Check AWS version
        Press 3: Configure IAM credentials
        Press 4: EC2 Services
        Press 5: S3 Services
        Press 6: CloudFront Services
        Press 7: Return to main menu
        """)
        separator()
        set_color("white")

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
            print("Invalid choice.")

        pause()
        clear_screen()
