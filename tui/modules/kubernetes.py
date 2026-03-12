"""Kubernetes module - cluster management, deployments, services, and pods."""

from tui.utils import (
    banner, clear_screen, get_choice, pause, run_cmd_safe,
    separator, set_color,
)


# ---------------------------------------------------------------------------
# Cluster setup
# ---------------------------------------------------------------------------

def _setup_cluster():
    print("""
    --- Cluster Setup ---
    Press 1: Install kubectl
    Press 2: Install Minikube (local single-node cluster)
    Press 3: Install kind (Kubernetes in Docker)
    Press 4: Install Helm
    Press 5: Back
    """)
    while True:
        choice = get_choice()
        if choice is None:
            continue
        if choice == 1:
            print("Installing kubectl...")
            run_cmd_safe([
                "curl", "-LO",
                "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl",
            ])
            run_cmd_safe(["chmod", "+x", "kubectl"])
            run_cmd_safe(["sudo", "mv", "kubectl", "/usr/local/bin/kubectl"])
            run_cmd_safe(["kubectl", "version", "--client"])
        elif choice == 2:
            print("Installing Minikube...")
            run_cmd_safe([
                "curl", "-LO",
                "https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64",
            ])
            run_cmd_safe(["sudo", "install", "minikube-linux-amd64", "/usr/local/bin/minikube"])
            run_cmd_safe(["minikube", "version"])
        elif choice == 3:
            print("Installing kind...")
            run_cmd_safe([
                "curl", "-Lo", "./kind",
                "https://kind.sigs.k8s.io/dl/latest/kind-linux-amd64",
            ])
            run_cmd_safe(["chmod", "+x", "./kind"])
            run_cmd_safe(["sudo", "mv", "./kind", "/usr/local/bin/kind"])
            run_cmd_safe(["kind", "version"])
        elif choice == 4:
            print("Installing Helm...")
            run_cmd_safe([
                "curl", "-fsSL",
                "https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3",
                "-o", "get_helm.sh",
            ])
            run_cmd_safe(["chmod", "+x", "get_helm.sh"])
            run_cmd_safe(["./get_helm.sh"])
            run_cmd_safe(["helm", "version"])
        elif choice == 5:
            break
        else:
            print("Invalid choice.")
        pause()
        clear_screen()


# ---------------------------------------------------------------------------
# Minikube
# ---------------------------------------------------------------------------

def _minikube():
    print("""
    --- Minikube ---
    Press 1: Start cluster
    Press 2: Stop cluster
    Press 3: Delete cluster
    Press 4: Cluster status
    Press 5: Open dashboard
    Press 6: View cluster IP
    Press 7: Back
    """)
    while True:
        choice = get_choice()
        if choice is None:
            continue
        if choice == 1:
            run_cmd_safe(["minikube", "start"])
        elif choice == 2:
            run_cmd_safe(["minikube", "stop"])
        elif choice == 3:
            run_cmd_safe(["minikube", "delete"])
        elif choice == 4:
            run_cmd_safe(["minikube", "status"])
        elif choice == 5:
            run_cmd_safe(["minikube", "dashboard"])
        elif choice == 6:
            run_cmd_safe(["minikube", "ip"])
        elif choice == 7:
            break
        else:
            print("Invalid choice.")
        pause()
        clear_screen()


# ---------------------------------------------------------------------------
# Nodes
# ---------------------------------------------------------------------------

def _nodes():
    print("""
    --- Nodes ---
    Press 1: List all nodes
    Press 2: Describe a node
    Press 3: View node resource usage
    Press 4: Cordon node (mark unschedulable)
    Press 5: Uncordon node
    Press 6: Drain node
    Press 7: Back
    """)
    while True:
        choice = get_choice()
        if choice is None:
            continue
        if choice == 1:
            run_cmd_safe(["kubectl", "get", "nodes", "-o", "wide"])
        elif choice == 2:
            name = input("Enter node name: ")
            run_cmd_safe(["kubectl", "describe", "node", name])
        elif choice == 3:
            run_cmd_safe(["kubectl", "top", "nodes"])
        elif choice == 4:
            name = input("Enter node name: ")
            run_cmd_safe(["kubectl", "cordon", name])
        elif choice == 5:
            name = input("Enter node name: ")
            run_cmd_safe(["kubectl", "uncordon", name])
        elif choice == 6:
            name = input("Enter node name: ")
            run_cmd_safe(["kubectl", "drain", name, "--ignore-daemonsets", "--delete-emptydir-data"])
        elif choice == 7:
            break
        else:
            print("Invalid choice.")
        pause()
        clear_screen()


