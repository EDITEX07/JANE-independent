
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Orbitron:wght@500;600;700;800;900&display=swap');

:root {
    --bg: #08080b;
    --panel: #0e0d13;
    --panel-light: #15121a;
    --red: #ff465c;
    --red-dark: #a10f2b;
    --text: #f4f1f5;
    --muted: #a49ba8;
    --border: rgba(255, 70, 92, 0.19);
    --glow: rgba(255, 36, 61, 0.35);
}

* {
    box-sizing: border-box;
}

html, body {
    margin: 0;
    min-height: 100%;
    background: var(--bg);
    color: var(--text);
    font-family: Inter, sans-serif;
}

body {
    min-height: 100vh;
    overflow: hidden;
}

button, input, textarea, select {
    font: inherit;
}

button {
    cursor: pointer;
}

.app {
    display: flex;
    flex-direction: column;
    height: 100vh;
    min-height: 100vh;
    background:
        radial-gradient(ellipse at 50% 0%, #29101b 0%, #130d14 38%, #08080b 78%);
}

/* TOP BAR */

.topbar {
    height: 76px;
    min-height: 76px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 24px;
    background: rgba(8, 8, 11, 0.88);
    border-bottom: 1px solid var(--border);
    backdrop-filter: blur(16px);
    z-index: 5;
}

.brand {
    display: flex;
    align-items: center;
    gap: 13px;
}

.brand-icon {
    width: 43px;
    height: 43px;
    display: grid;
    place-items: center;
    border: 1px solid var(--red);
    border-radius: 13px;
    color: var(--red);
    font-family: Orbitron, sans-serif;
    font-size: 27px;
    font-weight: 900;
    box-shadow: 0 0 16px var(--glow), inset 0 0 12px rgba(255, 70, 92, 0.12);
}

.brand h1 {
    margin: 0;
    font-family: Orbitron, sans-serif;
    font-size: 21px;
    letter-spacing: 3px;
    color: #fff;
    text-shadow: 0 0 12px var(--glow);
}

.brand span {
    display: block;
    margin-top: 4px;
    color: var(--muted);
    font-size: 9px;
    letter-spacing: 1.1px;
}

.menu-button {
    width: 42px;
    height: 42px;
    border: 1px solid var(--border);
    border-radius: 12px;
    background: var(--panel-light);
    color: var(--red);
    font-size: 21px;
}

/* SIDEBAR */

.sidebar {
    position: fixed;
    top: 76px;
    bottom: 0;
    left: 0;
    width: 265px;
    padding: 20px 15px;
    display: flex;
    flex-direction: column;
    gap: 15px;
    background: rgba(10, 9, 14, 0.98);
    border-right: 1px solid var(--border);
    transform: translateX(-105%);
    transition: transform 0.28s ease;
    z-index: 10;
}

.sidebar.open {
    transform: translateX(0);
}

#newChatButton {
    width: 100%;
    padding: 13px;
    border: 1px solid rgba(255, 70, 92, 0.55);
    border-radius: 12px;
    background: linear-gradient(110deg, #a10f2b, #310d19);
    color: white;
    font-weight: 700;
    box-shadow: 0 0 17px rgba(255, 36, 61, 0.12);
}

#chatHistory {
    flex: 1;
    overflow-y: auto;
}

.sidebar-footer {
    padding-top: 14px;
    border-top: 1px solid var(--border);
    color: var(--muted);
    text-align: center;
    font-size: 11px;
    letter-spacing: 1px;
}

/* MAIN WORKSPACE */

.workspace {
    position: relative;
    flex: 1;
    min-height: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px 22px 12px;
    overflow: hidden;
}

.welcome {
    width: 100%;
    flex: 1;
    min-height: 0;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 20px;
}

.welcome-logo {
    position: relative;
    width: 84px;
    height: 84px;
    display: grid;
    place-items: center;
    margin-bottom: 24px;
    border: 1px solid rgba(255, 70, 92, 0.9);
    border-radius: 50%;
    color: var(--red);
    font-family: Orbitron, sans-serif;
    font-size: 49px;
    font-weight: 900;
    text-shadow: 0 0 14px var(--red);
    box-shadow:
        0 0 16px var(--glow),
        inset 0 0 18px rgba(255, 70, 92, 0.2);
    animation: corePulse 2.8s ease-in-out infinite;
}

.welcome-logo::before,
.welcome-logo::after {
    content: "";
    position: absolute;
    inset: -9px;
    border: 1px solid rgba(255, 70, 92, 0.38);
    border-radius: 50%;
    transform: rotateX(65deg);
    animation: coreSpin 8s linear infinite;
}

.welcome-logo::after {
    inset: -15px;
    transform: rotateY(65deg);
    animation-direction: reverse;
}

.welcome h2 {
    margin: 0;
    font-family: Orbitron, sans-serif;
    font-size: clamp(23px, 4vw, 34px);
    letter-spacing: 1px;
    color: #fff;
}

.welcome p {
    margin: 12px 0;
    color: var(--muted);
    font-size: 14px;
    line-height: 1.6;
}

#userEmail {
    font-size: 12px;
    color: var(--red);
}

/* LOGIN */

.login-box {
    width: min(100%, 360px);
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin-top: 18px;
    padding: 22px;
    border: 1px solid var(--border);
    border-radius: 18px;
    background: rgba(17, 14, 21, 0.88);
    box-shadow: 0 0 35px rgba(255, 36, 61, 0.08);
}

