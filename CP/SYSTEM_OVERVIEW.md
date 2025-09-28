# Offline QR-Code-Based Secure Certificate System

## 🎯 Project Overview

This system provides a complete solution for generating and verifying secure data wipe certificates using QR codes with modern shield-based design. The system consists of two main components:

1. **Python Certificate Generator** - Creates signed JWT certificates with real hardware detection and displays them as QR codes
2. **React Native Verifier App** - Scans QR codes and verifies certificates offline with professional shield-based UI

## 🏗️ System Architecture

```
┌─────────────────────┐    QR Code    ┌─────────────────────┐
│  Python Generator   │──────────────▶│ React Native App    │
│                     │               │                     │
│ • Hardware Detection│               │ • Scan QR Code      │
│ • Generate Keys     │               │ • Verify JWT        │
│ • Sign Certificate  │               │ • Shield UI Design  │
│ • Create QR Code    │               │ • Display Results   │
│ • Display GUI       │               │ • Offline Operation │
└─────────────────────┘               └─────────────────────┘
```

## 📁 Project Structure

```
CP/
├── python-scripts/                 # Python certificate generator
│   ├── generate_keys.py            # RSA key pair generation
│   ├── certificate_generator.py    # Main certificate generator with GUI
│   ├── hardware_info.py            # Hardware detection utilities
│   ├── generate_test_jwt.py        # Test JWT generator (no GUI)
│   ├── requirements.txt            # Python dependencies
│   └── output/                     # Generated files
│       ├── private_key.pem         # RSA private key
│       ├── public_key.pem          # RSA public key
│       ├── test_jwt_token.txt      # Sample JWT for testing
│       └── certificate_qr_*.png    # Generated QR code images
│
├── react-native-app/               # React Native verifier app
│   ├── package.json                # App dependencies
│   ├── App.js                      # Main app navigation
│   ├── metro.config.js             # Metro bundler configuration
│   ├── assets/                     # App icons and shield graphics
│   │   ├── shield.png              # Shield background image
│   │   └── oblivion-logo.png       # App logo
│   ├── src/
│   │   ├── components/
│   │   │   ├── ScannerScreen.js    # QR code scanner component
│   │   │   └── CertificateView.js  # Certificate display with shield design
│   │   ├── utils/
│   │   │   └── jwtVerifier.js      # JWT verification utility
│   │   └── demo-data/
│   │       └── sampleCertificates.js # Test data for development
│   ├── android/
│   │   └── app/src/main/AndroidManifest.xml # Android permissions
│   └── ios/
│       └── CertificateVerifier/Info.plist   # iOS permissions
│
└── README.md                       # Project documentation
```

## 🔐 Security Features

### Cryptographic Implementation
- **Algorithm**: RS256 (RSA with SHA-256)
- **Key Size**: 2048-bit RSA keys
- **JWT Standard**: RFC 7519 compliant
- **Offline Verification**: No network required for certificate validation

### Certificate Contents
- **Certificate ID**: Unique UUID for each certificate
- **Issuer**: Certificate authority identifier (SecureWipe Pro v2.1)
- **Version**: Certificate format version (2.1.0)
- **Issue Timestamp**: When the certificate was created
- **Device Type**: Automatically detected (Desktop, Laptop, Server, etc.)
- **Device ID**: Motherboard serial number and disk serial number
- **Wipe Method**: Sanitization standard used (DoD 5220.22-M 3-pass)
- **Wipe Timestamp**: When the wipe was performed
- **Data Hash**: SHA-256 hash of wiped data for integrity verification

## 🚀 Getting Started

### Prerequisites
- Python 3.7+ with pip
- Node.js 14+ with npm/yarn
- React Native development environment
- Android Studio (for Android) or Xcode (for iOS)

### Step 1: Set Up Python Environment

```bash
cd python-scripts
pip install -r requirements.txt
```

### Step 2: Generate RSA Key Pair

```bash
python generate_keys.py
```

This creates:
- `output/private_key.pem` - Used by the certificate generator
- `output/public_key.pem` - Used by the React Native app

### Step 3: Generate Test Certificate

```bash
# For GUI version (displays QR code window)
python certificate_generator.py

# For command-line version (generates JWT token only)
python generate_test_jwt.py
```

