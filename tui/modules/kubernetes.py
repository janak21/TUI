"""Kubernetes module — cluster management, deployments, services, and pods."""

from tui.utils import (
    banner, clear_screen, error, get_choice, info, pause,
    print_menu, run_cmd_safe, separator, success, warn,
)


def _setup_cluster() -> None:
    while True:
        print_menu("Cluster Setup", [
            "Install kubectl",
            "Install Minikube (local single-node cluster)",
            "Install kind (Kubernetes in Docker)",
            "Install Helm",
            "Back",
        ])
        choice = get_choice()
        if choice is None:
            continue
        if choice == 1:
            info("Installing kubectl...")
            run_cmd_safe(["curl", "-LO",
                "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"])
            run_cmd_safe(["chmod", "+x", "kubectl"])
            run_cmd_safe(["sudo", "mv", "kubectl", "/usr/local/bin/kubectl"])
            run_cmd_safe(["kubectl", "version", "--client"])
            success("kubectl installed.")
        elif choice == 2:
            info("Installing Minikube...")
            run_cmd_safe(["curl", "-LO",
                "https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64"])
            run_cmd_safe(["sudo", "install", "minikube-linux-amd64", "/usr/local/bin/minikube"])
            run_cmd_safe(["minikube", "version"])
            success("Minikube installed.")
        elif choice == 3:
            info("Installing kind...")
            run_cmd_safe(["curl", "-Lo", "./kind",
                "https://kind.sigs.k8s.io/dl/latest/kind-linux-amd64"])
            run_cmd_safe(["chmod", "+x", "./kind"])
            run_cmd_safe(["sudo", "mv", "./kind", "/usr/local/bin/kind"])
            run_cmd_safe(["kind", "version"])
            success("kind installed.")
        elif choice == 4:
            info("Installing Helm...")
            run_cmd_safe(["curl", "-fsSL",
                "https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3",
                "-o", "get_helm.sh"])
            run_cmd_safe(["chmod", "+x", "get_helm.sh"])
            run_cmd_safe(["./get_helm.sh"])
            run_cmd_safe(["helm", "version"])
            success("Helm installed.")
        elif choice == 5:
            break
        else:
            error("Invalid choice.")
        pause()
        clear_screen()


def _minikube() -> None:
    while True:
        print_menu("Minikube", [
            "Start cluster",
            "Stop cluster",
            "Delete cluster",
            "Cluster status",
            "Open dashboard",
            "View cluster IP",
            "Back",
        ])
        choice = get_choice()
        if choice is None:
            continue
        if choice == 1:
            run_cmd_safe(["minikube", "start"])
            success("Cluster started.")
        elif choice == 2:
            run_cmd_safe(["minikube", "stop"])
            success("Cluster stopped.")
        elif choice == 3:
            run_cmd_safe(["minikube", "delete"])
            success("Cluster deleted.")
        elif choice == 4:
            run_cmd_safe(["minikube", "status"])
        elif choice == 5:
            run_cmd_safe(["minikube", "dashboard"])
        elif choice == 6:
            run_cmd_safe(["minikube", "ip"])
        elif choice == 7:
            break
        else:
            error("Invalid choice.")
        pause()
        clear_screen()


def _nodes() -> None:
    while True:
        print_menu("Nodes", [
            "List all nodes",
            "Describe a node",
            "Node resource usage (top)",
            "Cordon node (mark unschedulable)",
            "Uncordon node",
            "Drain node",
            "Back",
        ])
        choice = get_choice()
        if choice is None:
            continue
        if choice == 1:
            run_cmd_safe(["kubectl", "get", "nodes", "-o", "wide"])
        elif choice == 2:
            run_cmd_safe(["kubectl", "describe", "node", input("  Node name: ")])
        elif choice == 3:
            run_cmd_safe(["kubectl", "top", "nodes"])
        elif choice == 4:
            name = input("  Node name: ")
            run_cmd_safe(["kubectl", "cordon", name])
            success(f"Node {name} cordoned.")
        elif choice == 5:
            name = input("  Node name: ")
            run_cmd_safe(["kubectl", "uncordon", name])
            success(f"Node {name} uncordoned.")
        elif choice == 6:
            name = input("  Node name: ")
            run_cmd_safe(["kubectl", "drain", name, "--ignore-daemonsets", "--delete-emptydir-data"])
            success(f"Node {name} drained.")
        elif choice == 7:
            break
        else:
            error("Invalid choice.")
        pause()
        clear_screen()


