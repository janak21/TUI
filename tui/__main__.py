"""Entry point for running TUI as a module: python -m tui"""

from tui.utils import check_root
from tui.cli import main_menu


def main():
    check_root()
    main_menu()


if __name__ == "__main__":
    main()
