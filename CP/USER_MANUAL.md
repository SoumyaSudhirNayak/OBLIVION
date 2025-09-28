# Complete Certificate System - User Manual

## 🎯 **System Overview**

This system provides a complete solution for generating and verifying secure data wipe certificates using QR codes. The system consists of two main components:

1. **Python Certificate Generator** - Creates signed JWT certificates and displays them as QR codes
2. **React Native Verifier App** - Scans QR codes and verifies certificates offline

Both components work together to provide end-to-end certificate generation and verification that operates 100% offline.

---

## 🔧 **Part 1: Python Certificate Generator**

### **Prerequisites**
- **Python 3.7+** installed on your computer
- **Required Python packages** (see installation below)

### **Installation**
1. Navigate to the Python scripts directory:
   ```bash
   cd e:\SIH2025\SIH25070\CP\python-scripts
   ```
2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

### **Key Generation (One-time Setup)**
Before generating certificates, you need to create cryptographic keys:

1. **Generate Key Pair**:
   ```bash
   python generate_keys.py
   ```
   - Creates `private_key.pem` and `public_key.pem` in the `output/` folder
   - These keys are used for signing and verifying certificates
   - **Keep the private key secure** - it's used to sign certificates

### **Certificate Generation**
To generate a certificate after data wipe completion:

1. **Run Certificate Generator**:
   ```bash
   python certificate_generator.py
   ```

2. **Certificate Process**:
   - Automatically detects device type (Desktop, Laptop, Server, etc.)
   - Automatically detects device information (motherboard serial, disk serial)
   - Creates a signed JWT certificate with:
     - Certificate ID (unique UUID)
     - Device Type (automatically detected)
     - Device ID (motherboard and disk serial numbers)
     - Wipe method (DoD 5220.22-M 3-pass)
     - Wipe timestamp
     - Cryptographic hash for integrity
     - Issuer information and version
   - Generates QR code containing the certificate
   - Displays QR code in a modern GUI window
   - Saves QR code as PNG file in `output/` folder

3. **Certificate Display**:
   - A window opens showing the QR code with updated design
   - Certificate details are displayed below the QR code including device type
   - Print or photograph the QR code for verification
   - Close the window when done

### **Testing Tools**
The system includes several testing utilities:

- **`generate_test_jwt.py`** - Creates sample certificates for testing
- **`test_jwt_validation.py`** - Validates JWT token signatures
- **`test_end_to_end.py`** - Tests complete certificate pipeline
- **`test_qr_generation.py`** - Tests QR code generation

---

## 📱 **Part 2: React Native Verifier App**

### **Prerequisites**
- **Smartphone** (Android or iOS)
- **Expo Go App** installed on your phone
- **WiFi Connection** (same network as development computer)

---

## 🚀 **Getting Started with Mobile App**

