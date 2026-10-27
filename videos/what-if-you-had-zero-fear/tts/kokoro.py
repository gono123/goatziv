# A tiny stand-in for the `kokoro` (PyTorch) package that engine/audio/voice.js calls, backed by
# kokoro-onnx (pip install kokoro-onnx soundfile) and the v1.0 ONNX model files in tts/models/.
#   voice names: one Kokoro voice ("am_onyx") or a blend ("am_onyx*0.7+am_michael*0.3"),
#   optionally with "@0.94" to play it back slower and lower (a deeper, bigger-chested read).
import os
import numpy as np
from kokoro_onnx import Kokoro

_DIR = os.environ.get("KOKORO_ONNX_DIR", os.path.join(os.path.dirname(__file__), "models"))
_K = None


def _model():
    global _K
    if _K is None:
        _K = Kokoro(os.path.join(_DIR, "kokoro-v1.0.onnx"), os.path.join(_DIR, "voices-v1.0.bin"))
    return _K


class _Chunk:
    def __init__(self, audio):
        self.audio = audio


class KPipeline:
    def __init__(self, lang_code="a"):
        self.lang = "en-gb" if lang_code == "b" else "en-us"

    def __call__(self, text, voice="am_onyx", speed=1.0):
        k = _model()
        voice, _, drop = voice.partition("@")
        parts = [p.split("*") for p in voice.split("+")]
        style = sum(k.get_voice_style(n) * (float(w[0]) if w else 1.0) for n, *w in parts)
        audio, sr = k.create(text, voice=style, speed=speed, lang=self.lang)
        if drop:  # resample: slower and lower by the same factor
            r = float(drop)
            n = int(len(audio) / r)
            audio = np.interp(np.arange(n) * r, np.arange(len(audio)), audio).astype(np.float32)
        yield _Chunk(audio)
