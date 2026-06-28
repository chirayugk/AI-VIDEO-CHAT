from faster_whisper import WhisperModel

# Load model only once when application starts
model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)


def transcribe_video(video_path: str):
    """
    Transcribes a video/audio file and returns:
    - transcript
    - detected language
    """

    segments, info = model.transcribe(
        video_path,
        beam_size=5
    )

    transcript = ""

    for segment in segments:
        transcript += segment.text + " "

    return {
        "transcript": transcript.strip(),
        "language": info.language
    }