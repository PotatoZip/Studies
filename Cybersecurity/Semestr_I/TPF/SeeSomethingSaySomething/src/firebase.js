import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';


const firebaseConfig = {
  apiKey: "AIzaSyBZ8P8QDm5fMw1iPDV4QZRGajxxTZo5vgk",
  authDomain: "seesomethingsaysomething-7a244.firebaseapp.com",
  projectId: "seesomethingsaysomething-7a244",
  storageBucket: "seesomethingsaysomething-7a244.firebasestorage.app",
  messagingSenderId: "412827813964",
  appId: "1:412827813964:web:2332e57dd45796c6274ce9",
  measurementId: "G-L81Z6QBEY2"
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
