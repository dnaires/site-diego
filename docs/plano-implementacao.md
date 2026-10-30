# Landing Dr. Diego Aires - Plano de Implementação

> **Para quem executar:** usar superpowers:subagent-driven-development (recomendado) ou superpowers:executing-plans, tarefa por tarefa. Passos com checkbox (`- [ ]`). **Esta pasta não é repositório git: não há commit.** O ponto de controle de cada tarefa é rodar `python "Site Diego/Ferramentas/verificar.py"` e ver o resultado indicado.

**Objetivo:** construir a landing page pessoal do Dr. Diego Aires com abertura em scroll (coração em chamas, oração, logo oficial) e as 8 seções da spec.

**Arquitetura:** página estática (HTML + CSS + JS puros, sem build). GSAP, ScrollTrigger e Lenis versionados em `assets/vendor/`. A abertura usa sequência de quadros em `<canvas>`, com fallback de gradiente quando os quadros não existem. Ferramentas Python geram os derivados (`assets/`) e o pacote de publicação.

**Tech Stack:** HTML/CSS/JS, GSAP 3 + ScrollTrigger, Lenis, Python 3.12 (Pillow, fonttools+brotli), `pdftocairo` (poppler), ffmpeg.

**Spec:** `Site Diego/docs/spec-landing-dr-diego.md`

## Global Constraints

- Idioma pt-BR com acentuação correta. **Proibido travessão (—)**; usar "-". Sem emoji.
- Cores: `#9D2235`, `#D9C89D`, `#D6D2C4`, `#A7A38A`, fundo escuro `#1A1615`. Fontes: Spectral SC (títulos), Ubuntu (texto), self-hosted woff2. Sem CDN nem Google Fonts.
- Logo: só pelo SVG derivado do PDF oficial; nunca `rotate`, nunca distorcido; positiva em fundo claro, negativa em fundo escuro. IA nunca gera o logo.
- CRM-DF 19878 e RQE 15628 visíveis no rodapé e em `#origem`. Cardiologista.
- Sem dado, título, estatística, depoimento ou citação além das permitidas (Agostinho, Pascal, Ezequiel 36,26, oração Vinde Espírito Santo). Itens A CONFIRMAR ficam visíveis com `<!-- TODO -->`.
- Sem promessa de resultado, sem antes/depois, sem foto de paciente. **Fotos: só o Dr. Diego sozinho** (nunca família, crianças ou Camila).
- Arte clássica só Leonardo, com `<!-- FONTE: ... -->`.
- Sem `<iframe>` estático. Tudo funciona sem JS (`html.js` só aplicado por script, failsafe de 3 s).
- Fotos escolhidas (proposta, o Dr. Diego aprova): `IMG_9983` (sorriso, jaleco), `IMG_9979` (retrato), `IMG_9992` e `IMG_9995` (fundo escuro). Origem em `C:\Users\kmili\OneDrive\Imagens\Fotos profissionais 2024`, somente leitura.

## Review Focus

- Sem JS ou JS falhando: todo o conteúdo e o CTA continuam visíveis e clicáveis.
- `prefers-reduced-motion` e celular: sem scroll-scrub, oração inteira legível, sem layout quebrado.
- Quadros do hero ausentes (404) ou carregando devagar: a abertura mostra gradiente + logo, sem tela vazia.
- Viewport de 320 px e de 1920 px: oração e cruz dos pilares sem estouro nem sobreposição.
- Âncoras do menu com Lenis ativo, e foco por teclado dentro da abertura fixa.

---

### Task 1: Ferramentas de verificação (testes primeiro)

**Files:**
- Create: `Site Diego/Ferramentas/verificar.py`

**Interfaces:**
- Produces: `python Site Diego/Ferramentas/verificar.py` imprime `OK` e sai com 0, ou lista falhas e sai com 1. Funções `check_*(html: str, css: str) -> list[str]` (lista de falhas).

