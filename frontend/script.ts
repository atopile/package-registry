// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import {
    connectDatabaseEmulator,
    getDatabase
} from 'firebase/database';
import { connectFunctionsEmulator, getFunctions, httpsCallable } from 'firebase/functions';
import { parse as parseMarkdown } from "marked";

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
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
const cors = require('cors')({origin: true});
// app.use(cors);

const functions = getFunctions();
const database = getDatabase();

// Locally, we use the firebase emulators.
if (window.location.hostname === 'localhost') {
    connectDatabaseEmulator(database, '127.0.0.1', 9040);
    connectFunctionsEmulator(functions, '127.0.0.1', 5001);
}

document.addEventListener('DOMContentLoaded', async function () {
    const container = document.getElementById('packagesList') as HTMLDivElement;
    const packageAPI = httpsCallable(functions, 'list_packages');

    packageAPI().then(function (result) {
        // Read result of the Cloud Function.
        const packages = result.data as [{ name: string, description: string, repo_url: string }];

        packages.forEach(pkg => {
            const card = document.createElement('li');
            card.className = 'package-card';

            card.innerHTML = `
                <div class="package-card-header">
                    <a href="${pkg.repo_url}" target="_blank"><h2>${pkg.name}</h2></a>
                    <pre><code>ato install ${pkg.name}</code></pre>
                </div>
                <p class="readme">${parseMarkdown(pkg.description)}</p>
            `;

            container.appendChild(card);
        });
    }).catch(function (error) {
        console.error('There was an error when calling the Cloud Function', error, error.stack);
    });
});

document.addEventListener('DOMContentLoaded', async function () {
    const form = document.getElementById('submitModuleForm');
    const submitButton = form.querySelector('button[type="submit"]');
    const loadingIcon = document.getElementById('loading');
    const successIcon = document.getElementById('success');

    form.onsubmit = async function (e) {
        e.preventDefault();

        // Hide submit button and show loading icon
        // submitButton.style.display = 'none';
        // loadingIcon.style.display = 'block';

        const formData = new FormData(form);
        const data = {};
        formData.forEach((value, key) => (data[key] = value));

        const packageAPI = httpsCallable(functions, 'add_package');
        console.log(data);

        packageAPI({name: data['name'], repo_url: data['repo_url']}).then(function (result) {
            // loadingIcon.style.display = 'none';
            // successIcon.style.display = 'block';
            {}
        }).catch(function (error) {
            alert('Network error!');
            console.error('There was an error when calling the Cloud Function', error, error.stack);
        }).finally(function () {
            // Hide loading icon
            // loadingIcon.style.display = 'none';
            // NOOP
            {}
        });
    }
});
