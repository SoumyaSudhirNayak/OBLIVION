#!/usr/bin/env python3
"""
RS256 Key Pair Generator for Secure Certificate System

This utility generates an RS256 private/public key pair for use in the
offline certificate system. The private key is used by the certificate
generator, and the public key is embedded in the mobile verifier app.

Usage:
    python generate_keys.py

Output:
    - output/private_key.pem: Private key for signing certificates
    - output/public_key.pem: Public key for verifying certificates
    - Console output: Key strings for embedding in code
"""

import os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


def generate_rsa_key_pair():
    """
    Generate an RSA key pair suitable for RS256 JWT signing.
    
    Returns:
        tuple: (private_key, public_key) cryptography objects
    """
    # Generate private key with 2048-bit key size (recommended for RS256)
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    
    # Extract public key from private key
    public_key = private_key.public_key()
    
    return private_key, public_key


def serialize_keys(private_key, public_key):
    """
    Serialize keys to PEM format strings.
    
    Args:
        private_key: RSA private key object
        public_key: RSA public key object
        
    Returns:
        tuple: (private_pem_string, public_pem_string)
    """
    # Serialize private key to PEM format
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    # Serialize public key to PEM format
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    return private_pem.decode('utf-8'), public_pem.decode('utf-8')


def save_keys_to_files(private_pem, public_pem, output_dir='output'):
    """
    Save PEM-formatted keys to files in the output directory.
    
    Args:
        private_pem (str): Private key in PEM format
        public_pem (str): Public key in PEM format
        output_dir (str): Directory to save keys (default: 'output')
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Save private key
    private_key_path = os.path.join(output_dir, 'private_key.pem')
    with open(private_key_path, 'w') as f:
        f.write(private_pem)
    
    # Save public key
    public_key_path = os.path.join(output_dir, 'public_key.pem')
    with open(public_key_path, 'w') as f:
        f.write(public_pem)
    
    return private_key_path, public_key_path


def print_keys_for_embedding(private_pem, public_pem):
    """
    Print keys in a format suitable for embedding in source code.
    
    Args:
        private_pem (str): Private key in PEM format
        public_pem (str): Public key in PEM format
    """
    print("\n" + "="*80)
    print("GENERATED RSA KEY PAIR FOR CERTIFICATE SYSTEM")
    print("="*80)
    
    print("\n📁 FILES SAVED:")
    print("   - output/private_key.pem")
    print("   - output/public_key.pem")
    
    print("\n🔐 PRIVATE KEY (for certificate_generator.py):")
    print("Copy this string into the PRIVATE_KEY variable:")
    print("-" * 60)
    print(f'PRIVATE_KEY = """{private_pem}"""')
    
    print("\n🔓 PUBLIC KEY (for React Native App.js):")
    print("Copy this string into the PUBLIC_KEY variable:")
    print("-" * 60)
    print(f'const PUBLIC_KEY = `{public_pem}`;')
    
    print("\n⚠️  SECURITY NOTES:")
    print("   - Keep the private key secure and never share it")
    print("   - The public key can be safely embedded in the mobile app")
    print("   - These keys are paired - use them together for the system")
    print("="*80)


def main():
    """
    Main function to generate and save RSA key pair.
    """
    try:
        print("🔑 Generating RSA key pair for certificate system...")
        
        # Generate key pair
        private_key, public_key = generate_rsa_key_pair()
        
        # Serialize to PEM format
        private_pem, public_pem = serialize_keys(private_key, public_key)
        
        # Save to files
        private_path, public_path = save_keys_to_files(private_pem, public_pem)
        
        # Print for embedding in code
        print_keys_for_embedding(private_pem, public_pem)
        
        print(f"\n✅ Key generation completed successfully!")
        print(f"   Private key saved to: {private_path}")
        print(f"   Public key saved to: {public_path}")
        
    except Exception as e:
        print(f"❌ Error generating keys: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())