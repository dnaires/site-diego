"""Gera Publicacao/public_html/ e public_html.zip. Roda verificar.py antes e aborta se falhar.
Uso: python empacotar.py"""
import shutil
import subprocess
import sys
import time
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PUB = RAIZ / "Publicacao"
SAIDA = PUB / "public_html"
ARQUIVOS = ["index.html", "privacidade.html", "robots.txt", "sitemap.xml"]


def tenta(fn, *args, vezes=5, **kw):
    for n in range(vezes):  # o OneDrive pode segurar arquivos por alguns segundos
        try:
            return fn(*args, **kw)
        except OSError:
            if n == vezes - 1:
                raise
            time.sleep(2)


def main() -> int:
    r = subprocess.run([sys.executable, str(RAIZ / "Ferramentas" / "verificar.py"), "--sem-pacote"], capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout)
        return 1
    SAIDA.mkdir(parents=True, exist_ok=True)
    # copia por cima (o OneDrive pode travar pastas inteiras) e remove só o que saiu da origem
    for nome in ARQUIVOS:
        tenta(shutil.copy, RAIZ / nome, SAIDA / nome)
    tenta(shutil.copytree, RAIZ / "assets", SAIDA / "assets", dirs_exist_ok=True)
    esperado = {SAIDA / n for n in ARQUIVOS} | {SAIDA / "assets" / f.relative_to(RAIZ / "assets")
                                                for f in (RAIZ / "assets").rglob("*") if f.is_file()}
    for f in list(SAIDA.rglob("*")):
        if f.is_file() and f not in esperado:
            tenta(f.unlink)
    zip_path = PUB / "public_html.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(SAIDA.rglob("*")):
            if f.is_file():
                z.write(f, f.relative_to(SAIDA).as_posix())
    total = sum(f.stat().st_size for f in SAIDA.rglob("*") if f.is_file()) // 1024
    print(f"OK: {SAIDA} ({total} KB) e {zip_path.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
