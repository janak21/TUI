# TUI — Terminal User Interface for Cloud & DevOps

![CI](https://github.com/janak21/TUI/actions/workflows/ci.yml/badge.svg)

A Python CLI tool for managing and automating enterprise technologies through an interactive menu-driven interface.

![](gif/working.gif)

---

## What It Does

TUI provides a single terminal entry point to install, configure, and manage:

| Module | Key Capabilities |
|---|---|
| **Hadoop** | Install, configure master/slave nodes, cluster operations, file management |
| **AWS** | EC2 (instances, EBS, security groups, key pairs), S3, CloudFront |
| **Docker** | Image search/pull, container lifecycle, service management |
| **Kubernetes** | kubectl/Minikube/kind/Helm setup, deployments, pods, services, ConfigMaps, YAML manifests |
| **Webserver** | Apache httpd install and service management |
| **Linux Partitions** | Full LVM workflow — PV, VG, LV creation, formatting, mounting, extending |
| **Linux Commands** | Common system utilities (network, files, processes, packages) |

---

## Installation

```bash
git clone https://github.com/your-username/TUI.git
cd TUI
pip install -e .
```

**Prerequisites**
- Python 3.10+
- `sudo` / root privileges (required for system-level operations)
- Linux environment (tested on CentOS/RHEL — uses `yum`, `systemctl`)
- Tools installed only as needed: `aws`, `docker`, `kubectl`, `hadoop`, etc.

---

## Usage

```bash
sudo tui
```

Navigate with number keys. Every menu has a **Return to main menu** option as its last entry.

---

## Project Structure

```
tui/
├── __main__.py           # Entry point
├── cli.py                # Main menu dispatcher
├── utils.py              # Shared utilities (Rich UI, subprocess, auth)
└── modules/
    ├── aws.py
    ├── docker.py
    ├── hadoop.py
    ├── kubernetes.py
    ├── linux.py
    ├── lvm.py
    └── webserver.py
```

---

## Dependencies

| Package | Purpose |
|---|---|
| `pyfiglet` | ASCII art banners |
| `rich` | Styled terminal output (panels, colors, status icons) |
