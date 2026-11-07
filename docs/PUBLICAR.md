# Publicar o site do Dr. Diego Aires

Endereço definido em 06/11/2026: **https://drdiegoaires.medicinacardeal.com.br/** (subdomínio da Medicina Cardeal, na mesma hospedagem Hostinger, plano Unlimited). Sem `www` na frente. Detalhes do ambiente da Cardeal: `Medicina Cardeal/Site Cardeal/CLAUDE.md` e `Docs/PUBLICAR-NA-HOSTINGER.md`.

## 1. Gerar o pacote (na máquina)

1. `python "Site Diego/Ferramentas/verificar.py"` deve imprimir `OK`.
2. `python "Site Diego/Ferramentas/empacotar.py"` gera `Publicacao/public_html/` e `public_html.zip` (inclui o `.htaccess`, o vídeo `assets/hero/` e tudo que a página usa).

## 2. Criar o subdomínio (uma única vez)

O domínio `medicinacardeal.com.br` fica no **Registro.br** (zona DNS em modo avançado; os nameservers **não** foram trocados, para preservar o e-mail do Google Workspace). Por isso o DNS do subdomínio é criado lá, e não na Hostinger.

1. **DNS no Registro.br** (modo avançado): adicione **somente**
   - `CNAME drdiegoaires` apontando para `medicinacardeal.com.br` (igual ao que já existe para `www`); ou, se preferir, `A drdiegoaires` apontando para o IP da Hostinger (hoje `77.37.127.9`; o assistente "Conectar domínio" do hPanel mostra o valor atual).
   - Opcional: `CNAME www.drdiegoaires` apontando para `medicinacardeal.com.br`. Só serve para quem digitar `www.` na frente; o `.htaccess` redireciona para o endereço sem `www`.
   - **Não mexa** em MX, TXT (google-site-verification, SPF) nem DKIM.
2. **hPanel (Hostinger)**: Domínios → Subdomínios (ou Sites → Adicionar site → subdomínio), domínio `medicinacardeal.com.br`, nome `drdiegoaires`. Pasta padrão: `public_html/drdiegoaires`. Se o hPanel permitir escolher a pasta, prefira uma **fora** do `public_html` da Cardeal (evita que a página também apareça em `www.medicinacardeal.com.br/drdiegoaires/`).
3. **SSL**: hPanel → Segurança → SSL → emitir o certificado grátis para `drdiegoaires.medicinacardeal.com.br` (só funciona depois que o DNS propagar: de minutos a algumas horas).

## 3. Enviar os arquivos

1. hPanel → Gerenciador de arquivos → pasta do subdomínio. Ative "mostrar arquivos ocultos" (o `.htaccess` é oculto).
2. Envie `Publicacao/public_html.zip` (cerca de 25 MB) e extraia **na própria pasta do subdomínio**; apague o ZIP. Confira que `index.html`, `.htaccess` e `assets/` ficaram direto nela, e não numa subpasta.
3. Atualizações futuras: gere o pacote de novo e envie só o que mudou ("Replace"). O vídeo (`assets/hero/`) só precisa subir quando for refeito.

## 4. Testar no ar

- `https://drdiegoaires.medicinacardeal.com.br/` abre, com cadeado, e `http://` redireciona para `https://`.
- A abertura em vídeo **anda com a rolagem** (se travar no primeiro quadro, o servidor não está enviando Range: ver `.htaccess` e o suporte da Hostinger).
- Celular real (Android e iPhone) e Lighthouse (LCP < 2,5 s em 4G).
- `https://drdiegoaires.medicinacardeal.com.br/robots.txt` e `/sitemap.xml` respondem.
- Cartão do WhatsApp/Instagram mostra o `og-image.jpg` (os dois exigem URL absoluta, já preenchida).

## 5. Depois de publicar

- **Search Console**: adicionar a propriedade do subdomínio e enviar o `sitemap.xml`.
- **Link de volta**: no `index.html` do Site Cardeal, preencher o `href` do `[data-doc-link]` ("Conhecer o Dr. Diego") com `https://drdiegoaires.medicinacardeal.com.br/`. Isso também ajuda o Google a ligar as duas páginas.
- **Robots da Cardeal**: se a pasta do subdomínio estiver dentro do `public_html` dela, acrescentar `Disallow: /drdiegoaires/` no `robots.txt` da Cardeal (evita duplicidade). A `canonical` da página já aponta para o subdomínio.
- GitHub Pages (`dnaires.github.io/site-diego`) é só prévia e não é necessário para publicar.

## Pendências antes de divulgar

- [x] **Domínio e hospedagem:** subdomínio escolhido; `canonical`, `og:url`, `og:image`, `robots.txt`, `sitemap.xml` e JSON-LD já usam o endereço.
- [ ] **Criar o subdomínio na Hostinger e o DNS no Registro.br** (seção 2) e enviar o pacote.
- [x] Endereço, horários, telefone e WhatsApp: são os da Medicina Cardeal (já no site e no JSON-LD).
- [x] **Vídeo da abertura:** pronto em `assets/hero/` (ver `CLAUDE.md`).
- [x] **Conteúdo da consulta** (seção `#consulta`) e demais títulos do Dr. Diego.
- [ ] **Relação com a Medicina Cardeal:** confirmar o texto do bloco e preencher o link de volta (seção 5).
- [x] **Revisão do Dr. Diego** de todos os trechos marcados `RASCUNHO` (07/11).
- [ ] **Fotos:** aprovar as usadas (`diego-sorriso-jaleco`, `diego-retrato`) e decidir se as de fundo escuro entram.
- [ ] **Número "cem mil batidas por dia":** só entra com fonte.
- [x] **Privacidade (LGPD):** `privacidade.html` completa em 07/11 (responsável, registros do servidor, WhatsApp, mapa só ao clique, direitos, contato contato@medicinacardeal.com.br). Revisão por advogado continua recomendável.
- [ ] **Métricas:** se houver analytics, atualizar a política e o aviso de cookies antes.
- [ ] **Lighthouse** (LCP < 2,5 s em 4G, acessibilidade) e **teste em celular real**.
