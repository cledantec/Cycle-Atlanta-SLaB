import React, {useState, useEffect} from 'react';
import {StyleSheet, Text, SafeAreaView, View, SectionList, Modal, ScrollView,
  StatusBar} from 'react-native';
import MapView, {Polyline, Marker} from 'react-native-maps';
import Voice from '@react-native-community/voice';
import BackgroundTimer from 'react-native-background-timer';
import DialogInput from 'react-native-dialog-input';
import surveyHelper from './surveyHelper';
import {Picker, Icon} from 'native-base';

import {
  magnetometer,
  accelerometer,
  gyroscope,
  barometer,
  SensorTypes,
  setUpdateIntervalForType,
} from 'react-native-sensors';
import {TouchableOpacity} from 'react-native-gesture-handler';
import {Colors} from 'react-native/Libraries/NewAppScreen';
import Geolocation from '@react-native-community/geolocation';


let mag = [];
let gyro = [];
let bar = [];
let acc = [];
let gps = [];
let coordsArr = [];
let voice = [];
let myMarkers = [];
let oldTime = 0;
let oldPhrase = "";
const  surveys = surveyHelper.InRide();
const post = surveyHelper.PostRide();

const useForceUpdate = () => useState()[1];

BackgroundTimer.runBackgroundTimer(() => { 
  //code that will be called every 20 seconds 
  // check if voice is still on 
    try {
      if (voiceRunning) {
        _startRecognizing()
        
      }
    } catch {
      console.log("possible problem with background timer")
    }
    
  }, 
  20000);

 

// This function turns on/off sensors and voice based of if the ride has started
const toggleMeasurements = (isRunning, voiceRunning) => {
  // measurements pushed to corresponding arrays
  const magSubscription = magnetometer.subscribe(
    ({x, y, z, timestamp}) => (mag.push({timestamp: timestamp, x: x, y: y, z: z})),
    error => console.log('magnetometer not available'),
  );
  const accSubscription = accelerometer.subscribe(({ x, y, z, timestamp }) =>
  acc.push({timestamp: timestamp, x:x, y:y, z:z}), 
  error => console.log('accelerometer not available'),
  );
  const gyroSubscription = gyroscope.subscribe(({ x, y, z, timestamp }) =>
  gyro.push({timestamp: timestamp, x:x, y:y, z:z}), 
  error => console.log('gyroscope not available'),
  );
  const barSubscription = barometer.subscribe(({ pressure }) =>
  bar.push({timestamp:timestamp, pressure:pressure}), 
  error => console.log('barometer not available'),
  );
  // if voice is enabled, start voice recording
  if (voiceRunning) {
    _startRecognizing();
  } else {
    _stopRecognizing();
  }
  if (!isRunning) {
    // turn off sensors if not running, in a try statement in case they were never turned on
    try {
      BackgroundTimer.stopBackgroundTimer(); //after this call all code on background stop run.
      magSubscription.unsubscribe();
      accSubscription.unsubscribe();
      gyroSubscription.unsubscribe();
      barSubscription.unsubscribe();
      _stopRecognizing();
    } catch {
      console.log("Sensors weren't all turned on so can't be turned off -- basically don't worry about it")
    }
  }
};



  // Set up sensors from Sensor Library
