"""Testes estáticos do Site Diego. Uso: python verificar.py  ->  imprime OK (exit 0) ou lista de falhas (exit 1)."""
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ARQUIVOS = ["index.html", "privacidade.html", "assets/css/site.css", "assets/js/site.js"]
ORACAO = ("Vinde, Espírito Santo, enchei os corações dos vossos fiéis "
          "e acendei neles o fogo do vosso amor.")
EXTERNOS = ("fonts.googleapis", "fonts.gstatic", "cdnjs.", "unpkg.com", "cdn.jsdelivr", "cdn.tailwindcss")


def ler(rel: str) -> str:
    p = RAIZ / rel
    return p.read_text(encoding="utf-8") if p.exists() else ""


def texto_visivel(html: str) -> str:
    html = re.sub(r"<(script|style)\b.*?</\1>", " ", html, flags=re.S | re.I)
    html = re.sub(r"<!--.*?-->", " ", html, flags=re.S)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", html)).strip()


def check_existe(html: str, css: str) -> list[str]:
    return [] if html else ["index.html não existe"]


def check_travessao(html: str, css: str) -> list[str]:
    return [f"travessão em {rel}" for rel in ARQUIVOS if "—" in ler(rel)]


def check_credenciais(html: str, css: str) -> list[str]:
    txt = texto_visivel(html)
    return [f"falta '{s}' no texto visível" for s in ("CRM-DF 19878", "RQE 15628") if s not in txt]


def check_contato_clinica(html: str, css: str) -> list[str]:
    return [f"falta '{x}' (dado da Medicina Cardeal)" for x in ("5561984026331", "SEPS 710/910", "08h00 às 18h00") if x not in html]


def check_frases_genericas(html: str, css: str) -> list[str]:
    ruins = ("caráter informativo", "acolhimento", "escuta ativa", "humanizado", "sem pressa", "plano possível")
    txt = texto_visivel(html).lower()
    return [f"frase genérica no texto: '{r}'" for r in ruins if r in txt]


def check_oracao(html: str, css: str) -> list[str]:
    return [] if ORACAO in texto_visivel(html) else ["oração 'Vinde, Espírito Santo' ausente ou alterada"]


def check_iframe(html: str, css: str) -> list[str]:
    return ["<iframe> estático"] if re.search(r"<iframe", html, re.I) else []


def check_logo_sem_rotacao(html: str, css: str) -> list[str]:
    falhas = []
    for sel, corpo in re.findall(r"([^{}]+)\{([^{}]*)\}", css):
        if re.search(r"logo|icone|marca", sel, re.I) and re.search(r"rotate|skew", corpo):
            falhas.append(f"rotate/skew em regra de logo: {sel.strip()}")
    for tag in re.findall(r"<img[^>]*(?:logo|icone)[^>]*>", html, re.I):
        if re.search(r"rotate|skew", tag):
            falhas.append("rotate/skew inline em logo")
    return falhas


def check_sem_externos(html: str, css: str) -> list[str]:
    falhas = []
    for rel in ARQUIVOS:
        c = ler(rel)
        falhas += [f"recurso externo '{e}' em {rel}" for e in EXTERNOS if e in c]
    return falhas


def check_links_locais(html: str, css: str) -> list[str]:
    falhas = []
    for url in re.findall(r'(?:src|href)="([^"]+)"', html):
        if re.match(r"(https?:|#|mailto:|tel:|data:|//)", url):
            continue
        alvo = (RAIZ / url.split("#")[0].split("?")[0])
        if not alvo.exists():
            falhas.append(f"arquivo local inexistente: {url}")
    return falhas


def check_imgs(html: str, css: str) -> list[str]:
    falhas = []
    for tag in re.findall(r"<img\b[^>]*>", html, re.I):
        for attr in ("alt=", "width=", "height="):
            if attr not in tag:
                falhas.append(f"<img> sem {attr[:-1]}: {tag[:70]}")
    return falhas


def check_lang(html: str, css: str) -> list[str]:
    return [] if re.search(r'<html[^>]*lang="pt-BR"', html) else ['<html lang="pt-BR"> ausente']


def check_secoes_com_id(html: str, css: str) -> list[str]:
    return [f"<section> sem id: {t[:50]}" for t in re.findall(r"<section\b[^>]*>", html) if "id=" not in t]


def check_pacote_atualizado(html: str, css: str) -> list[str]:
    pub = RAIZ / "Publicacao" / "public_html" / "index.html"
    idx = RAIZ / "index.html"
    if pub.exists() and idx.exists() and pub.stat().st_mtime < idx.stat().st_mtime:
        return ["Publicacao/ desatualizada: rode empacotar.py"]
    return []


CHECKS = [v for k, v in sorted(globals().items()) if k.startswith("check_")]


def main() -> int:
    html, css = ler("index.html"), ler("assets/css/site.css")
    falhas = check_existe(html, css)
    for fn in ([] if falhas else CHECKS):
        if fn is check_pacote_atualizado and "--sem-pacote" in sys.argv:
            continue  # empacotar.py regenera o pacote logo em seguida
        falhas += fn(html, css)
    if falhas:
        print("FALHAS:\n- " + "\n- ".join(falhas))
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
