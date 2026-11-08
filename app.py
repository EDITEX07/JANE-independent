
import os
import json
import base64
import logging

import firebase_admin
from firebase_admin import auth as firebase_auth
from firebase_admin import credentials

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from google import genai
from openai import OpenAI


# --------------------------------------------------
# J.A.N.E. BACKEND — VERSION 1.02
# --------------------------------------------------

APP_NAME = "J.A.N.E."
APP_VERSION = "1.02"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("jane")

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="J.A.N.E. independent AI backend"
)

# Only allow the J.A.N.E. GitHub Pages website.
ALLOWED_ORIGINS = [
    "https://editex07.github.io",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)


# --------------------------------------------------
# ENVIRONMENT SETTINGS
# --------------------------------------------------

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash"
)

OPENAI_MODEL = os.getenv(
    "OPENAI_MODEL",
    "gpt-4.1-mini"
)

FIREBASE_SERVICE_ACCOUNT_JSON = os.getenv(
    "FIREBASE_SERVICE_ACCOUNT_JSON",
    ""
)

FIREBASE_SERVICE_ACCOUNT_BASE64 = os.getenv(
    "FIREBASE_SERVICE_ACCOUNT_BASE64",
    ""
)


# --------------------------------------------------
# FIREBASE ADMIN INITIALIZATION
# --------------------------------------------------

firebase_ready = False

def initialize_firebase():
    global firebase_ready

    if firebase_ready:
        return

    try:
        if firebase_admin._apps:
            firebase_ready = True
            return

        service_account_data = None

        if FIREBASE_SERVICE_ACCOUNT_BASE64:
            decoded = base64.b64decode(
                FIREBASE_SERVICE_ACCOUNT_BASE64
            ).decode("utf-8")

            service_account_data = json.loads(decoded)

        elif FIREBASE_SERVICE_ACCOUNT_JSON:
            service_account_data = json.loads(
                FIREBASE_SERVICE_ACCOUNT_JSON
            )

        else:
            logger.error(
                "Firebase service account credentials are missing."
            )
            return

        certificate = credentials.Certificate(
            service_account_data
        )

        firebase_admin.initialize_app(certificate)

        firebase_ready = True
        logger.info("Firebase Admin initialized.")

    except Exception:
        logger.exception("Firebase initialization failed.")
        firebase_ready = False


initialize_firebase()


# --------------------------------------------------
# AI CLIENTS
# --------------------------------------------------

gemini_client = None
openai_client = None

if GEMINI_API_KEY:
    try:
        gemini_client = genai.Client(
            api_key=GEMINI_API_KEY
        )
    except Exception:
        logger.exception("Gemini client initialization failed.")

if OPENAI_API_KEY:
    try:
        openai_client = OpenAI(
            api_key=OPENAI_API_KEY,
            timeout=45.0,
            max_retries=1
        )
    except Exception:
        logger.exception("OpenAI client initialization failed.")


# --------------------------------------------------
# REQUEST MODEL
# --------------------------------------------------

class ChatRequest(BaseModel):
    message: str = Field(
        min_length=1,
        max_length=12000
    )

    mode: str = Field(
        default="Adaptive",
        max_length=30
    )


# --------------------------------------------------
# J.A.N.E. INTELLIGENCE MODES
# --------------------------------------------------

SYSTEM_PROMPTS = {
    "General": """
You are J.A.N.E., Judicial Analytical and Neuroresearch Engine.

Be friendly, clear, direct and helpful.
Explain difficult topics in simple language.
Avoid unnecessary technical language.
""",

    "Adaptive": """
You are J.A.N.E., Judicial Analytical and Neuroresearch Engine.

Adapt your response to the user's task.
For simple questions, be concise.
For complex questions, reason carefully and explain the
important steps and conclusions.
Be accurate, structured and practical.
Clearly mention uncertainty when information is incomplete.
""",

    "Thinker": """
You are J.A.N.E., Judicial Analytical and Neuroresearch Engine.

Use a careful analytical approach.
Break complex problems into smaller parts.
Consider assumptions, alternatives, risks and limitations.
Provide a clear conclusion and explain the reasoning
without revealing private chain-of-thought.
Do not invent facts or sources.
"""
}


