"""Servidor de prévia com suporte a Range (o http.server do Python não tem).
Sem Range o <video> não permite seek e a abertura em scroll não anda.
Uso: python Ferramentas/servir.py [porta] [pasta]   (padrão: 8870 e a pasta do site)"""
import os
import re
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

RAIZ = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PORTA = int(sys.argv[1]) if len(sys.argv) > 1 else 8870


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=RAIZ, **k)

    def send_head(self):
        faixa = self.headers.get("Range")
        caminho = self.translate_path(self.path)
        if not faixa or not os.path.isfile(caminho):
            return super().send_head()
        m = re.match(r"bytes=(\d*)-(\d*)$", faixa.strip())
        if not m:
            return super().send_head()
        tam = os.path.getsize(caminho)
        ini = int(m.group(1)) if m.group(1) else max(0, tam - int(m.group(2)))
        fim = int(m.group(2)) if m.group(1) and m.group(2) else tam - 1
        fim = min(fim, tam - 1)
        if ini > fim:
            self.send_error(416)
            return None
        f = open(caminho, "rb")
        f.seek(ini)
        self.send_response(206)
        self.send_header("Content-Type", self.guess_type(caminho))
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Range", f"bytes {ini}-{fim}/{tam}")
        self.send_header("Content-Length", str(fim - ini + 1))
        self.end_headers()
        self._restante = fim - ini + 1
        return f

    def copyfile(self, origem, destino):
        n = getattr(self, "_restante", None)
        if n is None:
            return super().copyfile(origem, destino)
        while n > 0:
            bloco = origem.read(min(65536, n))
            if not bloco:
                break
            destino.write(bloco)
            n -= len(bloco)
        self._restante = None

    def end_headers(self):
        if not self._headers_buffer or b"Accept-Ranges" not in b"".join(self._headers_buffer):
            self.send_header("Accept-Ranges", "bytes")
        super().end_headers()

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    ThreadingHTTPServer(("127.0.0.1", PORTA), Handler).serve_forever()
