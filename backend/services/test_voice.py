# backend/services/test_voice.py
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.voice_out import synthesize_speech
from services.translation import translate_to_english, translate_from_english

def test_tts():
    print("Testing Text-to-Speech...")

    # Test English
    audio = synthesize_speech("Your rights as a tenant include the right to fair rent.", "en")
    with open("test_english.mp3", "wb") as f:
        f.write(audio)
    print("English TTS saved to test_english.mp3")

    # Test Hindi
    audio = synthesize_speech("आपके किरायेदार के अधिकार हैं।", "hi")
    with open("test_hindi.mp3", "wb") as f:
        f.write(audio)
    print("Hindi TTS saved to test_hindi.mp3")

def test_translation():
    print("\nTesting Translation...")

    hindi_text = "मेरे किरायेदार अधिकार क्या हैं?"
    english = translate_to_english(hindi_text, "hi")
    print(f"Hindi: {hindi_text}")
    print(f"English: {english}")

    back_to_hindi = translate_from_english(english, "hi")
    print(f"Back to Hindi: {back_to_hindi}")

if __name__ == "__main__":
    test_tts()
    test_translation()