
import firebase from '@react-native-firebase/app';
//import database from '@react-native-firebase/database';

const helpers = {
    // Setting up firebase survey with code not manually:
    setUpSurvey: function() {
        firebase.database().ref("Surveys").set({
      "Pre_ride":{"Item1": 
                          {"Question1":"Type question 1 here",
                          "Answer1": {"a":"Type option a here", 
                                      "b":"Type option b here", 
                                      "c":"Type option c here",
                                      "d":"Type option d here" }
                          },
                  "Item2": 
                          {"Question2":"Type question 2 here",
                          "Answer2": {"a":"Type option a here", 
                                      "b":"Type option b here", 
                                      "c":"Type option c here",
                                      "d":"Type option d here" }
                          }
                  },
      "mid_ride1":{"Item1": 
                          {"Question1":"Type question 1 here",
                          "Answer1": {"a":"Type option a here", 
                                      "b":"Type option b here", 
                                      "c":"Type option c here",
                                      "d":"Type option d here" }
                          },
                  "Item2": 
                      {"Question2":"Type question 2 here",
                      "Answer2": {"a":"Type option a here", 
                                  "b":"Type option b here", 
                                  "c":"Type option c here",
                                  "d":"Type option d here" }
                      }
                  },
      "End_of_ride":{"Item1": 
                      {"Question1":"Type question 1 here",
                      "Answer1": {"a":"Type option a here", 
                                  "b":"Type option b here", 
                                  "c":"Type option c here",
                                  "d":"Type option d here" }
                      },
                    "Item2": 
                      {"Question2":"Type question 2 here",
                      "Answer2": {"a":"Type option a here", 
                                  "b":"Type option b here", 
                                  "c":"Type option c here",
                                  "d":"Type option d here" }
                      }
                    }  
      })
    },
}
export default helpers;