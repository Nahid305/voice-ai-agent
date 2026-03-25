"""
text_to_speech.py - Converts text to speech using Microsoft Edge neural voices.
Uses edge-tts for natural, human-like voice synthesis (free, no API key needed).
"""
import edge_tts
import pygame
import asyncio
import os


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
        # 1. Generate the MP3 with edge-tts (async, but we run it synchronously here)
        asyncio.run(_generate_speech(text, audio_file))

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
