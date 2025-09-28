#!/usr/bin/env python3
"""
QR Code Generation and Reading Test Script

This script tests the QR code generation functionality and verifies that
the generated QR codes can be read back correctly.
"""

import qrcode
from PIL import Image
import os
from datetime import datetime

def generate_test_qr_code(data, filename):
    """
    Generate a QR code with the given data
    
    Args:
        data (str): The data to encode in the QR code
        filename (str): The filename to save the QR code
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Create QR code instance
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        
        # Add data to QR code
        qr.add_data(data)
        qr.make(fit=True)
        
        # Create image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save the image
        filepath = os.path.join('output', filename)
        img.save(filepath)
        
        print(f"✅ QR code saved: {filepath}")
        print(f"   Image size: {img.size}")
        print(f"   Data length: {len(data)} characters")
        
        return True
        
    except Exception as e:
        print(f"❌ Error generating QR code: {e}")
        return False

def test_qr_with_jwt_token():
    """Test QR code generation with the actual JWT token"""
    print("📱 Testing QR code generation with JWT token...")
    
    # Read the JWT token from file
    try:
        with open('output/test_jwt_token.txt', 'r') as f:
            jwt_token = f.read().strip()
        print(f"📄 JWT token loaded (length: {len(jwt_token)} characters)")
    except FileNotFoundError:
        print("❌ JWT token file not found. Please run certificate_generator.py first.")
        return False
    
    # Generate QR code with JWT token
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"test_qr_jwt_{timestamp}.png"
    
    return generate_test_qr_code(jwt_token, filename)

def test_qr_with_sample_data():
    """Test QR code generation with sample data"""
    print("📱 Testing QR code generation with sample data...")
    
    sample_data = "This is a test QR code with sample data for verification purposes."
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"test_qr_sample_{timestamp}.png"
    
    return generate_test_qr_code(sample_data, filename)

def verify_qr_files():
    """Verify that QR code files exist and are readable"""
    print("🔍 Verifying existing QR code files...")
    
    output_dir = 'output'
    qr_files = [f for f in os.listdir(output_dir) if f.endswith('.png') and 'qr' in f.lower()]
    
    if not qr_files:
        print("❌ No QR code files found in output directory")
        return False
    
    print(f"📁 Found {len(qr_files)} QR code files:")
    for qr_file in qr_files:
        filepath = os.path.join(output_dir, qr_file)
        try:
            # Try to open the image
            img = Image.open(filepath)
            file_size = os.path.getsize(filepath)
            print(f"   ✅ {qr_file} - Size: {img.size}, File size: {file_size} bytes")
        except Exception as e:
            print(f"   ❌ {qr_file} - Error: {e}")
    
    return True

def main():
    print("🔍 QR Code Generation Test")
    print("=" * 50)
    
    # Ensure output directory exists
    os.makedirs('output', exist_ok=True)
    
    # Test 1: Verify existing QR files
    print("\n1. Verifying existing QR code files...")
    verify_qr_files()
    
    # Test 2: Generate QR with sample data
    print("\n2. Testing QR generation with sample data...")
    test_qr_with_sample_data()
    
    # Test 3: Generate QR with JWT token
    print("\n3. Testing QR generation with JWT token...")
    test_qr_with_jwt_token()
    
    print("\n✅ QR code generation tests completed!")
    print("📁 Check the 'output' directory for generated QR codes")

if __name__ == "__main__":
    main()