"""
audio_recorder.py - Records audio from the microphone with Voice Activity Detection (VAD).
Stops recording automatically when the user stops speaking.
"""
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import os
import time
import queue


def record_audio(fs=16000, filename="temp_recording.wav", silence_threshold=0.01,
                 silence_duration=1.5, max_duration=15):
    """
    Records audio from the microphone until the user stops speaking.

    Uses volume-based Voice Activity Detection to know when the user
    has finished talking (1.5s of silence after speech).

    Args:
        fs (int): Sampling frequency (16000 recommended for Whisper).
        filename (str): Output WAV file path.
        silence_threshold (float): RMS volume level that counts as "speech".
        silence_duration (float): Seconds of silence before auto-stop.
        max_duration (int): Hard cap on recording length.

    Returns:
        str | None: Path to the WAV file, or None if nothing was recorded.
    """
    audio_queue = queue.Queue()

    def _stream_callback(indata, frames, time_info, status):
        """Sounddevice callback – pushes each audio block into the queue."""
        audio_queue.put(indata.copy())

    recorded_chunks = []
    start_time = time.time()
    last_voice_time = time.time()
    user_has_spoken = False

    try:
        with sd.InputStream(samplerate=fs, channels=1, dtype="int16",
                            blocksize=2048, callback=_stream_callback):
            while True:
                chunk = audio_queue.get()
                recorded_chunks.append(chunk)

                # Normalised volume (0.0 – 1.0)
                volume = np.max(np.abs(chunk)) / 32768.0

                if volume > silence_threshold:
                    user_has_spoken = True
                    last_voice_time = time.time()

                elapsed = time.time() - start_time

                # Stop: user spoke and then went silent
                if user_has_spoken and (time.time() - last_voice_time) > silence_duration:
                    break
                # Stop: waited 8 s and user never spoke
                if not user_has_spoken and elapsed > 8:
                    break
                # Stop: hard cap
                if elapsed > max_duration:
                    break

        if not user_has_spoken:
            return None

        recording = np.concatenate(recorded_chunks, axis=0)
        directory = os.path.dirname(filename)
        if directory:
            os.makedirs(directory, exist_ok=True)
        wav.write(filename, fs, recording)
        return filename

    except Exception as exc:
        print(f"[audio_recorder] Error: {exc}")
        return None
