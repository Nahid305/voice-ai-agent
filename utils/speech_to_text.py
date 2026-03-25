"""
speech_to_text.py - Transcribes audio files using faster-whisper (CPU mode).
"""
from faster_whisper import WhisperModel
import os

# ── Model initialisation (runs once on import) ──────────────────────────
_model = None

def _get_model():
    """Lazy-load the Whisper model so the app doesn't crash on import."""
    global _model
    if _model is not None:
        return _model
    try:
        print("[STT] Loading Whisper model (base.en, CPU) …")
        _model = WhisperModel(
            "base.en",
            device="cpu",
            compute_type="int8",
            download_root=os.path.join(os.path.dirname(__file__), "..", "models"),
        )
        print("[STT] Model loaded successfully.")
    except Exception as exc:
        print(f"[STT] WARNING – could not load Whisper model: {exc}")
        _model = None
    return _model


def transcribe_audio(audio_path: str) -> str:
    """
    Transcribes the given WAV file and returns the text.

    Args:
        audio_path: Absolute or relative path to a .wav file.

    Returns:
        The transcribed text, or an empty string on failure.
    """
    model = _get_model()
    if model is None:
        print("[STT] Model not available – returning empty string.")
        return ""

    if not os.path.exists(audio_path):
        print(f"[STT] File not found: {audio_path}")
        return ""

    try:
        segments, _info = model.transcribe(audio_path, beam_size=5)
        text = " ".join(seg.text for seg in segments).strip()
        return text
    except Exception as exc:
        print(f"[STT] Transcription error: {exc}")
        return ""
