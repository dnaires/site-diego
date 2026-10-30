# Spec - Landing page do Dr. Diego Aires

Data: 29/10/2026 - Status: **aguardando revisão do Dr. Diego** - Idioma da página: português (pt-BR)

## 1. Objetivo e público

- **Objetivo:** página pessoal que apresenta o Dr. Diego (como pensa e como cuida) e leva ao agendamento.
- **Público:** pacientes em Brasília que chegam pelo Instagram `@dnaires` ou por busca.
- **Sucesso:** a página soa como o Diego (autoridade calma, frases curtas), cumpre a CFM 2.336/2023, tem uma abertura marcante em scroll e carrega rápido (LCP abaixo de 2,5 s em 4G).

## 2. Decisões tomadas (não reverter sem conversar)

| Tema | Decisão |
|---|---|
| Tipo | Página única. HTML, CSS e JS puros, **sem build e sem npm** (abordagem A, mesma família do Site Camila) |
| Estrutura | `index.html` + `assets/css/site.css` + `assets/js/site.js` (separados porque a página é grande) |
| Movimento | GSAP + ScrollTrigger + Lenis, arquivos locais em `assets/vendor/`. Nada de CDN |
| Fontes | Spectral SC (títulos) e Ubuntu (texto), woff2 geradas dos TTFs oficiais, em `assets/fonts/`. Sem Google Fonts |
| Logo | SVG derivado do **PDF vetorial oficial**. Nunca rotacionado, distorcido ou recolorido fora da paleta. IA nunca gera o logo |
| Arte clássica | Só **Leonardo da Vinci** (coração e vasos, domínio público) por enquanto. Vesalius e Batoni ficam em `referencias/` como opção futura |
| Tipo de página | Pessoal. Linka a Medicina Cardeal. O link de volta é feito na página da clínica (fora deste projeto) |
| Brief do Claude Chat | É guia, não lei. Esta spec prevalece onde diferir |

## 3. Dados verificados (únicos usáveis)

- Dr. Diego Aires, médico cardiologista, Brasília-DF. **CRM-DF 19878 - RQE 15628.**
- Nasceu no interior do Piauí, em cidade de cerca de 20 mil habitantes, na casa da avó.
- Pai farmacêutico, mãe enfermeira.
- Graduado em Medicina pela UFG (entrou aos 19, formou-se aos 25).
- 15 anos de formado, 10 deles em UTI.
- Católico, o Sagrado Coração de Jesus é sua âncora pessoal.
- Instagram: `@dnaires`.

**A CONFIRMAR (placeholder visível + `TODO` no código):** demais títulos, serviços, endereço, canal de agendamento (WhatsApp/telefone/agenda), conteúdo exato da consulta, o número "cem mil batidas por dia".

## 4. Marca (fonte: `Documentos\Logomarcas\Dr Diego Aires\`, somente leitura)

- **Cores:** carmim `#9D2235`, bege dourado `#D9C89D`, off-white `#D6D2C4`, cinza quente `#A7A38A`. Derivado só para fundo escuro profundo: `#1A1615`. Tokens em `:root`.
- **Fundo escuro/carmim:** Marca Negativa Colorida. **Fundo claro:** Marca Positiva Colorida. Largura mínima 30 mm (equivalente em tela, definir em px no plano). Respeitar a área de proteção do manual.
- **Tom:** médico que pensa, não vendedor. Frases curtas e declarativas, uma ideia por frase. Provocação intelectual sem agressividade. Termo técnico só quando necessário e explicado.

## 5. Regras de conteúdo e CFM 2.336/2023

- Nome completo, CRM-DF e RQE visíveis no rodapé e na seção Origem.
- Sem promessa de resultado, cura ou garantia. Sem antes/depois, depoimento ou foto de paciente. Sem comparação com outros médicos.
- Sem travessão (usar traço simples), sem emoji, sem clichês de marketing médico, sem gerúndio em excesso.
- Citações permitidas, só estas: Agostinho (*Confissões*, I, 1), Pascal (*Pensamentos*), Ezequiel 36,26. Oração "Vinde, Espírito Santo" (domínio público).
- Nenhum dado, estatística ou título inventado.
- Textos sem fonte do usuário levam `<!-- RASCUNHO -->` até aprovação.
- Sem imagem religiosa com direito autoral. Toda obra clássica com fonte e autor indicados no código (`<!-- FONTE: ... -->`).

## 6. Estrutura e conteúdo

```
Site Diego/
  index.html
  privacidade.html     (rascunho LGPD, noindex, precisa de revisão jurídica)
  robots.txt  sitemap.xml
  assets/
    css/site.css   js/site.js   vendor/ (gsap, ScrollTrigger, lenis)
    fonts/  logo/ (svg)  art/ (leonardo duotone)  hero/ (poster + frames)
    favicon.png  og-image.jpg
  Ferramentas/       (verificar.py, otimizar_assets.py, empacotar.py, frames_hero.py)
  Publicacao/        (gerado, não editar à mão)
  referencias/       (obras baixadas, não publicadas)
  docs/              (esta spec, plano, PUBLICAR.md)
```

