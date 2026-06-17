# backend/services/voice_in.py
import os
import tempfile
from faster_whisper import WhisperModel

# Load model once at startup — use 'base' for speed, 'medium' for better Hindi accuracy
model = WhisperModel("base", device="cpu", compute_type="int8")

SUPPORTED_LANGUAGES = {
    "hi": "Hindi",
    "en": "English",
    "ta": "Tamil",
    "te": "Telugu",
    "mr": "Marathi",
    "bn": "Bengali",
    "gu": "Gujarati",
    "kn": "Kannada",
    "pa": "Punjabi"
}

def transcribe_audio(audio_bytes: bytes, language: str = None) -> dict:
    """
    Transcribe audio bytes to text using faster-whisper.
    If language is None, auto-detects language.
    Returns dict with text, detected_language, confidence
    """
    # Save audio bytes to temp file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp.write(audio_bytes)
        tmp_path = tmp.name

    try:
        # Transcribe
        segments, info = model.transcribe(
            tmp_path,
            language=language,  # None = auto detect
            beam_size=5,
            vad_filter=True,  # filters out silence
            vad_parameters=dict(min_silence_duration_ms=500)
        )

        # Collect all segments
        text = " ".join([segment.text.strip() for segment in segments])

        return {
            "text": text.strip(),
            "detected_language": info.language,
            "language_probability": round(info.language_probability, 2),
            "duration": round(info.duration, 2)
        }

    finally:
        # Always clean up temp file
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

def transcribe_audio_file(file_path: str, language: str = None) -> dict:
    """Transcribe from file path directly"""
    with open(file_path, "rb") as f:
        return transcribe_audio(f.read(), language)