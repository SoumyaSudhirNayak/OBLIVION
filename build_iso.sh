#!/usr/bin/env bash
set -euo pipefail

# Build oblivion_os.iso using Buildroot and embed OBLIVION production scripts
# Requirements (host): git, make, gcc, bison, flex, ncurses, gawk, unzip, rsync, bc, wget, cpio, file, python3
# NOTE: Run this on Linux. It will download Buildroot, build a kernel, rootfs, and a bootable ISO image.

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
PROJECT_ROOT="$SCRIPT_DIR"
WORKDIR="$PROJECT_ROOT/.br_work"
BR_VER="2024.08"

mkdir -p "$WORKDIR"
cd "$WORKDIR"

if [ ! -d buildroot ]; then
  echo "Cloning Buildroot $BR_VER ..."
  git clone --branch "$BR_VER" --depth 1 https://github.com/buildroot/buildroot.git
fi

cd buildroot

# Prepare overlay with our Python app and autostart
OVERLAY="$WORKDIR/overlay"
APPDIR="$OVERLAY/usr/local/oblivion"
ETCDIR="$OVERLAY/etc"
mkdir -p "$APPDIR" "$ETCDIR"

# Copy production Python sources
cp -v "$PROJECT_ROOT/src/"*.py "$APPDIR/"
# Bundle private key if available (non-fatal if missing)
if [ -f "$PROJECT_ROOT/CP/python-scripts/output/private_key.pem" ]; then
  cp -v "$PROJECT_ROOT/CP/python-scripts/output/private_key.pem" "$APPDIR/"
else
  echo "WARNING: private_key.pem not found at CP/python-scripts/output/private_key.pem. Build will continue, but runtime JWT signing will fail until key is provided."
fi

# Create BusyBox inittab to autostart OBLIVION on tty1
# We replace the default getty on tty1 by our Python entrypoint.
cat > "$ETCDIR/inittab" << 'INITTAB'
# /etc/inittab - BusyBox init configuration

::sysinit:/etc/init.d/rcS
::shutdown:/etc/init.d/rcK
::ctrlaltdel:/sbin/reboot

# Auto-launch OBLIVION on the primary console
# Launch the production TUI directly per Phase 2 requirement
tty1::respawn:/usr/bin/python3 /usr/local/oblivion/oblivion_core.py

# Optional additional consoles
tty2::respawn:/sbin/getty -L tty2 115200 vt100
tty3::respawn:/sbin/getty -L tty3 115200 vt100
INITTAB

# Generate defconfig with required options
DEFCONFIG="$WORKDIR/oblivion_defconfig"
cat > "$DEFCONFIG" << EOF
# Target: x86_64 PC
BR2_x86_64=y

# Use Buildroot toolchain with glibc
BR2_TOOLCHAIN_BUILDROOT_GLIBC=y

# Linux kernel (use upstream defconfig for x86_64)
BR2_LINUX_KERNEL=y
BR2_LINUX_KERNEL_USE_DEFCONFIG=y
BR2_LINUX_KERNEL_DEFCONFIG="x86_64"
# Embed the root filesystem as initramfs inside the kernel image (simplifies ISO)
BR2_TARGET_ROOTFS_INITRAMFS=y

# Build a bootable ISO with GRUB2 (i386-pc) loader
BR2_TARGET_ROOTFS_ISO9660=y
BR2_TARGET_ROOTFS_ISO9660_GRUB2=y
BR2_TARGET_GRUB2=y
BR2_TARGET_GRUB2_I386_PC=y
# Ensure GRUB has iso9660 and required modules built-in, and boot partition is CD
BR2_TARGET_GRUB2_BOOT_PARTITION="cd"
BR2_TARGET_GRUB2_BUILTIN_MODULES="linux normal iso9660 biosdisk"

# Console over VGA
BR2_TARGET_GENERIC_GETTY=n
BR2_SYSTEM_DHCP=""

# Rootfs overlay to inject our app and config
BR2_ROOTFS_OVERLAY="${OVERLAY}"

# Python3 and runtime deps for our app
BR2_PACKAGE_PYTHON3=y
# Third-party Python packages required by OBLIVION
BR2_PACKAGE_PYTHON_PILLOW=y
BR2_PACKAGE_PYTHON_QRCODE=y
BR2_PACKAGE_PYTHON_PYJWT=y
BR2_PACKAGE_PYTHON_CRYPTOGRAPHY=y
EOF

# Apply defconfig and build
make BR2_DEFCONFIG="$DEFCONFIG" defconfig

# Parallel build (fall back to 1 if nproc not available)
JOBS=1
if command -v nproc >/dev/null 2>&1; then JOBS=$(nproc); fi
make -j"$JOBS"

IMAGES_DIR="$PWD/output/images"
ISO_SRC="$IMAGES_DIR/rootfs.iso9660"
OUT_ISO="$PROJECT_ROOT/oblivion_os.iso"

if [ -f "$ISO_SRC" ]; then
  cp -v "$ISO_SRC" "$OUT_ISO"
  echo "SUCCESS: Created ISO at $OUT_ISO"
  echo "You can boot this ISO on bare metal or in a VM. It will auto-launch OBLIVION on tty1."
else
  echo "ERROR: ISO not found at $ISO_SRC. Please open menuconfig and ensure ISO9660 target is enabled."
  exit 1
fi