def _namespaces() -> None:
    while True:
        print_menu("Namespaces", [
            "List namespaces",
            "Create namespace",
            "Delete namespace",
            "Describe namespace",
            "Back",
        ])
        choice = get_choice()
        if choice is None:
            continue
        if choice == 1:
            run_cmd_safe(["kubectl", "get", "namespaces"])
        elif choice == 2:
            name = input("  Namespace name: ")
            run_cmd_safe(["kubectl", "create", "namespace", name])
            success(f"Namespace '{name}' created.")
        elif choice == 3:
            name = input("  Namespace name: ")
            run_cmd_safe(["kubectl", "delete", "namespace", name])
            success(f"Namespace '{name}' deleted.")
        elif choice == 4:
            run_cmd_safe(["kubectl", "describe", "namespace", input("  Namespace name: ")])
        elif choice == 5:
            break
        else:
            error("Invalid choice.")
        pause()
        clear_screen()


def _deployments() -> None:
    while True:
        print_menu("Deployments", [
            "List deployments",
            "Create deployment",
            "Describe deployment",
            "Delete deployment",
            "Scale deployment",
            "Update image (rolling update)",
            "Rollout status",
            "Rollback deployment",
            "Pause rollout",
            "Resume rollout",
            "Back",
        ])
        choice = get_choice()
        if choice is None:
            continue

        ns = input("  Namespace (blank = 'default'): ").strip() or "default"

        if choice == 1:
            run_cmd_safe(["kubectl", "get", "deployments", "-n", ns, "-o", "wide"])
        elif choice == 2:
            name     = input("  Deployment name: ")
            image    = input("  Container image (e.g. nginx:latest): ")
            replicas = input("  Replicas (default 1): ").strip() or "1"
            run_cmd_safe(["kubectl", "create", "deployment", name,
                "--image", image, "--replicas", replicas, "-n", ns])
            success(f"Deployment '{name}' created.")
        elif choice == 3:
            run_cmd_safe(["kubectl", "describe", "deployment", input("  Deployment name: "), "-n", ns])
        elif choice == 4:
            name = input("  Deployment name: ")
            run_cmd_safe(["kubectl", "delete", "deployment", name, "-n", ns])
            success(f"Deployment '{name}' deleted.")
        elif choice == 5:
            name     = input("  Deployment name: ")
            replicas = input("  Desired replicas: ")
            run_cmd_safe(["kubectl", "scale", "deployment", name, f"--replicas={replicas}", "-n", ns])
            success(f"Scaled to {replicas} replicas.")
        elif choice == 6:
            name      = input("  Deployment name: ")
            container = input("  Container name: ")
            image     = input("  New image: ")
            run_cmd_safe(["kubectl", "set", "image",
                f"deployment/{name}", f"{container}={image}", "-n", ns])
            info("Rolling update triggered.")
        elif choice == 7:
            run_cmd_safe(["kubectl", "rollout", "status",
                f"deployment/{input('  Deployment name: ')}", "-n", ns])
        elif choice == 8:
            name = input("  Deployment name: ")
            run_cmd_safe(["kubectl", "rollout", "undo", f"deployment/{name}", "-n", ns])
            success("Rollback complete.")
        elif choice == 9:
            name = input("  Deployment name: ")
            run_cmd_safe(["kubectl", "rollout", "pause", f"deployment/{name}", "-n", ns])
            success("Rollout paused.")
        elif choice == 10:
            name = input("  Deployment name: ")
            run_cmd_safe(["kubectl", "rollout", "resume", f"deployment/{name}", "-n", ns])
            success("Rollout resumed.")
        elif choice == 11:
            break
        else:
            error("Invalid choice.")
        pause()
        clear_screen()