.login-box input {
    width: 100%;
    padding: 14px;
    border: 1px solid #39202b;
    border-radius: 10px;
    outline: none;
    background: #0a090e;
    color: white;
}

.login-box input:focus {
    border-color: var(--red);
    box-shadow: 0 0 12px var(--glow);
}

.login-box button,
#logoutButton {
    padding: 13px;
    border: 1px solid var(--red);
    border-radius: 10px;
    background: linear-gradient(110deg, var(--red-dark), #390c1b);
    color: white;
    font-weight: 700;
}

#signupButton {
    background: #17121a;
    border-color: #53303c;
}

#authStatus {
    min-height: 18px;
    margin: 0;
    color: var(--red);
    font-size: 12px;
}

/* CHAT MESSAGES */

.messages {
    width: 100%;
    max-width: 900px;
    flex: 1;
    min-height: 0;
    display: flex;
    flex-direction: column;
    gap: 16px;
    padding: 12px 8px 22px;
    overflow-y: auto;
    scrollbar-width: thin;
    scrollbar-color: #57202e transparent;
}

.message {
    max-width: min(82%, 720px);
    padding: 14px 17px;
    border-radius: 16px;
    font-size: 14px;
    line-height: 1.65;
    white-space: pre-wrap;
    overflow-wrap: anywhere;
    animation: messageAppear 0.2s ease;
}

.message.user {
    align-self: flex-end;
    color: #fff;
    background: linear-gradient(120deg, #94172f, #4b1023);
    border: 1px solid rgba(255, 70, 92, 0.42);
    border-bottom-right-radius: 5px;
}

.message.assistant {
    align-self: flex-start;
    color: #eee9ef;
    background: rgba(22, 19, 27, 0.96);
    border: 1px solid rgba(255, 70, 92, 0.2);
    border-bottom-left-radius: 5px;
}

/* MESSAGE COMPOSER */

.composer {
    width: min(100%, 900px);
    display: flex;
    align-items: flex-end;
    gap: 10px;
    padding: 11px;
    border: 1px solid rgba(255, 70, 92, 0.38);
    border-radius: 18px;
    background: linear-gradient(120deg, #1b1018, #09090d);
    box-shadow: 0 0 24px rgba(255, 36, 61, 0.1);
}

#modeSelector {
    max-width: 112px;
    min-height: 43px;
    padding: 0 8px;
    border: 1px solid #482331;
    border-radius: 11px;
    outline: none;
    background: #100d13;
    color: var(--red);
    font-size: 12px;
}

#messageInput {
    flex: 1;
    min-width: 0;
    min-height: 43px;
    max-height: 150px;
    resize: none;
    padding: 12px 8px;
    border: none;
    outline: none;
    background: transparent;
    color: white;
    font-size: 14px;
}

#messageInput::placeholder {
    color: #827783;
}

#sendButton {
    flex-shrink: 0;
    width: 44px;
    height: 44px;
    display: grid;
    place-items: center;
    border: none;
    border-radius: 50%;
    background: linear-gradient(145deg, #ff5268, #a10f2b);
    color: white;
    font-size: 27px;
    font-weight: 700;
    box-shadow: 0 0 17px rgba(255, 36, 61, 0.35);
    transition: transform 0.2s, filter 0.2s;
}

#sendButton:hover {
    transform: scale(1.06);
    filter: brightness(1.12);
}

#sendButton:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.disclaimer {
    margin: 10px 0 0;
    color: #716873;
    font-size: 10px;
    text-align: center;
}

/* ANIMATIONS */

@keyframes corePulse {
    0%, 100% {
        box-shadow: 0 0 12px var(--glow), inset 0 0 12px rgba(255, 70, 92, 0.15);
    }
    50% {
        box-shadow: 0 0 28px rgba(255, 36, 61, 0.55), inset 0 0 22px rgba(255, 70, 92, 0.3);
    }
}

@keyframes coreSpin {
    from { transform: rotate(0deg) rotateX(65deg); }
    to { transform: rotate(360deg) rotateX(65deg); }
}

@keyframes messageAppear {
    from {
        opacity: 0;
        transform: translateY(7px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* SCROLLBARS */

* {
    scrollbar-width: thin;
    scrollbar-color: #51202d transparent;
}

::-webkit-scrollbar {
    width: 6px;
}

::-webkit-scrollbar-thumb {
    background: #51202d;
    border-radius: 10px;
}

/* MOBILE */

@media (max-width: 600px) {
    .topbar {
        height: 67px;
        min-height: 67px;
        padding: 0 14px;
    }

    .brand-icon {
        width: 38px;
        height: 38px;
        font-size: 23px;
    }

    .brand h1 {
        font-size: 17px;
    }

    .brand span {
        max-width: 225px;
        font-size: 8px;
        letter-spacing: 0.5px;
    }

    .sidebar {
        top: 67px;
        width: min(280px, 85vw);
    }

    .workspace {
        padding: 12px 10px 9px;
    }

    .welcome-logo {
        width: 72px;
        height: 72px;
        font-size: 42px;
    }

    .welcome h2 {
        font-size: 23px;
    }

    .welcome p {
        font-size: 12px;
    }

    .messages {
        padding: 10px 2px 16px;
    }

    .message {
        max-width: 90%;
        padding: 12px 14px;
        font-size: 13px;
    }

    .composer {
        gap: 6px;
        padding: 8px;
        border-radius: 15px;
    }

    #modeSelector {
        max-width: 91px;
        font-size: 11px;
    }

    #messageInput {
        font-size: 13px;
    }

    #sendButton {
        width: 41px;
        height: 41px;
    }
}

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}
