import React, {useEffect} from 'react';
import {StyleSheet, Text, View, Linking} from 'react-native';
import qs from 'qs';
import config from '../../../config.js';

function OAuth(client_id, cb, setFitbit) {
  Linking.addEventListener('url', handleUrl);
  function handleUrl(event) {
    // console.log(event.url);
    Linking.removeEventListener('url', handleUrl);
    const [, query_string] = event.url.match(/\#(.*)/);
    // console.log(query_string);
    const query = qs.parse(query_string);
    // console.log(`query: ${JSON.stringify(query)}`);
    cb(query.access_token, setFitbit);
  }
  const oauthurl = `https://www.fitbit.com/oauth2/authorize?${qs.stringify({
    client_id,
    response_type: 'token',
    scope: 'heartrate activity activity profile sleep',
    redirect_uri: 'wjmy://',
    expires_in: '31536000',
  })}`;
  // console.log(oauthurl);
  Linking.openURL(oauthurl).catch(err =>
    console.error('Error processing linking', err),
  );
}
function getData(access_token, setFitbit) {
  fetch('https://api.fitbit.com/1/user/-/activities/heart/date/today/1d.json', {
    method: 'GET',
    headers: {
      Authorization: `Bearer ${access_token}`,
    },
    // body: `root=auto&path=${Math.random()}`
  })
    .then(res => res.json())
    .then(res => {
      setFitbit(res);
    })
    .catch(err => {
      console.error('Error: ', err);
    });
}
const getFitbitData = setFitbit => {
  OAuth(config.client_id, getData, setFitbit);
};

export default getFitbitData;