# ---------------------------------------------------------------------------
# Namespaces
# ---------------------------------------------------------------------------

def _namespaces():
    print("""
    --- Namespaces ---
    Press 1: List namespaces
    Press 2: Create namespace
    Press 3: Delete namespace
    Press 4: Describe namespace
    Press 5: Back
    """)
    while True:
        choice = get_choice()
        if choice is None:
            continue
        if choice == 1:
            run_cmd_safe(["kubectl", "get", "namespaces"])
        elif choice == 2:
            name = input("Enter namespace name: ")
            run_cmd_safe(["kubectl", "create", "namespace", name])
        elif choice == 3:
            name = input("Enter namespace name: ")
            run_cmd_safe(["kubectl", "delete", "namespace", name])
        elif choice == 4:
            name = input("Enter namespace name: ")
            run_cmd_safe(["kubectl", "describe", "namespace", name])
        elif choice == 5:
            break
        else:
            print("Invalid choice.")
        pause()
        clear_screen()


# ---------------------------------------------------------------------------
# Deployments
# ---------------------------------------------------------------------------

def _deployments():
    print("""
    --- Deployments ---
    Press 1:  List deployments
    Press 2:  Create deployment
    Press 3:  Describe deployment
    Press 4:  Delete deployment
    Press 5:  Scale deployment
    Press 6:  Update image (rolling update)
    Press 7:  Rollout status
    Press 8:  Rollback deployment
    Press 9:  Pause rollout
    Press 10: Resume rollout
    Press 11: Back
    """)
    while True:
        choice = get_choice()
        if choice is None:
            continue

        ns = input("Enter namespace (leave blank for 'default'): ").strip() or "default"

        if choice == 1:
            run_cmd_safe(["kubectl", "get", "deployments", "-n", ns, "-o", "wide"])
        elif choice == 2:
            name = input("Enter deployment name: ")
            image = input("Enter container image (e.g. nginx:latest): ")
            replicas = input("Enter number of replicas (default 1): ").strip() or "1"
            run_cmd_safe([
                "kubectl", "create", "deployment", name,
                "--image", image,
                "--replicas", replicas,
                "-n", ns,
            ])
        elif choice == 3:
            name = input("Enter deployment name: ")
            run_cmd_safe(["kubectl", "describe", "deployment", name, "-n", ns])
        elif choice == 4:
            name = input("Enter deployment name: ")
            run_cmd_safe(["kubectl", "delete", "deployment", name, "-n", ns])
        elif choice == 5:
            name = input("Enter deployment name: ")
            replicas = input("Enter desired replica count: ")
            run_cmd_safe(["kubectl", "scale", "deployment", name, f"--replicas={replicas}", "-n", ns])
        elif choice == 6:
            name = input("Enter deployment name: ")
            container = input("Enter container name: ")
            image = input("Enter new image (e.g. nginx:1.25): ")
            run_cmd_safe([
                "kubectl", "set", "image",
                f"deployment/{name}", f"{container}={image}",
                "-n", ns,
            ])
        elif choice == 7:
            name = input("Enter deployment name: ")
            run_cmd_safe(["kubectl", "rollout", "status", f"deployment/{name}", "-n", ns])
        elif choice == 8:
            name = input("Enter deployment name: ")
            run_cmd_safe(["kubectl", "rollout", "undo", f"deployment/{name}", "-n", ns])
        elif choice == 9:
            name = input("Enter deployment name: ")
            run_cmd_safe(["kubectl", "rollout", "pause", f"deployment/{name}", "-n", ns])
        elif choice == 10:
            name = input("Enter deployment name: ")
            run_cmd_safe(["kubectl", "rollout", "resume", f"deployment/{name}", "-n", ns])
        elif choice == 11:
            break
        else:
            print("Invalid choice.")
        pause()
        clear_screen()


# ---------------------------------------------------------------------------
# Pods
# ---------------------------------------------------------------------------

