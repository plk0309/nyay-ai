# backend/services/voice_in.py
import os
from groq import Groq

# Hosted Whisper via Groq: no local model, so no torch/ctranslate2 in memory
WHISPER_MODEL = "whisper-large-v3-turbo"

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

_client = None

def _get_client() -> Groq:
    global _client
    if _client is None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not set in environment")
        _client = Groq(api_key=api_key)
    return _client

def transcribe_audio(audio_bytes: bytes, language: str = None, filename: str = "audio.wav") -> dict:
    """
    Transcribe audio bytes to text using Groq's hosted Whisper.
    If language is None, auto-detects language.
    Returns dict with text, detected_language, language_probability, duration
    """
    kwargs = {}
    if language:
        kwargs["language"] = language

    result = _get_client().audio.transcriptions.create(
        file=(filename, audio_bytes),
        model=WHISPER_MODEL,
        response_format="verbose_json",
        **kwargs,
    )

    return {
        "text": (result.text or "").strip(),
        "detected_language": language or getattr(result, "language", None),
        "language_probability": None,  # hosted API doesn't return this
        "duration": round(getattr(result, "duration", 0) or 0, 2),
    }

def transcribe_audio_file(file_path: str, language: str = None) -> dict:
    """Transcribe from file path directly"""
    with open(file_path, "rb") as f:
        return transcribe_audio(f.read(), language, filename=os.path.basename(file_path))