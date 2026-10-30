# CLAUDE.md - Site Dr. Diego Aires

Landing page pessoal do **Dr. Diego Aires** (cardiologista, `@dnaires`). HTML/CSS/JS puros, sem build. Spec: `docs/spec-landing-dr-diego.md`; plano: `docs/plano-implementacao.md`; decisões da execução: `docs/ledger.md`; publicação: `docs/PUBLICAR.md`.

## Estrutura

| Caminho | O que é |
|---|---|
| `index.html` | Página inteira. Seções: `#inicio` (abertura) > `#origem` > `#camadas` > `#pilares` > `#consulta` > `#fe` > `#conteudo` > `#agendar` > rodapé |
| `assets/css/site.css`, `assets/js/site.js`, `assets/js/hero.js` | Estilo, núcleo (Lenis, revelações) e abertura (canvas + oração + logo) |
| `assets/` (resto) | **Derivados**: não editar à mão; regenerar com `Ferramentas/otimizar_assets.py` |
| `assets/hero/` | Quadros do clipe do Higgsfield (gerados por `frames_hero.py`; vazio até o clipe existir) |
| `referencias/` | Obras e imagens baixadas (Leonardo, Vesalius, Batoni). Não publicadas |
| `Publicacao/` | Pacote gerado por `empacotar.py`; não editar à mão (fora do Git: regenere) |

## Comandos (a partir da pasta `Diego/`)

```powershell
python "Site Diego/Ferramentas/verificar.py"        # deve dar OK antes de qualquer entrega
python "Site Diego/Ferramentas/otimizar_assets.py"  # fontes, logos, vendor, fotos, arte
python "Site Diego/Ferramentas/frames_hero.py" "clipe.mp4"
python "Site Diego/Ferramentas/empacotar.py"
```
Prévia: `.claude/launch.json` (em `Diego/`) define `site-diego` na porta 8870.

## Decisões (não reverter sem conversar)

