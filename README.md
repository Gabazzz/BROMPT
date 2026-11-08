# Brompt

Catálogo buscável de 120 prompts de IA para quem vende e cria conteúdo no TikTok Shop (imagens, vídeos, automações, copy e estratégia). Busca por intenção com sugestões em tempo real e prévia do resultado de cada prompt antes de copiar.

Baseado no material "120 Prompts Poderosos para Empreender com IA" (Influencers Lab.ia).

## Estrutura

```
index.html          página completa, pronta para abrir direto no navegador ou publicar (ex.: GitHub Pages)
data/prompts.json   os 120 prompts estruturados (id, categoria, título, prompt, para que serve, como usar, resultado esperado, exemplo)
scripts/build_page.py  gera o index.html a partir de data/prompts.json
```

## Editar os prompts

1. Edite `data/prompts.json` (adicionar, remover ou corrigir prompts).
2. Rode:
   ```
   python3 scripts/build_page.py
   ```
3. O `index.html` é regenerado com os dados atualizados — é só abrir o arquivo ou publicar.

## Publicar no GitHub Pages

Em Settings → Pages, aponte para a branch `main` e a pasta raiz (`/`). O site fica disponível em `https://<usuário>.github.io/brompt/`.
