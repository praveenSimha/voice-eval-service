# 🎙️ Voice Evaluation Microservice

This project is part of the **Samvad Saathi Voice Feedback Loop**, designed to evaluate spoken responses and provide structured feedback on:

- ✅ **Pronunciation**
- 🚀 **Pacing (Words Per Minute)**
- ⏸️ **Pauses and Fluency**
- 🧠 **User-Friendly Summary Feedback**

---

## 🔧 Tech Stack

- 🐍 **Python 3.9+**
- ⚡ **FastAPI**
- ☁️ **AssemblyAI** (for Speech-to-Text and metadata)
- 📁 Local File Handling for uploads
- 🧪 Tested via Postman / curl

---

## 📦 Features

### 1. `/transcribe` Endpoint

- Accepts `.wav` or `.mp3` audio files (max 60 seconds)
- Uses AssemblyAI to:
  - Transcribe speech
  - Extract word-level metadata (start, end, confidence, pause duration)
- Computes:
  - **Pronunciation score**
  - **Pacing (WPM)**
  - **Pause analysis**
  - **Natural language feedback**

---

## 🧪 Sample Output

```json
{
  "transcript": "Hello, my name is Arjun.",
  "audio_duration_sec": 8.2,
  "pronunciation": {
    "pronunciation_score": 82,
    "mispronounced_words": [
      {"word": "Arjun", "start": 1.4, "confidence": 0.71}
    ]
  },
  "pacing": {
    "pacing_wpm": 104,
    "pacing_feedback": "Your speaking pace is appropriate."
  },
  "pauses": {
    "pause_count": 2,
    "total_pause_time_sec": 1.8,
    "pause_feedback": "Try to reduce long pauses to improve fluency."
  },
  "feedback": {
    "text_feedback": "Your speaking pace is appropriate. Focus on pronouncing 'Arjun' more clearly. Try to reduce long pauses to improve fluency."
  }
}


🛠️ Setup & Run
1. Clone the Repo
bash
Copy
Edit
git clone https://github.com/yourusername/voice-eval-microservice.git
cd voice-eval-microservice
2. Install Dependencies
It's recommended to use a virtual environment:

bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
3. Add API Key
Create a .env file and add your AssemblyAI API key:

ini
Copy
Edit
ASSEMBLYAI_API_KEY=your_api_key_here
4. Run the API
bash
Copy
Edit
uvicorn main:app --reload
Access the docs at: http://127.0.0.1:8000/docs

📂 Project Structure
bash
Copy
Edit
├── main.py                 # FastAPI app
├── .env                    # API key (not committed)
├── uploads/                # Folder to store uploaded audio
├── requirements.txt
├── utils/
│   ├── transcription.py    # Handles upload & transcription using AssemblyAI
│   ├── analysis.py         # Pronunciation, pacing, pause analysis
│   └── feedback.py         # Text-based feedback generator


📬 API Testing
POST /transcribe
Form Data:
file: .wav or .mp3 file

Example using curl:
bash
Copy
Edit
curl -X POST http://127.0.0.1:8000/transcribe \
  -F "file=@sample_audio.wav"
📌 Assumptions & Notes
Only supports .mp3 and .wav formats

Input audio must be ≤ 60 seconds

Uses confidence < 0.85 as the threshold for mispronunciation

Pauses > 0.5s are considered "long pauses"

🧠 Future Improvements
Speaker diarization for group conversations

Real-time transcription and feedback

Frontend dashboard for audio upload and report viewing
