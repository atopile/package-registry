// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getFunctions, connectFunctionsEmulator } from 'firebase/functions';
import { getDatabase, connectDatabaseEmulator } from 'firebase/database';
import { getStorage } from 'firebase/storage';
import { getFirestore } from "firebase/firestore";


// Your web app's Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyDFIscZoJ6jdP6iBhQTdTG2GTbHMVJB3oA",
    authDomain: "atopile.firebaseapp.com",
    projectId: "atopile",
    storageBucket: "atopile.appspot.com",
    messagingSenderId: "307706174757",
    appId: "1:307706174757:web:9c811734aefbedac500ecc",
    measurementId: "G-SLN8XZ30VX"
};
// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize services
const database = getDatabase(app);
const functions = getFunctions(app);
const storage = getStorage(app);
const db = getFirestore(app);

export { db };

// Connect to Firebase emulators in development environment
if (process.env.NODE_ENV === 'development') {
    connectDatabaseEmulator(database, 'localhost', 9000);
    connectFunctionsEmulator(functions, 'localhost', 5001);
}

// Export the Firebase services you want to use
export { database, functions, storage };