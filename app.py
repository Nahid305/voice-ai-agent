"""
AI IT Support Voice Agent – Streamlit UI
=========================================
A two-way, call-centre-style voice agent that:
  1. Greets the caller automatically
  2. Listens until the user stops speaking (VAD)
  3. Transcribes speech → text (faster-whisper)
  4. Generates an AI reply (Groq / Llama-3)
  5. Speaks the reply aloud (gTTS + pygame)
  6. Loops back to step 2 until the user clicks "End Call"
"""

import streamlit as st
import time
import os
from dotenv import load_dotenv

from utils.audio_recorder import record_audio
from utils.speech_to_text import transcribe_audio
from utils.llm_handler import generate_response
from utils.text_to_speech import speak_text

# ── Load .env (GROQ_API_KEY) ───────────────────────────────────────────
load_dotenv()

# ── Page config ─────────────────────────────────────────────────────────
st.set_page_config(page_title="AI IT Support Voice Agent", page_icon="🎧", layout="wide")
st.title("🎧 AI IT Support Voice Agent")
st.markdown("Click **Start Call** to begin a live voice conversation with your AI support agent.")

# ── Session state defaults ──────────────────────────────────────────────
for key, default in [
    ("is_calling", False),
    ("chat_history", []),
    ("ui_messages", []),
    ("needs_greeting", False),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# ── Sidebar ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")
    st.markdown("Make sure your **microphone** is connected.")
    st.markdown("Get a free API key → [console.groq.com](https://console.groq.com/)")

    api_key_input = st.text_input("Groq API Key (optional if in .env)", type="password")
    if api_key_input:
        os.environ["GROQ_API_KEY"] = api_key_input

    st.markdown("---")
    st.markdown("### 🔄 Call Loop")
    st.markdown("1. AI greets you automatically")
    st.markdown("2. Listens until you pause (VAD)")
    st.markdown("3. Transcribes with Faster-Whisper")
    st.markdown("4. AI responds via Groq / Llama-3")
    st.markdown("5. Speaks response via gTTS")

# ── Buttons ─────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)
with col1:
    start_btn = st.button("📞 Start Call", use_container_width=True, type="primary",
                           disabled=st.session_state.is_calling)
with col2:
    end_btn = st.button("📕 End Call", use_container_width=True,
                         disabled=not st.session_state.is_calling)

if start_btn:
    st.session_state.is_calling = True
    st.session_state.chat_history = []
    st.session_state.ui_messages = []
    st.session_state.needs_greeting = True
    st.rerun()

if end_btn:
    st.session_state.is_calling = False
    st.session_state.needs_greeting = False
    st.session_state.chat_history = []
    st.session_state.ui_messages = []
    st.rerun()

# ── Chat transcript ─────────────────────────────────────────────────────
with st.container():
    for msg in st.session_state.ui_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

status = st.empty()

# ── Main conversation loop ──────────────────────────────────────────────
if st.session_state.is_calling:

    # Guard: API key must be present
    if not os.environ.get("GROQ_API_KEY", "").strip():
        status.error("⚠️ Please enter your Groq API key in the sidebar (or in .env).")
        st.session_state.is_calling = False
        st.stop()

    # Step 0 – Greeting (first turn only)
    if st.session_state.needs_greeting:
        greeting = "Hello! This is IT support. How can I help you today?"
        st.session_state.ui_messages.append({"role": "assistant", "content": greeting})
        status.success(f"🔊 {greeting}")
        speak_text(greeting)
        st.session_state.needs_greeting = False
        st.rerun()

    # Step 1 – Listen
    status.info("🎤 Listening … speak now (stops automatically when you pause)")
    audio_file = record_audio()

    if audio_file:
        # Step 2 – Transcribe
        status.warning("⏳ Processing your speech …")
        user_text = transcribe_audio(audio_file)

        if user_text and len(user_text.strip()) > 2:
            # Show what the user said
            st.session_state.ui_messages.append({"role": "user", "content": user_text})
            status.info(f"🗣️ You said: _{user_text}_")

            # Step 3 – AI response
            status.info("🧠 AI is thinking …")
            ai_reply, st.session_state.chat_history = generate_response(
                user_text, st.session_state.chat_history
            )

            st.session_state.ui_messages.append({"role": "assistant", "content": ai_reply})

            # Step 4 – Speak
            status.success(f"🔊 {ai_reply}")
            speak_text(ai_reply)
        else:
            status.warning("🤔 Didn't catch that — let's try again.")
            time.sleep(1)

        # Clean up temp file
        try:
            if os.path.exists(audio_file):
                os.remove(audio_file)
        except OSError:
            pass

    else:
        # No speech detected within timeout
        status.warning("🤔 No speech detected. Listening again …")
        time.sleep(0.5)

    # Loop
    if st.session_state.is_calling:
        time.sleep(0.3)
        st.rerun()

else:
    status.markdown("📞 Call ended. Click **Start Call** to begin a new session.")
