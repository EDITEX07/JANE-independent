
import { auth, db } from "./firebase.js";

import {
    createUserWithEmailAndPassword,
    signInWithEmailAndPassword,
    signOut,
    onAuthStateChanged
} from "https://www.gstatic.com/firebasejs/11.10.0/firebase-auth.js";

import {
    collection,
    addDoc,
    query,
    orderBy,
    onSnapshot,
    serverTimestamp
} from "https://www.gstatic.com/firebasejs/11.10.0/firebase-firestore.js";

// J.A.N.E. backend address will be added after deployment.
const API_URL = "YOUR_BACKEND_URL/chat";

const welcome = document.getElementById("welcomeScreen");
const messages = document.getElementById("chatMessages");
const input = document.getElementById("messageInput");
const sendButton = document.getElementById("sendButton");
const modeSelector = document.getElementById("modeSelector");
const sidebar = document.getElementById("sidebar");

let currentUser = null;
let stopMessagesListener = null;
let sending = false;

// Sidebar
document.getElementById("menuButton").addEventListener("click", () => {
    sidebar.classList.toggle("open");
});

// Login interface
function showLogin() {
    welcome.innerHTML = `
        <div class="welcome-logo">J</div>
        <h2>Welcome to J.A.N.E.</h2>
        <p>Sign in to access your AI workspace.</p>

        <div class="login-box">
            <input id="emailInput" type="email"
                placeholder="Email address" autocomplete="email">

            <input id="passwordInput" type="password"
                placeholder="Password" autocomplete="current-password">

            <button id="loginButton">Sign In</button>
            <button id="signupButton">Create Account</button>

            <p id="authStatus"></p>
        </div>
    `;

    document.getElementById("loginButton").onclick = () => authenticate(false);
    document.getElementById("signupButton").onclick = () => authenticate(true);
}

async function authenticate(createAccount) {
    const email = document.getElementById("emailInput").value.trim();
    const password = document.getElementById("passwordInput").value;
    const status = document.getElementById("authStatus");

    if (!email || !password) {
        status.textContent = "Enter your email and password.";
        return;
    }

    status.textContent = "Please wait...";

    try {
        if (createAccount) {
            await createUserWithEmailAndPassword(auth, email, password);
        } else {
            await signInWithEmailAndPassword(auth, email, password);
        }
    } catch (error) {
        status.textContent = error.message;
    }
}

// Chat interface
function showWorkspace() {
    welcome.innerHTML = `
        <div class="welcome-logo">J</div>
        <h2>Welcome to J.A.N.E.</h2>
        <p>Your AI workspace is ready.</p>
        <p id="userEmail"></p>
        <button id="logoutButton">Sign Out</button>
    `;

    document.getElementById("userEmail").textContent = currentUser.email;

    document.getElementById("logoutButton").onclick = async () => {
        await signOut(auth);
    };
}

function addMessage(text, sender) {
    const element = document.createElement("div");
    element.className = `message ${sender}`;
    element.textContent = text;
    messages.appendChild(element);
    messages.scrollTop = messages.scrollHeight;
}

function loadMessages() {
    if (stopMessagesListener) {
        stopMessagesListener();
    }

    messages.innerHTML = "";

    const messageQuery = query(
        collection(db, "users", currentUser.uid, "messages"),
        orderBy("createdAt", "asc")
    );

    stopMessagesListener = onSnapshot(messageQuery, snapshot => {
        messages.innerHTML = "";

        snapshot.forEach(documentSnapshot => {
            const data = documentSnapshot.data();
            addMessage(data.text, data.sender);
        });
    }, error => {
        console.error("Message loading error:", error);
        addMessage("Unable to load saved messages. Check Firestore permissions.", "assistant");
    });
}

// Send a message
async function sendMessage() {
    const text = input.value.trim();

    if (!text || sending || !currentUser) return;

    if (API_URL.includes("YOUR_BACKEND_URL")) {
        addMessage("The Python backend is not connected yet. We'll connect it after deployment.", "assistant");
        return;
    }

    sending = true;
    input.value = "";
    sendButton.disabled = true;

    try {
        await addDoc(
            collection(db, "users", currentUser.uid, "messages"),
            {
                text,
                sender: "user",
                createdAt: serverTimestamp()
            }
        );

        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${await currentUser.getIdToken()}`
            },
            body: JSON.stringify({
                message: text,
                mode: modeSelector.value
            })
        });

        if (!response.ok) {
            throw new Error(`Backend error: ${response.status}`);
        }

        const result = await response.json();

        await addDoc(
            collection(db, "users", currentUser.uid, "messages"),
            {
                text: result.reply || "J.A.N.E. returned an empty response.",
                sender: "assistant",
                createdAt: serverTimestamp()
            }
        );

    } catch (error) {
        console.error(error);
        addMessage("J.A.N.E. couldn't complete that request. Please try again.", "assistant");
    } finally {
        sending = false;
        sendButton.disabled = false;
        input.focus();
    }
}

sendButton.addEventListener("click", sendMessage);

input.addEventListener("keydown", event => {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
});

// Authentication state
onAuthStateChanged(auth, user => {
    currentUser = user;

    if (user) {
        showWorkspace();
        loadMessages();
    } else {
        if (stopMessagesListener) {
            stopMessagesListener();
            stopMessagesListener = null;
        }

        messages.innerHTML = "";
        showLogin();
    }
});