- [ ] **Step 1: Implementar `verificar.py` com estes testes estáticos** (lê `index.html`, `assets/css/site.css`, `assets/js/site.js`): sem travessão `—` no HTML visível; contém `CRM-DF 19878` e `RQE 15628`; sem `<iframe`; sem `rotate` em regra que afete `.logo`/`img[src*=logo]`; sem `fonts.googleapis`, `cdn.` ou `unpkg`; links locais existem em disco; todo `<img>` tem `alt`, `width`, `height`; `<html lang="pt-BR">`; cada `<section>` tem `id`; `Publicacao/` mais antiga que `index.html` falha (só se `Publicacao/` existir).
- [ ] **Step 2: Rodar com a pasta vazia**
Run: `python "Site Diego/Ferramentas/verificar.py"`
Expected: sai com 1, falha por `index.html` inexistente (prova que o teste detecta).

### Task 2: Derivados de marca e vendor

**Files:**
- Create: `Site Diego/Ferramentas/otimizar_assets.py`
- Create (gerados): `assets/fonts/spectral-sc-{regular,semibold}.woff2`, `assets/fonts/ubuntu-{regular,medium}.woff2`, `assets/logo/logo-{positiva,negativa}-{vertical,horizontal}.svg`, `assets/logo/icone.svg`, `assets/vendor/{gsap.min.js,ScrollTrigger.min.js,lenis.min.js}`, `assets/img/diego-{origem,hero-escuro}.webp`, `assets/favicon.png`, `assets/og-image.jpg`

**Interfaces:**
- Produces: caminhos acima, usados por `index.html` e `site.css`. `icone.svg` é só o coração-chama (recorte do vetor, sem redesenho).

