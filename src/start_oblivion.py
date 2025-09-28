#!/usr/bin/env python3
"""
OBLIVION Launcher Entry Point

Provides a simple launcher that can invoke boot manager operations and
run the core wiping application.
"""
import sys
import os
from boot_manager import BootManager
from oblivion_core import OblivionCore

# Resource helper for PyInstaller
import sys as _sys
import os as _os

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        base_path = _sys._MEIPASS  # type: ignore[attr-defined]
    except Exception:
        base_path = _os.path.abspath(".")
    return _os.path.join(base_path, relative_path)


def main():
    bm = BootManager()
    print("=== OBLIVION Launcher ===")
    print(bm.get_platform_info())
    if bm.system == 'windows':
        print("\nCurrent BCD configuration (excerpt):")
        print(bm.run_bcdedit_enum()[:1000])  # show excerpt
    print("\nSelect an action:\n  1) Run OBLIVION Wiper\n  2) Reboot Now")
    choice = input("Enter choice: ").strip()
    if choice == '1':
        core = OblivionCore()
        return core.run()
    elif choice == '2':
        print("Rebooting...")
        bm.reboot_now()
        return 0
    else:
        print("Invalid choice.")
        return 1

if __name__ == '__main__':
    sys.exit(main())