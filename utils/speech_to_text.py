import whisper

# Use tiny for speed (change to "base" if needed)
model = whisper.load_model("tiny")

def transcribe_video(video_path):
    result = model.transcribe(video_path)
    return result["segments"]