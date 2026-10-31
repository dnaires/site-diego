# Prompts Kling: abertura do site (clipes 2 e 3)

O clipe 1 (`coracao_em_chamas.mp4`) não muda. Para entrar no vídeo 9:16 ele foi enquadrado por código, sem IA: `referencias/clipe1_9x16_v2.mp4` (1080x1920, escala 1,8x centrada no coração, chamas do topo esmaecendo no preto, marca d'água fora do quadro, sem áudio).

Configuração em todos os clipes: modo **imagem para vídeo com quadro inicial E quadro final**, proporção **9:16**, **1080p**, **5 s**, câmera fixa, sem áudio. Gere de 4 a 6 variações de cada clipe e escolha a que chegar mais limpa no quadro final. Baixe **sem marca d'água** (o plano pago do Kling remove).

## Clipe 2: coração em chamas -> coração envolto em fitas

- Quadro inicial: `referencias/clipe1_ultimo_quadro_9x16_v2.png`
- Quadro final: `referencias/coracao_fitas_v2.png`

Prompt:

```
Locked-off camera, no movement, no zoom, no pan. A realistic anatomical human heart engulfed in orange flames on a pure black background. The flames slowly die down and withdraw from the heart. As they fade, thick smooth satin ribbons in deep wine red and warm beige gently grow out of the heart surface and wrap around it in graceful S-shaped curves, following the heart's contours. The heart keeps exactly the same position and size throughout. The ribbons settle into a calm, elegant, sculptural composition. The background stays pure black (0,0,0) at all times. Cinematic, soft studio lighting, high detail, photorealistic, slow and smooth motion.
```

Prompt negativo:

```
text, letters, logo, watermark, caption, subtitles, camera movement, zoom, shaky camera, extra objects, hands, people, background change, colored background, smoke covering the heart, deformed heart, blurry, flicker, cut, scene change
```

Conferir no resultado: o fundo fica preto puro; o coração não muda de posição nem de tamanho; o último quadro bate com `coracao_fitas_v2.png`.

## Clipe 3: coração com fitas -> ícone do logo sobre fundo vinho

- Quadro inicial: `referencias/coracao_fitas_v2.png`
- Quadro final: `referencias/logo_icone_vinho_v2.png`

Prompt:

```
Locked-off camera, no movement, no zoom. A realistic anatomical heart wrapped in wine red and beige satin ribbons on black. The realistic texture, veins and shadows slowly smooth out and simplify, and the ribbons flow and settle into a clean flat vector emblem: a heart whose left side rises as stylized flame-shaped ribbons, in beige and soft rose tones. At the same time the black background gradually turns into a flat solid crimson color (#9D2235), spreading softly from the center to the edges. The emblem ends exactly as in the final reference image, same position, same size, same shape. Smooth, elegant, minimalist, slow motion. No text.
```

Prompt negativo:

```
text, letters, words, logo text, watermark, extra symbols, extra shapes, extra hearts, camera movement, zoom, shake, glow, lens flare, sparkles, particles, gradient background, vignette, textured background, flicker, cut, scene change, deformed shape
```

Conferir no resultado: o fundo termina em cor lisa (#9D2235); nada de texto; o desenho final é o do ícone oficial.

Garantia de exatidão (feita por mim, em código, depois da geração): o ícone **nunca** é gerado pela IA. Nos últimos 8 a 10 quadros do clipe 3 faço um dissolve para `logo_icone_vinho_v2.png`, então o quadro final é exatamente o ícone oficial. A página pinta as laterais com a cor do canto de cada quadro, então o fundo da seção acompanha sem ajuste.

## Se o clipe 3 não ficar bom depois de 6 variações

Opções, em ordem: (1) dividir em dois clipes, fitas -> forma simplificada e forma -> ícone; (2) usar só o dissolve por código (`clipe3_fitas_para_logo_v2.mp4`), que o Dr. Diego não aprovou; (3) dissolve por código com máscara em forma de onda carmim, que eu posso fazer.

## Depois de gerar

Traga os clipes 2 e 3 (e, se quiser, ajusto a ordem). Eu monto 1 + 2 + 3, rodo `Ferramentas/codificar_scroll.py` (all-intra, 1080 e 720, manifest) e empacoto.
