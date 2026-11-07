"""Gera versões menores das imagens grandes para o srcset do index.html (Lighthouse de 07/11).
Uso: python variantes.py   (idempotente; rode depois do otimizar_assets.py, se ele for rodado de novo)
Cada variante é <nome>-<largura>.webp ao lado do original; o original continua como a opção maior do srcset."""
from pathlib import Path

from PIL import Image

RAIZ = Path(__file__).resolve().parent.parent / "assets"
VARIANTES = {
    "logo/logo-negativa-horizontal.webp": [480],   # cabeçalho: 114 a 200px na tela
    "logo/logo-negativa-vertical.webp": [600],
    "logo/wordmark-negativa.webp": [800],          # abertura: 340 a 470px
    "img/diego-sorriso-jaleco.webp": [700],        # Origem: 440px no desktop
    "img/diego-retrato.webp": [700],               # Fé: até 420px
    "art/ricciolini-fig1-positivo.webp": [460],    # Camadas: 228px no desktop, até 340px no celular
}


def main() -> None:
    for rel, larguras in VARIANTES.items():
        orig = RAIZ / rel
        im = Image.open(orig)
        im = im.convert("RGBA" if im.mode in ("RGBA", "LA", "P") else "RGB")
        for larg in larguras:
            alt = round(im.height * larg / im.width)
            dest = orig.with_name(f"{orig.stem}-{larg}.webp")
            im.resize((larg, alt), Image.LANCZOS).save(dest, quality=84, method=6)
            print(f"{dest.relative_to(RAIZ)}: {larg}x{alt}, {dest.stat().st_size // 1024} KB (original {orig.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
