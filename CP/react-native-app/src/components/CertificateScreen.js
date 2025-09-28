/**
 * Certificate Display Screen
 * 
 * This component displays verified certificate information in a professional format.
 * It shows all certificate details and provides options to scan another certificate.
 */

import React, {useRef} from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Alert,
  Dimensions,
  PermissionsAndroid,
  Platform,
} from 'react-native';
import ViewShot from 'react-native-view-shot';
import * as Sharing from 'expo-sharing';
import CertificateView from './CertificateView';

const {width} = Dimensions.get('window');

const CertificateScreen = ({route, navigation}) => {
  const {certificateData, isValid} = route.params;
  const certificateRef = useRef();

  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp * 1000);
    return date.toLocaleString('en-IN', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      timeZone: 'Asia/Kolkata',
      timeZoneName: 'short',
    });
  };

  const formatDeviceId = (deviceId) => {
    if (!deviceId) return 'Unknown';
    // Split device ID for better readability
    const parts = deviceId.split('-');
    return parts.join('\n');
  };

  const formatDataHash = (hash) => {
    if (!hash) return 'N/A';
    // Display hash in groups of 8 characters for readability
    return hash.match(/.{1,8}/g)?.join(' ') || hash;
  };

  const handleScanAnother = () => {
    navigation.goBack();
  };

  const handleShowDetails = () => {
    Alert.alert(
      'Certificate Details',
      `Full Certificate Information:\n\n${JSON.stringify(certificateData, null, 2)}`,
      [{text: 'OK'}]
    );
  };

  const requestStoragePermission = async () => {
    if (Platform.OS === 'android') {
      try {
        const granted = await PermissionsAndroid.request(
          PermissionsAndroid.PERMISSIONS.WRITE_EXTERNAL_STORAGE,
          {
            title: 'Storage Permission',
            message: 'This app needs access to storage to save certificate images.',
            buttonNeutral: 'Ask Me Later',
            buttonNegative: 'Cancel',
            buttonPositive: 'OK',
          }
        );
        return granted === PermissionsAndroid.RESULTS.GRANTED;
      } catch (err) {
        console.warn(err);
        return false;
      }
    }
    return true;
  };

  const handleSaveAsImage = async () => {
    try {
      const hasPermission = await requestStoragePermission();
      if (!hasPermission) {
        Alert.alert('Permission Denied', 'Storage permission is required to save the certificate.');
        return;
      }

      const uri = await certificateRef.current.capture({
        format: 'png',
        quality: 1.0,
        result: 'tmpfile',
      });

      Alert.alert(
        'Certificate Saved',
        'The certificate has been saved to your device.',
        [{text: 'OK'}]
      );
    } catch (error) {
      console.error('Error saving certificate:', error);
      Alert.alert('Error', 'Failed to save certificate. Please try again.');
    }
  };

  const handleShare = async () => {
    try {
      const uri = await certificateRef.current.capture({
        format: 'png',
        quality: 1.0,
        result: 'tmpfile',
      });

      // Check if sharing is available on the device
      if (!(await Sharing.isAvailableAsync())) {
        Alert.alert('Error', 'Sharing is not available on this device');
        return;
      }

      await Sharing.shareAsync(uri, {
        mimeType: 'image/png',
        dialogTitle: 'Share Data Sanitization Certificate',
      });
    } catch (error) {
      console.error('Error sharing certificate:', error);
      Alert.alert('Error', 'Failed to share certificate. Please try again.');
    }
  };

  if (!isValid) {
    return (
      <View style={styles.container}>
        <View style={styles.errorContainer}>
          <Text style={styles.errorIcon}>❌</Text>
          <Text style={styles.errorTitle}>Invalid Certificate</Text>
          <Text style={styles.errorMessage}>
            The certificate could not be verified. This may indicate:
          </Text>
          <View style={styles.errorReasons}>
            <Text style={styles.errorReason}>• Invalid digital signature</Text>
            <Text style={styles.errorReason}>• Corrupted QR code data</Text>
            <Text style={styles.errorReason}>• Unsupported certificate format</Text>
          </View>
          <TouchableOpacity
            style={styles.scanAgainButton}
            onPress={handleScanAnother}>
            <Text style={styles.scanAgainButtonText}>🔍 Scan Another</Text>
          </TouchableOpacity>
        </View>
      </View>
    );
  }

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.scrollContent}>
      {/* Professional Certificate View */}
      <ViewShot ref={certificateRef} options={{ format: 'png', quality: 1.0 }}>
        <CertificateView certificateData={certificateData} />
      </ViewShot>

      {/* Action Buttons */}
      <View style={styles.buttonContainer}>
        <TouchableOpacity
          style={styles.saveButton}
          onPress={handleSaveAsImage}>
          <Text style={styles.saveButtonText}>💾 Save as Image</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.shareButton}
          onPress={handleShare}>
          <Text style={styles.shareButtonText}>📤 Share</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.detailsButton}
          onPress={handleShowDetails}>
          <Text style={styles.detailsButtonText}>📄 Show Full Details</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.scanButton}
          onPress={handleScanAnother}>
          <Text style={styles.scanButtonText}>🔍 Scan Another Certificate</Text>
        </TouchableOpacity>
      </View>

      {/* Footer */}
      <View style={styles.footer}>
        <Text style={styles.footerText}>
          ⚠️ This verification was performed offline using cryptographic signatures.
          Keep this information secure and do not share unnecessarily.
        </Text>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  scrollContent: {
    padding: 10,
  },
  buttonContainer: {
    marginVertical: 20,
    paddingHorizontal: 10,
  },
  saveButton: {
    backgroundColor: '#27ae60',
    borderRadius: 25,
    paddingVertical: 15,
    paddingHorizontal: 30,
    marginBottom: 10,
    alignItems: 'center',
    elevation: 3,
    shadowColor: '#000',
    shadowOffset: {width: 0, height: 2},
    shadowOpacity: 0.2,
    shadowRadius: 4,
  },
  saveButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  shareButton: {
    backgroundColor: '#3498db',
    borderRadius: 25,
    paddingVertical: 15,
    paddingHorizontal: 30,
    marginBottom: 10,
    alignItems: 'center',
    elevation: 3,
    shadowColor: '#000',
    shadowOffset: {width: 0, height: 2},
    shadowOpacity: 0.2,
    shadowRadius: 4,
  },
  shareButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  detailsButton: {
    backgroundColor: '#9b59b6',
    borderRadius: 25,
    paddingVertical: 15,
    paddingHorizontal: 30,
    marginBottom: 10,
    alignItems: 'center',
    elevation: 3,
    shadowColor: '#000',
    shadowOffset: {width: 0, height: 2},
    shadowOpacity: 0.2,
    shadowRadius: 4,
  },
  detailsButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  scanButton: {
    backgroundColor: '#95a5a6',
    borderRadius: 25,
    paddingVertical: 15,
    paddingHorizontal: 30,
    alignItems: 'center',
    elevation: 3,
    shadowColor: '#000',
    shadowOffset: {width: 0, height: 2},
    shadowOpacity: 0.2,
    shadowRadius: 4,
  },
  scanButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  footer: {
    backgroundColor: '#fff3cd',
    padding: 15,
    borderRadius: 10,
    borderLeftWidth: 4,
    borderLeftColor: '#ffc107',
    marginHorizontal: 10,
    marginBottom: 20,
  },
  footerText: {
    fontSize: 12,
    color: '#856404',
    lineHeight: 16,
    textAlign: 'center',
  },
  errorContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  errorIcon: {
    fontSize: 60,
    marginBottom: 20,
  },
  errorTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#e74c3c',
    marginBottom: 15,
  },
  errorMessage: {
    fontSize: 16,
    color: '#7f8c8d',
    textAlign: 'center',
    marginBottom: 20,
    lineHeight: 22,
  },
  errorReasons: {
    marginBottom: 30,
  },
  errorReason: {
    fontSize: 14,
    color: '#95a5a6',
    marginBottom: 5,
  },
  scanAgainButton: {
    backgroundColor: '#e74c3c',
    borderRadius: 25,
    paddingVertical: 15,
    paddingHorizontal: 30,
  },
  scanAgainButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
});

export default CertificateScreen;