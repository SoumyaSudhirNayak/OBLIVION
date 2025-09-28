#!/usr/bin/env python3
"""
Test JWT Generator for React Native App Testing

This script generates a sample JWT certificate that can be used to test
the React Native QR scanner and verification functionality.
"""

import jwt
import json
import time
import hashlib
import platform
import uuid
from datetime import datetime

# Use the same private key as the certificate generator
PRIVATE_KEY = """-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCsdBXu1MwviIQE
6Qvwy/jVWEDpJtx/VHbD8JL5Dn8Jg+WjsQwap3F+MBgUX6TVeFgTDrqO/zPgKD7R
AuSTIQlwIN90+nk+5njvDCoUplXwhtt+Q8GoZfTH8uz7rqTuO0hZeUYmLbYtG2kz
NJwR1WMggEwuivFL1Tka2bADIMZo2JrYocY1oaal6JNf0b7kxPVz5fFQblr0C7UQ
Yn6j5bp5BSWCN5qLkuLZuicF2mdcmogubMvO9TkpscwLnUaK4GXX6ep35lMc1FyA
RRzUAj9Bq1GEHcOXzcZ8lgjGT3LGOyK6C+LK6jXZrzVepkeF/coCH93dGvx3uyxr
9KVXgRIJAgMBAAECggEATq5kN2R1iJZjjY36ebHGZShv7TBi1+Fkkn9XvzRC98dq
5aVonVyaJnWw9tKwdQkEPiWxLn73XyVdi6UjPpGLKdKFwWxqFy22LXLCXEuL2ELf
MBuf5sIlzXhjcW08KMl5eAEh5Vdjz+66r7coIebW5ERE/dM8xlmRRVPev36bp8ez
JlVkWKg7Lg5Ktubv4e2CQxoHOe/B9qKRTY6YPCIn41RylMzStzTJGXm4iyAdBHfc
wwu09YfHbY2GSZ2JxeO7eHQkERLgwzYk3JchJjkYHMlAkPed4W0IQAoIjHCJ+bMh
1KLxFS822ykmDbwbPrLsxgQpomvQUODT2K5vtWRxhQKBgQDoL5l3yRh+MmXomK7a
KVwsVyRg3r/bUcS/KjSN5PsJeR+K6DCyBpmaUteNNJB9r4/hENuEn05in5W3idim
MjA0DnYzW62u69XQNjvM+tSmA0qaaFwBNHKuDib6cug4Yp3furj97/PJMABm0N+O
16g8Tg9o/g38KGauEHMkaAvWJwKBgQC+JB4kIRpuslKfFvNNLQ+fpLHKfe7zeAM9
Kir62cv7FmByQeHKFS5LRd645+2x2XObePeL0oVhNWs7vCJHOaggWpvFPltVljFt
y4wtkJLjSznBzMqy7O7G6ni+HeawfoFdD5EsYLNaRyORZA3k4KhiAWs0Kpgp2nRh
GSAe7q+kTwKBgQC0khAwcFx0CI3ozpVtZS0h7sOD8rgSwQzZ/uDQWXxCach2Jw13
5lofAr5QOskEdjzXNF0ET0COwr2U98dduTpzwat7VZlFqHOocgUf7RLj6TtjyjWD
Wl61rpvxutuOvmM5U+X611oo5QPq8hZq6J0WCT9C0BHgQStZw8FIVwKdkQKBgFlu
kYK60zznwPa1C8DsBeI3y6wLaZ24gAV/1PFiCZBS6RA0rqenKLwc4/IinGk/dyHU
VtK8NSIQxxw0lAbeNpbpJ0Ux3DG4UA1tZMR1sLEZy9O8qEZaLMEAvcPmOoAfMGd+
D/FIlnNK7I7Q+bwCcxCNzEegFSvyZTTaZYJHD/P/AoGAe1pEEYHhCwF1axbhpsY4
ZeXrY6VugGPRQ8PKY2ZcJbjp5MODorR6kLOOn6XsFIug3u7E9KP8cxFbV5PlFaxw
/bjpxleEMqE5ljjpYL2p//maTkRyF3mWg9inWMzMRUETeUOGM/gNTvXcVaPTeSkm
BfghFptmmOTXmABztywt2lU=
-----END PRIVATE KEY-----"""

def generate_test_certificate():
    """Generate a test certificate with sample data"""
    
    # Current timestamp
    current_time = int(time.time())
    wipe_time = current_time - 300  # 5 minutes ago
    
    # Sample certificate payload
    payload = {
        "iss": "OBLIVION",
        "iat": current_time,
        "deviceID": "TEST-DEVICE-12345",
        "wipeMethod": "NIST SP 800-88 Purge",
        "wipeStatus": "Complete",
        "wipeTimestamp": wipe_time,
        "dataHash": "sha256:abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890"
    }
    
    try:
        # Sign the JWT
        token = jwt.encode(payload, PRIVATE_KEY, algorithm='RS256')
        return token, payload
    except Exception as e:
        print(f"❌ Error generating test certificate: {e}")
        return None, None

def main():
    print("🧪 Test JWT Certificate Generator")
    print("=" * 50)
    
    # Generate test certificate
    token, payload = generate_test_certificate()
    
    if token:
        print("✅ Test certificate generated successfully!")
        print("\n📋 Certificate Details:")
        print(f"   Device ID: {payload['deviceID']}")
        print(f"   Wipe Method: {payload['wipeMethod']}")
        print(f"   Wipe Status: {payload['wipeStatus']}")
        print(f"   Issue Time: {datetime.fromtimestamp(payload['iat']).strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   Wipe Time: {datetime.fromtimestamp(payload['wipeTimestamp']).strftime('%Y-%m-%d %H:%M:%S')}")
        
        print("\n🔐 JWT Token:")
        print("-" * 80)
        print(token)
        print("-" * 80)
        
        # Save to file for easy copying
        with open('output/test_jwt_token.txt', 'w') as f:
            f.write(token)
        
        print(f"\n💾 Token saved to: output/test_jwt_token.txt")
        print("\n📱 You can use this token to test the React Native app!")
        print("   Copy the token and paste it into the demo data or scan it as a QR code.")
        
    else:
        print("❌ Failed to generate test certificate")

if __name__ == "__main__":
    main()