- Marca: carmim `#9D2235`, bege `#D9C89D`, off-white `#D6D2C4`, cinza `#A7A38A`, escuro `#1A1615`. Spectral SC (títulos) e Ubuntu (texto), self-hosted. Sem CDN.
- **Logo** só pelos PNGs oficiais (convertidos em WebP). O PDF oficial não é vetor limpo. Nunca rotacionado. **IA nunca gera o logo**: o vídeo termina num coração de fogo e o código troca pelo logo oficial.
- A oração "Vinde, Espírito Santo" é texto HTML, nunca gerado por IA.
- Arte clássica em `#camadas`: gravura **Tab. IV, Fig. I (com traqueia, letras e legendas), de Niccolò Ricciolini, Roma, 1703**, do livro de Lancisi *De motu cordis et aneurysmatibus* (1728), cópia do Wellcome (domínio público). **Não é de William Harvey** (o *De motu cordis* de Harvey é de 1628 e não tem essas gravuras). Legenda de autoria e ano sob o desenho; fonte no comentário do HTML. Leonardo (RCIN 919072 e 912281), Vesalius e Batoni ficam em `referencias/` como alternativas.
- Fotos: só o Dr. Diego sozinho. Nunca família, crianças ou a Dra. Camila (pasta `Imagens\Fotos profissionais 2024`).
- **Sem travessão** em nenhum texto. CFM 2.336/2023: sem promessa, sem antes/depois, sem depoimento. CRM-DF 19878, RQE 15628 no rodapé e na Origem.
- **Atendimento = Medicina Cardeal** (dados do `Medicina Cardeal/Site Cardeal/CLAUDE.md`): Edifício Via Brasil, SEPS 710/910, Salas 345 e 347, Asa Sul, 70390-108; seg a sex 08h-18h, sáb 08h-12h; (61) 98402-6331 (telefone e WhatsApp, `wa.me/5561984026331` com mensagem em nome do Dr. Diego); contato@medicinacardeal.com.br. Mapa do Google carrega direto na seção (iframe criado por JS). Barra fixa Agendar/Ligar no celular (vinda do Cardeal).
- O Dr. Diego tem RQE em Clínica Médica (não usa). No Site Cardeal, Estilo de Vida e Longevidade são "áreas de interesse", separadas das especialidades.
- Seções compactas: `.sec` com padding `clamp(40px,5vw,68px)` (pedido do cliente, como no Cardeal: não aumentar).
- **Texto**: fatos com nome, lugar e data no lugar de abstrações. Evitar "não é X, é Y", trios de substantivos, "cuidado/escuta/acolhimento" como enfeite e rótulos pequenos acima dos títulos (o Dr. Diego achou o texto parecido com o de sites feitos por IA). Origem: texto curto em primeira pessoa e trajetória em linha do tempo (UFG 2006-2011; Clínica Médica HRAN 2013-2015; Cardiologia HBDF 2015-2017; UTI Hospital Santa Lúcia Sul; CBMDF desde 2022). Atendimento **somente particular**, dito em #agendar. Foto da Origem: diego-sorriso-jaleco em retângulo simples (o painel carmim com recorte foi recusado em 30/10).
- **Seções (estado em 30/10)**: Camadas com listas Ritmo/Pressão/Artérias e Razão/Vontade/Afeto (título só "O coração em duas camadas"). Pilares: título em uma linha ("Uma cruz, com o coração ao centro.") com "Quatro pilares" pequeno, alinhado ao fim do título, abaixo à direita; cruz = silhueta única (`.cruz__forma` em subgrid, contorno por `drop-shadow`, degradê bege) com medalhão no centro, só a partir de 900px; pensadores: Aristóteles (Razão), Viktor Frankl (Emoção), Tomás de Aquino (Espírito, frase "onde todo paciente é acolhido como irmão"). Consulta: lista única, incluindo "Consultas particulares de no mínimo 1h de duração" e "Possibilidade de adesão a planos de acompanhamento contínuo". Fé: "Sou cardiologista e sou Cristão." (sem a frase sobre pacientes de qualquer crença). Conteúdo: kicker + frase + print do Instagram (`assets/img/instagram-grade.webp`, captura de 30/10/2026) fundido no carmim por máscara. Agendar: topo (título, frase, WhatsApp), faixa de 3 colunas (endereço, horário, contato), mapa + cartão carmim da Medicina Cardeal (logo `cardeal-horizontal-negativa.webp`, salta e brilha). Rodapé escuro como o Hero, marca d'água Van Mieris "A visita do médico" (1657, KHM Viena, domínio público), versículo Pv 4:23 com "coração" em Spectral, aviso "ligue 193/192". Botão fixo do cabeçalho abre o WhatsApp.
- Textura de fundo ("papel de gravura"): só proposta em `referencias/texturas.html`; **não aplicada** até o Dr. Diego aprovar.
- Itens não confirmados: `<span class="pendente">A confirmar</span>` + `<!-- TODO -->`. Textos sem fonte: `<!-- RASCUNHO -->`.

## Armadilhas

- No painel de navegador embutido, `requestAnimationFrame` e `IntersectionObserver` não disparam e a tela não repinta durante testes. Por isso as revelações usam scroll listener + `getBoundingClientRect`. Para testar o scrub do hero: `scrollTo`, `ScrollTrigger.update()` e vários `gsap.ticker.tick()` com pausa. Lenis depende de rAF: no painel use `SiteDiego.lenis.destroy()` antes de rolar.
- `pdftocairo` não escreve em caminho com acento: use pasta temporária ASCII.
- Scripts Python: `PYTHONUTF8=1` e `encoding="utf-8"`. O Git foi iniciado em 30/10/2026; `Publicacao/` e `.claude/` ficam fora (ver `.gitignore`). Páginas do Chrome/CSS em cache: ao testar, recarregue com `fetch(url,{cache:"reload"})`.
