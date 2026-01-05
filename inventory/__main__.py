"""Main entry point for the inventory application."""

import sys
from inventory import __version__


def main():
    """Main function for the inventory application."""
    print("Inventory Management Application")
    print(f"Version: {__version__}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
