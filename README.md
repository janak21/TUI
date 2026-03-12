# TUI - Terminal User Interface for Cloud & DevOps

A modern, refactored Python CLI tool for managing and automating enterprise technologies including Hadoop, AWS, Docker, and Linux system administration.

## Overview

TUI provides an interactive menu-driven interface to simplify installation, configuration, and management of:
- **Hadoop** - Distributed computing cluster setup and operations
- **AWS** - EC2 instances, S3 buckets, CloudFront distributions, and more
- **Docker** - Image and container management
- **Webserver** - Apache httpd configuration
- **Linux Partitions** - LVM (Logical Volume Manager) operations
- **Linux Commands** - Common system utilities

## Features

✨ **Refactored Architecture** (v2.0)
- Modular package structure with separate files per service
- Safe command execution using `subprocess` (no shell injection risks)
- Input validation and error handling
- Type hints for better code quality

🔒 **Security Improvements**
- Replaced `os.system()` with `subprocess.run()`
- Shell-quoted user input via `shlex.quote()`
- Removes hardcoded external URLs

📦 **Modern Python Packaging**
- `pyproject.toml` for dependency management
- Installable as a CLI command
- Python 3.10+ support

## Installation

### Option 1: Development Install (recommended for modifications)
```bash
pip install -e .
```

Then run:
```bash
sudo tui
```

### Option 2: Run as Module
```bash
pip install .
sudo python -m tui
```

### Option 3: Direct Execution
```bash
pip install pyfiglet
sudo python tui/__main__.py
```

## Dependencies

- Python 3.10+
- pyfiglet (for ASCII art banners)
- System tools: `aws`, `docker`, `hadoop`, `systemctl`, etc. (depending on which modules you use)

## Project Structure

```
tui/
├── __init__.py           # Package metadata
├── __main__.py           # Entry point
├── cli.py                # Main menu dispatcher
├── utils.py              # Shared utilities (colors, commands, input)
└── modules/
    ├── aws.py            # AWS services (EC2, S3, CloudFront)
    ├── docker.py         # Docker image & container management
    ├── hadoop.py         # Hadoop cluster setup & operations
    ├── linux.py          # Common Linux commands
    ├── lvm.py            # Logical Volume Management
    └── webserver.py      # Apache httpd management
```

## Usage

Run as root/sudo:
```bash
sudo tui
```

Or with Python module syntax:
```bash
sudo python -m tui
```

### Modules Overview

**Hadoop**
- Install Hadoop with Java dependencies
- Configure master/slave nodes
- Manage cluster operations (file upload/download, block size)
- Monitor cluster status

**AWS**
- Install AWS CLI for multiple platforms
- EC2: Launch, manage, and monitor instances
- EBS: Create and manage volumes
- S3: Create buckets, upload/download data
- CloudFront: Manage distributions

**Docker**
- Install/update Docker
- Search, pull, and manage images
- Create, run, and manage containers
- Delete images and containers

**Webserver**
- Install Apache httpd
- Start/stop service
- Check service status

**Linux Partitions (LVM)**
- Create and manage physical volumes
- Create and manage volume groups
- Create and manage logical volumes
- Mount volumes and manage storage

**Linux Commands**
- File and folder operations
- Network configuration
- System monitoring
- Software installation/removal

## Requirements

- **Root/sudo privileges** - required for system-level operations
- **Linux environment** - tested on CentOS/RHEL with yum package manager
- **AWS CLI, Docker, Hadoop** - only needed if using those modules

## Previous Version

The original single-file implementation (`Menu.py`) is included for reference.

## Demo

![](gif/working.gif)
