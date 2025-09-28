/**
 * QR Code Scanner Screen
 * 
 * This component handles QR code scanning, JWT verification, and navigation to certificate display.
 * It operates entirely offline using a hardcoded public key for verification.
 */

import React, {useState, useEffect} from 'react';
import {
  View,
  Text,
  StyleSheet,
  Alert,
  TouchableOpacity,
  Dimensions,
  ActivityIndicator,
} from 'react-native';
import { CameraView, Camera } from 'expo-camera';
import {verifyJWT} from '../utils/jwtVerifier';

const {width, height} = Dimensions.get('window');

const ScannerScreen = ({navigation}) => {
  const [scanning, setScanning] = useState(true);
  const [hasPermission, setHasPermission] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    getBarCodeScannerPermissions();
  }, []);

  const getBarCodeScannerPermissions = async () => {
    const { status } = await Camera.requestCameraPermissionsAsync();
    setHasPermission(status === 'granted');
  };

  const handleBarCodeScanned = async ({ type, data }) => {
    if (!scanning) return;
    
    setScanning(false);
    setLoading(true);

    try {
      const qrData = data;
      console.log('QR Code scanned:', qrData);

      // Verify the JWT token
      const verificationResult = await verifyJWT(qrData);

      setLoading(false);

      if (verificationResult.valid) {
        // Navigate to certificate display with verified data
        navigation.navigate('Certificate', {
          certificateData: verificationResult.payload,
          isValid: true,
        });
      } else {
        // Show error and allow scanning again
        Alert.alert(
          '❌ Invalid Certificate',
          verificationResult.error || 'The certificate could not be verified.',
          [
            {
              text: 'Scan Again',
              onPress: () => setScanning(true),
            },
          ],
        );
      }
    } catch (error) {
      setLoading(false);
      console.error('Error processing QR code:', error);
      
      Alert.alert(
        '❌ Scan Error',
        'Failed to process the QR code. Please try again.',
        [
          {
            text: 'Scan Again',
            onPress: () => setScanning(true),
          },
        ],
      );
    }
  };

  const resetScanner = () => {
    setScanning(true);
  };

  if (hasPermission === null) {
    return (
      <View style={styles.permissionContainer}>
        <ActivityIndicator size="large" color="#3498db" />
        <Text style={styles.permissionText}>Requesting camera permission...</Text>
      </View>
    );
  }

  if (hasPermission === false) {
    return (
      <View style={styles.permissionContainer}>
        <Text style={styles.permissionText}>
          📷 Camera access is required to scan QR codes
        </Text>
        <TouchableOpacity
          style={styles.permissionButton}
          onPress={getBarCodeScannerPermissions}>
          <Text style={styles.permissionButtonText}>Grant Permission</Text>
        </TouchableOpacity>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {loading && (
        <View style={styles.loadingOverlay}>
          <ActivityIndicator size="large" color="#fff" />
          <Text style={styles.loadingText}>Verifying certificate...</Text>
        </View>
      )}

      <View style={styles.topContent}>
        <Text style={styles.centerText}>
          🔍 Scan Certificate QR Code
        </Text>
        <Text style={styles.instructionText}>
          Position the QR code within the frame to verify the certificate
        </Text>
      </View>

      <CameraView
        style={styles.camera}
        facing="back"
        onBarcodeScanned={scanning ? handleBarCodeScanned : undefined}
        barcodeScannerSettings={{
          barcodeTypes: ["qr", "pdf417"],
        }}
      />

      <View style={styles.bottomContent}>
        <TouchableOpacity
          style={styles.buttonTouchable}
          onPress={resetScanner}
          disabled={loading}>
          <Text style={styles.buttonText}>🔄 Reset Scanner</Text>
        </TouchableOpacity>
        
        <View style={styles.infoContainer}>
          <Text style={styles.infoText}>
            ℹ️ This app verifies certificates offline using cryptographic signatures
          </Text>
        </View>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000',
  },
  permissionContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#ecf0f1',
    padding: 20,
  },
  permissionText: {
    fontSize: 16,
    textAlign: 'center',
    marginBottom: 20,
    color: '#2c3e50',
  },
  permissionButton: {
    backgroundColor: '#3498db',
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderRadius: 5,
  },
  permissionButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  loadingOverlay: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(0, 0, 0, 0.7)',
    justifyContent: 'center',
    alignItems: 'center',
    zIndex: 1000,
  },
  loadingText: {
    color: '#fff',
    fontSize: 16,
    marginTop: 10,
  },
  camera: {
    flex: 1,
  },
  marker: {
    borderColor: '#3498db',
    borderWidth: 3,
    borderRadius: 10,
  },
  topContent: {
    backgroundColor: '#ecf0f1',
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingVertical: 30,
  },
  centerText: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#2c3e50',
    marginBottom: 10,
  },
  instructionText: {
    fontSize: 14,
    color: '#7f8c8d',
    textAlign: 'center',
    lineHeight: 20,
  },
  bottomContent: {
    backgroundColor: '#ecf0f1',
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingVertical: 30,
  },
  buttonTouchable: {
    backgroundColor: '#3498db',
    paddingHorizontal: 30,
    paddingVertical: 15,
    borderRadius: 25,
    marginBottom: 20,
  },
  buttonText: {
    fontSize: 16,
    color: '#fff',
    fontWeight: 'bold',
  },
  infoContainer: {
    backgroundColor: '#fff',
    padding: 15,
    borderRadius: 10,
    borderLeftWidth: 4,
    borderLeftColor: '#3498db',
  },
  infoText: {
    fontSize: 12,
    color: '#7f8c8d',
    textAlign: 'center',
    lineHeight: 16,
  },
});

export default ScannerScreen;