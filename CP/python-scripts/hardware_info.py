#!/usr/bin/env python3
"""
Hardware Information Detection Module

This module provides cross-platform functions to detect hardware information
including device type (chassis type) and device ID (based on motherboard and disk serial numbers).

Supports both Windows and Linux platforms.
"""

import subprocess
import platform
import re
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_device_type():
    """
    Determine the physical form factor of the machine.
    
    Returns:
        str: Device type ("Laptop", "Desktop", or "Unknown Device")
    """
    system = platform.system().lower()
    
    try:
        if system == "linux":
            return _get_device_type_linux()
        elif system == "windows":
            return _get_device_type_windows()
        else:
            logger.warning(f"Unsupported operating system: {system}")
            return "Unknown Device"
    except Exception as e:
        logger.error(f"Error detecting device type: {e}")
        return "Unknown Device"


def _get_device_type_linux():
    """
    Get device type on Linux using dmidecode.
    
    Returns:
        str: Device type
    """
    try:
        # Execute dmidecode command to get chassis type
        result = subprocess.run(
            ["dmidecode", "-s", "chassis-type"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            chassis_type = result.stdout.strip().lower()
            logger.info(f"Linux chassis type detected: {chassis_type}")
            
            # Map chassis types to standardized names
            if chassis_type in ["notebook", "laptop", "portable", "sub notebook"]:
                return "Laptop"
            elif chassis_type in ["desktop", "mini tower", "tower", "low profile desktop"]:
                return "Desktop"
            elif chassis_type in ["server", "rack mount chassis"]:
                return "Server"
            elif chassis_type in ["all in one", "stick pc"]:
                return "All-in-One"
            else:
                logger.warning(f"Unknown chassis type: {chassis_type}")
                return "Unknown Device"
        else:
            logger.error(f"dmidecode failed with return code: {result.returncode}")
            return "Unknown Device"
            
    except subprocess.TimeoutExpired:
        logger.error("dmidecode command timed out")
        return "Unknown Device"
    except FileNotFoundError:
        logger.error("dmidecode command not found. Please install dmidecode.")
        return "Unknown Device"
    except Exception as e:
        logger.error(f"Error running dmidecode: {e}")
        return "Unknown Device"


def _get_device_type_windows():
    """
    Get device type on Windows using WMI.
    
    Returns:
        str: Device type
    """
    try:
        # Execute WMI query to get chassis types
        result = subprocess.run(
            ["wmic", "systemenclosure", "get", "chassistypes"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            output = result.stdout.strip()
            logger.info(f"Windows WMI output: {output}")
            
            # Extract numeric chassis type codes
            chassis_codes = re.findall(r'\d+', output)
            
            if chassis_codes:
                # Use the first chassis code found
                chassis_code = int(chassis_codes[0])
                logger.info(f"Windows chassis code detected: {chassis_code}")
                
                # Map chassis codes to device types
                # Reference: https://docs.microsoft.com/en-us/windows/win32/cimwin32prov/win32-systemenclosure
                if chassis_code in [8, 9, 10, 11, 12, 14, 18, 21]:  # Portable types
                    return "Laptop"
                elif chassis_code in [3, 4, 5, 6, 7, 15, 16]:  # Desktop types
                    return "Desktop"
                elif chassis_code in [17, 23]:  # Server types
                    return "Server"
                elif chassis_code in [13, 34]:  # All-in-One types
                    return "All-in-One"
                else:
                    logger.warning(f"Unknown chassis code: {chassis_code}")
                    return "Unknown Device"
            else:
                logger.error("No chassis codes found in WMI output")
                return "Unknown Device"
        else:
            logger.error(f"WMI command failed with return code: {result.returncode}")
            return "Unknown Device"
            
    except subprocess.TimeoutExpired:
        logger.error("WMI command timed out")
        return "Unknown Device"
    except Exception as e:
        logger.error(f"Error running WMI command: {e}")
        return "Unknown Device"


def get_device_id():
    """
    Create a unique device ID based on motherboard and disk serial numbers.
    
    Returns:
        str: Device ID in format "MB-SN-{board_sn}-DISK-SN-{disk_sn}"
    """
    system = platform.system().lower()
    
    try:
        if system == "linux":
            return _get_device_id_linux()
        elif system == "windows":
            return _get_device_id_windows()
        else:
            logger.warning(f"Unsupported operating system: {system}")
            return "MB-SN-SN_NOT_FOUND-DISK-SN-SN_NOT_FOUND"
    except Exception as e:
        logger.error(f"Error getting device ID: {e}")
        return "MB-SN-SN_NOT_FOUND-DISK-SN-SN_NOT_FOUND"


def _get_device_id_linux():
    """
    Get device ID on Linux using dmidecode and lsblk/hdparm.
    
    Returns:
        str: Device ID
    """
    motherboard_sn = "SN_NOT_FOUND"
    disk_sn = "SN_NOT_FOUND"
    
    # Get motherboard serial number
    try:
        result = subprocess.run(
            ["dmidecode", "-s", "baseboard-serial-number"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            mb_sn = result.stdout.strip()
            if mb_sn and mb_sn.lower() not in ["not specified", "not available", "to be filled by o.e.m."]:
                motherboard_sn = mb_sn
                logger.info(f"Linux motherboard SN: {motherboard_sn}")
    except Exception as e:
        logger.error(f"Error getting motherboard serial number: {e}")
    
    # Get disk serial number - try multiple methods
    # Method 1: lsblk
    try:
        result = subprocess.run(
            ["lsblk", "-dno", "SERIAL", "/dev/sda"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            disk_serial = result.stdout.strip()
            if disk_serial and disk_serial.lower() not in ["", "not specified"]:
                disk_sn = disk_serial
                logger.info(f"Linux disk SN (lsblk): {disk_sn}")
    except Exception as e:
        logger.warning(f"lsblk method failed: {e}")
        
        # Method 2: hdparm (fallback)
        try:
            result = subprocess.run(
                ["hdparm", "-i", "/dev/sda"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                # Parse hdparm output for serial number
                serial_match = re.search(r'SerialNo=(\S+)', result.stdout)
                if serial_match:
                    disk_sn = serial_match.group(1)
                    logger.info(f"Linux disk SN (hdparm): {disk_sn}")
        except Exception as e2:
            logger.error(f"hdparm method also failed: {e2}")
    
    return f"MB-SN-{motherboard_sn}-DISK-SN-{disk_sn}"


def _get_device_id_windows():
    """
    Get device ID on Windows using WMI.
    
    Returns:
        str: Device ID
    """
    motherboard_sn = "SN_NOT_FOUND"
    disk_sn = "SN_NOT_FOUND"
    
    # Get motherboard serial number
    try:
        result = subprocess.run(
            ["wmic", "baseboard", "get", "SerialNumber"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            for line in lines:
                line = line.strip()
                if line and line.lower() not in ["serialnumber", "", "not specified", "to be filled by o.e.m."]:
                    motherboard_sn = line
                    logger.info(f"Windows motherboard SN: {motherboard_sn}")
                    break
    except Exception as e:
        logger.error(f"Error getting motherboard serial number: {e}")
    
    # Get disk serial number
    try:
        result = subprocess.run(
            ["wmic", "diskdrive", "get", "SerialNumber"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            for line in lines:
                line = line.strip()
                if line and line.lower() not in ["serialnumber", "", "not specified"]:
                    disk_sn = line
                    logger.info(f"Windows disk SN: {disk_sn}")
                    break
    except Exception as e:
        logger.error(f"Error getting disk serial number: {e}")
    
    return f"MB-SN-{motherboard_sn}-DISK-SN-{disk_sn}"


def main():
    """
    Example usage and testing function.
    """
    print("Hardware Information Detection")
    print("=" * 40)
    
    # Test device type detection
    print(f"Operating System: {platform.system()}")
    device_type = get_device_type()
    print(f"Device Type: {device_type}")
    
    # Test device ID generation
    device_id = get_device_id()
    print(f"Device ID: {device_id}")
    
    print("\nDetection completed successfully!")


if __name__ == "__main__":
    main()