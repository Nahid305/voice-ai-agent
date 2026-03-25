"""
llm_handler.py - Calls the Groq REST API directly (no SDK needed).
"""
import os
import requests


GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL_NAME = "llama-3.1-8b-instant"

SYSTEM_PROMPT = (
    "You are a professional IT support agent on a live phone call. "
    "Diagnose technical problems step-by-step, ask clarifying questions, "
    "and provide simple solutions. Be conversational, concise, and helpful. "
    "Keep every response to 1-3 short sentences so it can be spoken quickly."
)


def generate_response(user_input: str, chat_history: list) -> tuple:
    """
    Sends the conversation to Groq and returns the AI reply.

    Args:
        user_input:   Latest transcribed text from the user.
        chat_history: List of message dicts (OpenAI chat format).

    Returns:
        (reply_text, updated_chat_history)
    """
    api_key = os.environ.get("GROQ_API_KEY", "").strip()
    if not api_key:
        return ("Error: Groq API key is not set. "
                "Please paste it in the sidebar or add it to .env"), chat_history

    # Seed the system prompt on first turn
    if not chat_history:
        chat_history = [{"role": "system", "content": SYSTEM_PROMPT}]

    chat_history.append({"role": "user", "content": user_input})

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL_NAME,
        "messages": chat_history,
        "temperature": 0.5,
        "max_tokens": 150,
    }

    try:
        resp = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=15)

        if resp.status_code != 200:
            err = f"API Error {resp.status_code}: {resp.text[:200]}"
            print(f"[LLM] {err}")
            return err, chat_history

        reply = resp.json()["choices"][0]["message"]["content"]
        chat_history.append({"role": "assistant", "content": reply})
        return reply, chat_history

    except requests.exceptions.Timeout:
        return "Sorry, the AI service timed out. Please try again.", chat_history
    except Exception as exc:
        err = f"Sorry, something went wrong: {exc}"
        print(f"[LLM] {err}")
        return err, chat_history
