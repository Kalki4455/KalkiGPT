import sqlite3
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from pypdf import PdfReader
import speech_recognition as sr
import os

# ==========================
# CONFIG
# ==========================

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

st.set_page_config(
    page_title="KalkiGPT",
    page_icon="🤖",
    layout="wide"
)

# ==========================
# FUNCTIONS
# ==========================

def listen():
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:

            st.info("🎤 Speak Now...")

            recognizer.adjust_for_ambient_noise(
                source,
                duration=1
            )

            audio = recognizer.listen(
                source,
                timeout=10,
                phrase_time_limit=10
            )

        text = recognizer.recognize_google(audio)

        return text

    except Exception as e:

        st.error(f"Voice Error: {e}")

        return ""

# ==========================
# SIDEBAR
# ==========================

with st.sidebar:

    st.title("🤖 KalkiGPT")

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"]
    )

    if st.button("🗑 Clear Chat"):

        st.session_state.messages = []

        if "chat" in st.session_state:
            del st.session_state.chat

        st.rerun()

# ==========================
# PDF
# ==========================

pdf_text = ""

if uploaded_file:

    pdf = PdfReader(uploaded_file)

    for page in pdf.pages:

        text = page.extract_text()

        if text:
            pdf_text += text + "\n"

# ==========================
# CHAT SESSION
# ==========================

if "chat" not in st.session_state:

    st.session_state.chat = (
        model.start_chat(history=[])
    )

if "messages" not in st.session_state:

    st.session_state.messages = []

# ==========================
# UI
# ==========================

st.title("🤖 KalkiGPT")

st.caption(
    "AI Chatbot + PDF Chat + Voice Input"
)

# Display old messages

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        st.markdown(
            msg["content"]
        )

# ==========================
# VOICE BUTTON
# ==========================

if st.button("🎤 Voice Input"):

    voice_text = listen()

    if voice_text:

        st.success(
            f"You said: {voice_text}"
        )

        st.session_state.voice_prompt = (
            voice_text
        )

# ==========================
# TEXT INPUT
# ==========================

prompt = st.chat_input(
    "Ask anything..."
)

if "voice_prompt" in st.session_state:

    prompt = st.session_state.voice_prompt

    del st.session_state.voice_prompt

# ==========================
# PROCESS
# ==========================

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):

        st.markdown(prompt)

    try:

        if pdf_text:

            full_prompt = f"""
Use the following PDF content to answer.

PDF:
{pdf_text}

Question:
{prompt}
"""

        else:

            full_prompt = prompt

        response = (
            st.session_state.chat
            .send_message(full_prompt)
        )

        answer = response.text

        with st.chat_message(
            "assistant"
        ):
            st.markdown(answer)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

    except Exception as e:

        st.error(
            f"Error: {e}"
        )