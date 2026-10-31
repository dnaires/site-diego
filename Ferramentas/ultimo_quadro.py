"""Extrai o último quadro de um clipe em PNG sem perdas, na resolução nativa (sem upscale, sem recorte).
Uso: python ultimo_quadro.py clipe.mp4 [saida.png]
Sem saida, grava <clipe>_ultimo_quadro.png ao lado do clipe. Avisa se o quadro não for 1080x1920 (9:16)
ou se o canto inferior direito parecer ter marca d'água (brilho alto num canto que deveria ser escuro).
Equivale a: ffmpeg -sseof -0.5 -i clipe.mp4 -an -update 1 saida.png (cada quadro sobrescreve o anterior; fica o último)."""
import subprocess
import sys
from pathlib import Path

from PIL import Image


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    clipe = Path(sys.argv[1])
    saida = Path(sys.argv[2]) if len(sys.argv) > 2 else clipe.with_name(clipe.stem + "_ultimo_quadro.png")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-sseof", "-0.5", "-i", str(clipe), "-an",
                    "-update", "1", "-compression_level", "9", str(saida)], check=True)
    im = Image.open(saida).convert("RGB")
    w, h = im.size
    print(f"{saida} {w}x{h}")
    if (w, h) != (1080, 1920):
        print(f"AVISO: esperado 1080x1920 (9:16), veio {w}x{h}.")
    canto = im.crop((int(w * .80), int(h * .92), w, h)).convert("L")
    if canto.getextrema()[1] > 200:
        print("AVISO: canto inferior direito tem pixels muito claros (marca d'água?). Confira o quadro.")


if __name__ == "__main__":
    main()
