# backend/routes/voice.py
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import Response
from services.voice_in import transcribe_audio
from services.voice_out import synthesize_speech
from services.translation import translate_to_english, translate_from_english
from rag.pipeline import answer_query

router = APIRouter()

@router.post("/transcribe")
async def transcribe(
    audio: UploadFile = File(...),
    language: str = Form(default=None)
):
    """
    Receive audio file, return transcribed text.
    language: 'hi', 'en', 'ta' etc. or None for auto-detect
    """
    try:
        audio_bytes = await audio.read()

        if len(audio_bytes) == 0:
            raise HTTPException(status_code=400, detail="Empty audio file")

        result = transcribe_audio(audio_bytes, language=language)

        return {
            "text": result["text"],
            "detected_language": result["detected_language"],
            "confidence": result["language_probability"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ask-voice")
async def ask_voice(
    audio: UploadFile = File(...),
    language: str = Form(default="hi"),
    return_audio: bool = Form(default=True)
):
    """
    Full voice pipeline:
    1. Transcribe audio to text
    2. Translate to English if needed
    3. Run RAG pipeline
    4. Translate answer back to user's language
    5. Convert answer to speech
    6. Return audio + text response
    """
    try:
        # Step 1: Transcribe
        audio_bytes = await audio.read()
        transcription = transcribe_audio(audio_bytes, language=language)
        user_text = transcription["text"]

        if not user_text:
            raise HTTPException(status_code=400, detail="Could not transcribe audio")

        # Step 2: Translate query to English for RAG
        english_query = translate_to_english(user_text, language)

        # Step 3: RAG pipeline
        result = answer_query(english_query)
        english_answer = result["answer"]

        # Step 4: Translate answer back to user's language
        final_answer = translate_from_english(english_answer, language)

        # Step 5: Convert to speech
        if return_audio:
            audio_response = synthesize_speech(final_answer, language)
            return Response(
                content=audio_response,
                media_type="audio/mpeg",
                headers={
                    "X-Question": user_text,
                    "X-English-Query": english_query,
                    "X-Answer": final_answer[:500],  # truncated for header
                    "X-Sources": str(result["sources"]),
                    "X-Category": result["category"]
                }
            )
        else:
            return {
                "question": user_text,
                "english_query": english_query,
                "answer": final_answer,
                "sources": result["sources"],
                "category": result["category"]
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/speak")
async def speak(
    text: str = Form(...),
    language: str = Form(default="en")
):
    """Convert any text to speech"""
    try:
        audio_bytes = synthesize_speech(text, language)
        return Response(content=audio_bytes, media_type="audio/mpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))