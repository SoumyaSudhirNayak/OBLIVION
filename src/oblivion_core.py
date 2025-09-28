#!/usr/bin/env python3
"""
OBLIVION Core TUI (Production)

Console application integrating DiskWiper, hardware info, and certificate
signing. Generates a JWT certificate and QR code after successful wipe.
"""
import os
import sys
import time
import uuid
import jwt
import qrcode
import hashlib
from datetime import datetime
from typing import Optional

from disk_wiper import DiskWiper
from hardware_info import get_device_type, get_device_id

# Helper: resource_path for PyInstaller and dev
def resource_path(relative_path: str) -> str:
    try:
        base_path = sys._MEIPASS  # type: ignore[attr-defined]
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

OUTPUT_DIR = os.path.join(os.path.abspath('.'), 'output')

class OblivionCore:
    def __init__(self):
        self.dw = DiskWiper()
        os.makedirs(OUTPUT_DIR, exist_ok=True)

    def run(self) -> int:
        self._print_header()
        disks = self.dw.list_disks()
        if not disks:
            print("❌ No disks detected. Run as Administrator/root.")
            return 1
        self._display_disks(disks)
        sel = self._prompt_int("Select disk index to wipe", min_val=0, max_val=len(disks)-1)
        target = disks[sel]
        print(f"\nTarget: {target['path']} ({target['model']}) Size: {target['size_bytes']/(1024**3):.1f} GiB")
        print("\nWipe Methods:\n  1) NIST Clear (single pass zeros)\n  2) NIST Purge (random + zeros + verify)")
        method = self._prompt_int("Choose method", min_val=1, max_val=2)
        print("\n⚠️  FINAL WARNING: This operation will PERMANENTLY ERASE data on the selected disk.")
        confirm = input("Type ERASE to proceed: ").strip()
        if confirm != "ERASE":
            print("Operation cancelled.")
            return 2
        start = time.time()
        try:
            def progress(written, total):
                pct = (written/total)*100
                print(f"\rProgress: {pct:6.2f}%", end='')
            if method == 1:
                self.dw.wipe_clear(target['path'], progress=progress)
            else:
                self.dw.wipe_purge(target['path'], progress=progress)
            print("\n✅ Wipe completed successfully.")
        except Exception as e:
            print(f"\n❌ Wipe failed: {e}")
            return 3
        duration = int(time.time() - start)
        token, qr_path = self._generate_certificate(duration, method)
        print(f"\n📄 Certificate JWT length: {len(token)}")
        print(f"📦 QR saved: {qr_path}")
        print("\nScan the QR code file using the OBLIVION mobile verifier app.")
        return 0

    def _generate_certificate(self, wipe_duration: int, method: int):
        device_type = get_device_type()
        device_id = get_device_id()
        cert_id = str(uuid.uuid4())
        now = int(time.time())
        wipe_method = "NIST SP 800-88 Purge" if method == 2 else "NIST SP 800-88 Clear"
        # Deterministic-ish data hash basis
        hash_input = f"{now}-{device_id}-{wipe_method}-{wipe_duration}"
        data_hash = hashlib.sha256(hash_input.encode()).hexdigest()
        payload = {
            'iss': 'OBLIVION',
            'iat': now,
            'certificateID': cert_id,
            'deviceType': device_type,
            'deviceID': device_id,
            'wipeMethod': wipe_method,
            'wipeTimestamp': now,
            'dataHash': data_hash,
        }
        # Load private key via resource_path
        key_path_candidates = [
            resource_path('private_key.pem'),
            os.path.join(os.path.dirname(__file__), '..', 'CP', 'python-scripts', 'output', 'private_key.pem'),
            os.path.join(os.path.abspath('.'), 'CP', 'python-scripts', 'output', 'private_key.pem'),
            os.path.join(os.path.abspath('.'), 'python-scripts', 'output', 'private_key.pem'),
        ]
        private_key = None
        for kp in key_path_candidates:
            try:
                if os.path.exists(kp):
                    with open(kp, 'r', encoding='utf-8') as f:
                        private_key = f.read()
                        break
            except Exception:
                pass
        if not private_key:
            raise RuntimeError('private_key.pem not found. Ensure it is bundled or present.')
        token = jwt.encode(payload, private_key, algorithm='RS256')
        # Generate QR
        qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=8, border=4)
        qr.add_data(token)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        qr_path = os.path.join(OUTPUT_DIR, f"certificate_qr_{ts}.png")
        img.save(qr_path)
        return token, qr_path

    def _display_disks(self, disks):
        print("Detected Disks:")
        for i, d in enumerate(disks):
            print(f"  [{i}] {d['path']} | {d['model']} | {d['size_bytes']/(1024**3):.1f} GiB")

    def _prompt_int(self, label: str, min_val: int, max_val: int) -> int:
        while True:
            try:
                val = int(input(f"{label} ({min_val}-{max_val}): ").strip())
                if min_val <= val <= max_val:
                    return val
            except Exception:
                pass
            print("Invalid selection. Try again.")

if __name__ == '__main__':
    core = OblivionCore()
    rc = core.run()
    sys.exit(rc)