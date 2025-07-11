# utils/analysis.py

def analyze_pronunciation(words, threshold=0.85):
    if not words:
        return {"pronunciation_score": 0, "mispronounced_words": []}

    total_conf = sum([w['confidence'] for w in words])
    avg_conf = total_conf / len(words)
    score = round(avg_conf * 100)

    mispronounced = [
        {
            "word": w['word'],
            "start": w['start'],
            "confidence": round(w['confidence'], 2)
        } for w in words if w['confidence'] < threshold
    ]

    return {"pronunciation_score": score, "mispronounced_words": mispronounced}


def analyze_pacing(words, audio_duration):
    word_count = len(words)
    if audio_duration == 0:
        return {"pacing_wpm": 0, "pacing_feedback": "No audio detected."}

    wpm = round((word_count / audio_duration) * 60)

    if wpm < 90:
        feedback = "Too slow"
    elif wpm > 150:
        feedback = "Too fast"
    else:
        feedback = "Your speaking pace is appropriate."

    return {"pacing_wpm": wpm, "pacing_feedback": feedback}


def analyze_pauses(words):
    pause_count = 0
    total_pause_duration = 0.0
    feedback = ""

    for i in range(1, len(words)):
        prev_end = words[i-1]['end']
        curr_start = words[i]['start']
        pause = curr_start - prev_end
        if pause > 0.5:
            pause_count += 1
            total_pause_duration += pause

    if pause_count > 0:
        feedback = "Try to reduce long pauses to improve fluency."
    else:
        feedback = "Good fluency with minimal pauses."

    return {
        "pause_count": pause_count,
        "total_pause_time_sec": round(total_pause_duration, 2),
        "pause_feedback": feedback
    }
