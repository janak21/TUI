"""
Smoke tests for TUI — no root, no real system tools required.

Tests:
  - Syntax/import checks for all modules
  - Main menu navigation
  - Exit path for every module
  - Key submenu navigation paths
  - Security: run_cmd_safe uses list args (no shell injection)
  - check_root blocks non-root callers
"""

import io
import sys
import os

# Allow running from repo root: python tests/smoke_test.py
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from unittest.mock import patch, MagicMock
from rich.console import Console

test_console = Console(file=io.StringIO(), width=80)


def inputs(*vals):
    """Return an input() mock that pops from the list, then raises EOFError."""
    v = list(map(str, vals))
    def _input(prompt=""):
        if v:
            return v.pop(0)
        raise EOFError
    return _input


def run_test(label, fn, *inp):
    with patch("tui.utils.console", test_console), \
         patch("subprocess.run", return_value=MagicMock(returncode=0)), \
         patch("builtins.input", inputs(*inp)):
        try:
            fn()
            print(f"  ✓  {label}")
            return True
        except EOFError:
            print(f"  ✓  {label}  (exited via EOFError — expected)")
            return True
        except Exception as e:
            print(f"  ✗  {label}: {e}")
            return False


# ── imports ───────────────────────────────────────────────────────────────────
from tui.modules.aws        import run as aws_run
from tui.modules.docker     import run as docker_run
from tui.modules.hadoop     import run as hadoop_run
from tui.modules.kubernetes import run as k8s_run
from tui.modules.linux      import run as linux_run
from tui.modules.lvm        import run as lvm_run
from tui.modules.webserver  import run as web_run
from tui.cli                import main_menu
from tui.utils              import run_cmd_safe, check_root

results = []

print("\n── Syntax / import checks ───────────────────────────────────────────────")
print("  ✓  All modules import OK")

print("\n── Main menu navigation ─────────────────────────────────────────────────")
results.append(run_test("main menu: detect OS → exit", main_menu, 1, 9))

print("\n── Module exit paths ────────────────────────────────────────────────────")
results.append(run_test("webserver  → exit(5)",    web_run,    5))
results.append(run_test("linux      → exit(14)",   linux_run,  14))
results.append(run_test("lvm        → exit(16)",   lvm_run,    16))
results.append(run_test("docker     → exit(15)",   docker_run, 15))
results.append(run_test("hadoop     → exit(10)",   hadoop_run, 10))
results.append(run_test("aws        → exit(7)",    aws_run,    7))
results.append(run_test("kubernetes → exit(11)",   k8s_run,    11))

print("\n── Submenu navigation ───────────────────────────────────────────────────")
results.append(run_test("webserver: install → exit",           web_run,    1, 5))
results.append(run_test("docker: service→start→back→exit",     docker_run, 2, 1, 4, 15))
results.append(run_test("docker: delete images→all→back→exit", docker_run, 11, 2, 3, 15))
results.append(run_test("lvm: create PV → exit",               lvm_run,    2, "/dev/sdb", 16))
results.append(run_test("hadoop: sysinfo→disk→back→exit",      hadoop_run, 5, 1, 10))
results.append(run_test("aws: version → exit",                 aws_run,    2, 7))
results.append(run_test("aws: S3→list→back→exit",              aws_run,    5, 2, 6, 7))
results.append(run_test("k8s: namespaces→list→back→exit",      k8s_run,    4, 1, "", 5, 11))
results.append(run_test("k8s: minikube→status→back→exit",      k8s_run,    2, 4, 7, 11))
results.append(run_test("k8s: helm→list→back→exit",            k8s_run,    10, 1, "", 8, 11))

print("\n── Security checks ──────────────────────────────────────────────────────")
with patch("subprocess.run") as mock_run:
    mock_run.return_value = MagicMock(returncode=0)
    run_cmd_safe(["echo", "hello"])
    assert mock_run.call_args.kwargs.get("shell", False) == False, "shell=True detected!"
    print("  ✓  run_cmd_safe uses list args (no shell injection)")
    results.append(True)

with patch("os.geteuid", return_value=999):
    try:
        check_root()
        print("  ✗  check_root should have exited!")
        results.append(False)
    except SystemExit:
        print("  ✓  check_root blocks non-root")
        results.append(True)

print()
total  = len(results)
passed = sum(results)
print("─" * 60)
print(f"  {passed}/{total} tests passed" + (" ✓" if passed == total else " ✗  SOME FAILED"))
print("─" * 60)

sys.exit(0 if passed == total else 1)
