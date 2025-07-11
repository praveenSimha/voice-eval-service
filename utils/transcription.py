import os
from dotenv import load_dotenv
import requests
import time

# Load environment variables from .env file
load_dotenv()

# Get AssemblyAI API key from environment
ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")

# Set default request headers for AssemblyAI API
headers = {
    "authorization": ASSEMBLYAI_API_KEY,
    "content-type": "application/json"
}

# Function to upload audio file to AssemblyAI and get the file's URL
def upload_audio(filepath):
    with open(filepath, 'rb') as f:
        # Send POST request to upload endpoint with audio file
        response = requests.post(
            "https://api.assemblyai.com/v2/upload",
            headers={'authorization': ASSEMBLYAI_API_KEY},
            files={'file': f}
        )
    # Return the uploaded file URL from the response
    return response.json()['upload_url']


# Function to start transcription and wait for it to complete
def transcribe_audio(audio_url):
    transcript_endpoint = "https://api.assemblyai.com/v2/transcript"

    # Submit transcription job with audio URL and options
    response = requests.post(
        transcript_endpoint,
        json={
            "audio_url": audio_url,
            "word_boost": [],          # Optional: specify keywords to boost
            "boost_param": "high",     # Boost strength
            "speaker_labels": False,   # Not needed for single-speaker audio
            "punctuate": True,         # Add punctuation to the transcript
            "format_text": True        # Format text properly (capitalization, etc.)
        },
        headers=headers
    )

    # Extract transcription job ID from response
    transcript_id = response.json()['id']

    # Build the polling endpoint to check status
    polling_endpoint = f"{transcript_endpoint}/{transcript_id}"

    # Poll the endpoint until transcription is completed or errors out
    while True:
        polling_response = requests.get(polling_endpoint, headers=headers)
        result = polling_response.json()

        # Check if transcription is done
        if result['status'] == 'completed':
            return result

        # Raise exception if an error occurred
        elif result['status'] == 'error':
            raise Exception(result['error'])

        # Wait 2 seconds before polling again (rate-limiting best practice)
        time.sleep(2)
