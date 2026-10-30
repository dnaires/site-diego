# Publicar o site do Dr. Diego Aires

1. `python "Site Diego/Ferramentas/verificar.py"` deve imprimir `OK`.
2. `python "Site Diego/Ferramentas/empacotar.py"` gera `Publicacao/public_html/` e `public_html.zip`.
3. Enviar o conteúdo de `public_html/` para a raiz da hospedagem (qualquer hospedagem estática).

## Antes de publicar (pendências)

- [ ] **Domínio e hospedagem.** Trocar `CONFIRMAR-DOMINIO` em `index.html` (canonical), `robots.txt` e `sitemap.xml`.
- [x] Endereço, horários, telefone e WhatsApp: são os da Medicina Cardeal (já no site e no JSON-LD).
- [ ] **Conteúdo da consulta** (seção `#consulta`) e demais títulos do Dr. Diego.
- [ ] **Relação com a Medicina Cardeal:** confirmar o texto do bloco e pedir o link de volta na página da clínica.
- [ ] **Revisão do Dr. Diego** de todos os trechos marcados `RASCUNHO`.
- [ ] **Clipe do Higgsfield:** gerar com `docs/prompt-higgsfield.md` e rodar `Ferramentas/frames_hero.py`. Depois `empacotar.py` de novo.
- [ ] **Fotos:** aprovar as usadas (`diego-sorriso-jaleco`, `diego-retrato`) e decidir se as de fundo escuro entram.
- [ ] **Número "cem mil batidas por dia":** só entra com fonte.
- [ ] **Privacidade (LGPD):** revisão jurídica de `privacidade.html`; e-mail de contato.
- [ ] **Métricas:** se houver analytics, atualizar a política e o aviso de cookies antes.
- [ ] **Lighthouse** (LCP < 2,5 s em 4G, acessibilidade) e **teste em celular real**.
- [ ] **Link de volta:** quando o domínio do site do Dr. Diego existir, preencher o `href` do `[data-doc-link]` ("Conhecer o Dr. Diego") no `index.html` do Site Cardeal.
