# 🔧 Troubleshooting Guide - Certificate Verification System

**Version**: 1.0.0  
**Last Updated**: January 26, 2025  
**Team**: Oblivion - SIH 2025

---

## 📋 **Table of Contents**

1. [Quick Troubleshooting](#-quick-troubleshooting)
2. [Python Certificate Generator Issues](#-python-certificate-generator-issues)
3. [React Native Mobile App Issues](#-react-native-mobile-app-issues)
4. [QR Code and Scanning Issues](#-qr-code-and-scanning-issues)
5. [JWT and Cryptographic Issues](#-jwt-and-cryptographic-issues)
6. [Build and Deployment Issues](#-build-and-deployment-issues)
7. [Performance Issues](#-performance-issues)
8. [Security and Permission Issues](#-security-and-permission-issues)
9. [Network and Connectivity Issues](#-network-and-connectivity-issues)
10. [Platform-Specific Issues](#-platform-specific-issues)
11. [Development Environment Issues](#-development-environment-issues)
12. [Debugging Tools and Techniques](#-debugging-tools-and-techniques)

---

## ⚡ **Quick Troubleshooting**

### **Common Quick Fixes**

| Issue | Quick Solution | Time Required |
|-------|---------------|---------------|
| **App won't start** | Restart device, clear app cache | 2 minutes |
| **QR code won't scan** | Check camera permissions, clean camera lens | 1 minute |
| **Certificate invalid** | Check system date/time, verify certificate expiry | 2 minutes |
| **Build fails** | Clear cache, reinstall dependencies | 5 minutes |
| **Keys not found** | Run key generation script | 3 minutes |
| **GUI not showing** | Check display settings, restart application | 2 minutes |

### **Emergency Contacts**
- **Technical Support**: support@certificateverifier.com
- **Emergency Hotline**: +1-XXX-XXX-XXXX (24/7)
- **Documentation**: https://docs.certificateverifier.com

### **System Health Check**
```bash
# Quick system health check script
python -c "
import os, sys
print('Python Version:', sys.version)
print('Current Directory:', os.getcwd())
print('Keys Exist:', os.path.exists('keys/private_key.pem') and os.path.exists('keys/public_key.pem'))
print('Output Directory Writable:', os.access('output/certificates', os.W_OK) if os.path.exists('output/certificates') else 'Directory not found')
"
```

---

## 🐍 **Python Certificate Generator Issues**

### **Issue 1: Application Won't Start**

#### **Symptoms**
- Double-clicking executable does nothing
- Command line shows "No module named..." errors
- GUI window doesn't appear

#### **Diagnosis**
```python
# diagnosis_script.py
import sys
import os
import tkinter as tk
from pathlib import Path

def diagnose_startup_issues():
    print("=== Certificate Generator Startup Diagnosis ===")
    
    # Check Python version
    print(f"Python Version: {sys.version}")
    
    # Check current directory
    print(f"Current Directory: {os.getcwd()}")
    
    # Check if running from correct location
    expected_files = ['certificate_generator.py', 'keys/', 'output/']
    missing_files = [f for f in expected_files if not os.path.exists(f)]
    
    if missing_files:
        print(f"❌ Missing files/directories: {missing_files}")
        print("Solution: Run from the correct project directory")
    else:
        print("✅ All required files/directories found")
    
    # Check dependencies
    required_modules = ['cryptography', 'PIL', 'qrcode', 'jwt', 'tkinter']
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module} - OK")
        except ImportError:
            missing_modules.append(module)
            print(f"❌ {module} - MISSING")
    
    if missing_modules:
        print(f"\nSolution: Install missing modules:")
        print(f"pip install {' '.join(missing_modules)}")
    
    # Test GUI
    try:
        root = tk.Tk()
        root.withdraw()
        print("✅ GUI system - OK")
        root.destroy()
    except Exception as e:
        print(f"❌ GUI system - ERROR: {e}")
        print("Solution: Install tkinter or check display settings")

if __name__ == "__main__":
    diagnose_startup_issues()
```

#### **Solutions**

**Solution 1: Missing Dependencies**
```bash
# Install all required dependencies
pip install -r requirements.txt

# Or install individually
pip install cryptography Pillow qrcode PyJWT
```

**Solution 2: Wrong Directory**
```bash
# Navigate to correct directory
cd /path/to/certificate-verification-system/python-scripts

# Verify you're in the right place
ls -la
# Should see: certificate_generator.py, keys/, output/, requirements.txt
```

**Solution 3: GUI Issues (Linux)**
```bash
# Install tkinter (Ubuntu/Debian)
sudo apt-get install python3-tk

# Set display variable
export DISPLAY=:0.0

# For SSH connections, enable X11 forwarding
ssh -X username@hostname
```

**Solution 4: Executable Issues**
```bash
# Rebuild executable with all dependencies
pyinstaller --onefile --windowed \
    --add-data "keys;keys" \
    --add-data "templates;templates" \
    --hidden-import=cryptography \
    --hidden-import=PIL \
    --hidden-import=qrcode \
    --hidden-import=jwt \
    certificate_generator.py
```

### **Issue 2: Key Generation Failures**

#### **Symptoms**
- "Failed to generate RSA keys" error
- Empty or corrupted key files
- Permission denied when accessing keys

#### **Diagnosis**
```python
# key_diagnosis.py
import os
import stat
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

def diagnose_key_issues():
    print("=== Key Generation Diagnosis ===")
    
    key_dir = "keys"
    private_key_path = os.path.join(key_dir, "private_key.pem")
    public_key_path = os.path.join(key_dir, "public_key.pem")
    
    # Check directory permissions
    if not os.path.exists(key_dir):
        print(f"❌ Keys directory doesn't exist: {key_dir}")
        print("Solution: Create keys directory")
        os.makedirs(key_dir, exist_ok=True)
        return
    
    # Check write permissions
    if not os.access(key_dir, os.W_OK):
        print(f"❌ No write permission to keys directory")
        print("Solution: Fix directory permissions")
        return
    
    # Check existing keys
    for key_path, key_type in [(private_key_path, "Private"), (public_key_path, "Public")]:
        if os.path.exists(key_path):
            try:
                with open(key_path, 'rb') as f:
                    key_data = f.read()
                
                if key_type == "Private":
                    serialization.load_pem_private_key(key_data, password=None)
                else:
                    serialization.load_pem_public_key(key_data)
                
                # Check permissions
                file_stat = os.stat(key_path)
                permissions = stat.filemode(file_stat.st_mode)
                print(f"✅ {key_type} key valid - Permissions: {permissions}")
                
            except Exception as e:
                print(f"❌ {key_type} key corrupted: {e}")
                print(f"Solution: Delete and regenerate {key_path}")
        else:
            print(f"❌ {key_type} key missing: {key_path}")
    
    # Test key generation
    try:
        test_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        print("✅ Key generation capability - OK")
    except Exception as e:
        print(f"❌ Key generation failed: {e}")

if __name__ == "__main__":
    diagnose_key_issues()
```

#### **Solutions**

**Solution 1: Regenerate Keys**
```python
# regenerate_keys.py
import os
from generate_keys import generate_rsa_keypair

def force_regenerate_keys():
    # Backup existing keys
    if os.path.exists("keys/private_key.pem"):
        os.rename("keys/private_key.pem", "keys/private_key_backup.pem")
    if os.path.exists("keys/public_key.pem"):
        os.rename("keys/public_key.pem", "keys/public_key_backup.pem")
    
    # Generate new keys
    result = generate_rsa_keypair()
    
    if result["success"]:
        print("✅ Keys regenerated successfully")
        # Remove backups
        for backup in ["keys/private_key_backup.pem", "keys/public_key_backup.pem"]:
            if os.path.exists(backup):
                os.remove(backup)
    else:
        print(f"❌ Key generation failed: {result['error']}")
        # Restore backups
        if os.path.exists("keys/private_key_backup.pem"):
            os.rename("keys/private_key_backup.pem", "keys/private_key.pem")
        if os.path.exists("keys/public_key_backup.pem"):
            os.rename("keys/public_key_backup.pem", "keys/public_key.pem")

if __name__ == "__main__":
    force_regenerate_keys()
```

**Solution 2: Fix Permissions**
```bash
# Linux/macOS
chmod 700 keys/
chmod 600 keys/*.pem

# Windows (PowerShell as Administrator)
icacls keys /inheritance:d
icacls keys /grant:r "%USERNAME%:(OI)(CI)F"
icacls keys\*.pem /inheritance:d
icacls keys\*.pem /grant:r "%USERNAME%:R"
```

### **Issue 3: Certificate Generation Errors**

#### **Symptoms**
- "Failed to create certificate" errors
- Blank or corrupted QR codes
- Invalid JWT tokens

#### **Diagnosis**
```python
# certificate_diagnosis.py
import json
import jwt
from datetime import datetime, timedelta
import qrcode
from PIL import Image

def diagnose_certificate_generation():
    print("=== Certificate Generation Diagnosis ===")
    
    # Test data
    test_certificate = {
        "certificate_id": "TEST_001",
        "holder_name": "Test User",
        "certificate_type": "Test Certificate",
        "issue_date": datetime.now().isoformat(),
        "expiry_date": (datetime.now() + timedelta(days=365)).isoformat(),
        "issuer": "Test Issuer"
    }
    
    # Test JWT creation
    try:
        with open("keys/private_key.pem", "rb") as f:
            private_key = f.read()
        
        token = jwt.encode(test_certificate, private_key, algorithm="RS256")
        print("✅ JWT creation - OK")
        
        # Test JWT verification
        with open("keys/public_key.pem", "rb") as f:
            public_key = f.read()
        
        decoded = jwt.decode(token, public_key, algorithms=["RS256"])
        print("✅ JWT verification - OK")
        
    except Exception as e:
        print(f"❌ JWT processing failed: {e}")
        return
    
    # Test QR code generation
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(token)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        print("✅ QR code generation - OK")
        
        # Test image saving
        test_path = "output/certificates/test_qr.png"
        os.makedirs(os.path.dirname(test_path), exist_ok=True)
        img.save(test_path)
        print("✅ Image saving - OK")
        
        # Cleanup
        os.remove(test_path)
        
    except Exception as e:
        print(f"❌ QR code generation failed: {e}")

if __name__ == "__main__":
    diagnose_certificate_generation()
```

#### **Solutions**

**Solution 1: Fix Output Directory**
```python
# fix_output_directory.py
import os

def fix_output_directory():
    output_dir = "output/certificates"
    
    # Create directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Test write permissions
    test_file = os.path.join(output_dir, "test_write.txt")
    try:
        with open(test_file, "w") as f:
            f.write("test")
        os.remove(test_file)
        print("✅ Output directory is writable")
    except Exception as e:
        print(f"❌ Output directory not writable: {e}")
        print("Solution: Check directory permissions")

if __name__ == "__main__":
    fix_output_directory()
```

**Solution 2: Validate Certificate Data**
```python
# validate_certificate_data.py
from datetime import datetime

def validate_certificate_data(cert_data):
    """Validate certificate data before generation."""
    required_fields = [
        "holder_name", "certificate_type", "issuer"
    ]
    
    errors = []
    
    # Check required fields
    for field in required_fields:
        if field not in cert_data or not cert_data[field]:
            errors.append(f"Missing required field: {field}")
    
    # Validate dates
    try:
        if "issue_date" in cert_data:
            datetime.fromisoformat(cert_data["issue_date"])
        if "expiry_date" in cert_data:
            datetime.fromisoformat(cert_data["expiry_date"])
    except ValueError as e:
        errors.append(f"Invalid date format: {e}")
    
    # Check string lengths
    if len(cert_data.get("holder_name", "")) > 100:
        errors.append("Holder name too long (max 100 characters)")
    
    return errors

# Usage example
test_data = {
    "holder_name": "John Doe",
    "certificate_type": "Course Completion",
    "issuer": "Online University"
}

validation_errors = validate_certificate_data(test_data)
if validation_errors:
    print("❌ Validation errors:")
    for error in validation_errors:
        print(f"  - {error}")
else:
    print("✅ Certificate data is valid")
```

---

## 📱 **React Native Mobile App Issues**

### **Issue 1: App Won't Start or Crashes**

#### **Symptoms**
- App crashes immediately on launch
- White screen or blank display
- "Unable to load script" errors

#### **Diagnosis**
```javascript
// AppDiagnostics.js
import React, { useEffect, useState } from 'react';
import { View, Text, ScrollView, StyleSheet } from 'react-native';
import * as Application from 'expo-application';
import * as Device from 'expo-device';
import Constants from 'expo-constants';

export default function AppDiagnostics() {
  const [diagnostics, setDiagnostics] = useState({});

  useEffect(() => {
    runDiagnostics();
  }, []);

  const runDiagnostics = async () => {
    const results = {
      // App info
      appVersion: Application.nativeApplicationVersion,
      buildVersion: Application.nativeBuildVersion,
      expoVersion: Constants.expoVersion,
      
      // Device info
      deviceName: Device.deviceName,
      osName: Device.osName,
      osVersion: Device.osVersion,
      platform: Device.osName,
      
      // Runtime info
      isDevice: Device.isDevice,
      
      // Permissions check
      cameraPermission: 'checking...',
    };

    // Check camera permission
    try {
      const { Camera } = require('expo-camera');
      const { status } = await Camera.getCameraPermissionsAsync();
      results.cameraPermission = status;
    } catch (error) {
      results.cameraPermission = `Error: ${error.message}`;
    }

    setDiagnostics(results);
  };

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>App Diagnostics</Text>
      {Object.entries(diagnostics).map(([key, value]) => (
        <View key={key} style={styles.row}>
          <Text style={styles.label}>{key}:</Text>
          <Text style={styles.value}>{String(value)}</Text>
        </View>
      ))}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, backgroundColor: '#fff' },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 20 },
  row: { flexDirection: 'row', marginBottom: 10 },
  label: { fontWeight: 'bold', width: 150 },
  value: { flex: 1 },
});
```

#### **Solutions**

**Solution 1: Clear Cache and Restart**
```bash
# Clear Expo cache
npx expo start --clear

# Clear npm cache
npm cache clean --force

# Clear React Native cache
npx react-native start --reset-cache

# Restart Metro bundler
npx expo start --dev-client
```

**Solution 2: Reinstall Dependencies**
```bash
# Remove node_modules and package-lock.json
rm -rf node_modules package-lock.json

# Reinstall dependencies
npm install

# For iOS (macOS only)
cd ios && pod install && cd ..

# Start fresh
npx expo start
```

**Solution 3: Check App Configuration**
```javascript
// app.config.js - Verify configuration
export default {
  expo: {
    name: "Certificate Verifier",
    slug: "certificate-verifier",
    version: "1.0.0",
    orientation: "portrait",
    icon: "./assets/icon.png",
    userInterfaceStyle: "light",
    splash: {
      image: "./assets/splash.png",
      resizeMode: "contain",
      backgroundColor: "#ffffff"
    },
    assetBundlePatterns: ["**/*"],
    ios: {
      supportsTablet: true,
      bundleIdentifier: "com.oblivion.certificateverifier"
    },
    android: {
      adaptiveIcon: {
        foregroundImage: "./assets/adaptive-icon.png",
        backgroundColor: "#FFFFFF"
      },
      package: "com.oblivion.certificateverifier"
    },
    web: {
      favicon: "./assets/favicon.png"
    }
  }
};
```

### **Issue 2: Navigation Problems**

#### **Symptoms**
- Screens don't navigate properly
- Back button not working
- Navigation stack errors

#### **Diagnosis and Solution**
```javascript
// NavigationDiagnostics.js
import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

const Stack = createNativeStackNavigator();

// Add navigation state logging
const onStateChange = (state) => {
  console.log('Navigation state changed:', state);
};

// Add error boundary for navigation
class NavigationErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    console.error('Navigation error:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
          <Text>Navigation Error. Please restart the app.</Text>
        </View>
      );
    }

    return this.props.children;
  }
}

export default function App() {
  return (
    <NavigationErrorBoundary>
      <NavigationContainer onStateChange={onStateChange}>
        <Stack.Navigator initialRouteName="Home">
          <Stack.Screen name="Home" component={HomeScreen} />
          <Stack.Screen name="Scanner" component={ScannerScreen} />
          <Stack.Screen name="Certificate" component={CertificateScreen} />
        </Stack.Navigator>
      </NavigationContainer>
    </NavigationErrorBoundary>
  );
}
```

### **Issue 3: Performance Issues**

#### **Symptoms**
- App runs slowly
- UI freezes or becomes unresponsive
- High memory usage

#### **Performance Monitoring**
```javascript
// PerformanceMonitor.js
import { InteractionManager } from 'react-native';

class PerformanceMonitor {
  static measureRenderTime(componentName, renderFunction) {
    return (...args) => {
      const startTime = Date.now();
      
      const result = renderFunction(...args);
      
      InteractionManager.runAfterInteractions(() => {
        const endTime = Date.now();
        const renderTime = endTime - startTime;
        
        if (renderTime > 16) { // More than one frame (60fps)
          console.warn(`Slow render detected in ${componentName}: ${renderTime}ms`);
        }
      });
      
      return result;
    };
  }
  
  static measureAsyncOperation(operationName, asyncFunction) {
    return async (...args) => {
      const startTime = Date.now();
      
      try {
        const result = await asyncFunction(...args);
        const endTime = Date.now();
        const duration = endTime - startTime;
        
        console.log(`${operationName} completed in ${duration}ms`);
        
        if (duration > 1000) {
          console.warn(`Slow operation detected: ${operationName} took ${duration}ms`);
        }
        
        return result;
      } catch (error) {
        const endTime = Date.now();
        const duration = endTime - startTime;
        console.error(`${operationName} failed after ${duration}ms:`, error);
        throw error;
      }
    };
  }
}

// Usage example
const optimizedVerifyCertificate = PerformanceMonitor.measureAsyncOperation(
  'Certificate Verification',
  verifyCertificate
);
```

#### **Memory Optimization**
```javascript
// MemoryOptimization.js
import { memo, useMemo, useCallback } from 'react';

// Memoize expensive components
export const OptimizedCertificateItem = memo(({ certificate, onPress }) => {
  const formattedDate = useMemo(() => {
    return new Date(certificate.issue_date).toLocaleDateString();
  }, [certificate.issue_date]);
  
  const handlePress = useCallback(() => {
    onPress(certificate);
  }, [certificate, onPress]);
  
  return (
    <TouchableOpacity onPress={handlePress}>
      <Text>{certificate.holder_name}</Text>
      <Text>{formattedDate}</Text>
    </TouchableOpacity>
  );
});

// Optimize large lists
export const OptimizedCertificateList = ({ certificates, onItemPress }) => {
  const renderItem = useCallback(({ item }) => (
    <OptimizedCertificateItem certificate={item} onPress={onItemPress} />
  ), [onItemPress]);
  
  const keyExtractor = useCallback((item) => item.certificate_id, []);
  
  return (
    <FlatList
      data={certificates}
      renderItem={renderItem}
      keyExtractor={keyExtractor}
      removeClippedSubviews={true}
      maxToRenderPerBatch={10}
      updateCellsBatchingPeriod={50}
      initialNumToRender={10}
      windowSize={10}
    />
  );
};
```

---

## 📷 **QR Code and Scanning Issues**

### **Issue 1: QR Code Won't Scan**

#### **Symptoms**
- Camera shows but doesn't detect QR codes
- "No QR code detected" messages
- Scanner freezes or crashes

#### **Diagnosis**
```javascript
// QRScannerDiagnostics.js
import React, { useState, useEffect } from 'react';
import { View, Text, Button, Alert } from 'react-native';
import { BarCodeScanner } from 'expo-barcode-scanner';
import * as ImagePicker from 'expo-image-picker';

export default function QRScannerDiagnostics() {
  const [hasPermission, setHasPermission] = useState(null);
  const [cameraReady, setCameraReady] = useState(false);
  const [scannerActive, setScannerActive] = useState(true);

  useEffect(() => {
    checkPermissions();
  }, []);

  const checkPermissions = async () => {
    try {
      const { status } = await BarCodeScanner.requestPermissionsAsync();
      setHasPermission(status === 'granted');
      
      if (status !== 'granted') {
        Alert.alert(
          'Camera Permission Required',
          'Please enable camera permission in device settings',
          [
            { text: 'Cancel', style: 'cancel' },
            { text: 'Open Settings', onPress: () => Linking.openSettings() }
          ]
        );
      }
    } catch (error) {
      console.error('Permission check failed:', error);
      Alert.alert('Error', 'Failed to check camera permissions');
    }
  };

  const testQRCodeGeneration = () => {
    // Test with a simple QR code
    const testData = JSON.stringify({
      test: true,
      timestamp: Date.now(),
      message: "This is a test QR code"
    });
    
    console.log('Test QR data:', testData);
    Alert.alert('Test QR Code', 'Check console for test data that should be scannable');
  };

  const handleBarCodeScanned = ({ type, data }) => {
    if (!scannerActive) return;
    
    setScannerActive(false);
    
    console.log('Scanned data:', data);
    console.log('Scan type:', type);
    
    Alert.alert(
      'QR Code Scanned',
      `Type: ${type}\nData: ${data.substring(0, 100)}...`,
      [
        { text: 'OK', onPress: () => setScannerActive(true) }
      ]
    );
  };

  const scanFromGallery = async () => {
    try {
      const result = await ImagePicker.launchImageLibraryAsync({
        mediaTypes: ImagePicker.MediaTypeOptions.Images,
        allowsEditing: false,
        quality: 1,
      });

      if (!result.canceled) {
        // Note: Scanning from gallery requires additional implementation
        Alert.alert('Gallery Scan', 'Gallery scanning requires additional setup');
      }
    } catch (error) {
      console.error('Gallery scan error:', error);
      Alert.alert('Error', 'Failed to scan from gallery');
    }
  };

  if (hasPermission === null) {
    return <Text>Requesting camera permission...</Text>;
  }

  if (hasPermission === false) {
    return (
      <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
        <Text>Camera permission denied</Text>
        <Button title="Request Permission" onPress={checkPermissions} />
      </View>
    );
  }

  return (
    <View style={{ flex: 1 }}>
      <BarCodeScanner
        onBarCodeScanned={scannerActive ? handleBarCodeScanned : undefined}
        style={{ flex: 1 }}
        barCodeTypes={[BarCodeScanner.Constants.BarCodeType.qr]}
        onCameraReady={() => setCameraReady(true)}
      />
      
      <View style={{ position: 'absolute', bottom: 50, left: 0, right: 0, alignItems: 'center' }}>
        <Text style={{ color: 'white', marginBottom: 10 }}>
          Camera Ready: {cameraReady ? 'Yes' : 'No'}
        </Text>
        <Button title="Test QR Generation" onPress={testQRCodeGeneration} />
        <Button title="Scan from Gallery" onPress={scanFromGallery} />
      </View>
    </View>
  );
}
```

#### **Solutions**

**Solution 1: Camera Permission Issues**
```javascript
// PermissionManager.js
import { Alert, Linking } from 'react-native';
import { BarCodeScanner } from 'expo-barcode-scanner';

export class PermissionManager {
  static async requestCameraPermission() {
    try {
      const { status } = await BarCodeScanner.requestPermissionsAsync();
      
      if (status === 'granted') {
        return true;
      } else if (status === 'denied') {
        Alert.alert(
          'Camera Permission Required',
          'This app needs camera access to scan QR codes. Please enable it in settings.',
          [
            { text: 'Cancel', style: 'cancel' },
            { text: 'Open Settings', onPress: () => Linking.openSettings() }
          ]
        );
        return false;
      }
    } catch (error) {
      console.error('Permission request failed:', error);
      return false;
    }
  }
  
  static async checkCameraPermission() {
    try {
      const { status } = await BarCodeScanner.getCameraPermissionsAsync();
      return status === 'granted';
    } catch (error) {
      console.error('Permission check failed:', error);
      return false;
    }
  }
}
```

**Solution 2: Improve QR Code Detection**
```javascript
// ImprovedQRScanner.js
import React, { useState, useEffect, useRef } from 'react';
import { View, Text, StyleSheet, Dimensions } from 'react-native';
import { BarCodeScanner } from 'expo-barcode-scanner';

const { width, height } = Dimensions.get('window');

export default function ImprovedQRScanner({ onScan }) {
  const [hasPermission, setHasPermission] = useState(null);
  const [scanned, setScanned] = useState(false);
  const scanTimeoutRef = useRef(null);

  useEffect(() => {
    const getBarCodeScannerPermissions = async () => {
      const { status } = await BarCodeScanner.requestPermissionsAsync();
      setHasPermission(status === 'granted');
    };

    getBarCodeScannerPermissions();
  }, []);

  const handleBarCodeScanned = ({ type, data }) => {
    if (scanned) return;
    
    setScanned(true);
    
    // Clear any existing timeout
    if (scanTimeoutRef.current) {
      clearTimeout(scanTimeoutRef.current);
    }
    
    // Validate QR code data
    if (isValidQRCode(data)) {
      onScan(data);
    } else {
      console.warn('Invalid QR code format:', data);
      // Reset scanner after a delay for invalid codes
      scanTimeoutRef.current = setTimeout(() => {
        setScanned(false);
      }, 2000);
    }
  };

  const isValidQRCode = (data) => {
    try {
      // Check if it's a JWT token (basic validation)
      const parts = data.split('.');
      if (parts.length === 3) {
        // Looks like a JWT
        return true;
      }
      
      // Check if it's valid JSON
      JSON.parse(data);
      return true;
    } catch (error) {
      return false;
    }
  };

  const resetScanner = () => {
    setScanned(false);
    if (scanTimeoutRef.current) {
      clearTimeout(scanTimeoutRef.current);
    }
  };

  if (hasPermission === null) {
    return <Text>Requesting camera permission</Text>;
  }
  if (hasPermission === false) {
    return <Text>No access to camera</Text>;
  }

  return (
    <View style={styles.container}>
      <BarCodeScanner
        onBarCodeScanned={scanned ? undefined : handleBarCodeScanned}
        style={StyleSheet.absoluteFillObject}
        barCodeTypes={[BarCodeScanner.Constants.BarCodeType.qr]}
      />
      
      {/* Scanning overlay */}
      <View style={styles.overlay}>
        <View style={styles.scanArea}>
          <View style={[styles.corner, styles.topLeft]} />
          <View style={[styles.corner, styles.topRight]} />
          <View style={[styles.corner, styles.bottomLeft]} />
          <View style={[styles.corner, styles.bottomRight]} />
        </View>
        
        <Text style={styles.instruction}>
          {scanned ? 'Processing...' : 'Point camera at QR code'}
        </Text>
      </View>
      
      {scanned && (
        <TouchableOpacity style={styles.resetButton} onPress={resetScanner}>
          <Text style={styles.resetButtonText}>Scan Again</Text>
        </TouchableOpacity>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  overlay: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    justifyContent: 'center',
    alignItems: 'center',
  },
  scanArea: {
    width: 250,
    height: 250,
    position: 'relative',
  },
  corner: {
    position: 'absolute',
    width: 30,
    height: 30,
    borderColor: '#fff',
  },
  topLeft: {
    top: 0,
    left: 0,
    borderTopWidth: 3,
    borderLeftWidth: 3,
  },
  topRight: {
    top: 0,
    right: 0,
    borderTopWidth: 3,
    borderRightWidth: 3,
  },
  bottomLeft: {
    bottom: 0,
    left: 0,
    borderBottomWidth: 3,
    borderLeftWidth: 3,
  },
  bottomRight: {
    bottom: 0,
    right: 0,
    borderBottomWidth: 3,
    borderRightWidth: 3,
  },
  instruction: {
    color: '#fff',
    fontSize: 16,
    marginTop: 20,
    textAlign: 'center',
  },
  resetButton: {
    position: 'absolute',
    bottom: 50,
    alignSelf: 'center',
    backgroundColor: '#007AFF',
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderRadius: 5,
  },
  resetButtonText: {
    color: '#fff',
    fontSize: 16,
  },
});
```

### **Issue 2: QR Code Generation Problems**

#### **Symptoms**
- QR codes appear blank or corrupted
- QR codes are too small or too large
- Generated QR codes can't be scanned

#### **Solutions**

**Solution 1: Optimize QR Code Generation**
```python
# optimized_qr_generator.py
import qrcode
from PIL import Image, ImageDraw, ImageFont
import io
import base64

class OptimizedQRGenerator:
    def __init__(self):
        self.default_settings = {
            'version': 1,
            'error_correction': qrcode.constants.ERROR_CORRECT_M,
            'box_size': 10,
            'border': 4,
        }
    
    def generate_qr_code(self, data, settings=None):
        """Generate optimized QR code with validation."""
        if settings is None:
            settings = self.default_settings
        
        try:
            # Validate data size
            if len(data) > 2000:  # Approximate limit for QR codes
                raise ValueError("Data too large for QR code")
            
            # Create QR code instance
            qr = qrcode.QRCode(**settings)
            qr.add_data(data)
            qr.make(fit=True)
            
            # Generate image
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Ensure minimum size
            if img.size[0] < 200:
                img = img.resize((200, 200), Image.NEAREST)
            
            return {
                'success': True,
                'image': img,
                'size': img.size,
                'data_length': len(data)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'data_length': len(data)
            }
    
    def add_logo_to_qr(self, qr_image, logo_path, logo_size_ratio=0.3):
        """Add logo to center of QR code."""
        try:
            # Open logo image
            logo = Image.open(logo_path)
            
            # Calculate logo size
            qr_width, qr_height = qr_image.size
            logo_size = int(min(qr_width, qr_height) * logo_size_ratio)
            
            # Resize logo
            logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
            
            # Create a white background for the logo
            logo_bg = Image.new('RGB', (logo_size + 20, logo_size + 20), 'white')
            logo_bg.paste(logo, (10, 10))
            
            # Calculate position to center the logo
            pos = ((qr_width - logo_bg.size[0]) // 2, (qr_height - logo_bg.size[1]) // 2)
            
            # Paste logo onto QR code
            qr_image.paste(logo_bg, pos)
            
            return qr_image
            
        except Exception as e:
            print(f"Failed to add logo: {e}")
            return qr_image
    
    def validate_qr_code(self, qr_image):
        """Validate generated QR code by attempting to decode it."""
        try:
            from pyzbar import pyzbar
            
            # Convert PIL image to format suitable for pyzbar
            decoded_objects = pyzbar.decode(qr_image)
            
            if decoded_objects:
                return {
                    'valid': True,
                    'decoded_data': decoded_objects[0].data.decode('utf-8')
                }
            else:
                return {
                    'valid': False,
                    'error': 'QR code could not be decoded'
                }
                
        except ImportError:
            print("pyzbar not installed, skipping validation")
            return {'valid': True, 'note': 'Validation skipped'}
        except Exception as e:
            return {
                'valid': False,
                'error': str(e)
            }

# Usage example
if __name__ == "__main__":
    generator = OptimizedQRGenerator()
    
    test_data = "This is test data for QR code generation"
    result = generator.generate_qr_code(test_data)
    
    if result['success']:
        print(f"✅ QR code generated successfully")
        print(f"   Size: {result['size']}")
        print(f"   Data length: {result['data_length']}")
        
        # Validate the generated QR code
        validation = generator.validate_qr_code(result['image'])
        if validation['valid']:
            print("✅ QR code validation passed")
        else:
            print(f"❌ QR code validation failed: {validation['error']}")
    else:
        print(f"❌ QR code generation failed: {result['error']}")
```

---

## 🔐 **JWT and Cryptographic Issues**

### **Issue 1: JWT Verification Failures**

#### **Symptoms**
- "Invalid signature" errors
- "Token expired" messages
- "Malformed JWT" errors

#### **Diagnosis**
```javascript
// JWTDiagnostics.js
import jwt from 'jsonwebtoken';

export class JWTDiagnostics {
  static diagnoseJWT(token, publicKey) {
    console.log('=== JWT Diagnostics ===');
    
    try {
      // Check JWT format
      const parts = token.split('.');
      if (parts.length !== 3) {
        return {
          valid: false,
          error: 'Invalid JWT format - should have 3 parts separated by dots',
          parts: parts.length
        };
      }
      
      // Decode header without verification
      const header = JSON.parse(atob(parts[0]));
      console.log('JWT Header:', header);
      
      // Decode payload without verification
      const payload = JSON.parse(atob(parts[1]));
      console.log('JWT Payload:', payload);
      
      // Check algorithm
      if (header.alg !== 'RS256') {
        console.warn(`Unexpected algorithm: ${header.alg}, expected RS256`);
      }
      
      // Check expiration
      if (payload.exp) {
        const expirationDate = new Date(payload.exp * 1000);
        const now = new Date();
        
        if (expirationDate < now) {
          return {
            valid: false,
            error: 'Token expired',
            expiredAt: expirationDate.toISOString(),
            currentTime: now.toISOString()
          };
        }
      }
      
      // Verify signature
      try {
        const decoded = jwt.verify(token, publicKey, { algorithms: ['RS256'] });
        return {
          valid: true,
          decoded: decoded,
          header: header,
          payload: payload
        };
      } catch (verifyError) {
        return {
          valid: false,
          error: `Signature verification failed: ${verifyError.message}`,
          header: header,
          payload: payload
        };
      }
      
    } catch (error) {
      return {
        valid: false,
        error: `JWT parsing failed: ${error.message}`
      };
    }
  }
  
  static validateCertificatePayload(payload) {
    const requiredFields = [
      'certificate_id',
      'holder_name',
      'certificate_type',
      'issue_date',
      'issuer'
    ];
    
    const missingFields = requiredFields.filter(field => !payload[field]);
    
    if (missingFields.length > 0) {
      return {
        valid: false,
        error: `Missing required fields: ${missingFields.join(', ')}`
      };
    }
    
    // Validate date formats
    try {
      new Date(payload.issue_date);
      if (payload.expiry_date) {
        new Date(payload.expiry_date);
      }
    } catch (error) {
      return {
        valid: false,
        error: 'Invalid date format in certificate'
      };
    }
    
    return { valid: true };
  }
}

// Usage example
const testToken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9..."; // Your JWT token
const publicKey = `-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA...
-----END PUBLIC KEY-----`;

const diagnostics = JWTDiagnostics.diagnoseJWT(testToken, publicKey);
console.log('Diagnostics result:', diagnostics);
```

#### **Solutions**

**Solution 1: Fix Key Format Issues**
```javascript
// KeyFormatFixer.js
export class KeyFormatFixer {
  static formatPublicKey(keyString) {
    // Remove any existing headers/footers
    let cleanKey = keyString
      .replace(/-----BEGIN PUBLIC KEY-----/g, '')
      .replace(/-----END PUBLIC KEY-----/g, '')
      .replace(/\s/g, '');
    
    // Add proper headers and line breaks
    const formattedKey = `-----BEGIN PUBLIC KEY-----\n${cleanKey.match(/.{1,64}/g).join('\n')}\n-----END PUBLIC KEY-----`;
    
    return formattedKey;
  }
  
  static validateKeyFormat(keyString) {
    try {
      // Try to create a crypto key object
      const crypto = require('crypto');
      crypto.createPublicKey(keyString);
      return { valid: true };
    } catch (error) {
      return { 
        valid: false, 
        error: error.message,
        suggestion: 'Check key format and ensure proper PEM encoding'
      };
    }
  }
}
```

**Solution 2: Handle Clock Skew**
```javascript
// ClockSkewHandler.js
import jwt from 'jsonwebtoken';

export class ClockSkewHandler {
  static verifyWithClockTolerance(token, publicKey, toleranceSeconds = 300) {
    const options = {
      algorithms: ['RS256'],
      clockTolerance: toleranceSeconds, // 5 minutes tolerance
      ignoreExpiration: false,
      ignoreNotBefore: false
    };
    
    try {
      const decoded = jwt.verify(token, publicKey, options);
      return { valid: true, decoded };
    } catch (error) {
      if (error.name === 'TokenExpiredError') {
        // Check if it's within tolerance
        const payload = jwt.decode(token);
        const now = Math.floor(Date.now() / 1000);
        const expiredBy = now - payload.exp;
        
        if (expiredBy <= toleranceSeconds) {
          console.warn(`Token expired by ${expiredBy} seconds, within tolerance`);
          return { 
            valid: true, 
            decoded: payload,
            warning: `Token expired by ${expiredBy} seconds`
          };
        }
      }
      
      return { 
        valid: false, 
        error: error.message,
        name: error.name
      };
    }
  }
}
```

### **Issue 2: Key Management Problems**

#### **Symptoms**
- "Key not found" errors
- "Invalid key format" messages
- Key rotation failures

#### **Solutions**

**Solution 1: Key Validation and Recovery**
```python
# key_recovery.py
import os
import shutil
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from datetime import datetime

class KeyRecoveryManager:
    def __init__(self, key_dir="keys", backup_dir="keys/backup"):
        self.key_dir = key_dir
        self.backup_dir = backup_dir
        os.makedirs(backup_dir, exist_ok=True)
    
    def diagnose_keys(self):
        """Diagnose key-related issues."""
        issues = []
        
        private_key_path = os.path.join(self.key_dir, "private_key.pem")
        public_key_path = os.path.join(self.key_dir, "public_key.pem")
        
        # Check if keys exist
        if not os.path.exists(private_key_path):
            issues.append("Private key file missing")
        
        if not os.path.exists(public_key_path):
            issues.append("Public key file missing")
        
        # Validate key formats
        for key_path, key_type in [(private_key_path, "private"), (public_key_path, "public")]:
            if os.path.exists(key_path):
                try:
                    with open(key_path, 'rb') as f:
                        key_data = f.read()
                    
                    if key_type == "private":
                        serialization.load_pem_private_key(key_data, password=None)
                    else:
                        serialization.load_pem_public_key(key_data)
                        
                except Exception as e:
                    issues.append(f"{key_type.title()} key corrupted: {str(e)}")
        
        # Check key pair consistency
        if not issues:  # Only if both keys are valid
            try:
                self._validate_key_pair(private_key_path, public_key_path)
            except Exception as e:
                issues.append(f"Key pair mismatch: {str(e)}")
        
        return issues
    
    def _validate_key_pair(self, private_key_path, public_key_path):
        """Validate that private and public keys are a matching pair."""
        with open(private_key_path, 'rb') as f:
            private_key = serialization.load_pem_private_key(f.read(), password=None)
        
        with open(public_key_path, 'rb') as f:
            public_key = serialization.load_pem_public_key(f.read())
        
        # Compare public key from private key with stored public key
        derived_public_key = private_key.public_key()
        
        # Serialize both keys for comparison
        stored_public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        derived_public_pem = derived_public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        if stored_public_pem != derived_public_pem:
            raise ValueError("Private and public keys do not match")
    
    def backup_keys(self):
        """Backup existing keys before recovery."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for key_file in ["private_key.pem", "public_key.pem"]:
            src_path = os.path.join(self.key_dir, key_file)
            if os.path.exists(src_path):
                backup_path = os.path.join(self.backup_dir, f"{key_file}_{timestamp}")
                shutil.copy2(src_path, backup_path)
                print(f"Backed up {key_file} to {backup_path}")
    
    def recover_keys(self):
        """Attempt to recover or regenerate keys."""
        issues = self.diagnose_keys()
        
        if not issues:
            print("✅ Keys are healthy, no recovery needed")
            return True
        
        print(f"❌ Found {len(issues)} key issues:")
        for issue in issues:
            print(f"  - {issue}")
        
        # Backup existing keys
        self.backup_keys()
        
        # Regenerate keys
        print("Regenerating key pair...")
        try:
            from generate_keys import generate_rsa_keypair
            result = generate_rsa_keypair()
            
            if result["success"]:
                print("✅ Keys regenerated successfully")
                return True
            else:
                print(f"❌ Key regeneration failed: {result['error']}")
                return False
                
        except Exception as e:
            print(f"❌ Key recovery failed: {str(e)}")
            return False

# Usage
if __name__ == "__main__":
    recovery_manager = KeyRecoveryManager()
    recovery_manager.recover_keys()
```

---

## 🚀 **Build and Deployment Issues**

### **Issue 1: EAS Build Failures**

#### **Symptoms**
- Build fails with credential errors
- "No suitable credentials found" messages
- Build timeouts or hangs

#### **Diagnosis and Solutions**

**Solution 1: Credential Configuration**
```bash
# Check current credentials
eas credentials

# List all credentials
eas credentials:list

# Configure iOS credentials
eas credentials:configure -p ios

# Configure Android credentials  
eas credentials:configure -p android

# Delete and reconfigure if corrupted
eas credentials:delete -p ios
eas credentials:delete -p android
eas build:configure
```

**Solution 2: EAS Configuration Issues**
```json
// Fixed eas.json configuration
{
  "cli": {
    "version": ">= 5.9.0"
  },
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal",
      "env": {
        "NODE_OPTIONS": "--max-old-space-size=4096"
      }
    },
    "preview": {
      "distribution": "internal",
      "ios": {
        "simulator": true
      },
      "android": {
        "buildType": "apk"
      },
      "env": {
        "NODE_OPTIONS": "--max-old-space-size=4096"
      }
    },
    "production": {
      "env": {
        "NODE_OPTIONS": "--max-old-space-size=4096"
      }
    }
  },
  "submit": {
    "production": {}
  }
}
```

### **Issue 2: Metro Bundle Errors**

#### **Symptoms**
- "Unable to resolve module" errors
- Bundle build failures
- Transformation errors

#### **Solutions**

**Solution 1: Clear All Caches**
```bash
# Clear Expo cache
npx expo start --clear

# Clear npm cache
npm cache clean --force

# Clear React Native cache
npx react-native start --reset-cache

# Clear Metro cache
rm -rf node_modules/.cache

# Clear Watchman cache (macOS/Linux)
watchman watch-del-all

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

**Solution 2: Fix Metro Configuration**
```javascript
// metro.config.js - Fixed configuration
const { getDefaultConfig } = require('expo/metro-config');

const config = getDefaultConfig(__dirname);

// Add resolver configuration
config.resolver = {
  ...config.resolver,
  alias: {
    // Add any necessary aliases
  },
  extensions: [
    '.ios.js',
    '.android.js',
    '.native.js',
    '.js',
    '.jsx',
    '.json',
    '.ts',
    '.tsx',
  ],
};

// Add transformer configuration
config.transformer = {
  ...config.transformer,
  babelTransformerPath: require.resolve('react-native-svg-transformer'),
};

// Add serializer configuration
config.serializer = {
  ...config.serializer,
  customSerializer: require('@expo/metro-serializer-esbuild'),
};

module.exports = config;
```

### **Issue 3: Android Build Issues**

#### **Symptoms**
- Gradle build failures
- "SDK not found" errors
- Signing key issues

#### **Solutions**

**Solution 1: Android SDK Issues**
```bash
# Check Android SDK installation
echo $ANDROID_HOME
echo $ANDROID_SDK_ROOT

# Install required SDK components
sdkmanager "platform-tools" "platforms;android-33" "build-tools;33.0.0"

# Accept licenses
sdkmanager --licenses
```

**Solution 2: Gradle Issues**
```bash
# Clean Gradle cache
cd android
./gradlew clean

# Clear Gradle cache globally
rm -rf ~/.gradle/caches/

# Rebuild
./gradlew assembleRelease
```

---

## ⚡ **Performance Issues**

### **Issue 1: Slow App Performance**

#### **Symptoms**
- App takes long time to start
- UI freezes or becomes unresponsive
- High memory usage

#### **Performance Monitoring**
```javascript
// PerformanceProfiler.js
import { InteractionManager, Alert } from 'react-native';

export class PerformanceProfiler {
  static measurements = new Map();
  
  static startMeasurement(name) {
    this.measurements.set(name, {
      startTime: Date.now(),
      startMemory: this.getMemoryUsage()
    });
  }
  
  static endMeasurement(name) {
    const measurement = this.measurements.get(name);
    if (!measurement) {
      console.warn(`No measurement started for: ${name}`);
      return;
    }
    
    const endTime = Date.now();
    const endMemory = this.getMemoryUsage();
    
    const result = {
      name,
      duration: endTime - measurement.startTime,
      memoryDelta: endMemory - measurement.startMemory,
      timestamp: new Date().toISOString()
    };
    
    console.log(`Performance: ${name}`, result);
    
    // Alert for slow operations
    if (result.duration > 1000) {
      console.warn(`Slow operation detected: ${name} took ${result.duration}ms`);
    }
    
    this.measurements.delete(name);
    return result;
  }
  
  static getMemoryUsage() {
    // This is a simplified version - actual memory monitoring
    // would require native modules or performance APIs
    return performance.memory ? performance.memory.usedJSHeapSize : 0;
  }
  
  static profileAsyncOperation(name, asyncFunction) {
    return async (...args) => {
      this.startMeasurement(name);
      
      try {
        const result = await asyncFunction(...args);
        this.endMeasurement(name);
        return result;
      } catch (error) {
        this.endMeasurement(name);
        throw error;
      }
    };
  }
  
  static profileComponent(WrappedComponent, componentName) {
    return class extends React.Component {
      componentDidMount() {
        PerformanceProfiler.endMeasurement(`${componentName}_mount`);
      }
      
      componentWillUnmount() {
        PerformanceProfiler.startMeasurement(`${componentName}_unmount`);
      }
      
      render() {
        PerformanceProfiler.startMeasurement(`${componentName}_mount`);
        return <WrappedComponent {...this.props} />;
      }
    };
  }
}

// Usage examples
const profiledVerifyCertificate = PerformanceProfiler.profileAsyncOperation(
  'Certificate Verification',
  verifyCertificate
);

const ProfiledScannerScreen = PerformanceProfiler.profileComponent(
  ScannerScreen,
  'ScannerScreen'
);
```

#### **Memory Optimization**
```javascript
// MemoryOptimizer.js
import { memo, useMemo, useCallback, useRef, useEffect } from 'react';

export const MemoryOptimizer = {
  // Memoize expensive calculations
  memoizeExpensiveCalculation: (calculation, dependencies) => {
    return useMemo(calculation, dependencies);
  },
  
  // Optimize event handlers
  optimizeEventHandler: (handler, dependencies) => {
    return useCallback(handler, dependencies);
  },
  
  // Clean up resources
  useCleanup: (cleanupFunction) => {
    useEffect(() => {
      return cleanupFunction;
    }, []);
  },
  
  // Debounce expensive operations
  useDebounce: (value, delay) => {
    const [debouncedValue, setDebouncedValue] = useState(value);
    
    useEffect(() => {
      const handler = setTimeout(() => {
        setDebouncedValue(value);
      }, delay);
      
      return () => {
        clearTimeout(handler);
      };
    }, [value, delay]);
    
    return debouncedValue;
  },
  
  // Optimize large lists
  optimizeList: (data, renderItem, keyExtractor) => {
    const optimizedRenderItem = useCallback(renderItem, []);
    const optimizedKeyExtractor = useCallback(keyExtractor, []);
    
    return {
      data,
      renderItem: optimizedRenderItem,
      keyExtractor: optimizedKeyExtractor,
      removeClippedSubviews: true,
      maxToRenderPerBatch: 10,
      updateCellsBatchingPeriod: 50,
      initialNumToRender: 10,
      windowSize: 10,
    };
  }
};

// Example usage
const OptimizedCertificateList = memo(({ certificates, onItemPress }) => {
  const listProps = MemoryOptimizer.optimizeList(
    certificates,
    ({ item }) => <CertificateItem certificate={item} onPress={onItemPress} />,
    (item) => item.certificate_id
  );
  
  return <FlatList {...listProps} />;
});
```

---

## 🔒 **Security and Permission Issues**

### **Issue 1: Camera Permission Denied**

#### **Symptoms**
- "Camera permission denied" messages
- Black screen when trying to scan
- App crashes when accessing camera

#### **Solutions**

**Solution 1: Comprehensive Permission Management**
```javascript
// PermissionManager.js
import { Alert, Linking, Platform } from 'react-native';
import { Camera } from 'expo-camera';
import * as MediaLibrary from 'expo-media-library';

export class PermissionManager {
  static async requestAllPermissions() {
    const results = {};
    
    // Camera permission
    try {
      const cameraResult = await Camera.requestCameraPermissionsAsync();
      results.camera = cameraResult.status === 'granted';
      
      if (!results.camera) {
        this.showPermissionAlert('Camera', 'scan QR codes');
      }
    } catch (error) {
      console.error('Camera permission error:', error);
      results.camera = false;
    }
    
    // Media library permission (for saving certificates)
    try {
      const mediaResult = await MediaLibrary.requestPermissionsAsync();
      results.mediaLibrary = mediaResult.status === 'granted';
    } catch (error) {
      console.error('Media library permission error:', error);
      results.mediaLibrary = false;
    }
    
    return results;
  }
  
  static showPermissionAlert(permissionType, purpose) {
    Alert.alert(
      `${permissionType} Permission Required`,
      `This app needs ${permissionType.toLowerCase()} access to ${purpose}. Please enable it in your device settings.`,
      [
        { text: 'Cancel', style: 'cancel' },
        { text: 'Open Settings', onPress: () => Linking.openSettings() }
      ]
    );
  }
  
  static async checkPermissionStatus() {
    const cameraStatus = await Camera.getCameraPermissionsAsync();
    const mediaStatus = await MediaLibrary.getPermissionsAsync();
    
    return {
      camera: cameraStatus.status === 'granted',
      mediaLibrary: mediaStatus.status === 'granted',
      cameraCanAskAgain: cameraStatus.canAskAgain,
      mediaCanAskAgain: mediaStatus.canAskAgain
    };
  }
}
```

**Solution 2: Platform-Specific Permission Handling**
```javascript
// PlatformPermissions.js
import { Platform } from 'react-native';

export const PlatformPermissions = {
  async handleCameraPermission() {
    if (Platform.OS === 'ios') {
      return this.handleiOSCameraPermission();
    } else if (Platform.OS === 'android') {
      return this.handleAndroidCameraPermission();
    }
  },
  
  async handleiOSCameraPermission() {
    const { Camera } = require('expo-camera');
    const { status } = await Camera.requestCameraPermissionsAsync();
    
    if (status === 'denied') {
      Alert.alert(
        'Camera Access Required',
        'Please enable camera access in Settings > Privacy & Security > Camera > Certificate Verifier',
        [
          { text: 'Cancel', style: 'cancel' },
          { text: 'Open Settings', onPress: () => Linking.openURL('app-settings:') }
        ]
      );
      return false;
    }
    
    return status === 'granted';
  },
  
  async handleAndroidCameraPermission() {
    const { Camera } = require('expo-camera');
    const { status } = await Camera.requestCameraPermissionsAsync();
    
    if (status === 'denied') {
      Alert.alert(
        'Camera Permission Required',
        'Please enable camera permission in Settings > Apps > Certificate Verifier > Permissions',
        [
          { text: 'Cancel', style: 'cancel' },
          { text: 'Open Settings', onPress: () => Linking.openSettings() }
        ]
      );
      return false;
    }
    
    return status === 'granted';
  }
};
```

### **Issue 2: Certificate Storage Security**

#### **Symptoms**
- Certificates stored in plain text
- Unauthorized access to stored certificates
- Data leakage concerns

#### **Solutions**

**Solution 1: Secure Storage Implementation**
```javascript
// SecureStorage.js
import * as SecureStore from 'expo-secure-store';
import CryptoJS from 'crypto-js';

export class SecureStorage {
  static ENCRYPTION_KEY = 'certificate_verifier_key_2025';
  
  static async storeCertificate(certificateId, certificateData) {
    try {
      // Encrypt certificate data
      const encryptedData = CryptoJS.AES.encrypt(
        JSON.stringify(certificateData),
        this.ENCRYPTION_KEY
      ).toString();
      
      // Store in secure storage
      await SecureStore.setItemAsync(
        `cert_${certificateId}`,
        encryptedData
      );
      
      return { success: true };
    } catch (error) {
      console.error('Failed to store certificate:', error);
      return { success: false, error: error.message };
    }
  }
  
  static async retrieveCertificate(certificateId) {
    try {
      // Retrieve from secure storage
      const encryptedData = await SecureStore.getItemAsync(`cert_${certificateId}`);
      
      if (!encryptedData) {
        return { success: false, error: 'Certificate not found' };
      }
      
      // Decrypt certificate data
      const decryptedBytes = CryptoJS.AES.decrypt(encryptedData, this.ENCRYPTION_KEY);
      const decryptedData = JSON.parse(decryptedBytes.toString(CryptoJS.enc.Utf8));
      
      return { success: true, data: decryptedData };
    } catch (error) {
      console.error('Failed to retrieve certificate:', error);
      return { success: false, error: error.message };
    }
  }
  
  static async deleteCertificate(certificateId) {
    try {
      await SecureStore.deleteItemAsync(`cert_${certificateId}`);
      return { success: true };
    } catch (error) {
      console.error('Failed to delete certificate:', error);
      return { success: false, error: error.message };
    }
  }
  
  static async listStoredCertificates() {
    try {
      // Note: SecureStore doesn't provide a list function
      // This would need to be implemented with a separate index
      const indexData = await SecureStore.getItemAsync('certificate_index');
      
      if (!indexData) {
        return { success: true, certificates: [] };
      }
      
      const certificateIds = JSON.parse(indexData);
      return { success: true, certificates: certificateIds };
    } catch (error) {
      console.error('Failed to list certificates:', error);
      return { success: false, error: error.message };
    }
  }
}
```

---

## 🌐 **Network and Connectivity Issues**

### **Issue 1: Offline Functionality**

#### **Symptoms**
- App doesn't work without internet
- Certificate verification fails offline
- Sync issues when connection restored

#### **Solutions**

**Solution 1: Offline-First Architecture**
```javascript
// OfflineManager.js
import NetInfo from '@react-native-async-storage/async-storage';
import AsyncStorage from '@react-native-async-storage/async-storage';

export class OfflineManager {
  static isOnline = true;
  static listeners = [];
  
  static async initialize() {
    // Monitor network status
    const unsubscribe = NetInfo.addEventListener(state => {
      const wasOnline = this.isOnline;
      this.isOnline = state.isConnected;
      
      if (wasOnline !== this.isOnline) {
        this.notifyListeners(this.isOnline);
        
        if (this.isOnline) {
          this.handleConnectionRestored();
        } else {
          this.handleConnectionLost();
        }
      }
    });
    
    // Check initial connection status
    const state = await NetInfo.fetch();
    this.isOnline = state.isConnected;
    
    return unsubscribe;
  }
  
  static addListener(callback) {
    this.listeners.push(callback);
    return () => {
      this.listeners = this.listeners.filter(listener => listener !== callback);
    };
  }
  
  static notifyListeners(isOnline) {
    this.listeners.forEach(listener => listener(isOnline));
  }
  
  static async handleConnectionLost() {
    console.log('Connection lost - switching to offline mode');
    await AsyncStorage.setItem('offline_mode', 'true');
  }
  
  static async handleConnectionRestored() {
    console.log('Connection restored - syncing data');
    await AsyncStorage.setItem('offline_mode', 'false');
    await this.syncPendingData();
  }
  
  static async syncPendingData() {
    try {
      const pendingData = await AsyncStorage.getItem('pending_sync');
      if (pendingData) {
        const data = JSON.parse(pendingData);
        // Process pending sync data
        console.log('Syncing pending data:', data);
        
        // Clear pending data after successful sync
        await AsyncStorage.removeItem('pending_sync');
      }
    } catch (error) {
      console.error('Sync failed:', error);
    }
  }
  
  static async isOfflineMode() {
    const offlineMode = await AsyncStorage.getItem('offline_mode');
    return offlineMode === 'true' || !this.isOnline;
  }
}
```

**Solution 2: Offline Certificate Verification**
```javascript
// OfflineCertificateVerifier.js
import { JWTVerifier } from './jwtVerifier';
import { SecureStorage } from './SecureStorage';

export class OfflineCertificateVerifier {
  static async verifyCertificateOffline(qrData) {
    try {
      // Verify JWT signature using stored public key
      const verificationResult = await JWTVerifier.verifyJWT(qrData);
      
      if (!verificationResult.valid) {
        return {
          success: false,
          error: 'Invalid certificate signature',
          offline: true
        };
      }
      
      // Check certificate against local blacklist
      const isBlacklisted = await this.checkLocalBlacklist(
        verificationResult.payload.certificate_id
      );
      
      if (isBlacklisted) {
        return {
          success: false,
          error: 'Certificate has been revoked',
          offline: true
        };
      }
      
      // Store verification log for later sync
      await this.logVerificationOffline(verificationResult.payload);
      
      return {
        success: true,
        certificate: verificationResult.payload,
        offline: true,
        warning: 'Verified offline - some checks may be limited'
      };
      
    } catch (error) {
      console.error('Offline verification failed:', error);
      return {
        success: false,
        error: 'Offline verification failed',
        offline: true
      };
    }
  }
  
  static async checkLocalBlacklist(certificateId) {
    try {
      const blacklist = await SecureStorage.retrieveCertificate('blacklist');
      if (blacklist.success && blacklist.data) {
        return blacklist.data.includes(certificateId);
      }
      return false;
    } catch (error) {
      console.error('Blacklist check failed:', error);
      return false;
    }
  }
  
  static async logVerificationOffline(certificate) {
    try {
      const logEntry = {
        certificateId: certificate.certificate_id,
        holderName: certificate.holder_name,
        verificationTime: new Date().toISOString(),
        offline: true
      };
      
      // Store in pending sync queue
      const pendingLogs = await AsyncStorage.getItem('pending_verification_logs');
      const logs = pendingLogs ? JSON.parse(pendingLogs) : [];
      logs.push(logEntry);
      
      await AsyncStorage.setItem('pending_verification_logs', JSON.stringify(logs));
    } catch (error) {
      console.error('Failed to log offline verification:', error);
    }
  }
}
```

---

## 📱 **Platform-Specific Issues**

### **Issue 1: iOS-Specific Problems**

#### **Symptoms**
- App crashes on iOS devices
- Camera not working on iOS
- Build issues with iOS

#### **Solutions**

**Solution 1: iOS Configuration**
```xml
<!-- ios/CertificateVerifier/Info.plist -->
<key>NSCameraUsageDescription</key>
<string>This app needs camera access to scan QR codes for certificate verification</string>

<key>NSPhotoLibraryUsageDescription</key>
<string>This app needs photo library access to save certificate images</string>

<key>CFBundleURLTypes</key>
<array>
  <dict>
    <key>CFBundleURLName</key>
    <string>com.oblivion.certificateverifier</string>
    <key>CFBundleURLSchemes</key>
    <array>
      <string>certificateverifier</string>
    </array>
  </dict>
</array>
```

**Solution 2: iOS Build Configuration**
```javascript
// app.config.js - iOS specific settings
export default {
  expo: {
    ios: {
      supportsTablet: true,
      bundleIdentifier: "com.oblivion.certificateverifier",
      buildNumber: "1.0.0",
      infoPlist: {
        NSCameraUsageDescription: "This app needs camera access to scan QR codes",
        NSPhotoLibraryUsageDescription: "This app needs photo library access to save certificates"
      }
    }
  }
};
```

### **Issue 2: Android-Specific Problems**

#### **Symptoms**
- Permission issues on Android
- APK installation problems
- Performance issues on older Android devices

#### **Solutions**

**Solution 1: Android Permissions**
```xml
<!-- android/app/src/main/AndroidManifest.xml -->
<uses-permission android:name="android.permission.CAMERA" />
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
<uses-permission android:name="android.permission.INTERNET" />

<application
  android:name=".MainApplication"
  android:label="@string/app_name"
  android:icon="@mipmap/ic_launcher"
  android:allowBackup="false"
  android:theme="@style/AppTheme"
  android:usesCleartextTraffic="true">
  
  <activity
    android:name=".MainActivity"
    android:exported="true"
    android:launchMode="singleTask"
    android:theme="@style/LaunchTheme"
    android:configChanges="keyboard|keyboardHidden|orientation|screenSize|uiMode"
    android:screenOrientation="portrait"
    android:windowSoftInputMode="adjustResize">
    
    <intent-filter>
      <action android:name="android.intent.action.MAIN" />
      <category android:name="android.intent.category.LAUNCHER" />
    </intent-filter>
  </activity>
</application>
```

---

## 🛠️ **Development Environment Issues**

### **Issue 1: Node.js and npm Issues**

#### **Symptoms**
- "Module not found" errors
- npm install failures
- Version conflicts

#### **Solutions**

**Solution 1: Environment Setup Script**
```bash
#!/bin/bash
# setup_environment.sh

echo "=== Certificate Verifier Development Environment Setup ==="

# Check Node.js version
NODE_VERSION=$(node --version 2>/dev/null)
if [ $? -eq 0 ]; then
    echo "✅ Node.js version: $NODE_VERSION"
else
    echo "❌ Node.js not installed"
    echo "Please install Node.js 16 or later from https://nodejs.org/"
    exit 1
fi

# Check npm version
NPM_VERSION=$(npm --version 2>/dev/null)
if [ $? -eq 0 ]; then
    echo "✅ npm version: $NPM_VERSION"
else
    echo "❌ npm not found"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python --version 2>/dev/null || python3 --version 2>/dev/null)
if [ $? -eq 0 ]; then
    echo "✅ Python version: $PYTHON_VERSION"
else
    echo "❌ Python not installed"
    echo "Please install Python 3.8 or later"
    exit 1
fi

# Install global dependencies
echo "Installing global dependencies..."
npm install -g @expo/cli eas-cli

# Setup React Native project
echo "Setting up React Native project..."
cd react-native-app
npm install

# Setup Python environment
echo "Setting up Python environment..."
cd ../python-scripts
pip install -r requirements.txt

echo "✅ Environment setup complete!"
echo "Run 'npm start' in react-native-app directory to start development server"
```

### **Issue 2: IDE and Editor Issues**

#### **Symptoms**
- IntelliSense not working
- Import errors in editor
- Debugging not working

#### **Solutions**

**Solution 1: VS Code Configuration**
```json
// .vscode/settings.json
{
  "typescript.preferences.importModuleSpecifier": "relative",
  "javascript.preferences.importModuleSpecifier": "relative",
  "emmet.includeLanguages": {
    "javascript": "javascriptreact"
  },
  "files.associations": {
    "*.js": "javascriptreact"
  },
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "python.defaultInterpreterPath": "./python-scripts/venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true
}
```

---

## 🔍 **Debugging Tools and Techniques**

### **Debug Console Setup**
```javascript
// DebugConsole.js
export class DebugConsole {
  static isEnabled = __DEV__;
  
  static log(message, data = null) {
    if (this.isEnabled) {
      console.log(`[DEBUG] ${message}`, data);
    }
  }
  
  static error(message, error = null) {
    if (this.isEnabled) {
      console.error(`[ERROR] ${message}`, error);
    }
  }
  
  static warn(message, data = null) {
    if (this.isEnabled) {
      console.warn(`[WARN] ${message}`, data);
    }
  }
  
  static trace(message) {
    if (this.isEnabled) {
      console.trace(`[TRACE] ${message}`);
    }
  }
}
```

### **System Health Check Script**
```python
# system_health_check.py
import os
import sys
import subprocess
import json
from datetime import datetime

def run_health_check():
    """Comprehensive system health check."""
    results = {
        "timestamp": datetime.now().isoformat(),
        "system": {},
        "python": {},
        "nodejs": {},
        "project": {}
    }
    
    # System information
    results["system"]["platform"] = sys.platform
    results["system"]["python_version"] = sys.version
    
    # Python dependencies
    try:
        import cryptography, PIL, qrcode, jwt, tkinter
        results["python"]["dependencies"] = "OK"
    except ImportError as e:
        results["python"]["dependencies"] = f"MISSING: {e}"
    
    # Node.js check
    try:
        node_version = subprocess.check_output(["node", "--version"]).decode().strip()
        results["nodejs"]["version"] = node_version
    except:
        results["nodejs"]["version"] = "NOT_FOUND"
    
    # Project structure
    required_files = [
        "certificate_generator.py",
        "keys/private_key.pem",
        "keys/public_key.pem",
        "react-native-app/package.json"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    results["project"]["missing_files"] = missing_files
    results["project"]["status"] = "OK" if not missing_files else "INCOMPLETE"
    
    return results

if __name__ == "__main__":
    health_results = run_health_check()
    print(json.dumps(health_results, indent=2))
```

---

## 📞 **Support and Escalation**

### **Getting Help**

1. **Documentation**: Check all documentation in the `Documentation/` folder
2. **GitHub Issues**: Report bugs at repository issues page
3. **Email Support**: support@certificateverifier.com
4. **Emergency Contact**: +1-XXX-XXX-XXXX (24/7 for critical issues)

### **When to Escalate**

- **Critical Security Issues**: Immediately
- **Data Loss or Corruption**: Within 1 hour
- **System-Wide Failures**: Within 2 hours
- **Performance Degradation**: Within 4 hours
- **Feature Requests**: Standard support channels

### **Information to Provide**

When reporting issues, include:
- **System Information**: OS, device model, app version
- **Error Messages**: Complete error text and stack traces
- **Steps to Reproduce**: Detailed reproduction steps
- **Screenshots/Videos**: Visual evidence of the issue
- **Log Files**: Relevant application logs

---

## 📋 **Quick Reference**

### **Emergency Commands**
```bash
# Reset everything
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
npx expo start --clear

# Regenerate keys
python generate_keys.py

# Check system health
python system_health_check.py

# Clear all caches
npx expo start --clear
watchman watch-del-all
```

### **Common Error Codes**

| Error Code | Description | Quick Fix |
|------------|-------------|-----------|
| **CERT_001** | Invalid JWT signature | Check keys, regenerate if needed |
| **CERT_002** | Certificate expired | Check system date/time |
| **CERT_003** | QR code unreadable | Clean camera lens, improve lighting |
| **PERM_001** | Camera permission denied | Enable in device settings |
| **NET_001** | Network connectivity issue | Check internet connection |
| **BUILD_001** | EAS build failure | Check credentials and configuration |

---

**End of Troubleshooting Guide**

For additional support, please refer to other documentation files or contact our support team.

---

**Document Information**
- **Created**: January 26, 2025
- **Team**: Oblivion - SIH 2025
- **Version**: 1.0.0
- **Next Review**: February 26, 2025