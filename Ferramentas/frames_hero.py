"""Converte o clipe da abertura (Higgsfield) em sequência de quadros WebP para o scroll.
Uso: python frames_hero.py <clipe.mp4> [--largura 1280] [--max 150]
Gera assets/hero/frame_0001.webp ... e assets/hero/manifest.json. Apaga quadros antigos."""
import argparse
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image

RAIZ = Path(__file__).resolve().parent.parent
DEST = RAIZ / "assets" / "hero"


def duracao(clipe: Path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(clipe)],
                         capture_output=True, text=True, check=True).stdout
    return float(out.strip())


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("clipe", type=Path)
    ap.add_argument("--largura", type=int, default=1280)
    ap.add_argument("--max", type=int, default=150, help="máximo de quadros")
    a = ap.parse_args()

    fps = min(24.0, a.max / duracao(a.clipe))
    DEST.mkdir(parents=True, exist_ok=True)
    for velho in DEST.glob("frame_*.webp"):
        velho.unlink()
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["ffmpeg", "-v", "error", "-i", str(a.clipe), "-vf", f"fps={fps:.4f},scale={a.largura}:-2",
                        str(Path(tmp) / "f_%04d.png")], check=True)
        pngs = sorted(Path(tmp).glob("f_*.png"))[: a.max]
        for n, png in enumerate(pngs, 1):
            im = Image.open(png).convert("RGB")
            im.save(DEST / f"frame_{n:04d}.webp", quality=70, method=6)
        w, h = Image.open(pngs[0]).size
    (DEST / "manifest.json").write_text(json.dumps({"count": len(pngs), "width": w, "height": h}), encoding="utf-8")
    total = sum(f.stat().st_size for f in DEST.glob("frame_*.webp")) // 1024
    print(f"{len(pngs)} quadros {w}x{h}, {total} KB no total (fps usado {fps:.2f})")


if __name__ == "__main__":
    main()
