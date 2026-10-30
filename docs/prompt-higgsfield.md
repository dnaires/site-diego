# Clipe da abertura (Higgsfield)

O clipe é só atmosfera. **Não pedir logo nem texto à IA**: a troca para o logo oficial e a oração são feitas em código pela página.

## O que o clipe precisa mostrar (5 a 8 segundos, vertical ou horizontal 16:9)

1. Coração humano real, anatomicamente fiel, em fundo preto, visto de baixo.
2. A câmera gira devagar para cima e para a frente em torno do coração.
3. O coração pega fogo de baixo para cima, de forma súbita.
4. O fogo forma um coração de chamas, **centralizado no quadro e parado nos últimos 1 a 2 segundos**, em tons de brasa dourada e carmim (`#9D2235`, `#D9C89D`).
5. Sem texto, sem letras, sem logo, sem marca d'água, sem pessoas.

## Prompt sugerido (inglês, melhor para o modelo)

> Cinematic macro shot of a real anatomical human heart on a pure black background, seen from below, slowly rotating upward and forward. Suddenly flames ignite at the base and climb upward, consuming the heart until it becomes a glowing heart made of fire, centered in the frame, motionless in the final seconds. Warm amber-gold embers and deep crimson light, volumetric smoke, floating sparks, dark moody chiaroscuro lighting, photorealistic, shallow depth of field. No text, no letters, no logo, no people.

Negativo: `text, letters, watermark, logo, hands, face, cartoon, illustration, blur`.

## Depois de gerar

1. Exportar em MP4 (qualquer resolução a partir de 1280 px de largura).
2. Rodar: `python "Site Diego/Ferramentas/frames_hero.py" "caminho/do/clipe.mp4"`
3. A página passa a usar os quadros sozinha (`assets/hero/manifest.json`). Sem os quadros, a abertura usa um brilho de brasa em CSS.
4. Rodar `python "Site Diego/Ferramentas/verificar.py"` e `empacotar.py`.

Observação: o último quadro precisa ficar com o coração de fogo no centro, porque é nele que o logo oficial se sobrepõe (a página esmaece o vídeo e acende o logo).