### **Step 1: Install Expo Go**
- **Android**: Download from [Google Play Store](https://play.google.com/store/apps/details?id=host.exp.exponent)
- **iOS**: Download from [App Store](https://apps.apple.com/app/expo-go/id982107779)

### **Step 2: Start the Development Server**
1. Open terminal/command prompt
2. Navigate to the app directory:
   ```bash
   cd e:\SIH2025\SIH25070\CP\react-native-app
   ```
3. Start the server:
   ```bash
   npx expo start
   ```
4. Wait for the QR code to appear in the terminal

### **Step 3: Connect Your Phone**
1. **Android**: Open Expo Go app → Scan QR code from terminal
2. **iOS**: Open Camera app → Point at QR code → Tap notification

### **Step 4: App Will Load**
- The Certificate Verifier app will automatically download and open
- First launch may take 30-60 seconds

---

## 📋 **App Features**

### **🔍 QR Code Scanner**
- **Purpose**: Scan certificate QR codes for verification
- **How to Use**:
  1. Tap "Scan QR Code" on home screen
  2. Point camera at certificate QR code
  3. App automatically scans and processes

### **📄 Professional Certificate Display**
- **Beautiful Design**: Professional certificate layout with Oblivion branding
- **Verification Status**: Clear ✅ VERIFIED badge for authentic certificates
- **Certificate Details**:
  - Device ID
  - Wipe Method (NIST 800-88 Purge)
  - Data Wiped (storage capacity)
  - Completion Time (with IST timezone)
  - Status with color-coded badges

### **💾 Save as Image**
- **Purpose**: Save certificate as PNG image to phone gallery
- **How to Use**:
  1. After scanning a certificate, tap "Save as Image"
  2. Grant storage permissions if prompted
  3. Image saved to phone's gallery/photos

### **📤 Share Certificate**
- **Purpose**: Share certificate via WhatsApp, email, etc.
- **How to Use**:
  1. After scanning a certificate, tap "Share"
  2. Choose sharing method (WhatsApp, Email, etc.)
  3. Certificate image attached automatically

### **📊 Show Full Details**
- **Purpose**: View complete certificate data in JSON format
- **Technical Information**: All certificate fields and metadata

### **🔄 Scan Another Certificate**
- **Purpose**: Return to scanner for additional certificates
- **Quick Access**: One-tap return to scanning mode

---

## 🔒 **Security Features**

### **Offline Verification**
- ✅ **No Internet Required**: All verification happens locally
- ✅ **Privacy Protected**: No data sent to external servers
- ✅ **Instant Results**: Immediate verification feedback

### **Cryptographic Validation**
- ✅ **JWT Token Verification**: Digital signature validation
- ✅ **Public Key Cryptography**: RSA signature verification
- ✅ **Tamper Detection**: Invalid certificates clearly marked

### **Data Integrity**
- ✅ **Certificate Authenticity**: Ensures certificates are genuine
- ✅ **Timestamp Validation**: Verifies certificate creation time
- ✅ **Issuer Verification**: Confirms certificate source

---

---

## 🔄 **Complete Workflow**

### **Step-by-Step Process**

1. **Setup Phase** (One-time):
   - Install Python dependencies: `pip install -r requirements.txt`
   - Generate cryptographic keys: `python generate_keys.py`
   - Install Expo Go app on your phone
   - Set up React Native development environment

2. **Certificate Generation Phase**:
   - After completing data wipe on a device
   - Run: `python certificate_generator.py`
   - QR code window displays with certificate
   - Save/print the QR code for verification

3. **Certificate Verification Phase**:
   - Start React Native app: `npx expo start`
   - Scan QR code with Expo Go app
   - Use app's QR scanner to scan the certificate QR code
   - View verification results and certificate details with modern shield design
   - Save or share the verified certificate

### **Integration Points**
- **Python Generator** creates JWT tokens signed with private key
- **React Native App** verifies JWT tokens using embedded public key
- **QR Codes** serve as the bridge between both systems
- **Offline Operation** ensures security and privacy

---

## 🔒 **Security Features**

### **Cryptographic Security**
- ✅ **RSA-256 Digital Signatures**: Certificates are cryptographically signed
- ✅ **JWT Token Format**: Industry-standard JSON Web Token format
- ✅ **Public Key Verification**: App verifies signatures using embedded public key
- ✅ **Tamper Detection**: Any modification to certificate is detected

### **Offline Operation**
- ✅ **No Internet Required**: Complete system works offline
- ✅ **Privacy Protected**: No data transmitted to external servers
- ✅ **Local Verification**: All verification happens on device
- ✅ **Secure Storage**: Keys and certificates stored locally

### **Certificate Integrity**
- ✅ **Device Identification**: Unique device fingerprinting with motherboard and disk serials
- ✅ **Timestamp Validation**: Wipe completion time verification
- ✅ **Method Verification**: Confirms DoD 5220.22-M 3-pass compliance
- ✅ **Certificate ID**: Unique UUID for each certificate
- ✅ **Device Type Detection**: Automatic hardware type identification

---

## 🛠️ **Troubleshooting**

### **Python Certificate Generator Issues**

**Key Generation Problems**:
- Ensure Python 3.7+ is installed
- Install required packages: `pip install -r requirements.txt`
- Check write permissions in `output/` directory

**Certificate Generation Errors**:
- Verify private key exists in `output/private_key.pem`
- Check device permissions for hardware information access
- Ensure sufficient disk space for QR code images

**QR Code Display Issues**:
- Install tkinter: `pip install tkinter` (if not included with Python)
- Check display settings and screen resolution
- Try running with administrator privileges

### **React Native App Issues**

### **App Won't Load**
1. **Check WiFi**: Ensure phone and computer on same network
2. **Restart Server**: Press `Ctrl+C` in terminal, then `npm start`
3. **Clear Expo Cache**: Shake phone → "Reload" → "Clear cache and reload"

### **QR Code Scanner Issues**
1. **Camera Permissions**: Grant camera access when prompted
2. **Lighting**: Ensure good lighting on QR code
3. **Distance**: Hold phone 6-12 inches from QR code
4. **Focus**: Tap screen to focus camera

### **Save Image Not Working**
1. **Storage Permissions**: Grant storage access when prompted
2. **Storage Space**: Ensure phone has available storage
3. **Try Again**: Close and reopen app if needed

### **Share Feature Issues**
1. **App Selection**: Choose sharing app from the list
2. **Network**: Some sharing methods require internet
3. **Permissions**: Grant necessary app permissions

---

## 📱 **Development Commands**

### **Basic Commands**
```bash
npm start              # Start with Expo Go
npm run start-dev      # Start with development build
npm run start-tunnel   # Start with tunnel (remote access)
```

### **Terminal Controls (while server running)**
- **`r`** - Reload app
- **`j`** - Open debugger
- **`m`** - Toggle developer menu
- **`a`** - Open Android emulator
- **`w`** - Open web version
- **`Ctrl+C`** - Stop server

---

## 🎯 **Usage Scenarios**

### **For IT Administrators**
1. **Device Decommissioning**:
   - Run data wipe on device using NIST SP 800-88 methods
   - Generate certificate: `python certificate_generator.py`
   - Print QR code for physical attachment to device
   - Verify certificate using mobile app for audit trail

2. **Compliance Documentation**:
   - Generate certificates for all wiped devices
   - Save QR codes as digital records
   - Use mobile app to verify and share certificates
   - Maintain audit trail for regulatory compliance

### **For Security Teams**
1. **Asset Disposal Process**:
   - Integrate certificate generation into disposal workflow
   - Verify secure data destruction before device disposal
   - Maintain digital chain of custody with certificates
   - Use mobile verification for field validation

2. **Audit and Compliance**:
   - Generate certificates for audit requirements
   - Verify certificate authenticity during audits
   - Share verified certificates with compliance teams
   - Maintain offline verification capability

### **For End Users**
1. **Personal Device Sales**:
   - Generate certificate after wiping personal device
   - Provide QR code to buyer as proof of data sanitization
   - Buyer can verify certificate using mobile app
   - Ensures privacy protection and buyer confidence

2. **Corporate Device Returns**:
   - Verify corporate device has been properly wiped
   - Scan certificate QR code to confirm data sanitization
   - Submit verified certificate to IT department
   - Maintain proof of secure data handling

---

## 📞 **Support & Maintenance**

### **System Requirements**
- **Python Environment**: Python 3.7+ with pip package manager
- **Mobile Device**: Android 5.0+ or iOS 10.0+
- **Development Environment**: Node.js 14+ for React Native development
- **Network**: WiFi connection for initial app setup
- **Storage**: 100MB free space for certificates and QR codes

### **Regular Maintenance**
- **Key Rotation**: Regenerate keys periodically for enhanced security
- **App Updates**: Update React Native app when new features are added
- **Certificate Cleanup**: Archive old certificates and QR codes
- **Testing**: Run test scripts regularly to verify system integrity

### **Backup and Recovery**
- **Key Backup**: Securely backup private/public key pairs
- **Certificate Archive**: Maintain archive of generated certificates
- **App Configuration**: Backup React Native app configuration
- **Documentation**: Keep updated copies of user manual

---

## 📋 **Technical Specifications**

### **Certificate Format**
- **Standard**: JSON Web Token (JWT) with RS256 signature
- **Key Size**: 2048-bit RSA keys
- **Hash Algorithm**: SHA-256 for data integrity
- **QR Code**: Error correction level M, auto-sizing

### **Supported Platforms**
- **Certificate Generator**: Windows, macOS, Linux (Python 3.7+)
- **Mobile Verifier**: Android 5.0+, iOS 10.0+ (via Expo Go)
- **Development**: Cross-platform React Native development

### **Security Standards**
- **Data Wipe**: NIST SP 800-88 Rev. 1 compliance
- **Cryptography**: RSA-2048 with SHA-256 signatures
- **Token Format**: RFC 7519 JSON Web Token standard
- **Offline Operation**: No network dependencies for verification

---

### **For IT Administrators**
1. **Device Verification**: Quickly verify data sanitization completion
2. **Compliance Audits**: Save certificates as proof of secure data wiping
3. **Record Keeping**: Share certificates with compliance teams

### **For Security Teams**
1. **Asset Disposal**: Verify secure data destruction before device disposal
2. **Chain of Custody**: Maintain digital records of sanitization
3. **Audit Trail**: Professional certificates for regulatory compliance

### **For End Users**
1. **Personal Devices**: Verify your device data has been securely wiped
2. **Device Sales**: Provide proof of data sanitization to buyers
3. **Privacy Assurance**: Confirm personal data completely removed

---

## 📞 **Support**

### **Common Issues**
- **Server Connection**: Ensure same WiFi network
- **QR Code Quality**: Use high-quality printed QR codes
- **App Performance**: Close other apps for better performance

### **Technical Requirements**
- **Android**: Version 5.0+ (API 21+)
- **iOS**: Version 10.0+
- **Network**: WiFi connection for initial setup
- **Storage**: 50MB free space recommended

---

## 🔄 **Updates & Maintenance**

### **App Updates**
- **Automatic**: App updates automatically when server restarts
- **Manual Reload**: Shake phone → "Reload" for manual refresh
- **Cache Clear**: Use "Clear cache and reload" for major updates

### **Server Maintenance**
- **Regular Restarts**: Restart server daily for optimal performance
- **Dependency Updates**: Keep npm packages updated
- **Log Monitoring**: Check terminal for error messages

---

## ✅ **Success Indicators**

### **App Working Correctly**
- ✅ QR code appears in terminal
- ✅ Phone connects without errors
- ✅ Scanner opens and focuses properly
- ✅ Certificates display with professional layout
- ✅ Save and share functions work smoothly

### **Verification Working**
- ✅ Valid certificates show "VERIFIED" badge
- ✅ Invalid certificates show clear error messages
- ✅ All certificate details display correctly
- ✅ Timestamps show in IST timezone

---

**🎉 Your Complete Certificate System is now ready for professional use!**

*This comprehensive system provides end-to-end certificate generation and verification with enterprise-grade security and offline operation capabilities.*

---

## 📚 **Quick Reference**

### **Python Commands**
```bash
# One-time setup
cd e:\SIH2025\SIH25070\CP\python-scripts
pip install -r requirements.txt
python generate_keys.py

# Generate certificate
python certificate_generator.py

# Testing utilities
python generate_test_jwt.py
python test_end_to_end.py
```

### **React Native Commands**
```bash
# Start development server
cd e:\SIH2025\SIH25070\CP\react-native-app
npx expo start

# Terminal controls (while server running)
r - Reload app
j - Open debugger
m - Toggle developer menu
Ctrl+C - Stop server
```

### **File Locations**
- **Keys**: `python-scripts/output/private_key.pem`, `public_key.pem`
- **QR Codes**: `python-scripts/output/certificate_qr_*.png`
- **Test Tokens**: `python-scripts/output/test_jwt_token.txt`
- **App Source**: `react-native-app/src/`

*For technical support or feature requests, refer to the development team.*