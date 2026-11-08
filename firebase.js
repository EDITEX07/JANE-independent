
import { initializeApp } from "https://www.gstatic.com/firebasejs/11.10.0/firebase-app.js";

import {
    getAuth
} from "https://www.gstatic.com/firebasejs/11.10.0/firebase-auth.js";

import {
    getFirestore
} from "https://www.gstatic.com/firebasejs/11.10.0/firebase-firestore.js";

const firebaseConfig = {
    apiKey: "AIzaSyC833RXl0kY5x5bkwrRs9QBB_kA08eTzDA",
    authDomain: "jane-18f44.firebaseapp.com",
    projectId: "jane-18f44",
    storageBucket: "jane-18f44.firebasestorage.app",
    messagingSenderId: "898297641037",
    appId: "1:898297641037:web:d1f393fa49ef6e42c18404"
};

const app = initializeApp(firebaseConfig);

export const auth = getAuth(app);
export const db = getFirestore(app);