### Step 4: Set Up React Native App

```bash
cd ../react-native-app
npm install

# Run with Expo
npx expo start

# Scan QR code with Expo Go app or run on simulator
```

## 📱 Using the System

### Certificate Generation (Python)

1. **Run the generator**:
   ```bash
   python certificate_generator.py
   ```

2. **Review certificate details** in the GUI window

3. **Scan the QR code** with the React Native app or save the image

4. **Share the certificate** by saving or printing the QR code

### Certificate Verification (React Native)

1. **Open the app** on your mobile device

2. **Tap "Scan Certificate"** to activate the camera

3. **Point camera at QR code** - the app will automatically scan

4. **View results**:
   - ✅ **Valid Certificate**: Shows detailed information
   - ❌ **Invalid Certificate**: Shows error message

5. **Review certificate details** including device info, wipe method, and timestamps

## 🧪 Testing

### Test Data Available

The system includes comprehensive test data:

- **Valid Certificate**: Properly signed JWT with current timestamp
- **Invalid Certificate**: Malformed or unsigned token
- **Expired Certificate**: Valid signature but expired timestamp
- **Test Scenarios**: Various edge cases for thorough testing

### Manual Testing Steps

1. **Generate test JWT**:
   ```bash
   python generate_test_jwt.py
   ```

2. **Copy the generated token** from `output/test_jwt_token.txt`

3. **Create a QR code** from the token using any QR generator

4. **Scan with the React Native app** to verify functionality

## 🔧 Configuration

### Updating Keys

If you need to generate new keys:

1. **Generate new key pair**:
   ```bash
   python generate_keys.py
   ```

2. **Update the private key** in `certificate_generator.py`

3. **Update the public key** in `react-native-app/src/utils/jwtVerifier.js`

4. **Ensure both keys match** for proper verification

### Customizing Certificate Fields

Edit the `create_certificate_payload()` function in `certificate_generator.py` to modify:
- Certificate issuer name
- Additional metadata fields
- Validation rules
- Expiration policies

## 🛠️ Troubleshooting

### Common Issues

1. **"Invalid signature" error**:
   - Ensure private and public keys match
   - Verify key format (PEM with proper headers)

2. **Camera permission denied**:
   - Check Android/iOS permissions in manifest files
   - Grant camera access in device settings

3. **QR code not scanning**:
   - Ensure good lighting and steady camera
   - Verify QR code contains valid JWT token

4. **Python dependencies error**:
   - Use virtual environment
   - Install exact versions from requirements.txt

### Debug Mode

Enable debug logging in the React Native app by modifying `jwtVerifier.js`:

```javascript
// Add console.log statements for debugging
console.log('Token received:', token);
console.log('Verification result:', result);
```

## 📋 System Requirements

### Python Component
- Python 3.7+
- Libraries: PyJWT, qrcode, Pillow, cryptography
- GUI: tkinter (usually included with Python)

### React Native Component
- React Native 0.70+
- Libraries: react-native-camera, jsrsasign, react-navigation
- Platforms: Android 6.0+, iOS 11.0+

## 🔒 Security Considerations

### Production Deployment

1. **Key Management**:
   - Store private keys securely (HSM, key vault)
   - Rotate keys periodically
   - Use different keys for different environments

2. **Certificate Validation**:
   - Implement expiration checks
   - Add revocation list support
   - Validate certificate chain

3. **Mobile App Security**:
   - Enable certificate pinning
   - Implement anti-tampering measures
   - Use secure storage for sensitive data

### Compliance

This system supports compliance with:
- **NIST SP 800-88**: Guidelines for Media Sanitization
- **DoD 5220.22-M**: Data Sanitization Standards
- **GDPR**: Right to erasure verification
- **HIPAA**: Secure data destruction requirements

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the code comments for implementation details
3. Test with the provided sample data
4. Verify key pair compatibility between components

## 🎉 Success Indicators

The system is working correctly when:
- ✅ Keys generate without errors
- ✅ Certificates display in GUI window
- ✅ QR codes scan successfully
- ✅ Valid certificates show green checkmark
- ✅ Invalid certificates show error message
- ✅ Certificate details display correctly

This completes the offline QR-code-based secure certificate system implementation!