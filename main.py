# main.py

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import os
import shutil
from utils.transcription import upload_audio, transcribe_audio
from utils.analysis import analyze_pronunciation, analyze_pacing, analyze_pauses
from utils.feedback import generate_feedback

app = FastAPI()
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    if file.content_type not in ["audio/wav", "audio/mpeg"]:
        return JSONResponse(status_code=400, content={"error": "Only .wav or .mp3 files allowed"})

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        audio_url = upload_audio(file_path)
        result = transcribe_audio(audio_url)

        transcript = result["text"]
        duration = result["audio_duration"]
        words_raw = result["words"]

        words = [
            {
                "word": w["text"],
                "start": w["start"] / 1000,
                "end": w["end"] / 1000,
                "confidence": w["confidence"]
            } for w in words_raw
        ]

        # Run all analyses
        pronunciation = analyze_pronunciation(words)
        pacing = analyze_pacing(words, duration)
        pauses = analyze_pauses(words)
        feedback = generate_feedback(pronunciation, pacing, pauses)

        return {
            "transcript": transcript,
            "audio_duration_sec": duration,
            "pronunciation": pronunciation,
            "pacing": pacing,
            "pauses": pauses,
            "feedback": feedback
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
