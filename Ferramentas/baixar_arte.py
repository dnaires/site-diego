"""Baixa para referencias/ a gravura usada em #camadas (domínio público).
Niccolò Ricciolini, Tab. IV, desenhada e gravada em Roma, 1703. Publicada em G. M. Lancisi, De motu cordis et aneurysmatibus
(Roma: Salvioni, 1728). Cópia digital: Wellcome Collection b30456599, imagem 0185 (Public Domain Mark)."""
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
URL = "https://iiif.wellcomecollection.org/image/b30456599_0185.jp2/full/2000,/0/default.jpg"
DEST = RAIZ / "referencias" / "lancisi-ricciolini-tab-IV.jpg"

if __name__ == "__main__":
    DEST.parent.mkdir(exist_ok=True)
    req = urllib.request.Request(URL, headers={"User-Agent": "SiteDiegoAires/1.0 (dnaires@gmail.com)"})
    DEST.write_bytes(urllib.request.urlopen(req, timeout=90).read())
    print(f"OK {DEST.name} {DEST.stat().st_size // 1024} KB")