def _pods():
    print("""
    --- Pods ---
    Press 1: List pods
    Press 2: Describe pod
    Press 3: View pod logs
    Press 4: Follow pod logs
    Press 5: Execute command in pod
    Press 6: Open shell in pod
    Press 7: Delete pod
    Press 8: View pod resource usage
    Press 9: Back
    """)
    while True:
        choice = get_choice()
        if choice is None:
            continue

        ns = input("Enter namespace (leave blank for 'default'): ").strip() or "default"

        if choice == 1:
            run_cmd_safe(["kubectl", "get", "pods", "-n", ns, "-o", "wide"])
        elif choice == 2:
            name = input("Enter pod name: ")
            run_cmd_safe(["kubectl", "describe", "pod", name, "-n", ns])
        elif choice == 3:
            name = input("Enter pod name: ")
            run_cmd_safe(["kubectl", "logs", name, "-n", ns])
        elif choice == 4:
            name = input("Enter pod name: ")
            run_cmd_safe(["kubectl", "logs", "-f", name, "-n", ns])
        elif choice == 5:
            name = input("Enter pod name: ")
            cmd = input("Enter command to run (e.g. ls /): ")
            run_cmd_safe(["kubectl", "exec", name, "-n", ns, "--", *cmd.split()])
        elif choice == 6:
            name = input("Enter pod name: ")
            run_cmd_safe(["kubectl", "exec", "-it", name, "-n", ns, "--", "/bin/sh"])
        elif choice == 7:
            name = input("Enter pod name: ")
            run_cmd_safe(["kubectl", "delete", "pod", name, "-n", ns])
        elif choice == 8:
            run_cmd_safe(["kubectl", "top", "pods", "-n", ns])
        elif choice == 9:
            break
        else:
            print("Invalid choice.")
        pause()
        clear_screen()


# ---------------------------------------------------------------------------
# Services
# ---------------------------------------------------------------------------

def _services():
    print("""
    --- Services ---
    Press 1: List services
    Press 2: Expose deployment as service
    Press 3: Describe service
    Press 4: Delete service
    Press 5: Get service URL (Minikube)
    Press 6: Back
    """)
    while True:
        choice = get_choice()
        if choice is None:
            continue

        ns = input("Enter namespace (leave blank for 'default'): ").strip() or "default"

        if choice == 1:
            run_cmd_safe(["kubectl", "get", "services", "-n", ns])
        elif choice == 2:
            name = input("Enter deployment name to expose: ")
            port = input("Enter port: ")
            svc_type = input("Enter service type (ClusterIP/NodePort/LoadBalancer): ").strip() or "ClusterIP"
            run_cmd_safe([
                "kubectl", "expose", "deployment", name,
                "--port", port,
                "--type", svc_type,
                "-n", ns,
            ])
        elif choice == 3:
            name = input("Enter service name: ")
            run_cmd_safe(["kubectl", "describe", "service", name, "-n", ns])
        elif choice == 4:
            name = input("Enter service name: ")
            run_cmd_safe(["kubectl", "delete", "service", name, "-n", ns])
        elif choice == 5:
            name = input("Enter service name: ")
            run_cmd_safe(["minikube", "service", name, "-n", ns, "--url"])
        elif choice == 6:
            break
        else:
            print("Invalid choice.")
        pause()
        clear_screen()


# ---------------------------------------------------------------------------
# ConfigMaps & Secrets
# ---------------------------------------------------------------------------

def _config_secrets():
    print("""
    --- ConfigMaps & Secrets ---
    Press 1: List ConfigMaps
    Press 2: Create ConfigMap from literal
    Press 3: Describe ConfigMap
    Press 4: Delete ConfigMap
    Press 5: List Secrets
    Press 6: Create Secret (generic)
    Press 7: Describe Secret
    Press 8: Delete Secret
    Press 9: Back
    """)
    while True:
        choice = get_choice()
        if choice is None:
            continue

        ns = input("Enter namespace (leave blank for 'default'): ").strip() or "default"

        if choice == 1:
            run_cmd_safe(["kubectl", "get", "configmaps", "-n", ns])
        elif choice == 2:
            name = input("Enter ConfigMap name: ")
            key = input("Enter key: ")
            value = input("Enter value: ")
            run_cmd_safe([
                "kubectl", "create", "configmap", name,
                f"--from-literal={key}={value}",
                "-n", ns,
            ])
        elif choice == 3:
            name = input("Enter ConfigMap name: ")
            run_cmd_safe(["kubectl", "describe", "configmap", name, "-n", ns])
        elif choice == 4:
            name = input("Enter ConfigMap name: ")
            run_cmd_safe(["kubectl", "delete", "configmap", name, "-n", ns])
        elif choice == 5:
            run_cmd_safe(["kubectl", "get", "secrets", "-n", ns])
        elif choice == 6:
            name = input("Enter Secret name: ")
            key = input("Enter key: ")
            value = input("Enter value: ")
            run_cmd_safe([
                "kubectl", "create", "secret", "generic", name,
                f"--from-literal={key}={value}",
                "-n", ns,
            ])
        elif choice == 7:
            name = input("Enter Secret name: ")
            run_cmd_safe(["kubectl", "describe", "secret", name, "-n", ns])
        elif choice == 8:
            name = input("Enter Secret name: ")
            run_cmd_safe(["kubectl", "delete", "secret", name, "-n", ns])
        elif choice == 9:
            break
        else:
            print("Invalid choice.")
        pause()
        clear_screen()


