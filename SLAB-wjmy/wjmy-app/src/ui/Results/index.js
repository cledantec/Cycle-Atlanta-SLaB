/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 *
 * @format
 * @flow
 */

import React, {useState, useEffect} from 'react';
import {
  SafeAreaView,
  StyleSheet,
  ScrollView,
  View,
  Text,
  StatusBar,
  Alert,
  TouchableOpacity,
  Modal,
} from 'react-native';

import {Picker, Icon} from 'native-base';

import {Colors} from 'react-native/Libraries/NewAppScreen';
import setUpUser from '../../arch/setUpUser';
import getFitbitData from './getFitbitData';
import surveyHelper from '../InRide/surveyHelper';



// import firebase from '@react-native-firebase/app';
// import database from '@react-native-firebase/database';
const submitMeasures = (gps, mag, gyro, bar, acc, voice, heartRate, survey, myRide) => {
  let problems = ''
  if (heartRate == null) {
    Alert.alert(
      'Fitbit data not gathered',
      'Do you want to send to the database anyway',
      [
        {
          text: "Don't Send",
          onPress: () => console.log('Cancel Pressed'),
          style: 'cancel',
        },
        {
          text: 'SEND',
          onPress: () => {
            
            let obj = {}
              try {
                myRide.doc('magnemometer').set(Object.assign(obj, mag), {merge: true});
              } catch {
                console.log("Magnemometer data not collected")
                problems = problems + "Magnemometer, "
              }
              obj = {}
              try {
                myRide.doc('gyroscope').set(Object.assign(obj, gyro), {merge: true});
              } catch {
                console.log("Gyroscope data not collected")
                problems = problems + "Gyroscope, "
              }
              obj = {}
              try {
                myRide.doc('barometer').set(Object.assign(obj, bar), {merge: true});
              } catch {
                console.log("Barometer data not collected")
                problems = problems +"Barometer, "
              }
              obj = {}
              try {
                myRide.doc('accelerometer').set(Object.assign(obj, acc), {merge: true});
              }
              catch {
                console.log("Accelerometer data not collected")
                problems = problems +"Accelorometer, "
              }
              obj = {}
              try {
                myRide.doc('gps').set(Object.assign(obj, gps), {merge: true});
              } catch {
                console.log("GPS data not collected")
                problems = problems + "GPS, "
              }
              obj = {}
              try {
                myRide.doc('voice').set(Object.assign(obj, voice), {merge: true});
              } catch {
                console.log("Voice data not collected")
                problems = problems + "Voice Markers "
              }
              obj = {}
              try {
                console.log(survey)
                myRide.doc("Surveys").set(Object.assign(obj, survey), {merge: true});
              } catch (e) {
                console.log("Not able to send surveys. Data not collected")
                problems = problems + "Surveys, "
              }
              if (problems !== "") {
                console.log("sending alert")
                Alert.alert(
                  'Could not send data from: ' + problems,
                  'All other data successfully sent to database.',
                  [
                    {
                      text: "OK",
                      onPress: () => console.log('Cancel Pressed'),
                      style: 'cancel',
                    },
                    
                  ],
                  {cancelable: false},
                )
                        
              } else {
                Alert.alert(
                  'All data successfully saved.',
                  'You may exit the app now or return to sign up to start a new ride.',
                  [
                    {
                      text: "OK",
                      onPress: () => console.log('Cancel Pressed'),
                      style: 'cancel',
                    },
                    
                  ],
                  {cancelable: false},
                )
              }
  
          },
        },
      ],
      {cancelable: false},
    );
  } else {
    let obj = {}
    try {
      myRide.doc('magnemometer').set(Object.assign(obj, mag), {merge: true});
    } catch {
      console.log("Magnemometer data not collected")
      problems = problems + "Magnemometer, "
    }
    obj = {}
    try {
      myRide.doc('gyroscope').set(Object.assign(obj, gyro), {merge: true});
    } catch {
      console.log("Gyroscope data not collected")
      problems = problems + "Gyroscope, "
    }
    obj = {}
    try {
      myRide.doc('barometer').set(Object.assign(obj, bar), {merge: true});
    } catch {
      console.log("Barometer data not collected")
      problems = problems + "Barometer, "
    }
    obj = {}
    try {
      myRide.doc('accelerometer').set(Object.assign(obj, acc), {merge: true});
    }
    catch {
      console.log("Accelerometer data not collected")
      problems = problems + "Accelorometer, "
    }
    obj = {}
    try {
      myRide.doc('gps').set(Object.assign(obj, gps), {merge: true});
    } catch {
      console.log("GPS data not collected")
      problems = problems + "GPS, "
    }
    obj = {}
    try {
      myRide.doc('voice').set(Object.assign(obj, voice), {merge: true});
    } catch {
      console.log("Voice data not collected")
      problems = problems + "Voice Markers, "
    }
    obj = {}
    try {
      myRide.doc('heartrate').set(Object.assign(obj, heartRate), {merge: true});
    } catch {
      problems = problems + "Heart rate, "
    }
    
    obj = {}
    try {
      myRide.doc("Surveys").set(Object.assign(obj, survey), {merge: true});
    } catch (e) {
      console.log("Not able to send surveys. Data not collected")
      problems = problems + "Survey, "
    }
    if (problems !== "") {
      console.log("sending alert")
      Alert.alert(
        'Could not send data from: ' + problems,
        'All other data successfully sent to database.',
        [
          {
            text: "OK",
            onPress: () => console.log('Cancel Pressed'),
            style: 'cancel',
          },
          
        ],
        {cancelable: false},
      )
              
    } else {
      Alert.alert(
        'All data successfully sent',
        'You may exit the app now or return to sign up to start a new ride.',
        [
          {
            text: "OK",
            onPress: () => console.log('Cancel Pressed'),
            style: 'cancel',
          },
          
        ],
        {cancelable: false},
      )
    }
  }
  
};




