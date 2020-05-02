/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 *
 * @format
 * @flow
 */

import React, {useState} from 'react';
import {
  SafeAreaView,
  StyleSheet,
  ScrollView,
  View,
  Text,
  StatusBar,
  Button,
  Image,
  PermissionsAndroid,
  Platform,
} from 'react-native';

import {Colors} from 'react-native/Libraries/NewAppScreen';

// import firebase from '@react-native-firebase/app';
// import database from '@react-native-firebase/database';

import UserInput from './UserInput';

import {
  magnetometer,
  SensorTypes,
  setUpdateIntervalForType,
} from 'react-native-sensors';
import {TouchableOpacity} from 'react-native-gesture-handler';

async function requestLocationPermission() {
  if (Platform === 'android') {
    try {
      const granted = await PermissionsAndroid.request(
        PermissionsAndroid.PERMISSIONS.ACCESS_FINE_LOCATION,
        {
          title: 'we just met yesterday requires fine location',
          message:
            'wjmy requires fine location to ' +
            'see where our riders are stressed.',
          buttonNeutral: 'Ask Me Later',
          buttonNegative: 'Cancel',
          buttonPositive: 'OK',
        },
      );
      if (granted === PermissionsAndroid.RESULTS.GRANTED) {
        console.log('You can use location');
      } else {
        console.log('location permission denied');
      }
    } catch (err) {
      console.warn(err);
    }
  }
}

// let batch = db.batch();
const submit = (name, level, navigate) => {
  if (name && level >= 0) {
    navigate('InRide', {name: name, level: level});
  }
};

const Home: () => React$Node = ({navigation: {navigate}}) => {
  setUpdateIntervalForType(SensorTypes.magnetometer, 400); // defaults to 100ms
  const [name, setName] = useState();
  const [level, setLevel] = useState(-1);
  // const subscription = magnetometer.subscribe(({x, y, z, timestamp}) =>
  //   console.log({x, y, z, timestamp}),
  // );
  requestLocationPermission();
  return (
    <>
      <StatusBar barStyle="dark-content" />
      <SafeAreaView>
        <ScrollView
          contentInsetAdjustmentBehavior="automatic"
          style={styles.scrollView}>
          <Image
            style={styles.image}
            source={require('./bikeSplash.jpg')}
            overflow={'visible'}
          />
          {global.HermesInternal == null ? null : (
            <View style={styles.engine}>
              <Text style={styles.footer}>Engine: Hermes</Text>
            </View>
          )}
          <View style={styles.body}>
            <View style={styles.sectionContainer}>
              <Text style={styles.sectionTitle}>Rider Setup</Text>
              <Text style={styles.highlight}>Name </Text>
              <UserInput text={name} setText={setName} />
              <Text style={styles.highlight}>Rider Level </Text>
              <TouchableOpacity
                onPress={() => setLevel(0)}
                style={[
                  styles.button,
                  level === 0 ? styles.clickedButton : styles.unClickedButton,
                ]}>
                <Text
                  style={
                    level === 0 ? styles.clickedText : styles.unClickedText
                  }>
                  Interested, but Concerned
                </Text>
              </TouchableOpacity>
              <TouchableOpacity
                onPress={() => setLevel(1)}
                style={[
                  styles.button,
                  level === 1 ? styles.clickedButton : styles.unClickedButton,
                ]}>
                <Text
                  style={
                    level === 1 ? styles.clickedText : styles.unClickedText
                  }>
                  Comfortable, but Cautious
                </Text>
              </TouchableOpacity>
              <TouchableOpacity
                onPress={() => setLevel(2)}
                style={[
                  styles.button,
                  level === 2 ? styles.clickedButton : styles.unClickedButton,
                ]}>
                <Text
                  style={
                    level === 2 ? styles.clickedText : styles.unClickedText
                  }>
                  Enthused & Confident
                </Text>
              </TouchableOpacity>
              <TouchableOpacity
                onPress={() => setLevel(3)}
                style={[
                  styles.button,
                  level === 3 ? styles.clickedButton : styles.unClickedButton,
                ]}>
                <Text
                  style={
                    level === 3 ? styles.clickedText : styles.unClickedText
                  }>
                  Strong & Fearless
                </Text>
              </TouchableOpacity>
              <TouchableOpacity
                style={[styles.button, styles.submit]}
                onPress={() => submit(name, level, navigate)}>
                <Text>Submit</Text>
              </TouchableOpacity>
            </View>
          </View>
        </ScrollView>
      </SafeAreaView>
    </>
  );
};

const styles = StyleSheet.create({
  clickedText: {
    color: Colors.white,
  },
  unClickedText: {
    color: Colors.black,
  },
  clickedButton: {
    backgroundColor: '#4A6572',
  },
  unClickedButton: {
    backgroundColor: Colors.lighter,
  },
  submit: {
    marginTop: 40,
    backgroundColor: '#F9AA33',
  },
  button: {
    alignItems: 'center',
    paddingHorizontal: 5,
    paddingVertical: 20,
    marginVertical: 5,
    borderRadius: 8,
  },
  scrollView: {
    backgroundColor: Colors.lighter,
  },
  engine: {
    position: 'absolute',
    right: 0,
  },
  body: {
    backgroundColor: Colors.white,
  },
  sectionContainer: {
    marginTop: 32,
    paddingHorizontal: 24,
  },
  sectionTitle: {
    fontSize: 24,
    fontWeight: '600',
    color: Colors.black,
  },
  highlight: {
    paddingVertical: 5,
    fontWeight: '700',
  },
  footer: {
    color: Colors.dark,
    fontSize: 12,
    fontWeight: '600',
    padding: 4,
    paddingRight: 12,
    textAlign: 'right',
  },
  image: {
    width: '100%',
    height: 200,
  },
});

export default Home;
