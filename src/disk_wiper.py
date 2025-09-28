#!/usr/bin/env python3
"""
OBLIVION Disk Wiper (Production)

Implements real, destructive disk wiping operations with NIST SP 800-88
Clear (single pass zeros) and Purge (multi-pass with verification) methods.

This module performs raw writes directly to block devices:
- Windows: \\.\PhysicalDriveN
- Linux:   /dev/sdX or /dev/nvmeXnY

WARNING: Running these functions will PERMANENTLY DESTROY DATA.
Administrator/root privileges are required.
"""

from __future__ import annotations
import os
import sys
import platform
import ctypes
import subprocess
import time
from typing import Callable, List, Optional, Dict

ProgressCallback = Optional[Callable[[int, int], None]]  # (written_bytes, total_bytes)

DEFAULT_BLOCK_SIZE = 8 * 1024 * 1024  # 8 MiB

class DiskWiper:
    def __init__(self, block_size: int = DEFAULT_BLOCK_SIZE):
        self.block_size = block_size
        self.system = platform.system().lower()

    # ---------------------- Public API ----------------------
    def list_disks(self) -> List[Dict]:
        """Enumerate physical disks with model and size.
        Returns list of dicts: {id, path, model, size_bytes}.
        """
        if self.system == 'windows':
            return self._list_disks_windows()
        elif self.system == 'linux':
            return self._list_disks_linux()
        else:
            return []

    def wipe_clear(self, device_path: str, progress: ProgressCallback = None) -> None:
        """NIST Clear: single pass of zeros across the entire device."""
        total = self._get_device_size(device_path)
        self._write_pattern(device_path, total, pattern=b"\x00", progress=progress)

    def wipe_purge(self, device_path: str, progress: ProgressCallback = None) -> None:
        """NIST Purge: multi-pass (random, zeros) with lightweight verification."""
        total = self._get_device_size(device_path)
        # Pass 1: random
        self._write_random(device_path, total, progress=progress)
        # Pass 2: zeros
        self._write_pattern(device_path, total, pattern=b"\x00", progress=progress)
        # Verify sample sectors (read back a few offsets)
        self._verify_zeros(device_path, total)

    # ---------------------- Internals ----------------------
    def _write_pattern(self, device_path: str, total: int, pattern: bytes, progress: ProgressCallback) -> None:
        block = pattern * (self.block_size // len(pattern))
        if len(block) == 0:
            block = b"\x00"
        written = 0
        flags = os.O_RDWR
        if self.system == 'windows':
            flags |= os.O_BINARY
        fd = os.open(device_path, flags)
        try:
            # Position to start
            os.lseek(fd, 0, os.SEEK_SET)
            while written < total:
                to_write = min(self.block_size, total - written)
                if to_write != len(block):
                    buf = block[:to_write]
                else:
                    buf = block
                n = os.write(fd, buf)
                if n <= 0:
                    raise OSError("Short write while wiping")
                written += n
                if progress:
                    progress(written, total)
        finally:
            os.close(fd)

    def _write_random(self, device_path: str, total: int, progress: ProgressCallback) -> None:
        written = 0
        flags = os.O_RDWR
        if self.system == 'windows':
            flags |= os.O_BINARY
        fd = os.open(device_path, flags)
        try:
            os.lseek(fd, 0, os.SEEK_SET)
            while written < total:
                to_write = min(self.block_size, total - written)
                rnd = os.urandom(to_write)
                n = os.write(fd, rnd)
                if n <= 0:
                    raise OSError("Short write while wiping (random)")
                written += n
                if progress:
                    progress(written, total)
        finally:
            os.close(fd)

    def _verify_zeros(self, device_path: str, total: int) -> None:
        # Read a few evenly spaced sectors and ensure they are zeroed
        samples = 8
        step = max(total // samples, 512)
        size = 4096
        flags = os.O_RDONLY
        if self.system == 'windows':
            flags |= os.O_BINARY
        fd = os.open(device_path, flags)
        try:
            for i in range(samples):
                offset = min(step * i, max(0, total - size))
                os.lseek(fd, offset, os.SEEK_SET)
                data = os.read(fd, size)
                if any(b != 0 for b in data):
                    raise IOError(f"Verification failed at offset {offset}")
        finally:
            os.close(fd)

    # ---------------------- Enumeration ----------------------
    def _list_disks_windows(self) -> List[Dict]:
        disks: List[Dict] = []
        try:
            # Query physical disks
            result = subprocess.run(
                ["wmic", "diskdrive", "get", "Index,Model,Size"],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode != 0:
                return disks
            lines = [l.strip() for l in result.stdout.splitlines() if l.strip()]
            # Skip header
            for line in lines[1:]:
                parts = line.split()
                # Last token is Size, first is Index, the rest join to Model
                try:
                    index = int(parts[0])
                    size = int(parts[-1]) if parts[-1].isdigit() else 0
                    model = " ".join(parts[1:-1]) or f"PhysicalDrive{index}"
                    path = f"\\\\.\\PhysicalDrive{index}"
                    disks.append({
                        'id': index,
                        'path': path,
                        'model': model,
                        'size_bytes': size,
                    })
                except Exception:
                    continue
        except Exception:
            pass
        return disks

    def _list_disks_linux(self) -> List[Dict]:
        disks: List[Dict] = []
        try:
            # Use lsblk to list disks
            cmd = ["lsblk", "-dn", "-o", "NAME,SIZE,MODEL,TYPE"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                return disks
            for line in result.stdout.splitlines():
                if not line.strip():
                    continue
                name, size_str, model, dtype = (line.split(None, 3) + ['','','',''])[:4]
                if dtype != 'disk':
                    continue
                device = f"/dev/{name}"
                size_bytes = self._get_device_size(device)
                disks.append({
                    'id': name,
                    'path': device,
                    'model': model or device,
                    'size_bytes': size_bytes,
                })
        except Exception:
            pass
        return disks

    # ---------------------- Size helpers ----------------------
    def _get_device_size(self, device_path: str) -> int:
        if self.system == 'windows':
            return self._get_device_size_windows(device_path)
        return self._get_device_size_linux(device_path)

    def _get_device_size_windows(self, device_path: str) -> int:
        # Try IOCTL_DISK_GET_LENGTH_INFO
        GENERIC_READ = 0x80000000
        FILE_SHARE_READ = 0x00000001
        FILE_SHARE_WRITE = 0x00000002
        OPEN_EXISTING = 3
        IOCTL_DISK_GET_LENGTH_INFO = 0x0007405C
        class LARGE_INTEGER(ctypes.Structure):
            _fields_ = [("QuadPart", ctypes.c_longlong)]
        size = 0
        try:
            CreateFileW = ctypes.windll.kernel32.CreateFileW
            DeviceIoControl = ctypes.windll.kernel32.DeviceIoControl
            CloseHandle = ctypes.windll.kernel32.CloseHandle
            handle = CreateFileW(device_path, GENERIC_READ, FILE_SHARE_READ | FILE_SHARE_WRITE, None, OPEN_EXISTING, 0, None)
            if handle == ctypes.c_void_p(-1).value:
                raise OSError("CreateFile failed")
            length = LARGE_INTEGER()
            returned = ctypes.c_ulong(0)
            ok = DeviceIoControl(handle, IOCTL_DISK_GET_LENGTH_INFO, None, 0, ctypes.byref(length), ctypes.sizeof(length), ctypes.byref(returned), None)
            CloseHandle(handle)
            if ok:
                size = int(length.QuadPart)
        except Exception:
            pass
        if size > 0:
            return size
        # Fallback wmic query by index in path
        try:
            if device_path.lower().startswith('\\\\.\\physicaldrive'):
                index = int(device_path.split('physicaldrive',1)[1])
                cmd = f'wmic diskdrive where "Index={index}" get Size /value'
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
                for line in result.stdout.splitlines():
                    if line.strip().startswith('Size='):
                        return int(line.split('=',1)[1].strip())
        except Exception:
            pass
        raise RuntimeError(f"Unable to determine device size for {device_path}")

    def _get_device_size_linux(self, device_path: str) -> int:
        # Prefer blockdev --getsize64
        try:
            result = subprocess.run(["blockdev", "--getsize64", device_path], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                return int(result.stdout.strip())
        except Exception:
            pass
        # Fallback using os.lseek to end
        try:
            flags = os.O_RDONLY
            fd = os.open(device_path, flags)
            try:
                end = os.lseek(fd, 0, os.SEEK_END)
                return int(end)
            finally:
                os.close(fd)
        except Exception:
            pass
        raise RuntimeError(f"Unable to determine device size for {device_path}")


if __name__ == '__main__':
    # Simple self-test listing disks (non-destructive)
    dw = DiskWiper()
    for d in dw.list_disks():
        sz_gb = d['size_bytes'] / (1024**3)
        print(f"{d['path']} - {d['model']} - {sz_gb:.1f} GiB")