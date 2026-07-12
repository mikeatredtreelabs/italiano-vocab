# Segneri Voice Server (XTTS — your cloned voice)

Makes the AI tutor speak in **your voice**, in Italian, for $0. Runs on your Windows PC;
the app (laptop or phone) sends tutor replies here and plays back the generated audio.

## One-time setup (on the PC)

1. **Install Python 3.10–3.12** if not present (python.org, check "Add to PATH").

2. **Install dependencies** (in a terminal):
   ```
   pip install coqui-tts fastapi uvicorn soundfile
   ```
   If you have an NVIDIA GPU, install CUDA-enabled PyTorch first for fast generation
   (see pytorch.org/get-started for the command matching your GPU — newer cards like
   RTX 50-series need the latest torch build). CPU works too, just slower (~a few
   seconds per sentence).

3. **Record your voice sample.** 15–30 seconds of you speaking normally (English is
   fine — the clone will still speak Italian). Quiet room, no music. Save it as
   `speaker.wav` in this `server/` folder.
   - iPhone Voice Memos → share the file to your PC, then convert m4a → wav
     (e.g. `ffmpeg -i sample.m4a speaker.wav`, or any online converter).
   - Longer/cleaner sample = better clone. Swap the file anytime; no retraining.

4. **Run it:**
   ```
   python server/xtts_server.py
   ```
   First run downloads the XTTS-v2 model (~1.8 GB). When you see "Model ready",
   check http://localhost:8757/health — you want `"ok": true, "speaker": true`.

## Connecting the app

In the app: Tutor → ⚙️ → **Voice engine: My voice**, then set the XTTS server URL.

- **On the PC itself:** `http://localhost:8757` — works immediately.
- **On your phone:** the app is served over HTTPS, so browsers block plain
  `http://192.168.x.x` calls (mixed content). The clean fix is **Tailscale** (free):
  1. Install Tailscale on the PC and your iPhone, sign in to the same account.
  2. On the PC: `tailscale serve --bg 8757`
  3. It prints an `https://<your-pc>.<tailnet>.ts.net` URL — use that as the XTTS
     server URL on the phone. Bonus: this works away from home too.

If the server is unreachable, the app automatically falls back to the browser voice.

## Notes

- XTTS-v2 is licensed for non-commercial/personal use (fits this project).
- Model + your voice sample never leave your machine.
- Port is 8757 (whisper STT server, when added, will use 8756).