const InRide = ({route, navigation: {navigate}}) => {
  const {name, level} = route.params;

  setUpdateIntervalForType(SensorTypes.magnetometer, 400); // defaults to 100ms
  setUpdateIntervalForType(SensorTypes.accelerometer, 400); // defaults to 100ms
  setUpdateIntervalForType(SensorTypes.gyroscope, 400); // defaults to 100ms
  setUpdateIntervalForType(SensorTypes.barometer, 400); // defaults to 100ms
  const forceUpdate = useForceUpdate();
  // Get questions from firebase realtime database
 

  [isRunning, setIsRunning] = useState();
  [region, setRegion] = useState({
    latitude: 37.78825,
    longitude: -122.4324,
    latitudeDelta: 0.0922,
    longitudeDelta: 0.0421,
  });

  [position, setPosition] = useState({
    latitude: 0,
    longitude: 0,
  });

  [voiceRunning, setVoice] = useState(true);
  [isDialogVisible, setDialog] = useState(false);
  [modalVisible, setVisible] = useState(false);
  [modalInfo, setModalInfo] = useState({name:'', content: []});
  [surveyAnswers, setAnswers] = useState(surveys);
  [select, setSelect] = useState(0)

  
 

  Voice.onSpeechStart = e => {
    //Invoked when .start() is called without error
    //console.log("Speech Starting")
    oldPhrase = "";
    oldTime = "";
  };

  Voice.onSpeechEnd = e => {
    //Invoked when SpeechRecognizer stops recognition
    //console.log('Speech End', e);
  };

  Voice.onSpeechError = e => {
    //Invoked when an error occurs. 
    console.log('onSpeechError: ', e);
  };

  Voice.onSpeechResults = e => {
    let now = new Date().getTime()
    let mins = new Date().getMinutes()
    let secs = new Date().getSeconds()
    if (mins < 10) {
      mins = "0" + mins
    }
    if (secs < 10 ) {
      secs = "0" + secs
    }
    nowReadable = new Date().getHours() + ':' + mins + ":" + secs

    let phrase = String(e.value)
    if ((now - oldTime) > 3000) { 
      // at least 3 second difference between saying things
        edited = phrase.replace(oldPhrase, "")
        oldPhrase = phrase
        oldTime = now
    } else {
         edited = phrase
    }

    let myMemo = {
      "coordinate": {latitude: position.latitude, longitude:position.longitude},
      "timestamp": String(now),
      "readableTime": nowReadable,
      "memo" : edited,
    }
    voice.push(myMemo);
    myMarkers.push(myMemo)
    console.log(myMemo)
  }

  _startRecognizing = async () => {
    //Starts listening for speech for a specific locale
    try {
      await Voice.start('en-US');
    } catch (e) {
      console.error(e);
    }
  };

  _stopRecognizing = async () => {
    //Stops listening for speech
    try {
      await Voice.cancel();
      //console.log("Stopped")
    } catch (e) {
      //eslint-disable-next-line
      console.error(e);
    }
  };

  const addMarker = (phrase) => {
    setDialog(false)
    let now = new Date().getTime()
    let mins = new Date().getMinutes()
    let secs = new Date().getSeconds()
    if (mins < 10) {
      mins = "0" + mins
    }
    if (secs < 10 ) {
      secs = "0" + secs
    }
    nowReadable = new Date().getHours() + ':' + mins + ":" + secs
    let myMemo = {
      "coordinate": {latitude: position.latitude, longitude:position.longitude},
      "timestamp": String(now),
      "readableTime": nowReadable,
      "memo" : phrase,
    }
    voice.push(myMemo);
    myMarkers.push(myMemo)

  }

  useEffect(() => {
    const watchId = Geolocation.watchPosition(
      pos => {
        //console.log("really " + pos.coords.longitude)
        setPosition(pos.coords)
        if (isRunning) {
          gps.push({timestamp: pos.timestamp, coordinates: pos.coords});
          coordsArr = [
            {
              longitude: pos.coords.longitude,
              latitude: pos.coords.latitude,
            },
            ...coordsArr,
          ];
        }
        //console.log("position " + position.longitude)
        //console.log("reegion " + region.longitude)
        setRegion({
          longitude: pos.coords.longitude,
          latitude: pos.coords.latitude,
          latitudeDelta: 0.00922,
          longitudeDelta: 0.00421,
        });
      },
      e => console.log(e.message),
      {
        timeout: 20000,
        enableHighAccuracy: true,
        maximumAge: 0,
        distanceFilter: 0.1,
      },
    );
    return () => Geolocation.clearWatch(watchId);
  }, [isRunning]);

  const playPause = () => {
    toggleMeasurements(isRunning, voiceRunning, myRide);
    setIsRunning(!isRunning);
    BackgroundTimer.stopBackgroundTimer(); 
    //setVoice(!voiceRunning);
  };
  const playPauseVoice = () => {
    if (!voiceRunning) {
      setVoice(true)
      _startRecognizing()
    } else {
      setVoice(false)
      _stopRecognizing()
    }
    console.log(voiceRunning)
    
  };

  const onValueChangeType= (answer, index) => {
    // Update the document title using the browser API
      updated = modalInfo.content
      updated[index].userAnswer = answer
      updatedAnswers = surveyAnswers
      console.log(updatedAnswers)
      console.log(modalInfo)
      console.log(modalInfo.num)
      updatedAnswers[modalInfo.num]["content"] = updated
      setModalInfo({name: modalInfo.name, num: modalInfo.num, content:updated})
      setAnswers(updatedAnswers)
      console.log(updatedAnswers)
    }

  const setSurveysUp = () => {
    half = surveyAnswers
    half.unshift(post[0])
    setAnswers(half)
  }

  return (
    <View style={styles.container}>
    <View style={styles.topbuttonContainer}>
      <TouchableOpacity style={styles.surveyButton} onPress={() => setDialog(true)}><Text>Add Note/Marker</Text></TouchableOpacity>
      <Text>Take Surveys:</Text>
        <View style={styles.tabs}>
          {surveys.map((survey, i) => (
            <TouchableOpacity style={styles.surveyButton} onPress={() => [setVisible(true), setModalInfo(survey), console.log(survey)]}>
              <Text>{survey.name}</Text>
            </TouchableOpacity>
          ))}
          
        </View>
    </View>
      <DialogInput isDialogVisible={isDialogVisible}
            title={"Add Marker to Current Location"}
            message={"Add note about ride"}
            hintInput ={"type description here"}
            submitInput={ (inputText) => {addMarker(inputText)} }
            closeDialog={ () => {setDialog(false)}}>
      </DialogInput>
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
      <MapView 
        style={styles.map} 
        showsUserLocation={ true }
        zoomEnabled={true}
        region={region}> 
        <Polyline
          coordinates={coordsArr}
          strokeColor="#000" // fallback for when `strokeColors` is not supported by the map-provider
          // strokeColors={[
          //   '#7F0000',
          //   '#00000000', // no color, creates a "long" gradient between the previous and next coordinate
          //   '#B24112',
          //   '#E5845C',
          //   '#238C23',
          //   '#7F0000',
          // ]}
          strokeWidth={6}
        />
        {myMarkers.map(marker => (
          <Marker
            coordinate={marker.coordinate}
            title={marker.memo}
            description={marker.readableTime}
          />
        ))}
      </MapView>
      

      <View style={styles.buttonContainer}>
        <TouchableOpacity
          onPress={() => setIsRunning(!isRunning)}
          style={[
            styles.button,
            isRunning === true ? styles.clickedButton : styles.unClickedButton,
          ]}>
          <Text style={styles.text}>
            {isRunning === true ? 'pause ride' : 'start ride'}
          </Text>
        </TouchableOpacity>
        <TouchableOpacity
          onPress={playPauseVoice}
          style={[
            styles.button,
            voiceRunning === true ? styles.clickedButton : styles.unClickedButton,
          ]}>
          <Text style={styles.text}>
            {voiceRunning === true ? 'Turn Voice Recording Off' : 'Turn Voice Recording On'}
          </Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[styles.button, styles.submit]}
          onPress={() => {
            //submitMeasures(isRunning, myRide);
            if (isRunning) {
              console.log("turning off ride")
              setIsRunning(false)
              setVoice(false)
              toggleMeasurements(isRunning, voiceRunning);
            }
            setSurveysUp();
            navigate('Results', {name: name, level: level, mag: mag, gps: gps, gyro: gyro, bar: bar, voice: voice, acc: acc, surveyAnswers: surveyAnswers});
          }}>
          <Text style={styles.text}>send to database</Text>
        </TouchableOpacity>
        
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  map: {
    flex: 1,
  },
  topbuttonContainer: {
    justifyContent: 'center',
    paddingHorizontal: 30,
    alignSelf: 'center',
 
  },
  buttonContainer: {
    position: 'absolute',
    justifyContent: 'center',
    paddingHorizontal: 30,
    alignSelf: 'center',
    bottom: 50,
  },
  text: {
    fontSize: 15,
    color: Colors.white,
  },
  clickedButton: {
    backgroundColor: '#72574a',
  },
  unClickedButton: {
    backgroundColor: '#4A6572',
  },
  submit: {
    marginTop: 10,
    backgroundColor: '#F9AA33',
  },
  button: {
    alignItems: 'center',
    paddingHorizontal: 30,
    paddingVertical: 20,
    marginVertical: 5,
    borderRadius: 8,
    textAlign: 'center',
  },
  surveyButton:{
    textAlign: 'center',
    paddingHorizontal: 10,
    paddingVertical: 10,
    borderRadius: 8,
    backgroundColor: '#F9AA33',
  },
  tabs: {
    alignSelf: 'center',
    flexDirection: "row",
    justifyContent: "space-between",
    height:40,

  },
  instructions: {
    textAlign: 'center',
    color: '#333333',
    marginBottom: 5,
  },
  sectionTitle: {
    fontSize: 25,
  }
});

export default InRide;


