# Offline QR-Code-Based Secure Certificate System

This project implements a complete, end-to-end system for generating and verifying secure data wipe certificates that works 100% offline. The system has been updated with a new certificate format and modern shield-based design.

## Project Structure

```
CP/
├── python-scripts/          # Part 1: Certificate Generator (Python)
│   ├── generate_keys.py     # Utility to generate RS256 key pairs
│   ├── certificate_generator.py  # Main certificate generation script
│   ├── hardware_info.py     # Hardware detection utilities
│   ├── requirements.txt     # Python dependencies
│   └── output/             # Generated keys and QR codes
├── react-native-app/       # Part 2: Verifier App (React Native)
│   ├── App.js              # Main app component
│   ├── package.json        # React Native dependencies
│   ├── assets/             # App icons and shield graphics
│   └── src/
│       ├── components/     # Certificate display components
│       ├── utils/          # JWT verification utilities
│       └── demo-data/      # Mock data for development
└── README.md               # This file
```

## Part 1: Python Certificate Generator

The Python module generates a signed certificate as a QR code after a successful data wipe with real hardware detection.

### Features:
- Generates RS256 private/public key pairs
- Creates JWT-signed certificates with device and wipe information
- Real hardware detection (device type, motherboard SN, disk SN)
- Displays QR codes for offline verification with modern GUI
- Works in RAM-resident environments with no file system access

### Usage:
1. Run `generate_keys.py` to create key pairs (one-time setup)
2. Run `certificate_generator.py` to generate and display certificates

## Part 2: React Native Verifier App

A lightweight mobile app that scans and verifies certificate QR codes offline with a modern shield-based design.

### Features:
- Camera-based QR code scanning
- Offline JWT signature verification
- Professional certificate display with shield background
- Tamper detection and error handling
- Modern UI with improved visual design

### Setup:
1. Install dependencies: `npm install`
2. Run with Expo: `npx expo start`
3. Scan QR code with Expo Go app or run on simulator

## Security Features

- **Asymmetric Cryptography**: Uses RS256 for tamper-proof signatures
- **Offline Operation**: No network connectivity required
- **Hardcoded Keys**: Public key embedded in mobile app
- **JWT Standard**: Industry-standard token format for certificates

## Certificate Information

Each certificate contains:
- Certificate ID (unique UUID)
- Device Type (automatically detected: Desktop, Laptop, Server, etc.)
- Device ID (motherboard and disk serial numbers)
- Wipe method (DoD 5220.22-M 3-pass)
- Timestamp and completion status
- Data hash for integrity verification
- Issuer information and version