def _pods() -> None:
    while True:
        print_menu("Pods", [
            "List pods",
            "Describe pod",
            "View pod logs",
            "Follow pod logs (live)",
            "Execute command in pod",
            "Open shell in pod",
            "Delete pod",
            "Pod resource usage (top)",
            "Back",
        ])
        choice = get_choice()
        if choice is None:
            continue

        ns = input("  Namespace (blank = 'default'): ").strip() or "default"

        if choice == 1:
            run_cmd_safe(["kubectl", "get", "pods", "-n", ns, "-o", "wide"])
        elif choice == 2:
            run_cmd_safe(["kubectl", "describe", "pod", input("  Pod name: "), "-n", ns])
        elif choice == 3:
            run_cmd_safe(["kubectl", "logs", input("  Pod name: "), "-n", ns])
        elif choice == 4:
            run_cmd_safe(["kubectl", "logs", "-f", input("  Pod name: "), "-n", ns])
        elif choice == 5:
            name = input("  Pod name: ")
            cmd  = input("  Command to run (e.g. ls /): ")
            run_cmd_safe(["kubectl", "exec", name, "-n", ns, "--", *cmd.split()])
        elif choice == 6:
            run_cmd_safe(["kubectl", "exec", "-it", input("  Pod name: "), "-n", ns, "--", "/bin/sh"])
        elif choice == 7:
            name = input("  Pod name: ")
            run_cmd_safe(["kubectl", "delete", "pod", name, "-n", ns])
            success(f"Pod '{name}' deleted.")
        elif choice == 8:
            run_cmd_safe(["kubectl", "top", "pods", "-n", ns])
        elif choice == 9:
            break
        else:
            error("Invalid choice.")
        pause()
        clear_screen()


def _services() -> None:
    while True:
        print_menu("Services", [
            "List services",
            "Expose deployment as service",
            "Describe service",
            "Delete service",
            "Get service URL (Minikube)",
            "Back",
        ])
        choice = get_choice()
        if choice is None:
            continue

        ns = input("  Namespace (blank = 'default'): ").strip() or "default"

        if choice == 1:
            run_cmd_safe(["kubectl", "get", "services", "-n", ns])
        elif choice == 2:
            name     = input("  Deployment name: ")
            port     = input("  Port: ")
            svc_type = input("  Type (ClusterIP/NodePort/LoadBalancer): ").strip() or "ClusterIP"
            run_cmd_safe(["kubectl", "expose", "deployment", name,
                "--port", port, "--type", svc_type, "-n", ns])
            success(f"Service '{name}' created.")
        elif choice == 3:
            run_cmd_safe(["kubectl", "describe", "service", input("  Service name: "), "-n", ns])
        elif choice == 4:
            name = input("  Service name: ")
            run_cmd_safe(["kubectl", "delete", "service", name, "-n", ns])
            success(f"Service '{name}' deleted.")
        elif choice == 5:
            run_cmd_safe(["minikube", "service", input("  Service name: "), "-n", ns, "--url"])
        elif choice == 6:
            break
        else:
            error("Invalid choice.")
        pause()
        clear_screen()


def _config_secrets() -> None:
    while True:
        print_menu("ConfigMaps & Secrets", [
            "List ConfigMaps",
            "Create ConfigMap (from literal)",
            "Describe ConfigMap",
            "Delete ConfigMap",
            "List Secrets",
            "Create Secret (generic)",
            "Describe Secret",
            "Delete Secret",
            "Back",
        ])
        choice = get_choice()
        if choice is None:
            continue

        ns = input("  Namespace (blank = 'default'): ").strip() or "default"

        if choice == 1:
            run_cmd_safe(["kubectl", "get", "configmaps", "-n", ns])
        elif choice == 2:
            name  = input("  ConfigMap name: ")
            key   = input("  Key: ")
            value = input("  Value: ")
            run_cmd_safe(["kubectl", "create", "configmap", name,
                f"--from-literal={key}={value}", "-n", ns])
            success(f"ConfigMap '{name}' created.")
        elif choice == 3:
            run_cmd_safe(["kubectl", "describe", "configmap", input("  ConfigMap name: "), "-n", ns])
        elif choice == 4:
            name = input("  ConfigMap name: ")
            run_cmd_safe(["kubectl", "delete", "configmap", name, "-n", ns])
            success(f"ConfigMap '{name}' deleted.")
        elif choice == 5:
            run_cmd_safe(["kubectl", "get", "secrets", "-n", ns])
        elif choice == 6:
            name  = input("  Secret name: ")
            key   = input("  Key: ")
            value = input("  Value: ")
            run_cmd_safe(["kubectl", "create", "secret", "generic", name,
                f"--from-literal={key}={value}", "-n", ns])
            success(f"Secret '{name}' created.")
        elif choice == 7:
            run_cmd_safe(["kubectl", "describe", "secret", input("  Secret name: "), "-n", ns])
        elif choice == 8:
            name = input("  Secret name: ")
            run_cmd_safe(["kubectl", "delete", "secret", name, "-n", ns])
            success(f"Secret '{name}' deleted.")
        elif choice == 9:
            break
        else:
            error("Invalid choice.")
        pause()
        clear_screen()


