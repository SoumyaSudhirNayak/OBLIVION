#!/usr/bin/env python3
"""
OBLIVION Boot Manager (Production)

Executes real reboot operations and integrates with platform boot tools:
- Windows: bcdedit for boot configuration, shutdown for reboot
- Linux: grub-reboot for selecting next boot entry, reboot command

Administrator/root privileges are required for most operations.
"""
import os
import platform
import subprocess
from typing import Optional, List

class BootManager:
    def __init__(self):
        self.system = platform.system().lower()

    def reboot_now(self) -> None:
        """Perform an immediate system reboot using native commands."""
        if self.system == 'windows':
            # Immediate reboot
            subprocess.run(["shutdown", "/r", "/t", "0"], check=True)
        else:
            subprocess.run(["reboot"], check=True)

    def run_bcdedit_enum(self) -> str:
        """Windows: Return current bcdedit configuration."""
        if self.system != 'windows':
            return "bcdedit not applicable on this platform"
        result = subprocess.run(["bcdedit", "/enum", "all"], capture_output=True, text=True)
        return result.stdout if result.returncode == 0 else result.stderr

    def execute_bcdedit(self, args: List[str]) -> str:
        """Windows: Execute a bcdedit command with provided arguments."""
        if self.system != 'windows':
            return "bcdedit not applicable on this platform"
        cmd = ["bcdedit"] + args
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout if result.returncode == 0 else result.stderr

    def set_next_boot_entry_linux(self, entry: str = "0") -> bool:
        """Linux: Set next boot entry using grub-reboot (requires root)."""
        if self.system != 'linux':
            return False
        try:
            subprocess.run(["grub-reboot", entry], check=True)
            return True
        except Exception:
            return False

    def get_platform_info(self) -> str:
        return f"Platform: {platform.system()} {platform.release()}"

if __name__ == '__main__':
    bm = BootManager()
    print(bm.get_platform_info())
    print("bcdedit enum:")
    print(bm.run_bcdedit_enum())