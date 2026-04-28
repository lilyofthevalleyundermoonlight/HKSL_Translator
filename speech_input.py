import whisper
from pathlib import Path

MODEL_NAME = "base"
_model = None


def get_model():
    global _model

    if _model is None:
        print(f"Loading Whisper model: {MODEL_NAME}")
        _model = whisper.load_model(MODEL_NAME)

    return _model


def speech_to_text(audio_path):
    path = Path(audio_path)

    if not path.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    model = get_model()

    result = model.transcribe(
        str(path),
        fp16=False,
        language="en",
        task="transcribe",
        temperature=0,
        condition_on_previous_text=False
    )

    text = result.get("text", "").strip()
    return text