# ---------------------------------------------------------------------------
# Apply / Delete manifests
# ---------------------------------------------------------------------------

def _manifests():
    print("""
    --- YAML Manifests ---
    Press 1: Apply manifest (kubectl apply -f)
    Press 2: Delete resources from manifest (kubectl delete -f)
    Press 3: Dry-run apply (validate without applying)
    Press 4: View current context / cluster info
    Press 5: Switch context
    Press 6: List all contexts
    Press 7: Back
    """)
    while True:
        choice = get_choice()
        if choice is None:
            continue
        if choice == 1:
            path = input("Enter path to YAML file or directory: ")
            run_cmd_safe(["kubectl", "apply", "-f", path])
        elif choice == 2:
            path = input("Enter path to YAML file or directory: ")
            run_cmd_safe(["kubectl", "delete", "-f", path])
        elif choice == 3:
            path = input("Enter path to YAML file or directory: ")
            run_cmd_safe(["kubectl", "apply", "--dry-run=client", "-f", path])
        elif choice == 4:
            run_cmd_safe(["kubectl", "cluster-info"])
        elif choice == 5:
            name = input("Enter context name: ")
            run_cmd_safe(["kubectl", "config", "use-context", name])
        elif choice == 6:
            run_cmd_safe(["kubectl", "config", "get-contexts"])
        elif choice == 7:
            break
        else:
            print("Invalid choice.")
        pause()
        clear_screen()


# ---------------------------------------------------------------------------
# Helm
# ---------------------------------------------------------------------------

def _helm():
    print("""
    --- Helm ---
    Press 1: List installed releases
    Press 2: Add Helm repo
    Press 3: Update repos
    Press 4: Search a chart
    Press 5: Install a chart
    Press 6: Upgrade a release
    Press 7: Uninstall a release
    Press 8: Back
    """)
    while True:
        choice = get_choice()
        if choice is None:
            continue
        if choice == 1:
            ns = input("Enter namespace (leave blank for all): ").strip()
            cmd = ["helm", "list"]
            if ns:
                cmd += ["-n", ns]
            else:
                cmd += ["-A"]
            run_cmd_safe(cmd)
        elif choice == 2:
            name = input("Enter repo name: ")
            url = input("Enter repo URL: ")
            run_cmd_safe(["helm", "repo", "add", name, url])
        elif choice == 3:
            run_cmd_safe(["helm", "repo", "update"])
        elif choice == 4:
            term = input("Enter search term: ")
            run_cmd_safe(["helm", "search", "repo", term])
        elif choice == 5:
            release = input("Enter release name: ")
            chart = input("Enter chart (e.g. bitnami/nginx): ")
            ns = input("Enter namespace (leave blank for 'default'): ").strip() or "default"
            run_cmd_safe(["helm", "install", release, chart, "-n", ns, "--create-namespace"])
        elif choice == 6:
            release = input("Enter release name: ")
            chart = input("Enter chart: ")
            ns = input("Enter namespace: ").strip() or "default"
            run_cmd_safe(["helm", "upgrade", release, chart, "-n", ns])
        elif choice == 7:
            release = input("Enter release name: ")
            ns = input("Enter namespace: ").strip() or "default"
            run_cmd_safe(["helm", "uninstall", release, "-n", ns])
        elif choice == 8:
            break
        else:
            print("Invalid choice.")
        pause()
        clear_screen()


# ---------------------------------------------------------------------------
# Main entry
# ---------------------------------------------------------------------------

def run():
    """Main Kubernetes menu."""
    while True:
        clear_screen()
        banner("Kubernetes")
        set_color("green")
        separator()
        print("""
        Press 1: Setup (kubectl / Minikube / kind / Helm)
        Press 2: Minikube cluster management
        Press 3: Nodes
        Press 4: Namespaces
        Press 5: Deployments
        Press 6: Pods
        Press 7: Services
        Press 8: ConfigMaps & Secrets
        Press 9: Apply / Delete YAML manifests
        Press 10: Helm
        Press 11: Return to main menu
        """)
        separator()
        set_color("white")

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
            print("Invalid choice.")

        pause()
