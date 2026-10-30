"""Gera os derivados em assets/ a partir da marca oficial (somente leitura), fotos e npm.
Uso: python otimizar_assets.py   (idempotente; sobrescreve assets/)"""
import shutil
import subprocess
import tarfile
import tempfile
from pathlib import Path

import numpy as np
from fontTools import subset
from fontTools.ttLib import TTFont
from PIL import Image, ImageOps

RAIZ = Path(__file__).resolve().parent.parent
ASSETS = RAIZ / "assets"
MARCA = Path(r"C:\Users\kmili\OneDrive\Documentos\Logomarcas\Dr Diego Aires")
FOTOS = Path(r"C:\Users\kmili\OneDrive\Imagens\Fotos profissionais 2024")
CARMIM, BEGE = (157, 34, 53), (217, 200, 157)

FONTES = {  # arquivo de origem -> saída
    "Spectral_SC/SpectralSC-Regular.ttf": "spectral-sc-regular.woff2",
    "Spectral_SC/SpectralSC-SemiBold.ttf": "spectral-sc-semibold.woff2",
    "Ubuntu/Ubuntu-Regular.ttf": "ubuntu-regular.woff2",
    "Ubuntu/Ubuntu-Medium.ttf": "ubuntu-medium.woff2",
    "Ubuntu/Ubuntu-Italic.ttf": "ubuntu-italic.woff2",
    "Spectral_SC/SpectralSC-SemiBoldItalic.ttf": "spectral-sc-semibolditalic.woff2",
}
LOGOS = {  # prefixo da pasta (sem acento) -> nome de saída
    "Marca Positiva Colorida - Uso": "logo-positiva-vertical",
    "Marca Positiva Colorida Horizontal": "logo-positiva-horizontal",
    "Marca Negativa Colorida - Uso": "logo-negativa-vertical",
    "Marca Megativa Colorida Horizontal": "logo-negativa-horizontal",
}
FOTOS_USADAS = {
    "IMG_9983": "diego-sorriso-jaleco",
    "IMG_9979": "diego-retrato",
    "IMG_9992": "diego-escuro-sentado",
    "IMG_9995": "diego-escuro-em-pe",
}
VENDOR = [("gsap@3.12.5", {"package/dist/gsap.min.js": "gsap.min.js",
                           "package/dist/ScrollTrigger.min.js": "ScrollTrigger.min.js"}),
          ("lenis@1.1.20", {"package/dist/lenis.min.js": "lenis.min.js"})]
UNICODES = list(range(0x20, 0x7F)) + list(range(0xA0, 0x100)) + [0x2013, 0x2018, 0x2019, 0x201C, 0x201D, 0x2022, 0x2026]


def log(msg: str) -> None:
    print(msg.encode("ascii", "replace").decode())


def fontes() -> None:
    d = ASSETS / "fonts"
    d.mkdir(parents=True, exist_ok=True)
    opts = subset.Options(layout_features=["*"], flavor="woff2")
    for rel, out in FONTES.items():
        f = TTFont(MARCA / "Fonts" / rel)
        s = subset.Subsetter(opts)
        s.populate(unicodes=UNICODES)
        s.subset(f)
        f.flavor = "woff2"
        f.save(d / out)
        log(f"fonte {out} {(d / out).stat().st_size // 1024} KB")


def achar_png(prefixo: str) -> Path:
    pastas = [p for p in (MARCA / "Arquivos" / "RGB").iterdir() if p.name.startswith(prefixo)]
    return next(f for p in pastas for f in p.glob("*.png"))


def logos() -> None:
    """Logos = PNGs oficiais (RGBA) em WebP. O PDF oficial é uma página A4 com rasters embutidos, não um vetor limpo."""
    d = ASSETS / "logo"
    d.mkdir(parents=True, exist_ok=True)
    for prefixo, nome in LOGOS.items():
        im = Image.open(achar_png(prefixo)).convert("RGBA")
        im.thumbnail((1200 if "vertical" in nome else 1800, 1200), Image.LANCZOS)
        im.save(d / f"{nome}.webp", quality=92, method=6)
        log(f"logo {nome}.webp {im.size} {(d / f'{nome}.webp').stat().st_size // 1024} KB")
    icone()


def faixa_icone(png: Path) -> tuple[Image.Image, tuple[int, int, int, int]]:
    """Imagem e bbox do ícone: segmento de cima, separado do wordmark pelo maior vazio no alfa."""
    im = Image.open(png).convert("RGBA")
    a = np.array(im)[:, :, 3] > 10
    ys = np.where(a.any(axis=1))[0]
    gaps = [(ys[i + 1] - ys[i], ys[i], ys[i + 1]) for i in range(len(ys) - 1) if ys[i + 1] - ys[i] > 1]
    topo = max(gaps)[1] if gaps else ys[-1]
    xs = np.where(a[: topo + 1].any(axis=0))[0]
    return im, (int(xs[0]), int(ys[0]), int(xs[-1]) + 1, int(topo) + 1)


