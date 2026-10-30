"""Baixa os desenhos de Leonardo da Vinci usados em #camadas (domínio público) para referencias/.
Fonte: Wikimedia Commons, Royal Collection. Em uso: RCIN 919072 verso, "Studies of the heart and pulmonary vessels of an ox", c. 1511-13.
Alternativa (não usada hoje): RCIN 912281 recto, "The cardiovascular system and principal organs of a woman", c. 1509-10."""
import json
import urllib.parse
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
UA = {"User-Agent": "SiteDiegoAires/1.0 (dnaires@gmail.com)"}
OBRAS = {
    "leonardo-rcin-919072-verso.jpg": "File:Leonardo da Vinci - RCIN 919072, Verso Studies of the heart and pulmonary vessels of an ox c. 1511-13.jpg",
    "leonardo-rcin-912281.jpg": "File:Leonardo da Vinci - RCIN 912281, The cardiovascular system and principal organs of a woman c.1509-10.jpg",
}


def get(url: str) -> bytes:
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()


if __name__ == "__main__":
    (RAIZ / "referencias").mkdir(exist_ok=True)
    for arq, titulo in OBRAS.items():
        api = "https://commons.wikimedia.org/w/api.php?action=query&format=json&prop=imageinfo&iiprop=url&titles=" + urllib.parse.quote(titulo)
        info = list(json.loads(get(api))["query"]["pages"].values())[0]["imageinfo"][0]
        dest = RAIZ / "referencias" / arq
        dest.write_bytes(get(info["url"]))
        print(f"OK {arq} {dest.stat().st_size // 1024} KB")
