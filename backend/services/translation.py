# backend/services/translation.py
from deep_translator import GoogleTranslator

def translate_to_english(text: str, source_language: str) -> str:
    if source_language == "en":
        return text
    try:
        return GoogleTranslator(source=source_language, target="en").translate(text)
    except Exception as e:
        print(f"Translation error: {e}")
        return text

def translate_from_english(text: str, target_language: str) -> str:
    if target_language == "en":
        return text
    try:
        return GoogleTranslator(source="en", target=target_language).translate(text)
    except Exception as e:
        print(f"Translation error: {e}")
        return text