- [ ] **Step 1: Fontes** com `fontTools.ttLib` → woff2 (TTFs de `Logomarcas\Dr Diego Aires\Fonts\`), somente os pesos acima.
- [ ] **Step 2: Logo** com `pdftocairo -svg` sobre os PDFs oficiais das pastas "Marca Positiva/Negativa Colorida" (vertical e horizontal); localizar pastas por prefixo, nunca por nome acentuado literal. Extrair `icone.svg` pelo grupo do ícone.
- [ ] **Step 3: Vendor** baixar GSAP e ScrollTrigger (versão 3.12.5 fixada) e Lenis (1.1.x fixada) do npm tarball ou jsDelivr, **uma vez**, gravando em `assets/vendor/` com comentário da versão. Nada é carregado de CDN em runtime.
- [ ] **Step 4: Fotos** converter as 4 escolhidas para WebP (largura máxima 1600, qualidade 82, EXIF transposto), `favicon.png` (ícone sobre carmim, 180 px) e `og-image.jpg` 1200x630.
- [ ] **Step 5: Verificar**
Run: `python "Site Diego/Ferramentas/otimizar_assets.py"`
Expected: lista cada arquivo gerado com tamanho; abrir `logo-negativa-vertical.svg` no navegador embutido e conferir fidelidade ao PNG oficial.

### Task 3: Base visual (`site.css`) e esqueleto do HTML

**Files:**
- Create: `Site Diego/assets/css/site.css`
- Create: `Site Diego/index.html`

**Interfaces:**
- Produces: tokens `:root` (`--carmim`, `--bege`, `--offwhite`, `--cinza`, `--escuro`), classes `.sec`, `.sec--escuro|carmim|claro|bege`, `.reveal` (alvo do GSAP), `.btn`, `.container`. Ids: `#inicio #origem #camadas #pilares #consulta #fe #conteudo #agendar`. `html.js` ativa o estado oculto de `.reveal`.

- [ ] **Step 1: `site.css`** com `@font-face` (`font-display: swap`), tokens, tipografia fluida (`clamp`), seções e alternância de fundo conforme a tabela da spec, foco visível, `@media (prefers-reduced-motion: reduce)` mostrando tudo.
- [ ] **Step 2: `index.html`** com `<head>` (title e meta "cardiologista em Brasília", OG, canonical `<!-- TODO domínio -->`, preload das fontes) e as 8 seções + rodapé **com o texto final** do brief ajustado à spec (sem travessão; "A fé não substitui o diagnóstico, mas nenhum diagnóstico basta para explicar uma pessoa"). Itens A CONFIRMAR: `<span class="pendente">A confirmar</span>` + `<!-- TODO -->`. Textos sem fonte levam `<!-- RASCUNHO -->`. Rodapé com CRM-DF 19878, RQE 15628, aviso informativo, link `privacidade.html`.
- [ ] **Step 3: Rodar `verificar.py`**
Expected: `OK` (passa agora com HTML estático sem JS). Abrir no navegador embutido (servidor `python -m http.server`, ver `.claude/launch.json`) e conferir cada seção legível em 375 px e 1440 px.

### Task 4: Núcleo de JS (`site.js`): Lenis, revelações, falhas seguras

**Files:**
- Create: `Site Diego/assets/js/site.js`

**Interfaces:**
- Produces: `window.SiteDiego = { reduced: boolean, mobile: boolean, lenis: Lenis|null }`; funções `initSmooth()`, `initReveals()`, `sweepReveals()`. Consumido pelas Tasks 5 a 7.

- [ ] **Step 1: Adicionar `html.js` por script e failsafe de 3 s** que remove o estado oculto. `reduced` vem de `matchMedia('(prefers-reduced-motion: reduce)')`; `mobile` de `(max-width: 768px)`.
- [ ] **Step 2: `initSmooth()`** cria Lenis só se `!reduced`; liga ao ticker do GSAP; âncoras `a[href^="#"]` rolam via `lenis.scrollTo` com `offset` do header.
- [ ] **Step 3: `initReveals()`** com ScrollTrigger (`.reveal`: fade + 24 px); `sweepReveals()` por `setTimeout` como rede de segurança (IntersectionObserver e rAF não disparam no painel embutido).
- [ ] **Step 4: Verificar** no navegador embutido com `document.documentElement.style.scrollBehavior='auto'`: sem erros no console; com JS bloqueado o texto aparece.
Expected: `read_console_messages` sem erros; `verificar.py` → `OK`.

### Task 5: Abertura (hero) com scroll

**Files:**
- Modify: `Site Diego/index.html` (`#inicio`), `assets/css/site.css`, `assets/js/site.js`
- Create: `Site Diego/Ferramentas/frames_hero.py`
- Create: `Site Diego/docs/prompt-higgsfield.md`

**Interfaces:**
- Consumes: `SiteDiego.reduced/mobile`, `assets/logo/icone.svg`.
- Produces: `initHero()`; `frames_hero.py <clipe.mp4>` gera `assets/hero/frame_0001.webp ... frame_N.webp` (N ≤ 150, largura 1280, qualidade 70) e `assets/hero/manifest.json` `{"count": N, "width": 1280, "height": H}`.

- [ ] **Step 1: Estrutura do `#inicio`:** contêiner fixo (`position: sticky`, altura ~400vh), `<canvas id="hero-canvas">`, `<p class="oracao">` com uma `<span>` por palavra da oração (texto exato da spec, "fiéis" acentuado), `<img class="hero-logo">` com `icone.svg`/logo negativa, título "Dr. Diego Aires", subtítulo "Cardiologia preventiva para quem quer chegar antes do problema."
- [ ] **Step 2: Estilo** da oração: Spectral SC dourado `#D9C89D`, `text-shadow` em camadas (brasa), cada palavra com opacidade e brilho animáveis.
- [ ] **Step 3: `initHero()`:** lê `manifest.json`; se ausente (404) ou `reduced`/`mobile`, usa fundo gradiente + oração visível por inteiro + logo (sem scrub). Caso contrário pré-carrega frames em lotes e desenha o frame `round(progress * (count-1))` no canvas via ScrollTrigger (`scrub: true`, `pin: true`). Palavras da oração acendem de forma sequencial; ao ~85%, canvas faz fade e o logo oficial entra por opacidade + scale 0.96→1 (sem rotação).
- [ ] **Step 4: `frames_hero.py`** com `ffmpeg` (`-vf fps=24,scale=1280:-2`), converte para WebP e escreve o manifest. Escrever `docs/prompt-higgsfield.md` com o prompt do clipe (coração humano real, fundo escuro, visão inferior girando para cima e à frente, fogo de baixo para cima, termina em coração de fogo centralizado em dourado/carmim, sem texto, sem logo, 5-8 s) e instruções de exportação.
- [ ] **Step 5: Verificar** sem frames: abertura aparece com gradiente, oração e logo em 375 e 1440 px; com um clipe de teste curto (gerado por ffmpeg `testsrc`) o scrub avança e volta sem travar; `verificar.py` → `OK`.

### Task 6: Camadas e pilares (Leonardo)

**Files:**
- Modify: `Site Diego/index.html` (`#camadas`, `#pilares`), `assets/css/site.css`, `assets/js/site.js`
- Modify: `Site Diego/Ferramentas/otimizar_assets.py` (gera `assets/art/leonardo-coracao.webp`)
- Create: `Site Diego/Ferramentas/baixar_leonardo.py`

**Interfaces:**
- Produces: `initLayers()` (traço do desenho revelado por `clip-path`/máscara no scroll) e `initPillars()` (4 braços da cruz revelados em sequência); `assets/art/leonardo-coracao.webp` em duotone carmim/bege, com `<!-- FONTE: ... -->`.

- [ ] **Step 1: `baixar_leonardo.py`** busca no Wikimedia Commons a maior resolução de "Heart and blood vessels by da Vinci" (domínio público) com User-Agent identificado e salva em `referencias/`. Se só houver a versão de 365x464, usar apenas como detalhe pequeno e registrar a limitação no código.
- [ ] **Step 2: Duotone** (Pillow): luminância → gradiente carmim `#9D2235`→bege `#D9C89D`, WebP.
- [ ] **Step 3: `#camadas`** em duas colunas (biológico: ritmo, pressão, artérias; simbólico: razão, vontade, afeto) com o desenho ao centro; empilha em celular. **`#pilares`** com cruz em CSS grid (ícone `icone.svg` ao centro, **sem rotação**), um parágrafo por pilar sem promessa.
- [ ] **Step 4: Verificar** em 320, 768, 1920 px: sem estouro nem sobreposição; `reduced` mostra tudo estático; `verificar.py` → `OK`.

### Task 7: Consulta, fé, conteúdo, agendar, rodapé e SEO

**Files:**
- Modify: `Site Diego/index.html` (`#consulta #fe #conteudo #agendar`, rodapé), `assets/css/site.css`
- Create: `Site Diego/privacidade.html`, `robots.txt`, `sitemap.xml`

**Interfaces:**
- Produces: botão `.btn--wa` (`href` com `https://wa.me/<TODO>?text=<mensagem em nome do Dr. Diego>`); bloco `.cardeal` com link para `https://www.medicinacardeal.com.br/`; JSON-LD `Physician` com **apenas** nome, especialidade Cardiologia, CRM-DF 19878, RQE 15628, `sameAs` Instagram.

- [ ] **Step 1: Conteúdo das seções** conforme a tabela da spec (Agostinho grande em Spectral SC; Ezequiel e Pascal em menor escala; Instagram `https://www.instagram.com/dnaires/`).
- [ ] **Step 2: Agendar:** canal A CONFIRMAR como placeholder visível; botão "Agende sua consulta" apontando para `#agendar` até haver número, `<!-- TODO -->` no `href` do WhatsApp.
- [ ] **Step 3: `privacidade.html`** (rascunho LGPD, `noindex`), `robots.txt`, `sitemap.xml`, `og-image`, JSON-LD.
- [ ] **Step 4: Verificar**
Run: `python "Site Diego/Ferramentas/verificar.py"`
Expected: `OK`. Conferir o rodapé com CRM-DF 19878 e RQE 15628.

### Task 8: Empacotar e validar

**Files:**
- Create: `Site Diego/Ferramentas/empacotar.py`, `Site Diego/docs/PUBLICAR.md`
- Create (gerado): `Site Diego/Publicacao/public_html/` e `public_html.zip`

**Interfaces:**
- Consumes: todo o site. Produces: pacote de publicação sem `referencias/`, `Ferramentas/`, `docs/`.

- [ ] **Step 1: `empacotar.py`** copia `index.html`, `privacidade.html`, `robots.txt`, `sitemap.xml`, `assets/` (sem `hero/` vazio) para `Publicacao/public_html/` e zipa; repete a cópia se o OneDrive segurar o arquivo.
- [ ] **Step 2: `PUBLICAR.md`** com pendências: domínio, hospedagem, TODOs (canal, endereço, títulos), clipes do Higgsfield, revisão jurídica da privacidade, foto aprovada.
- [ ] **Step 3: Validação final**
Run: `python "Site Diego/Ferramentas/verificar.py"` e `python "Site Diego/Ferramentas/empacotar.py"`
Expected: `OK` nos dois. Depois Lighthouse no navegador (LCP < 2,5 s, acessibilidade ≥ 95) e teste em celular real; relatar o que não pôde ser medido.
