#!/usr/bin/env python3
"""
Hardware Information Detection Module (Production)

Cross-platform functions to detect device type and construct a stable device ID
based on motherboard and disk serial numbers. Supports Windows and Linux.
"""
import subprocess
import platform
import re


def get_device_type() -> str:
    system = platform.system().lower()
    try:
        if system == "linux":
            return _get_device_type_linux()
        elif system == "windows":
            return _get_device_type_windows()
        else:
            return "Unknown Device"
    except Exception:
        return "Unknown Device"


def _get_device_type_linux() -> str:
    try:
        result = subprocess.run(["dmidecode", "-s", "chassis-type"], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            chassis_type = result.stdout.strip().lower()
            if chassis_type in ["notebook", "laptop", "portable", "sub notebook"]:
                return "Laptop"
            if chassis_type in ["desktop", "mini tower", "tower", "low profile desktop"]:
                return "Desktop"
            if chassis_type in ["server", "rack mount chassis"]:
                return "Server"
            if chassis_type in ["all in one", "stick pc"]:
                return "All-in-One"
    except Exception:
        pass
    return "Unknown Device"


def _get_device_type_windows() -> str:
    try:
        result = subprocess.run(["wmic", "systemenclosure", "get", "chassistypes"], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            codes = re.findall(r"\d+", result.stdout)
            if codes:
                code = int(codes[0])
                if code in [8, 9, 10, 11, 12, 14, 18, 21]:
                    return "Laptop"
                if code in [3, 4, 5, 6, 7, 15, 16]:
                    return "Desktop"
                if code in [17, 23]:
                    return "Server"
                if code in [13, 34]:
                    return "All-in-One"
    except Exception:
        pass
    return "Unknown Device"


def get_device_id() -> str:
    system = platform.system().lower()
    try:
        if system == "linux":
            return _get_device_id_linux()
        elif system == "windows":
            return _get_device_id_windows()
        else:
            return "MB-SN-SN_NOT_FOUND-DISK-SN-SN_NOT_FOUND"
    except Exception:
        return "MB-SN-SN_NOT_FOUND-DISK-SN-SN_NOT_FOUND"


def _get_device_id_linux() -> str:
    motherboard_sn = "SN_NOT_FOUND"
    disk_sn = "SN_NOT_FOUND"
    try:
        res = subprocess.run(["dmidecode", "-s", "baseboard-serial-number"], capture_output=True, text=True, timeout=10)
        if res.returncode == 0:
            val = res.stdout.strip()
            if val and val.lower() not in ["not specified", "not available", "to be filled by o.e.m."]:
                motherboard_sn = val
    except Exception:
        pass
    try:
        res = subprocess.run(["lsblk", "-dno", "SERIAL", "/dev/sda"], capture_output=True, text=True, timeout=10)
        if res.returncode == 0:
            val = res.stdout.strip()
            if val:
                disk_sn = val
    except Exception:
        try:
            res = subprocess.run(["hdparm", "-i", "/dev/sda"], capture_output=True, text=True, timeout=10)
            if res.returncode == 0:
                m = re.search(r"SerialNo=(\S+)", res.stdout)
                if m:
                    disk_sn = m.group(1)
        except Exception:
            pass
    return f"MB-SN-{motherboard_sn}-DISK-SN-{disk_sn}"


def _get_device_id_windows() -> str:
    motherboard_sn = "SN_NOT_FOUND"
    disk_sn = "SN_NOT_FOUND"
    try:
        res = subprocess.run(["wmic", "baseboard", "get", "SerialNumber"], capture_output=True, text=True, timeout=10)
        if res.returncode == 0:
            for line in res.stdout.splitlines():
                line = line.strip()
                if line and line.lower() != "serialnumber":
                    motherboard_sn = line
                    break
    except Exception:
        pass
    try:
        res = subprocess.run(["wmic", "diskdrive", "get", "SerialNumber"], capture_output=True, text=True, timeout=10)
        if res.returncode == 0:
            for line in res.stdout.splitlines():
                line = line.strip()
                if line and line.lower() != "serialnumber":
                    disk_sn = line
                    break
    except Exception:
        pass
    return f"MB-SN-{motherboard_sn}-DISK-SN-{disk_sn}"