| # | Seção (`id`) | Fundo | Conteúdo e movimento |
|---|---|---|---|
| 1 | Abertura `#inicio` | `#1A1615` → carmim | Fixa por cerca de 4 telas de rolagem. Vídeo do coração em chamas (sequência de quadros em canvas), oração em letras de brasa (HTML), fogo dissolve no logo oficial, nome e subtítulo |
| 2 | Origem `#origem` | off-white | Texto em blocos de 1-2 frases, revelados ao rolar. Credenciais (CRM-DF, RQE) visíveis |
| 3 | Duas camadas `#camadas` | carmim | Tela dividida: biológico (ritmo, pressão, artérias) e simbólico (razão, vontade, afeto). Desenho de Leonardo em traço bege no centro, que se desenha ao rolar |
| 4 | Pilares `#pilares` | off-white | Cruz com o ícone no centro. Corpo, Razão, Emoção, Espírito, revelados em sequência. Um parágrafo curto cada, sem promessas |
| 5 | Consulta `#consulta` | bege | Lista com filetes finos. Conteúdo exato A CONFIRMAR |
| 6 | Ciência e fé `#fe` | off-white | Agostinho grande em Spectral SC, texto de testemunho, Ezequiel e Pascal em menor escala. Sem pregação |
| 7 | Conteúdo `#conteudo` | carmim | Acesso ao Instagram `@dnaires` |
| 8 | Agendar `#agendar` | bege | Botão "Agende sua consulta" (canal A CONFIRMAR). Bloco Medicina Cardeal com link |
| - | Rodapé | carmim | Nome, Cardiologista, **CRM-DF 19878 - RQE 15628**, endereço (A CONFIRMAR), Instagram, privacidade, aviso de conteúdo informativo |

### 6.1 Abertura (detalhe)

1. **Vídeo de IA (Higgsfield), só atmosfera:** coração humano real, fundo escuro, visto de baixo, girando para cima e para a frente. Pega fogo de baixo para cima de forma súbita e vira um coração de fogo, **terminando centralizado e na cor/posição do ícone** para o encaixe.
2. **Transição para o logo, em código:** o fogo se dissolve (opacidade + brilho) e o SVG oficial assume o lugar, sem rotação e sem deformação.
3. **Oração em HTML:** "Vinde, Espírito Santo, enchei os corações dos vossos fiéis e acendei neles o fogo do vosso amor." Letras douradas com brilho de brasa, reveladas por palavra sincronizadas ao scroll. Nunca texto gerado por IA.
4. **Entregáveis do vídeo:** prompt do clipe (preparado por Claude, executado pelo usuário no Higgsfield, que não tem conector na sessão), depois conversão com ffmpeg em sequência WebP ou MP4 com keyframe em todo quadro (`-g 1`).
5. **Enquanto o clipe não existe:** fundo de gradiente + grão, e o logo revelado em código. A página funciona sem o vídeo.

## 7. Movimento, desempenho e acessibilidade

- GSAP + ScrollTrigger coreografam; Lenis suaviza a rolagem.
- Poster estático carrega primeiro; frames sob demanda depois do LCP.
- **Celular:** poster com fade, oração inteira visível, sem scroll-scrub.
- **`prefers-reduced-motion`:** sem scroll-scrub nem animações de revelação, versão estática completa.
- Contraste AA, alt text descritivo, navegação por teclado, foco visível, `lang="pt-BR"`.
- Sem JS tudo aparece (`html.js` aplicado por script, com failsafe de 3 s), como no Site Camila.
- SEO: `<title>` e meta para "cardiologista em Brasília", schema.org `Physician` com dados confirmados apenas, OG image.
- Mapa/embeds de terceiros só carregam ao clique, sem cookies automáticos.

## 8. Verificação (`Ferramentas/verificar.py`)

Testes estáticos que falham a entrega se: houver travessão no HTML visível; faltar CRM-DF 19878 ou RQE 15628 no rodapé; houver `<iframe>` estático; o logo for rotacionado em CSS (`rotate`) ou distorcido; houver fonte de CDN; `<section>` com texto sem `RASCUNHO` pendente; a `Publicacao/` estiver desatualizada. Depois: Lighthouse (LCP) e teste em celular real.

## 9. Fora de escopo agora

Blog, área do paciente, agendamento próprio, depoimentos, fotos de pacientes, Vesalius e Batoni (opção futura), qualquer geração de logo por IA.

## 10. Pendências

CONFIRMAR: canal de agendamento, endereço, demais títulos, serviços, conteúdo da consulta, "cem mil batidas". Receber os clipes do Higgsfield. Domínio e hospedagem. Revisão jurídica da privacidade. Fotos: pasta `Imagens\Fotos profissionais 2024` (só as do Dr. Diego sozinho; proposta IMG_9983, 9979, 9992, 9995, a aprovar).