def icone() -> None:
    im, box = faixa_icone(achar_png("Marca Positiva Colorida - Uso"))
    ic = im.crop(box)
    ic.thumbnail((900, 900), Image.LANCZOS)
    ic.save(ASSETS / "logo" / "icone.webp", quality=92, method=6)
    log(f"icone.webp {ic.size}")
    mini = ic.copy()
    mini.thumbnail((192, 192), Image.LANCZOS)
    fav = Image.new("RGBA", (192, 192), (0, 0, 0, 0))  # só o coração-chama, fundo transparente
    fav.paste(mini, ((192 - mini.width) // 2, (192 - mini.height) // 2), mini)
    fav.save(ASSETS / "favicon.png")
    neg = Image.open(achar_png("Marca Negativa Colorida - Uso")).convert("RGBA")
    neg.thumbnail((520, 520))
    og = Image.new("RGB", (1200, 630), CARMIM)
    og.paste(neg, ((1200 - neg.width) // 2, (630 - neg.height) // 2), neg)
    og.save(ASSETS / "og-image.jpg", quality=88)
    log("favicon.png e og-image.jpg")


def arte() -> None:
    """Ricciolini (Lancisi, 1728, Tab. IV), só a Fig. I (coração, traqueia, letras e legendas), em negativo:
    traço bege sobre o carmim da seção. Grava também a versão positiva em referencias/ricciolini-fig1-positivo.webp (sem uso)."""
    from scipy import ndimage as ndi

    src = RAIZ / "referencias" / "lancisi-ricciolini-tab-IV.jpg"
    if not src.exists():
        log("arte: rode baixar_arte.py antes (pulado)")
        return
    box = (40, 80, 900, 1740)
    im = Image.open(src).convert("L").crop(box)
    a = np.asarray(ImageOps.autocontrast(im, cutoff=1), dtype=np.float32) / 255.0
    h, w = a.shape
    yy, xx = np.mgrid[0:h, 0:w]
    tinta = np.clip(((1 - a) - 0.30) / 0.40, 0, 1)                  # 1 = traço; ignora manchas do papel
    tinta[(xx - (114 - box[0])) ** 2 + (yy - (1210 - box[1])) ** 2 <= 14 ** 2] = 0   # pinta solta fora da gravura
    # molduras da placa (linhas finas e longas): abertura morfológica, sem tocar nas letras nem na figura
    b0 = tinta > 0.5
    vert = ndi.binary_opening(b0[:, :48], structure=np.ones((140, 1)))        # moldura vertical, à esquerda
    vert[250:330, :] = False                                                   # preserva o rótulo "Fig. I.", que toca a moldura
    tinta[:, :48][ndi.binary_dilation(vert, iterations=2)] = 0
    tinta[:, :27] = 0                                                         # resto da moldura, à esquerda do rótulo
    r0 = 90 + int(np.argmax(tinta[90:140].mean(axis=1)))                      # moldura horizontal, no topo
    for x0, x1 in ((0, 330), (600, w)):                                       # fora da traqueia
        faixa = b0[r0 - 14:r0 + 15, x0:x1]
        hor = ndi.binary_opening(faixa, structure=np.ones((1, 60)))
        tinta[r0 - 14:r0 + 15, x0:x1][ndi.binary_dilation(hor, structure=np.ones((5, 1)))] = 0
    bin_ = tinta > 0.5
    lab, n = ndi.label(bin_)
    area = ndi.sum(bin_, lab, index=np.arange(1, n + 1))
    grandes = np.isin(lab, 1 + np.where(area > 6000)[0])
    perto = ndi.binary_dilation(grandes, iterations=140)             # mantém letras e legendas junto da figura
    perto[240:345, :260] = True                                       # rótulo "Fig. I." (longe da figura)
    tinta = tinta * perto
    feather = np.clip(np.minimum.reduce([xx, yy, w - 1 - xx, h - 1 - yy]) / 8.0, 0, 1)
    m = (tinta * feather)[..., None]
    fundo = np.array(CARMIM, dtype=np.float32)
    traco = np.array(BEGE, dtype=np.float32)
    neg = Image.fromarray((fundo * (1 - m) + traco * m).astype(np.uint8))
    papel = np.array((232, 222, 196), dtype=np.float32)
    tint = np.array((92, 18, 32), dtype=np.float32)
    pos = Image.fromarray((papel * (1 - m) + tint * m).astype(np.uint8))
    for im2 in (neg, pos):
        im2.thumbnail((900, 1400), Image.LANCZOS)
    d = ASSETS / "art"
    d.mkdir(parents=True, exist_ok=True)
    neg.save(d / "ricciolini-fig1.webp", quality=88, method=6)
    pos.save(RAIZ / "referencias" / "ricciolini-fig1-positivo.webp", quality=88, method=6)
    log(f"arte ricciolini-fig1.webp {neg.size[0]}x{neg.size[1]}")


def vendor() -> None:
    d = ASSETS / "vendor"
    d.mkdir(parents=True, exist_ok=True)
    for pkg, arquivos in VENDOR:
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(["npm", "pack", pkg, "--silent"], cwd=tmp, check=True, shell=True)
            tgz = next(Path(tmp).glob("*.tgz"))
            with tarfile.open(tgz) as t:
                for interno, saida in arquivos.items():
                    conteudo = t.extractfile(interno).read()
                    (d / saida).write_bytes(f"/* {pkg} */\n".encode() + conteudo)
                    log(f"vendor {saida} {len(conteudo) // 1024} KB")


def fotos() -> None:
    d = ASSETS / "img"
    d.mkdir(parents=True, exist_ok=True)
    for orig, nome in FOTOS_USADAS.items():
        im = ImageOps.exif_transpose(Image.open(FOTOS / f"{orig}.JPG")).convert("RGB")
        im.thumbnail((1400, 1800), Image.LANCZOS)
        im.save(d / f"{nome}.webp", quality=82, method=6)
        log(f"foto {nome}.webp {im.size} {(d / f'{nome}.webp').stat().st_size // 1024} KB")


if __name__ == "__main__":
    for etapa in (fontes, logos, vendor, fotos, arte):
        etapa()
    log("OK")
