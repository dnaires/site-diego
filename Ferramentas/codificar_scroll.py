"""Prepara o vídeo final da abertura para o scroll da página.
Uso: python codificar_scroll.py <video_final.mp4> [--crf-desktop 30] [--crf-mobile 27]
(o vídeo final de 06/11 está em referencias/abertura_completa_v2.mp4)
Gera em assets/hero/:
  hero-1080.mp4  1080x1920, H.264 all-intra (keyframe em todo quadro), sem áudio, para telas grandes
                 (07/11: crf 26 = 13,5 MB; crf 30 = 9,6 MB, sem diferença visível em recorte 1:1)
  hero-540.mp4   540x960, mesma receita, para celulares (07/11: era 720p com 9,5 MB; 540p crf 27 = 4,9 MB)
  poster.webp    último quadro (estático para movimento reduzido)
  manifest.json  {video:{desktop,mobile}, width, height, fps, count, duration, fundo:[#rrggbb por quadro],
                  borda:[#rrggbb por quadro, cor das laterais do meio do quadro, para o brilho atrás do vídeo]}
O campo fundo guarda a cor do canto superior esquerdo de cada quadro; a página pinta o fundo da seção com
essa cor, então a lateral acompanha a troca de preto para #9D2235 sem ajuste manual.
Por que all-intra: com -g 1 todo quadro é keyframe, então rolar para trás (buscar um quadro qualquer)
não exige decodificar uma cadeia de quadros P/B e não engasga."""
import argparse
import json
import subprocess
from pathlib import Path

from PIL import Image

RAIZ = Path(__file__).resolve().parent.parent
DEST = RAIZ / "assets" / "hero"


def sonda(video: Path) -> dict:
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames",
                          "-show_entries", "stream=width,height,r_frame_rate,nb_read_frames,duration",
                          "-of", "json", str(video)], capture_output=True, text=True, check=True).stdout
    s = json.loads(out)["streams"][0]
    num, den = s["r_frame_rate"].split("/")
    return {"w": int(s["width"]), "h": int(s["height"]), "fps": float(num) / float(den),
            "n": int(s["nb_read_frames"]), "dur": float(s["duration"])}


def codifica(video: Path, saida: Path, largura: int, crf: int) -> int:
    alt = round(largura * 16 / 9 / 2) * 2
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(video), "-an",
                    "-vf", f"scale={largura}:{alt}:flags=lanczos:out_color_matrix=bt709,format=yuv420p",
                    "-c:v", "libx264", "-preset", "slow", "-g", "1", "-crf", str(crf),
                    "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv",
                    "-movflags", "+faststart", str(saida)],  # tags bt709: o navegador decodifica igual ao CSS
                   check=True)
    return saida.stat().st_size


def fundos(video: Path) -> list[str]:
    """Cor média do bloco 8x8 do canto superior esquerdo de cada quadro."""
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(video), "-an", "-vf", "crop=8:8:0:0,scale=1:1:flags=area",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    return ["#%02x%02x%02x" % tuple(raw[i:i + 3]) for i in range(0, len(raw) - 2, 3)]


def bordas(video: Path) -> list[str]:
    """Cor média das faixas laterais (6% da largura, 30% a 70% da altura) de cada quadro, esquerda e direita
    juntas. A página usa essa cor num brilho atrás do vídeo, para a borda do 9:16 não aparecer como um retângulo
    quando o meio do quadro é claro e o canto é escuro."""
    def faixa(x: str) -> bytes:
        return subprocess.run(["ffmpeg", "-v", "error", "-i", str(video), "-an",
                               "-vf", f"crop=iw*0.06:ih*0.4:{x}:ih*0.3,scale=1:1:flags=area",
                               "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    e, d = faixa("0"), faixa("iw*0.94")
    return ["#%02x%02x%02x" % tuple((e[i + k] + d[i + k]) // 2 for k in range(3)) for i in range(0, len(e) - 2, 3)]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("video", type=Path, nargs="?")
    ap.add_argument("--crf-desktop", type=int, default=30)
    ap.add_argument("--crf-mobile", type=int, default=27)
    ap.add_argument("--so-bordas", action="store_true",
                    help="só recalcula 'borda' no manifest atual, a partir do vídeo de celular do manifest (sem recodificar)")
    a = ap.parse_args()
    if a.so_bordas:
        man = json.loads((DEST / "manifest.json").read_text(encoding="utf-8"))
        man["borda"] = bordas(DEST / man["video"]["mobile"])
        (DEST / "manifest.json").write_text(json.dumps(man, separators=(",", ":")), encoding="utf-8")
        print(f"borda: {len(man['borda'])} quadros ({man['count']} no manifest). Rode empacotar.py em seguida.")
        return
    if not a.video:
        ap.error("informe o vídeo final (ou use --so-bordas)")

    info = sonda(a.video)
    if (info["w"], info["h"]) != (1080, 1920):
        print(f"AVISO: esperado 1080x1920, veio {info['w']}x{info['h']}. A página assume 9:16.")
    DEST.mkdir(parents=True, exist_ok=True)
    for velho in DEST.glob("frame_*.webp"):
        velho.unlink()
    pesos = {}
    for nome, larg, crf in (("hero-1080.mp4", 1080, a.crf_desktop), ("hero-540.mp4", 540, a.crf_mobile)):
        pesos[nome] = codifica(a.video, DEST / nome, larg, crf)
        print(f"{nome}: {pesos[nome] / 1048576:.1f} MB (crf {crf})")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-sseof", "-0.5", "-i", str(a.video), "-an", "-update", "1",
                    str(DEST / "_ultimo.png")], check=True)
    Image.open(DEST / "_ultimo.png").convert("RGB").save(DEST / "poster.webp", quality=88, method=6)
    (DEST / "_ultimo.png").unlink()
    f = fundos(a.video)
    manifest = {"video": {"desktop": "hero-1080.mp4", "mobile": "hero-540.mp4"}, "width": 1080, "height": 1920,
                "fps": info["fps"], "count": len(f), "duration": info["dur"], "fundo": f, "borda": bordas(a.video)}
    (DEST / "manifest.json").write_text(json.dumps(manifest, separators=(",", ":")), encoding="utf-8")
    print(f"{len(f)} quadros, {info['dur']:.2f} s, fundo {f[0]} -> {f[-1]}. Rode empacotar.py em seguida.")


if __name__ == "__main__":
    main()
