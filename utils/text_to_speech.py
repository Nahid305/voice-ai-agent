"""
text_to_speech.py - Converts text to speech using Microsoft Edge neural voices.
Uses edge-tts for natural, human-like voice synthesis (free, no API key needed).
"""
import edge_tts
import asyncio
import os
import tempfile
import threading


# Natural-sounding voices (pick one):
#   en-US-JennyNeural       – Female, warm & professional
#   en-US-GuyNeural         – Male, conversational
#   en-US-AriaNeural        – Female, friendly
#   en-US-DavisNeural       – Male, calm & professional
#   en-GB-SoniaNeural       – British female
VOICE = "en-US-JennyNeural"


async def _generate_speech(text: str, output_file: str) -> None:
    """Async helper – generates an MP3 from text using Edge TTS."""
    communicate = edge_tts.Communicate(text, VOICE, rate="+5%", pitch="+0Hz")
    await communicate.save(output_file)


def _run_async_task(coro) -> None:
    """Run async coroutine safely across different runtime environments."""
    try:
        asyncio.run(coro)
        return
    except RuntimeError as exc:
        if "asyncio.run() cannot be called from a running event loop" not in str(exc):
            raise

    task_error = {"exception": None}

    def _runner():
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(coro)
            loop.close()
        except Exception as thread_exc:
            task_error["exception"] = thread_exc

    thread = threading.Thread(target=_runner, daemon=True)
    thread.start()
    thread.join()

    if task_error["exception"] is not None:
        raise task_error["exception"]


def synthesize_speech_bytes(text: str) -> bytes:
    """
    Generates MP3 bytes from text for browser playback.

    Args:
        text: The sentence to synthesize.

    Returns:
        MP3 bytes, or empty bytes on failure.
    """
    if not text or not text.strip():
        return b""

    temp_file_path = ""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            temp_file_path = temp_file.name

        _run_async_task(_generate_speech(text, temp_file_path))

        with open(temp_file_path, "rb") as file_handle:
            return file_handle.read()
    except Exception as exc:
        print(f"[TTS] Error generating bytes: {exc}")
        return b""
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
            except OSError:
                pass


def speak_text(text: str, language: str = "en") -> None:
    """
    Converts text to speech with a natural-sounding neural voice and plays it.

    Args:
        text:     The sentence to speak.
        language: Unused (kept for API compatibility). Voice is set via VOICE constant.
    """
    if not text or not text.strip():
        return

    audio_file = "temp_response.mp3"

    try:
        import pygame

        # 1. Generate the MP3 with edge-tts (async, but we run it synchronously here)
        _run_async_task(_generate_speech(text, audio_file))

        # 2. Play it via pygame
        pygame.mixer.init()
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        # 3. Cleanup
        pygame.mixer.music.unload()
        pygame.mixer.quit()

        if os.path.exists(audio_file):
            os.remove(audio_file)

    except Exception as exc:
        print(f"[TTS] Error: {exc}")
        try:
            if pygame.mixer.get_init():
                pygame.mixer.quit()
        except Exception:
            pass
