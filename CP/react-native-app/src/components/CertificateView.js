/**
 * Professional Certificate View Component
 * 
 * This component renders a formal digital certificate for data sanitization
 * with professional styling, logo, and shield background design.
 */

import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  Image,
  Dimensions,
  ImageBackground,
} from 'react-native';

const {width} = Dimensions.get('window');

const CertificateView = React.forwardRef(({certificateData}, ref) => {
  // Helper function to format timestamp
  const formatTimestamp = (timestamp) => {
    if (!timestamp) return 'N/A';
    const date = new Date(timestamp * 1000);
    return date.toLocaleString('en-IN', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      timeZone: 'Asia/Kolkata',
    });
  };

  // Helper function to truncate hash
  const truncateHash = (hash) => {
    if (!hash) return 'N/A';
    return hash.length > 16 ? `${hash.substring(0, 16)}...` : hash;
  };

  return (
    <View ref={ref} style={styles.certificateContainer}>
      {/* Shield Background */}
      <ImageBackground
        source={require('../../assets/shield.png')}
        style={styles.shieldBackground}
        resizeMode="contain"
        imageStyle={styles.shieldBackgroundImage}
      >
        {/* Header Section */}
        <View style={styles.header}>
          <View style={styles.headerTop}>
            <Image
              source={require('../../assets/oblivion-logo.png')}
              style={styles.logo}
              resizeMode="contain"
            />
            <View style={styles.titleContainer}>
              <Text style={styles.certificateTitle}>
                CERTIFICATE OF DATA SANITIZATION
              </Text>
              <Text style={styles.certificateSubtitle}>
                Digital Security Verification
              </Text>
            </View>
          </View>
        </View>

        {/* Verification Badge */}
        <View style={styles.verificationBadge}>
          <Text style={styles.verifiedText}>VERIFIED</Text>
          <Text style={styles.authenticText}>AUTHENTIC CERTIFICATE</Text>
        </View>

        {/* Main Content Area */}
        <View style={styles.contentArea}>
          <Text style={styles.sectionTitle}>CERTIFICATE DETAILS</Text>
          
          <View style={styles.detailsGrid}>
            <View style={styles.detailRow}>
              <Text style={styles.detailLabel}>Device Type:</Text>
              <Text style={styles.detailValue}>{certificateData.deviceType || 'Unknown Device'}</Text>
            </View>

            <View style={styles.detailRow}>
              <Text style={styles.detailLabel}>Device ID:</Text>
              <Text style={styles.detailValue}>{certificateData.deviceID || 'N/A'}</Text>
            </View>

            <View style={styles.detailRow}>
              <Text style={styles.detailLabel}>Sanitization Method:</Text>
              <Text style={styles.detailValue}>NIST 800-88 Secure Wipe</Text>
            </View>

            <View style={styles.detailRow}>
              <Text style={styles.detailLabel}>Completion Time:</Text>
              <Text style={styles.detailValue}>
                {formatTimestamp(certificateData.iat)}
              </Text>
            </View>

            <View style={styles.detailRow}>
              <Text style={styles.detailLabel}>Status:</Text>
              <View style={styles.statusBadge}>
                <Text style={styles.statusText}>COMPLETED</Text>
              </View>
            </View>
          </View>
        </View>

        {/* Footer Section */}
        <View style={styles.footer}>
          <View style={styles.footerRow}>
            <Text style={styles.footerLabel}>Issued By:</Text>
            <Text style={styles.footerValue}>{certificateData.iss || 'Oblivion v1.0'}</Text>
          </View>
          
          <View style={styles.footerRow}>
            <Text style={styles.footerLabel}>Certificate ID:</Text>
            <Text style={styles.footerValue}>{certificateData.certificateID || truncateHash(certificateData.dataHash)}</Text>
          </View>
          
          <View style={styles.signatureArea}>
            <Text style={styles.signatureText}>🔒 Digitally Signed & Cryptographically Verified</Text>
            <Text style={styles.timestampText}>
              Generated on {new Date().toLocaleDateString('en-IN')}
            </Text>
          </View>
        </View>
      </ImageBackground>

      {/* Certificate Border */}
      <View style={styles.certificateBorder} />
    </View>
  );
});

