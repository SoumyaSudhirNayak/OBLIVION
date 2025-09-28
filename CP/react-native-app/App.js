/**
 * Certificate Verifier App
 * 
 * Main application component with navigation between scanner and certificate display screens.
 * This app operates entirely offline and verifies JWT certificates from QR codes.
 */

import React from 'react';
import {NavigationContainer} from '@react-navigation/native';
import {createStackNavigator} from '@react-navigation/stack';
import {StatusBar, StyleSheet} from 'react-native';

import ScannerScreen from './src/components/ScannerScreen';
import CertificateScreen from './src/components/CertificateScreen';

const Stack = createStackNavigator();

const App = () => {
  return (
    <>
      <StatusBar barStyle="light-content" backgroundColor="#2c3e50" />
      <NavigationContainer>
        <Stack.Navigator
          initialRouteName="Scanner"
          screenOptions={{
            headerStyle: {
              backgroundColor: '#2c3e50',
            },
            headerTintColor: '#fff',
            headerTitleStyle: {
              fontWeight: 'bold',
              fontSize: 18,
            },
          }}>
          <Stack.Screen
            name="Scanner"
            component={ScannerScreen}
            options={{
              title: 'QR Code Scanner',
              headerStyle: {
                backgroundColor: '#007AFF',
              },
              headerTintColor: '#fff',
              headerTitleStyle: {
                fontWeight: 'bold',
              },
              headerBackTitleVisible: false,
              headerLeft: () => null,
            }}
          />
          <Stack.Screen
              name="Certificate"
              component={CertificateScreen}
              options={{
                title: 'Certificate Details',
                headerStyle: {
                  backgroundColor: '#007AFF',
                },
                headerTintColor: '#fff',
                headerTitleStyle: {
                  fontWeight: 'bold',
                },
                headerBackTitleVisible: false,
                headerLeft: () => null,
              }}
            />
        </Stack.Navigator>
      </NavigationContainer>
    </>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#ecf0f1',
  },
});

export default App;