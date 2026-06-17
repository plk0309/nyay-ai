# backend/services/voice_out.py
import io
from gtts import gTTS

LANGUAGE_CODES = {
    "hi": "hi",
    "en": "en",
    "ta": "ta",
    "te": "te",
    "mr": "mr",
    "bn": "bn",
    "gu": "gu",
    "kn": "kn",
    "pa": "pa"
}

def synthesize_speech(text: str, language: str = "en") -> bytes:
    """
    Convert text to speech and return audio bytes.
    """
    lang_code = LANGUAGE_CODES.get(language, "en")

    # gTTS has a limit — truncate very long texts
    if len(text) > 3000:
        text = text[:3000] + "..."

    tts = gTTS(text=text, lang=lang_code, slow=False)

    audio_buffer = io.BytesIO()
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)

    return audio_buffer.read()

def synthesize_speech_hindi(text: str) -> bytes:
    """Convenience function for Hindi TTS"""
    return synthesize_speech(text, language="hi")