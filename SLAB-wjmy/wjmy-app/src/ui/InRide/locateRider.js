import {useState, useEffect} from 'react';
import Geolocation from '@react-native-community/geolocation';

export const useGeolocation = () => {
  const [error, setError] = useState('');
  const [position, setPosition] = useState({
    latitude: 0,
    longitude: 0,
  });

  useEffect(() => {
    const watchId = Geolocation.watchPosition(
      pos => {
        setError('');
        setPosition({
          latitude: pos.coords.latitude,
          longitude: pos.coords.longitude,
        });
      },
      e => setError(e.message),
    );
    return () => Geolocation.clearWatch(watchId);
  }, []);

  return [error, position];
};