def _manifests() -> None:
    while True:
        print_menu("YAML Manifests & Contexts", [
            "Apply manifest (kubectl apply -f)",
            "Delete resources from manifest",
            "Dry-run apply (validate only)",
            "View cluster info / current context",
            "Switch context",
            "List all contexts",
            "Back",
        ])
        choice = get_choice()
        if choice is None:
            continue
        if choice == 1:
            path = input("  Path to YAML file or directory: ")
            run_cmd_safe(["kubectl", "apply", "-f", path])
        elif choice == 2:
            path = input("  Path to YAML file or directory: ")
            run_cmd_safe(["kubectl", "delete", "-f", path])
        elif choice == 3:
            path = input("  Path to YAML file or directory: ")
            run_cmd_safe(["kubectl", "apply", "--dry-run=client", "-f", path])
        elif choice == 4:
            run_cmd_safe(["kubectl", "cluster-info"])
        elif choice == 5:
            name = input("  Context name: ")
            run_cmd_safe(["kubectl", "config", "use-context", name])
            success(f"Switched to context '{name}'.")
        elif choice == 6:
            run_cmd_safe(["kubectl", "config", "get-contexts"])
        elif choice == 7:
            break
        else:
            error("Invalid choice.")
        pause()
        clear_screen()


def _helm() -> None:
    while True:
        print_menu("Helm", [
            "List installed releases",
            "Add Helm repo",
            "Update repos",
            "Search a chart",
            "Install a chart",
            "Upgrade a release",
            "Uninstall a release",
            "Back",
        ])
        choice = get_choice()
        if choice is None:
            continue
        if choice == 1:
            ns = input("  Namespace (blank = all): ").strip()
            run_cmd_safe(["helm", "list"] + (["-n", ns] if ns else ["-A"]))
        elif choice == 2:
            name = input("  Repo name: ")
            url  = input("  Repo URL: ")
            run_cmd_safe(["helm", "repo", "add", name, url])
            success(f"Repo '{name}' added.")
        elif choice == 3:
            run_cmd_safe(["helm", "repo", "update"])
            success("Repos updated.")
        elif choice == 4:
            run_cmd_safe(["helm", "search", "repo", input("  Search term: ")])
        elif choice == 5:
            release = input("  Release name: ")
            chart   = input("  Chart (e.g. bitnami/nginx): ")
            ns      = input("  Namespace (blank = 'default'): ").strip() or "default"
            run_cmd_safe(["helm", "install", release, chart, "-n", ns, "--create-namespace"])
            success(f"Release '{release}' installed.")
        elif choice == 6:
            release = input("  Release name: ")
            chart   = input("  Chart: ")
            ns      = input("  Namespace: ").strip() or "default"
            run_cmd_safe(["helm", "upgrade", release, chart, "-n", ns])
            success(f"Release '{release}' upgraded.")
        elif choice == 7:
            release = input("  Release name: ")
            ns      = input("  Namespace: ").strip() or "default"
            run_cmd_safe(["helm", "uninstall", release, "-n", ns])
            success(f"Release '{release}' uninstalled.")
        elif choice == 8:
            break
        else:
            error("Invalid choice.")
        pause()
        clear_screen()


def run() -> None:
    while True:
        clear_screen()
        banner("Kubernetes")
        separator()
        print_menu("Kubernetes", [
            "Setup (kubectl / Minikube / kind / Helm)",
            "Minikube cluster management",
            "Nodes",
            "Namespaces",
            "Deployments",
            "Pods",
            "Services",
            "ConfigMaps & Secrets",
            "Apply / Delete YAML manifests",
            "Helm",
            "Return to main menu",
        ])

        choice = get_choice()
        if choice is None:
            continue

        if choice == 1:
            _setup_cluster()
        elif choice == 2:
            _minikube()
        elif choice == 3:
            _nodes()
        elif choice == 4:
            _namespaces()
        elif choice == 5:
            _deployments()
        elif choice == 6:
            _pods()
        elif choice == 7:
            _services()
        elif choice == 8:
            _config_secrets()
        elif choice == 9:
            _manifests()
        elif choice == 10:
            _helm()
        elif choice == 11:
            break
        else:
            error("Invalid choice.")

        pause()
