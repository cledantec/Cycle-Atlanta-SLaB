import firebase from '@react-native-firebase/app';
import database from '@react-native-firebase/database';

const surveyHelper = {
    InRide: function() {
        inRide = []
        try {
            database().ref("Surveys").once('value', function (snapshot) {
                const events = snapshot.val()
                console.log("snapshot value: ")
                console.log(events)
                const keys = Object.keys(events)
                let orderPushed = 0;
                for (let i = 0; i < keys.length; i++) {
                    const currSurvey = events[keys[i]]
                    if (keys[i]=== 'Post Ride') {
                        console.log('ignoring')
                    } else {
                        mySurvey = {
                            name: keys[i],
                            content: [],
                            num: orderPushed,
                        }
                        orderPushed = orderPushed + 1
                        const newKeys = Object.keys(currSurvey)
                        for (let j = 0; j < newKeys.length; j++) {
                            const currItem = currSurvey[newKeys[j]]
                            let myKey = "item" + j
                            myItem = {
                                id: myKey,
                                question: currItem["Question"],
                                userAnswer: null
                            }
                            if (currItem["Answers"]){
                                myItem['answers'] = currItem["Answers"].split(',')
                            } else if (currItem["Answer"]){
                                myItem['answers'] = currItem["Answer"].split(',')
                            } else if (currItem["answer"]){
                                myItem['answers'] = currItem["answer"].split(',')
                            } else if (currItem["answer"]){
                                myItem['answers'] = currItem["answer"].split(',')
                            } else {
                                myItem['answers'] = 'none'
                            }
                            
                            mySurvey.content.push(myItem)
                        }
                        inRide.push(mySurvey)
                    }
                }
            })
        } finally {
            console.log("Cannot get data from Firebase")
        }
        
        return inRide;
    },
    PostRide: function() {
        postRide = []
        try {
            database().ref("Surveys").once('value', function (snapshot) {
                const events = snapshot.val()
                console.log("snapshot value: ")
                console.log(events)
                const keys = Object.keys(events)
                let orderPushed = 0;
                for (let i = 0; i < keys.length; i++) {
                    const currSurvey = events[keys[i]]
                    if (keys[i]=== 'Post Ride') {
                        mySurvey = {
                            name: keys[i],
                            content: [],
                            num: 0,
                        }
                        const newKeys = Object.keys(currSurvey)
                        for (let j = 0; j < newKeys.length; j++) {
                            const currItem = currSurvey[newKeys[j]]
                            let myKey = "item" + j
                            myItem = {
                                id: myKey,
                                question: currItem["Question"],
                                userAnswer: null
                            }
                            if (currItem["Answers"]){
                                myItem['answers'] = currItem["Answers"].split(',')
                            } else if (currItem["Answer"]){
                                myItem['answers'] = currItem["Answer"].split(',')
                            } else if (currItem["answer"]){
                                myItem['answers'] = currItem["answer"].split(',')
                            } else if (currItem["answer"]){
                                myItem['answers'] = currItem["answer"].split(',')
                            } else {
                                myItem['answers'] = 'none'
                            }
                            
                            mySurvey.content.push(myItem)
                        }
                        postRide.push(mySurvey)
                    } else {
                        console.log('ignoring')
                        orderPushed = orderPushed + 1
                        
                    }
                }
            })
        } finally {
            console.log("Cannot get data from Firebase")
        }
        
        return postRide;
    }

}
export default surveyHelper;


