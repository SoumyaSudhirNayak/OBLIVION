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

# Ensure no legacy configs from previous runs
echo "--- Resetting previous Buildroot state (distclean) ---"
make distclean || true

# Prepare overlay with our Python app and autostart
OVERLAY="$WORKDIR/overlay"
APPDIR="$OVERLAY/usr/local/oblivion"
ETCDIR="$OVERLAY/etc"
mkdir -p "$APPDIR" "$ETCDIR"

# Copy production Python sources
echo "--- Copying OBLIVION source files into overlay ---"
cp -v "$PROJECT_ROOT/src/"*.py "$APPDIR/"
# Bundle private key if available (non-fatal if missing)
if [ -f "$PROJECT_ROOT/CP/python-scripts/output/private_key.pem" ]; then
  cp -v "$PROJECT_ROOT/CP/python-scripts/output/private_key.pem" "$APPDIR/"
else
  echo "WARNING: private_key.pem not found. Build will continue, but JWT signing will fail."
fi

# Create BusyBox inittab to autostart OBLIVION on tty1
cat > "$ETCDIR/inittab" << 'INITTAB'
# /etc/inittab - BusyBox init configuration

::sysinit:/etc/init.d/rcS
::shutdown:/etc/init.d/rcK
::ctrlaltdel:/sbin/reboot

# Auto-launch OBLIVION on the primary console
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
BR2_TARGET_ROOTFS_INITRAMFS=y

# Build a bootable ISO with ISOLINUX (avoids GRUB2 legacy symbols)
BR2_TARGET_ROOTFS_ISO9660=y
BR2_TARGET_ROOTFS_ISO9660_ISOLINUX=y
BR2_TARGET_ROOTFS_ISO9660_HYBRID=y

# Rootfs overlay to inject our app and config
BR2_ROOTFS_OVERLAY="${OVERLAY}"

# Python3 and runtime deps for our app (correct python3-* symbols)
BR2_PACKAGE_PYTHON3=y
BR2_PACKAGE_PYTHON3_PILLOW=y
BR2_PACKAGE_PYTHON3_QRCODE=y
BR2_PACKAGE_PYTHON3_PYJWT=y
BR2_PACKAGE_PYTHON3_CRYPTOGRAPHY=y

# Optional Python dependencies inside the target (readline, gdbm)
BR2_PACKAGE_READLINE=y
BR2_PACKAGE_GDBM=y

# Kernel build helper (objtool) needs libelf on host and target
BR2_PACKAGE_LIBELF=y

# Essential system utilities
BR2_PACKAGE_HDPARM=y
BR2_PACKAGE_DMIDECODE=y
BR2_PACKAGE_UTIL_LINUX=y
BR2_PACKAGE_UTIL_LINUX_LSBLK=y
EOF

# --- Robust build sequence ---

echo "--- Applying initial configuration ---"
make BR2_DEFCONFIG="$DEFCONFIG" defconfig

echo "--- Updating configuration to new format ---"
make olddefconfig

# Parallel build (fall back to 1 if nproc not available)
echo "--- Starting final build (this will take a while) ---"
JOBS=1
if command -v nproc >/dev/null 2>&1; then JOBS=$(nproc); fi
make -j"$JOBS"

# --- Final step: Copy the ISO to the project root ---
IMAGES_DIR="$PWD/output/images"
ISO_SRC="$IMAGES_DIR/rootfs.iso9660"
OUT_ISO="$PROJECT_ROOT/oblivion_os.iso"

if [ -f "$ISO_SRC" ]; then
  cp -v "$ISO_SRC" "$OUT_ISO"
  echo ""
  echo "--- SUCCESS ---"
  echo "Created ISO at: $OUT_ISO"
  echo "You can now boot this ISO in a virtual machine."
else
  echo ""
  echo "--- BUILD FAILED ---"
  echo "ERROR: ISO not found at $ISO_SRC. Please check the build logs for errors."
  exit 1
fi