def get_system_prompt(mode):
    selected_mode = mode.strip()

    if selected_mode not in SYSTEM_PROMPTS:
        selected_mode = "Adaptive"

    return SYSTEM_PROMPTS[selected_mode]


# --------------------------------------------------
# FIREBASE TOKEN VERIFICATION
# --------------------------------------------------

def verify_user_token(authorization):
    if not firebase_ready:
        raise HTTPException(
            status_code=503,
            detail="Firebase authentication is not configured."
        )

    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authentication token is required."
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization format."
        )

    token = authorization.split(" ", 1)[1].strip()

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Authentication token is empty."
        )

    try:
        decoded_token = firebase_auth.verify_id_token(
            token,
            check_revoked=True
        )

        return decoded_token["uid"]

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Your session is invalid or expired. Please sign in again."
        )


# --------------------------------------------------
# GEMINI RESPONSE
# --------------------------------------------------

def generate_with_gemini(message, system_prompt):
    if not gemini_client:
        raise RuntimeError("Gemini is not configured.")

    response = gemini_client.models.generate_content(
        model=GEMINI_MODEL,
        contents=message,
        config={
            "system_instruction": system_prompt,
            "temperature": 0.7,
            "max_output_tokens": 4096
        }
    )

    answer = response.text

    if not answer or not answer.strip():
        raise RuntimeError("Gemini returned an empty response.")

    return answer.strip()


# --------------------------------------------------
# OPENAI RESPONSE
# --------------------------------------------------

def generate_with_openai(message, system_prompt):
    if not openai_client:
        raise RuntimeError("OpenAI is not configured.")

    response = openai_client.responses.create(
        model=OPENAI_MODEL,
        instructions=system_prompt,
        input=message,
        max_output_tokens=4096
    )

    answer = response.output_text

    if not answer or not answer.strip():
        raise RuntimeError("OpenAI returned an empty response.")

    return answer.strip()


# --------------------------------------------------
# DUAL AI ROUTER
# --------------------------------------------------

def generate_jane_response(message, mode):
    system_prompt = get_system_prompt(mode)

    failures = []

    # First attempt: Gemini
    if gemini_client:
        try:
            answer = generate_with_gemini(
                message,
                system_prompt
            )

            return answer, "Gemini"

        except Exception as error:
            logger.warning(
                "Gemini request failed: %s",
                type(error).__name__
            )

            failures.append("Gemini unavailable")

    # Second attempt: OpenAI
    if openai_client:
        try:
            answer = generate_with_openai(
                message,
                system_prompt
            )

            return answer, "OpenAI"

        except Exception as error:
            logger.error(
                "OpenAI request failed: %s",
                type(error).__name__
            )

            failures.append("OpenAI unavailable")

    if not gemini_client and not openai_client:
        raise HTTPException(
            status_code=503,
            detail="No AI provider is configured."
        )

    raise HTTPException(
        status_code=502,
        detail="Both AI providers failed. Please try again later."
    )


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "application": APP_NAME,
        "version": APP_VERSION,
        "status": "online"
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "firebase": firebase_ready,
        "gemini": gemini_client is not None,
        "openai": openai_client is not None
    }


# --------------------------------------------------
# MAIN CHAT ENDPOINT
# --------------------------------------------------

@app.post("/chat")
def chat(
    request: ChatRequest,
    authorization: str = Header(default=None)
):
    # Verify the signed-in Firebase user.
    user_id = verify_user_token(authorization)

    message = request.message.strip()

    if not message:
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty."
        )

    # Generate response using Gemini with OpenAI fallback.
    reply, provider = generate_jane_response(
        message,
        request.mode
    )

    logger.info(
        "Response generated for authenticated user."
    )

    return {
        "reply": reply,
        "provider": provider,
        "mode": request.mode,
        "version": APP_VERSION
    }


# --------------------------------------------------
# STARTUP INFORMATION
# --------------------------------------------------

@app.on_event("startup")
def startup_event():
    logger.info("%s backend starting.", APP_NAME)

    if not firebase_ready:
        logger.warning("Firebase is not configured.")

    if not gemini_client:
        logger.warning("Gemini is not configured.")

    if not openai_client:
        logger.warning("OpenAI is not configured.")
