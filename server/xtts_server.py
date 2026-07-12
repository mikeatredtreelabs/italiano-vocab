"""
Segneri XTTS voice server — speaks tutor replies in YOUR voice.

Setup (see server/README.md for full instructions):
  1. pip install coqui-tts fastapi uvicorn soundfile
  2. Record speaker.wav (15-30s of your voice) into this folder
  3. python xtts_server.py
First run downloads the XTTS-v2 model (~1.8 GB).

Endpoints:
  GET  /health          -> {"ok": true, "device": "...", "speaker": true}
  POST /tts             -> WAV audio. Body: {"text": "...", "language": "it"}
"""
import io
import os

os.environ.setdefault("COQUI_TOS_AGREED", "1")  # XTTS is CPML-licensed: personal/non-commercial use

import torch
import soundfile as sf
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel
from TTS.api import TTS

HERE = os.path.dirname(os.path.abspath(__file__))
SPEAKER = os.path.join(HERE, "speaker.wav")
PORT = 8757

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Loading XTTS-v2 on {device} (first run downloads ~1.8 GB)...")
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
print("Model ready.")

app = FastAPI()
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)


class TTSRequest(BaseModel):
    text: str
    language: str = "it"


@app.get("/health")
def health():
    return {"ok": True, "device": device, "speaker": os.path.exists(SPEAKER)}


@app.post("/tts")
def synthesize(req: TTSRequest):
    if not os.path.exists(SPEAKER):
        raise HTTPException(500, "speaker.wav not found — record a 15-30s voice sample first")
    text = req.text.strip()
    if not text:
        raise HTTPException(400, "empty text")
    wav = tts.tts(text=text, speaker_wav=SPEAKER, language=req.language)
    buf = io.BytesIO()
    sf.write(buf, wav, 24000, format="WAV")
    return Response(buf.getvalue(), media_type="audio/wav")


if __name__ == "__main__":
    import uvicorn

    print(f"Segneri voice server on http://0.0.0.0:{PORT}  (health: http://localhost:{PORT}/health)")
    uvicorn.run(app, host="0.0.0.0", port=PORT)
