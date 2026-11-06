@echo off
rem Abre o site na sua máquina em http://localhost:8870/
rem Não abra o index.html com duplo clique: o navegador bloqueia a leitura do manifest.json
rem em file:// e a abertura em vídeo não roda. Este atalho sobe o servidor local (com Range,
rem necessário para o vídeo seguir a rolagem) e abre o navegador.
cd /d "%~dp0"
start "Site Diego - servidor local (feche esta janela para parar)" /min python Ferramentas\servir.py 8870 .
timeout /t 2 /nobreak >nul
start "" http://localhost:8870/