const styles = StyleSheet.create({
  certificateContainer: {
    backgroundColor: '#ffffff',
    margin: 10,
    borderRadius: 12,
    elevation: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 6 },
    shadowOpacity: 0.2,
    shadowRadius: 12,
    position: 'relative',
    overflow: 'hidden',
  },
  shieldBackground: {
    flex: 1,
    minHeight: 600,
  },
  shieldBackgroundImage: {
    opacity: 0.08,
    tintColor: '#2c3e50',
  },
  certificateBorder: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    borderWidth: 4,
    borderColor: '#2c3e50',
    borderRadius: 12,
    pointerEvents: 'none',
  },
  header: {
    backgroundColor: 'rgba(52, 73, 94, 0.95)',
    paddingVertical: 25,
    paddingHorizontal: 20,
    borderTopLeftRadius: 8,
    borderTopRightRadius: 8,
  },
  headerTop: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  logo: {
    width: 70,
    height: 70,
  },
  titleContainer: {
    flex: 1,
    alignItems: 'center',
    marginLeft: 15,
  },
  certificateTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#ffffff',
    textAlign: 'center',
    letterSpacing: 1.2,
    marginBottom: 4,
  },
  certificateSubtitle: {
    fontSize: 12,
    color: '#bdc3c7',
    textAlign: 'center',
    letterSpacing: 0.8,
  },
  verificationBadge: {
    alignItems: 'center',
    paddingVertical: 20,
    backgroundColor: 'rgba(255, 255, 255, 0.95)',
    marginHorizontal: 20,
    marginVertical: 15,
    borderRadius: 8,
    borderWidth: 2,
    borderColor: '#27ae60',
  },
  verifiedText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#27ae60',
    letterSpacing: 1.5,
    marginBottom: 4,
  },
  authenticText: {
    fontSize: 10,
    color: '#7f8c8d',
    letterSpacing: 1,
    fontWeight: '600',
  },
  contentArea: {
    padding: 25,
    backgroundColor: 'rgba(255, 255, 255, 0.95)',
    marginHorizontal: 20,
    marginBottom: 15,
    borderRadius: 8,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2c3e50',
    textAlign: 'center',
    marginBottom: 25,
    letterSpacing: 1,
    borderBottomWidth: 3,
    borderBottomColor: '#3498db',
    paddingBottom: 10,
  },
  detailsGrid: {
    marginBottom: 10,
  },
  detailRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 18,
    paddingBottom: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#ecf0f1',
  },
  detailLabel: {
    fontSize: 13,
    fontWeight: '700',
    color: '#7f8c8d',
    flex: 1,
    textTransform: 'uppercase',
    letterSpacing: 0.8,
  },
  detailValue: {
    fontSize: 13,
    color: '#2c3e50',
    flex: 2,
    textAlign: 'right',
    fontWeight: '600',
  },
  statusBadge: {
    backgroundColor: '#d5f4e6',
    paddingHorizontal: 15,
    paddingVertical: 6,
    borderRadius: 15,
    borderWidth: 1,
    borderColor: '#27ae60',
  },
  statusText: {
    fontSize: 12,
    fontWeight: 'bold',
    color: '#27ae60',
    letterSpacing: 0.5,
  },
  footer: {
    backgroundColor: 'rgba(248, 249, 250, 0.95)',
    padding: 20,
    marginHorizontal: 20,
    marginBottom: 20,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#dee2e6',
  },
  footerRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 10,
  },
  footerLabel: {
    fontSize: 12,
    color: '#6c757d',
    fontWeight: '700',
    letterSpacing: 0.5,
  },
  footerValue: {
    fontSize: 12,
    color: '#495057',
    fontWeight: '600',
  },
  signatureArea: {
    alignItems: 'center',
    marginTop: 20,
    paddingTop: 15,
    borderTopWidth: 2,
    borderTopColor: '#dee2e6',
  },
  signatureText: {
    fontSize: 11,
    color: '#6c757d',
    fontWeight: 'bold',
    marginBottom: 6,
    textAlign: 'center',
  },
  timestampText: {
    fontSize: 10,
    color: '#adb5bd',
    fontWeight: '500',
  },
});

export default CertificateView;