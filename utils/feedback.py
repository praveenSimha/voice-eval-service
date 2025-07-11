# utils/feedback.py

def generate_feedback(pronunciation, pacing, pauses):
    miswords = ", ".join([w["word"] for w in pronunciation["mispronounced_words"]])
    text = ""

    text += pacing["pacing_feedback"]
    if miswords:
        text += f" Focus on pronouncing '{miswords}' more clearly."
    if pauses["pause_count"] > 0:
        text += f" {pauses['pause_feedback']}"

    return {"text_feedback": text.strip()}