const Results: () => React$Node = ({route, navigation: {navigate}}) => {
  const {name, level, mag, gps, gyro, bar, voice, acc, surveyAnswers} = route.params;
  const [myRide, setRide] = useState();
  const [heartRate, setHeartRate] = useState();
  [allAnswers, setAnswers] = useState(surveyAnswers);
  console.log("all");
  console.log(allAnswers);
  [modalInfo, setModalInfo] = useState({name:'', content: []});
  [modalVisible, setVisible] = useState(false);

  
  useEffect(() => {
    setRide(setUpUser(name, level));
  }, [name, level]);


  const onValueChangeType= (answer, index) => {
    // Update the document title using the browser API
      updated = modalInfo.content // this is just the post survey
      updated[index].userAnswer = answer // set the user answer of post so drop down updates
      updatedAnswers = allAnswers  // this should be all the things
      updatedAnswers[0]["content"] = updated
      setModalInfo({name: modalInfo.name, num: modalInfo.num, content:updated})
      setAnswers(updatedAnswers)
      console.log("easy")
      console.log(updatedAnswers)
    }

  
  return (
    <>
      <StatusBar barStyle="dark-content" />
          <View style={styles.body}>
            <View style={styles.sectionContainer}>
              <Text style={styles.sectionTitle}>Take Survey</Text>
              <View style={styles.tabs}>
                  <TouchableOpacity style={[styles.button, styles.clickedButton]} onPress={() => [setVisible(true), setModalInfo(allAnswers[0]), console.log(modalInfo)]}>
                    <Text style={styles.clickedText}>Post Ride</Text>
                  </TouchableOpacity>
                </View></View>
            <Modal visible={modalVisible}>
            <StatusBar barStyle="dark-content" />
              <SafeAreaView>
                <ScrollView
                  contentInsetAdjustmentBehavior="automatic"
                  style={styles.scrollView}>
                  {global.HermesInternal == null ? null : (
                    <View style={styles.engine}>
                      <Text style={styles.footer}>Engine: Hermes</Text>
                    </View>
                  )}
                </ScrollView>
            </SafeAreaView>
              <View style={styles.sectionContainer}>
                <TouchableOpacity onPress = {() => setVisible(false)}>
                    <Text>
                      Cancel
                    </Text>
                  </TouchableOpacity>
                  <Text>{'\n'}</Text>
                  <Text style={styles.sectionTitle}>{modalInfo.name} Survey:</Text>
                  <Text>{'\n'}</Text>
                  
                  {(modalInfo.content).map((item, index) => {
                      return(
                      <View>
                        <Text>{item.question}</Text>
                        <Picker mode='dropdown' placeholder="Click here to select answer"  iosIcon={<Icon name="caretdown" type="AntDesign"/>} selectedValue={item.userAnswer} onValueChange={(value) => {onValueChangeType(value, index)}}>
                        {(item.answers).map((options, choice) => {
                          return(<Picker.Item label={options} value={options} />)
                        })}
                      </Picker>
                    </View>
                      )  
                  })}
  
                  
                <Text>{'\n'}</Text>
                <TouchableOpacity
                  style={[
                    styles.button, styles.submit]} onPress = {() => [setVisible(false)]}>
                  <Text>
                    Submit
                  </Text>
                </TouchableOpacity>
              </View>    
            </Modal>
            </View>
      <SafeAreaView>
        <ScrollView
          contentInsetAdjustmentBehavior="automatic"
          style={styles.scrollView}>
            <View>
          {global.HermesInternal == null ? null : (
            <View style={styles.engine}>
              <Text style={styles.footer}>Engine: Hermes</Text>
            </View>
          )}
          
            <View style={styles.sectionContainer}>
              <Text style={styles.sectionTitle}>Go to Fitbit</Text>
              <TouchableOpacity
                style={[styles.button, styles.clickedButton]}
                onPress={() => getFitbitData(setHeartRate)}>
                <Text style={styles.clickedText}>Get Data From Fibit</Text>
              </TouchableOpacity>
            </View>
            <TouchableOpacity
              onPress={() => submitMeasures(gps, mag, gyro, bar, acc, voice, heartRate, allAnswers, myRide)}
              style={[styles.button, styles.submit]}>
              <Text>Submit</Text>
            </TouchableOpacity>
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

export default Results;
