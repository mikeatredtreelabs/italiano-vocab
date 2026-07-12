"""
Segneri — local faster-whisper STT server (voice tutor spec, step 3)

Runs Whisper locally with CUDA so speech-to-text is instant and free.
The Segneri tutor posts recorded audio here and gets Italian text back.

Setup (Windows, once):
    pip install faster-whisper fastapi uvicorn python-multipart

Run (each session):
    python whisper_server.py
    → serves http://localhost:8756

Then in Segneri: Tutor → ⚙️ → Whisper server → http://localhost:8756

Notes:
- First run downloads the model (~500MB for "small"). Change MODEL below
  to "medium" for better accuracy if the RTX has headroom (it does).
- device="cuda" requires the NVIDIA CUDA runtime; if unavailable it
  falls back to CPU automatically (slower but works).
- This only works when Segneri runs on the SAME machine (localhost is
  exempt from HTTPS mixed-content rules). From the iPhone, leave the
  Whisper URL blank — the tutor falls back to iOS's built-in speech
  recognition automatically.
"""

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from faster_whisper import WhisperModel
import tempfile, os

MODEL = "small"          # "small" | "medium" — medium is better, slower to load
PORT = 8756

print(f"Loading faster-whisper '{MODEL}'…")
try:
    model = WhisperModel(MODEL, device="cuda", compute_type="float16")
    print("→ CUDA")
except Exception as e:
    print(f"→ CUDA unavailable ({e}); using CPU")
    model = WhisperModel(MODEL, device="cpu", compute_type="int8")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://mikeatredtreelabs.github.io", "http://localhost:8000"],
    allow_methods=["POST"],
    allow_headers=["*"],
)


@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    suffix = os.path.splitext(file.filename or "audio.webm")[1] or ".webm"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(await file.read())
        path = tmp.name
    try:
        segments, _info = model.transcribe(path, language="it", vad_filter=True)
        text = " ".join(s.text.strip() for s in segments).strip()
        return {"text": text}
    finally:
        os.unlink(path)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=PORT)
