import json, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
data = json.load(open(ROOT / 'data' / 'prompts.json', encoding='utf-8'))

CAT_ICON = {
    'imagens': 'img',
    'videos': 'play',
    'tiktok-shop': 'tag',
    'negocios': 'spark',
    'renda-extra': 'coin',
    'marketing': 'megaphone',
    'viral': 'bolt',
    'automacao': 'gear',
    'iniciantes': 'seed',
    'avancado': 'compass',
}

cats = []
seen = set()
for d in data:
    if d['categoria'] not in seen:
        seen.add(d['categoria'])
        cats.append({'nome': d['categoria'], 'slug': d['categoria_slug']})

json_data = json.dumps(data, ensure_ascii=False)
json_data = json_data.replace('</', '<\\/')
json_cats = json.dumps(cats, ensure_ascii=False)
json_cats = json_cats.replace('</', '<\\/')
json_icons = json.dumps(CAT_ICON, ensure_ascii=False)

TEMPLATE = r'''<meta name="claude:viewport-fit-sides" content="cover">
<title>Brompt</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,340..760&family=Work+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
/* Layout: a card-catalog drawer — search flips through numbered index cards; picking one pulls its full card into a reading panel */
:root{
  --bg:#17120d;
  --surface:#221a13;
  --fg:#f3ece1;
  --muted:#a89a8a;
  --accent:#ff5a36;
  --accent-fg:#1c0800;
  --line:#3a2d20;

  --font-display:'Fraunces',Georgia,serif;
  --font-body:'Work Sans',system-ui,-apple-system,sans-serif;
  --font-mono:'IBM Plex Mono','SFMono-Regular',Menlo,monospace;
  color-scheme:dark;
}
@media (prefers-color-scheme: light){
  :root:not([data-theme="dark"]){
    --bg:#f5efe3;
    --surface:#fffdf8;
    --fg:#201810;
    --muted:#6e6050;
    --accent:#d94c21;
    --accent-fg:#fff6ef;
    --line:#e3d7c3;
    color-scheme:light;
  }
}
:root[data-theme="light"]{
  --bg:#f5efe3;
  --surface:#fffdf8;
  --fg:#201810;
  --muted:#6e6050;
  --accent:#d94c21;
  --accent-fg:#fff6ef;
  --line:#e3d7c3;
  color-scheme:light;
}

*{box-sizing:border-box;}
html,body{height:100%;}
body{
  margin:0;
  background:var(--bg);
  color:var(--fg);
  font-family:var(--font-body);
  padding-left:max(16px, env(safe-area-inset-left,0px));
  padding-right:max(16px, env(safe-area-inset-right,0px));
  position:relative;
}
body::before{
  content:"";
  position:fixed;
  inset:0 0 auto;
  height:env(safe-area-inset-top,0px);
  z-index:10;
  background:var(--bg);
}
::selection{background:var(--accent);color:var(--accent-fg);}

.grain{
  position:fixed;inset:0;z-index:1;pointer-events:none;
  opacity:.05;mix-blend-mode:overlay;
  background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='160' height='160'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2' stitchTiles='stitch'/></filter><rect width='100%25' height='100%25' filter='url(%23n)'/></svg>");
}

.page{max-width:1040px;margin:0 auto;padding-block:48px 80px;position:relative;z-index:2;}

.topbar{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:40px;}
.brand{font-family:var(--font-display);font-weight:700;font-size:22px;letter-spacing:-0.01em;}
.brand__dot{color:var(--accent);}
.brand__meta{font-family:var(--font-mono);font-size:11px;color:var(--muted);letter-spacing:.03em;white-space:nowrap;font-variant-numeric:tabular-nums;}

.theme-toggle{
  border:1px solid var(--line);background:var(--surface);color:var(--muted);
  width:34px;height:34px;border-radius:999px;display:flex;align-items:center;justify-content:center;
  cursor:pointer;flex:none;transition:color .15s ease,border-color .15s ease,transform .15s ease;
}
.theme-toggle:hover{color:var(--fg);border-color:var(--accent);}
.theme-toggle:active{transform:scale(.92);}
.theme-toggle svg{transition:transform .45s cubic-bezier(.34,1.56,.64,1);}
.theme-toggle.is-spinning svg{transform:rotate(180deg);}
.topbar__meta{display:flex;align-items:center;gap:14px;}

.hero{margin-bottom:36px;}
.hero__title{
  font-family:var(--font-display);
  font-weight:600;
  font-size:clamp(28px,5vw,46px);
  line-height:1.08;
  letter-spacing:-0.015em;
  margin:0 0 14px;
  max-width:16ch;
  display:flex;flex-direction:column;
}
.reveal-line{display:block;}
.reveal-accent{color:var(--accent);}
.hero__sub{
  font-size:16px;
  color:var(--muted);
  max-width:46ch;
  line-height:1.55;
  margin:0;
}

.search{margin-bottom:28px;position:relative;}
.search__box{
  display:flex;align-items:center;gap:10px;
  background:var(--surface);
  border:1.5px solid var(--line);
  border-radius:14px;
  padding:14px 16px;
  transition:border-color .18s ease, box-shadow .18s ease;
}
.search__box:focus-within{border-color:var(--accent);box-shadow:0 0 0 4px color-mix(in srgb, var(--accent) 16%, transparent);}
.search__box svg{flex:none;color:var(--muted);transition:color .18s ease;}
.search__box:focus-within svg{color:var(--accent);}
.search__box input{
  flex:1;min-width:0;
  background:none;border:none;outline:none;
  font-family:var(--font-body);font-size:16px;color:var(--fg);
  padding:2px 0;
}
.search__box input::placeholder{color:var(--muted);}
.search__clear{
  flex:none;border:none;background:none;color:var(--muted);cursor:pointer;
  font-size:20px;line-height:1;padding:4px 6px;border-radius:8px;transition:color .15s ease,background .15s ease;
}
.search__clear:hover{color:var(--fg);background:var(--line);}

.suggestions{
  position:absolute;left:0;right:0;top:calc(100% + 8px);
  background:var(--surface);
  border:1px solid var(--line);
  border-radius:14px;
  overflow:hidden;
  z-index:30;
  box-shadow:0 18px 40px -16px rgba(0,0,0,.45);
  opacity:0;transform:translateY(-6px) scale(.99);
  transition:opacity .16s ease, transform .16s ease;
  pointer-events:none;
}
.suggestions.is-open{opacity:1;transform:none;pointer-events:auto;}
.suggestions__item{
  display:flex;align-items:baseline;gap:10px;
  padding:12px 16px;
  cursor:pointer;
  border-bottom:1px solid var(--line);
  transition:background .12s ease;
}
.suggestions__item:last-child{border-bottom:none;}
.suggestions__item:hover,.suggestions__item.is-active{background:var(--bg);}
.suggestions__id{font-family:var(--font-mono);font-size:11px;color:var(--accent);flex:none;}
.suggestions__title{font-weight:600;font-size:14.5px;flex:none;}
.suggestions__cat{font-size:12.5px;color:var(--muted);min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}

.quickrow{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px;}
.quickrow__label{font-size:12.5px;color:var(--muted);align-self:center;margin-right:2px;}
.quick{
  font-family:var(--font-body);font-size:13px;color:var(--fg);
  background:var(--surface);border:1px solid var(--line);border-radius:999px;
  padding:7px 13px;cursor:pointer;transition:border-color .15s ease, transform .1s ease;
}
.quick:hover{border-color:var(--accent);}
.quick:active{transform:scale(.96);}

.chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:18px;}
.chip{
  display:flex;align-items:center;gap:6px;
  font-family:var(--font-body);font-size:13px;font-weight:500;
  background:var(--surface);border:1px solid var(--line);color:var(--muted);
  border-radius:999px;padding:7px 14px 7px 11px;cursor:pointer;white-space:nowrap;
  transition:background .15s ease, border-color .15s ease, color .15s ease, transform .1s ease;
}
.chip svg{flex:none;opacity:.8;transition:opacity .15s ease;}
.chip:hover{color:var(--fg);border-color:var(--accent);}
.chip:active{transform:scale(.96);}
.chip.is-active{background:var(--accent);border-color:var(--accent);color:var(--accent-fg);}
.chip.is-active svg{color:var(--accent-fg);opacity:1;}
.chip__count{font-family:var(--font-mono);font-size:11px;opacity:.75;font-variant-numeric:tabular-nums;}

.results__head{
  display:flex;align-items:baseline;justify-content:space-between;
  margin:36px 0 16px;
  padding-bottom:10px;
  border-bottom:1px solid var(--line);
}
.results__count{font-family:var(--font-mono);font-size:12.5px;color:var(--muted);letter-spacing:.02em;font-variant-numeric:tabular-nums;}

.grid{
  display:grid;
  grid-template-columns:repeat(auto-fill,minmax(260px,1fr));
  gap:14px;
}
.card{
  text-align:left;
  background:var(--surface);
  border:1px solid var(--line);
  border-radius:16px;
  padding:18px;
  cursor:pointer;
  font-family:inherit;color:inherit;
  display:flex;flex-direction:column;gap:10px;
  min-width:0;position:relative;overflow:hidden;
  transition:border-color .2s ease, transform .2s ease, box-shadow .2s ease;
}
.card::after{
  content:"";position:absolute;inset:0;pointer-events:none;border-radius:inherit;
  background:radial-gradient(220px circle at var(--mx,50%) var(--my,0%), color-mix(in srgb, var(--accent) 16%, transparent), transparent 62%);
  opacity:0;transition:opacity .25s ease;
}
.card:hover{border-color:var(--accent);transform:translateY(-3px);box-shadow:0 16px 32px -20px rgba(0,0,0,.5);}
.card:hover::after{opacity:1;}
.card:active{transform:translateY(-1px);}
.card__top{display:flex;align-items:center;justify-content:space-between;gap:8px;}
.card__id{font-family:var(--font-mono);font-size:11px;color:var(--accent);}
.card__cat{font-family:var(--font-mono);font-size:10.5px;color:var(--muted);text-transform:uppercase;letter-spacing:.04em;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;min-width:0;}
.card__title{font-family:var(--font-display);font-weight:600;font-size:18px;line-height:1.22;margin:0;}
.card__desc{font-size:13.5px;color:var(--muted);line-height:1.5;margin:0;
  display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;}
.card__foot{font-size:12.5px;color:var(--accent);font-weight:600;margin-top:auto;display:flex;align-items:center;gap:5px;}
.card__foot svg{transition:transform .2s ease;}
.card:hover .card__foot svg{transform:translateX(3px);}

.empty{
  text-align:center;padding:56px 20px;color:var(--muted);
  border:1px dashed var(--line);border-radius:16px;
}
.empty strong{color:var(--fg);display:block;font-family:var(--font-display);font-size:19px;margin-bottom:6px;font-weight:600;}

.footer{margin-top:60px;padding-top:20px;border-top:1px solid var(--line);
  display:flex;flex-wrap:wrap;gap:8px;justify-content:space-between;color:var(--muted);font-size:12.5px;}

/* overlay / detail panel */
.overlay{
  position:fixed;inset:0;z-index:50;
  background:color-mix(in srgb, var(--bg) 45%, black 55%);
  display:flex;justify-content:flex-end;
  padding-left:max(16px, env(safe-area-inset-left,0px));
  padding-right:max(16px, env(safe-area-inset-right,0px));
  opacity:0;transition:opacity .22s ease;
}
.overlay.is-open{opacity:1;}
.panel{
  background:var(--bg);
  width:min(560px,100%);
  height:100%;
  overflow-y:auto;
  padding:28px 26px calc(40px + env(safe-area-inset-bottom,0px));
  position:relative;
  border-left:1px solid var(--line);
  transform:translateX(26px);opacity:0;
  transition:transform .32s cubic-bezier(.16,1,.3,1), opacity .28s ease;
}
.overlay.is-open .panel{transform:none;opacity:1;}
.panel__close{
  position:absolute;top:18px;right:18px;
  width:34px;height:34px;border-radius:999px;
  border:1px solid var(--line);background:var(--surface);color:var(--fg);
  font-size:18px;cursor:pointer;line-height:1;transition:border-color .15s ease,transform .1s ease;
}
.panel__close:hover{border-color:var(--accent);}
.panel__close:active{transform:scale(.92);}
.panel__eyebrow{display:flex;align-items:center;gap:6px;font-family:var(--font-mono);font-size:11.5px;color:var(--accent);letter-spacing:.03em;margin:0 0 10px;text-transform:uppercase;}
.panel__title{font-family:var(--font-display);font-weight:600;font-size:clamp(24px,4vw,32px);line-height:1.1;margin:0 0 22px;max-width:22ch;text-wrap:balance;}

.preview{
  background:var(--surface);
  border:1px solid var(--line);
  border-radius:16px;
  padding:20px;
  margin-bottom:22px;
}
.preview__label{display:flex;align-items:center;gap:8px;font-size:12.5px;color:var(--muted);margin-bottom:10px;}
.preview__label svg{color:var(--accent);}
.preview__result{font-family:var(--font-display);font-size:17px;line-height:1.45;margin:0 0 12px;font-weight:500;}
.preview__example{font-size:13.5px;color:var(--muted);line-height:1.55;margin:0;padding-top:12px;border-top:1px dashed var(--line);}
.preview__example b{color:var(--fg);font-weight:600;}

.section{margin-bottom:22px;}
.section__label{font-family:var(--font-mono);font-size:11.5px;color:var(--muted);text-transform:uppercase;letter-spacing:.04em;margin:0 0 8px;}
.section__text{font-size:14.5px;line-height:1.6;margin:0;}

.promptbox{
  background:var(--surface);border:1px solid var(--line);border-radius:14px;
  padding:16px;position:relative;
}
.promptbox pre{
  margin:0;font-family:var(--font-mono);font-size:13px;line-height:1.6;color:var(--fg);
  white-space:pre-wrap;word-break:break-word;padding-right:80px;
}
.copybtn{
  position:absolute;top:12px;right:12px;
  font-family:var(--font-body);font-size:12.5px;font-weight:600;
  background:var(--accent);color:var(--accent-fg);border:none;border-radius:8px;
  padding:7px 12px;cursor:pointer;transition:filter .15s ease, transform .15s ease;
}
.copybtn:hover{filter:brightness(1.08);}
.copybtn.is-done{background:var(--surface);color:var(--fg);border:1px solid var(--line);}

[hidden]{display:none!important;}

/* entrance choreography — only for viewers who haven't asked for less motion */
.motion-ok .reveal,
.motion-ok .reveal-line{opacity:0;transform:translateY(14px);animation:revealUp .62s cubic-bezier(.16,1,.3,1) forwards;animation-delay:calc(var(--d,0) * 70ms + 40ms);}
.motion-ok .card{opacity:0;transform:translateY(10px);animation:cardIn .4s cubic-bezier(.16,1,.3,1) forwards;animation-delay:calc(min(var(--i,0),16) * 26ms);}
.motion-ok .copybtn.is-done{animation:pop .32s ease;}
@keyframes revealUp{to{opacity:1;transform:none;}}
@keyframes cardIn{to{opacity:1;transform:none;}}
@keyframes pop{0%{transform:scale(1);}45%{transform:scale(1.07);}100%{transform:scale(1);}}

@media (max-width:640px){
  .page{padding-block:32px 60px;}
  .panel{width:100%;}
  .grid{grid-template-columns:1fr 1fr;}
}
@media (max-width:420px){
  .grid{grid-template-columns:1fr;}
}
</style>

<script>try{if(window.matchMedia && matchMedia('(prefers-reduced-motion: no-preference)').matches){document.documentElement.classList.add('motion-ok');}}catch(e){}</script>
<div class="grain" aria-hidden="true"></div>

<div class="page">
  <div class="topbar reveal" style="--d:0">
    <span class="brand">Brompt<span class="brand__dot">.</span></span>
    <div class="topbar__meta">
      <span class="brand__meta"><span class="count" data-target="120">120</span> PROMPTS · <span class="count" data-target="10">10</span> CATEGORIAS</span>
      <button class="theme-toggle" id="themeToggle" title="Alternar tema" aria-label="Alternar tema">
        <svg id="themeIcon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="5"></circle><path d="M12 1v2M12 21v2M4.2 4.2l1.4 1.4M18.4 18.4l1.4 1.4M1 12h2M21 12h2M4.2 19.8l1.4-1.4M18.4 5.6l1.4-1.4"></path></svg>
      </button>
    </div>
  </div>

  <header class="hero">
    <h1 class="hero__title">
      <span class="reveal-line" style="--d:1">Descreva o que</span>
      <span class="reveal-line" style="--d:2">você quer criar.</span>
      <span class="reveal-line reveal-accent" style="--d:3">A gente acha o</span>
      <span class="reveal-line reveal-accent" style="--d:4">prompt certo.</span>
    </h1>
    <p class="hero__sub reveal" style="--d:5">Catálogo vivo de prompts de IA para quem vende e cria conteúdo no TikTok Shop — imagens, vídeos, automações, copy e estratégia.</p>
  </header>

  <section class="search reveal" style="--d:6">
    <div class="search__box">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="7"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
      <input id="searchInput" type="text" placeholder="Ex.: quero um depoimento em vídeo pra anúncio" autocomplete="off" aria-label="Buscar prompt">
      <button class="search__clear" id="clearBtn" hidden aria-label="Limpar busca">×</button>
    </div>
    <div class="suggestions" id="suggestions" hidden></div>

    <div class="quickrow reveal" id="quickrow" style="--d:7">
      <span class="quickrow__label">Tente:</span>
    </div>

    <div class="chips reveal" id="chips" style="--d:8"></div>
  </section>

  <section class="results">
    <div class="results__head reveal" style="--d:9">
      <span class="results__count" id="resultsCount"></span>
    </div>
    <div class="grid" id="grid"></div>
    <div class="empty" id="empty" hidden>
      <strong>Nenhum prompt encontrado</strong>
      Tente outras palavras ou escolha uma categoria abaixo.
    </div>
  </section>

  <footer class="footer">
    <span>Brompt · biblioteca de prompts com IA</span>
    <span>Baseado em 120 Prompts Poderosos para Empreender com IA</span>
  </footer>
</div>

<div class="overlay" id="overlay" hidden>
  <div class="panel" id="panel" role="dialog" aria-modal="true" aria-label="Detalhe do prompt">
    <button class="panel__close" id="closeBtn" aria-label="Fechar">×</button>
    <div id="panelContent"></div>
  </div>
</div>

<script>
const MOTION_OK = document.documentElement.classList.contains('motion-ok');
const PROMPTS = __PROMPTS__;
const CATEGORIES = __CATEGORIES__;
const ICONS = {
  img:'<path d="M3 5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><circle cx="8.5" cy="9.5" r="1.5"/><path d="M21 15l-5-5L5 21"/>',
  play:'<circle cx="12" cy="12" r="9"/><path d="M10 8l6 4-6 4z"/>',
  tag:'<path d="M20.59 13.41L11 3.83A2 2 0 0 0 9.59 3.17H4a1 1 0 0 0-1 1v5.59a2 2 0 0 0 .59 1.41l9.59 9.58a2 2 0 0 0 2.82 0l4.59-4.59a2 2 0 0 0 0-2.58z"/><circle cx="7.5" cy="7.5" r="1.1"/>',
  spark:'<path d="M12 2l1.8 5.6L19 9l-5.2 1.4L12 16l-1.8-5.6L5 9l5.2-1.4z"/>',
  coin:'<circle cx="12" cy="12" r="9"/><path d="M9.5 15.3c.4.9 1.3 1.5 2.5 1.5 1.6 0 2.8-1 2.8-2.3 0-3-5.5-1.7-5.5-4.8 0-1.3 1.2-2.3 2.8-2.3 1.2 0 2.1.6 2.5 1.5M12 6.5v11"/>',
  megaphone:'<path d="M3 11v2a2 2 0 0 0 2 2h1l3 5h2l-1-5h4l6 4V6l-6 4H6a2 2 0 0 0-2 1z"/>',
  bolt:'<path d="M13 2L4 14h6l-1 8 9-12h-6z"/>',
  gear:'<circle cx="12" cy="12" r="3.2"/><path d="M19.4 13.5a1.7 1.7 0 0 0 .3 1.9l.1.1a2 2 0 1 1-2.9 2.9l-.1-.1a1.7 1.7 0 0 0-1.9-.3 1.7 1.7 0 0 0-1 1.6v.2a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1.1-1.6 1.7 1.7 0 0 0-1.9.3l-.1.1a2 2 0 1 1-2.9-2.9l.1-.1a1.7 1.7 0 0 0 .3-1.9 1.7 1.7 0 0 0-1.6-1H4a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.6-1 1.7 1.7 0 0 0-.3-1.9l-.1-.1a2 2 0 1 1 2.9-2.9l.1.1a1.7 1.7 0 0 0 1.9.3h.1a1.7 1.7 0 0 0 1-1.6V4a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.6h.1a1.7 1.7 0 0 0 1.9-.3l.1-.1a2 2 0 1 1 2.9 2.9l-.1.1a1.7 1.7 0 0 0-.3 1.9v.1a1.7 1.7 0 0 0 1.6 1H20a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.6 1z"/>',
  seed:'<path d="M12 22c4-1 8-5 8-11a8 8 0 0 0-8-8 8 8 0 0 0-8 8c0 6 4 10 8 11z"/><path d="M12 22V9"/>',
  compass:'<circle cx="12" cy="12" r="9"/><path d="M15.5 8.5l-2 5-5 2 2-5z"/>',
  arrow:'<path d="M5 12h14M13 6l6 6-6 6"/>'
};
const CAT_ICON = __ICONS__;

const SYN = {
  foto:'imagem', fotos:'imagem', imagens:'imagem', imagem:'imagem',
  video:'vídeo', vídeos:'vídeo', videos:'vídeo',
  vender:'vendas', venda:'vendas', vendas:'vendas', vendi:'vendas',
  cliente:'clientes', clientes:'clientes',
  anuncio:'anúncio', anuncios:'anúncio', anúncios:'anúncio', ads:'anúncio',
  depoimento:'depoimento', testemunho:'depoimento', prova:'depoimento',
  dinheiro:'renda', ganhar:'renda', lucro:'renda', faturar:'renda', faturamento:'renda',
  negocio:'negócio', negócios:'negócio', empresa:'negócio',
  automatizar:'automação', automatico:'automação', automática:'automação', bot:'automação',
  viral:'viral', viralizar:'viral', engajamento:'viral',
  curso:'curso', ebook:'ebook', infoproduto:'produto', produto:'produto',
  afiliado:'afiliado', afiliados:'afiliado', comissao:'afiliado', comissão:'afiliado',
  influenciador:'influenciadora', influencer:'influenciadora', influenciadora:'influenciadora',
  shop:'tiktokshop', tiktokshop:'tiktokshop',
  copy:'copy', texto:'copy', legenda:'copy',
  email:'email', mentoria:'mentoria', freelancer:'freelancer', dropshipping:'dropshipping',
  seguidores:'seguidores', instagram:'instagram', reels:'reels', shorts:'shorts', youtube:'youtube',
  comecar:'iniciante', começar:'iniciante', iniciante:'iniciante', iniciar:'iniciante',
  estrategia:'estratégia', estratégia:'estratégia', planejamento:'estratégia',
  webinar:'webinar', live:'live', mockup:'mockup', capa:'capa',
  roteiro:'roteiro', script:'roteiro'
};

function normalize(s){
  return (s||'').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'');
}
function expand(tokens){
  const out = new Set();
  tokens.forEach(t=>{
    out.add(t);
    const syn = SYN[t];
    if(syn) out.add(normalize(syn));
  });
  return [...out];
}

const INDEX = PROMPTS.map(p=>({
  p,
  title:normalize(p.titulo),
  cat:normalize(p.categoria),
  serve:normalize(p.para_que_serve),
  usar:normalize(p.como_usar),
  res:normalize(p.resultado_esperado),
  prompt:normalize(p.prompt)
}));

function score(entry, tokens){
  let s = 0;
  tokens.forEach(t=>{
    if(entry.title.includes(t)) s += entry.title===t?6:5;
    if(entry.cat.includes(t)) s += 3;
    if(entry.serve.includes(t)) s += 4;
    if(entry.usar.includes(t)) s += 2;
    if(entry.res.includes(t)) s += 2;
    if(entry.prompt.includes(t)) s += 1;
  });
  return s;
}

function search(query, activeCat){
  const q = normalize(query).trim();
  const tokens = q.length ? expand(q.split(/\s+/).filter(t=>t.length>1)) : [];
  let list = INDEX;
  if(activeCat){
    list = list.filter(e=>e.p.categoria_slug===activeCat);
  }
  if(!tokens.length){
    return list.map(e=>e.p);
  }
  const scored = list.map(e=>({p:e.p, s:score(e, tokens)}))
    .filter(e=>e.s>0)
    .sort((a,b)=>b.s-a.s);
  return scored.map(e=>e.p);
}

let activeCategory = null;
let currentQuery = '';

const els = {
  input: document.getElementById('searchInput'),
  clear: document.getElementById('clearBtn'),
  suggestions: document.getElementById('suggestions'),
  chips: document.getElementById('chips'),
  quickrow: document.getElementById('quickrow'),
  grid: document.getElementById('grid'),
  count: document.getElementById('resultsCount'),
  empty: document.getElementById('empty'),
  overlay: document.getElementById('overlay'),
  panel: document.getElementById('panel'),
  panelContent: document.getElementById('panelContent'),
  closeBtn: document.getElementById('closeBtn'),
};

function iconSvg(slug, size){
  size = size || 14;
  return '<svg width="'+size+'" height="'+size+'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'+(ICONS[CAT_ICON[slug]]||'')+'</svg>';
}

function renderChips(){
  const counts = {};
  PROMPTS.forEach(p=>{counts[p.categoria_slug]=(counts[p.categoria_slug]||0)+1;});
  els.chips.innerHTML = CATEGORIES.map(c=>{
    const active = activeCategory===c.slug ? ' is-active':'';
    return '<button class="chip'+active+'" data-slug="'+c.slug+'">'+iconSvg(c.slug)+'<span>'+c.nome+'</span><span class="chip__count">'+counts[c.slug]+'</span></button>';
  }).join('');
  els.chips.querySelectorAll('.chip').forEach(btn=>{
    btn.addEventListener('click', ()=>{
      const slug = btn.getAttribute('data-slug');
      activeCategory = activeCategory===slug ? null : slug;
      renderChips();
      runSearch();
    });
  });
}

const QUICK_EXAMPLES = [
  'depoimento em vídeo pra anúncio',
  'foto de produto pra loja',
  'validar ideia de produto digital',
  'automatizar atendimento ao cliente',
  'ganhar dinheiro com afiliados'
];
function renderQuick(){
  els.quickrow.innerHTML = '<span class="quickrow__label">Tente:</span>' +
    QUICK_EXAMPLES.map(q=>'<button class="quick" data-q="'+q+'">'+q+'</button>').join('');
  els.quickrow.querySelectorAll('.quick').forEach(btn=>{
    btn.addEventListener('click', ()=>{
      els.input.value = btn.getAttribute('data-q');
      currentQuery = els.input.value;
      els.clear.hidden = false;
      hideSuggestions();
      runSearch();
    });
  });
}

function cardHtml(p, i){
  return '<button class="card" data-id="'+p.id+'" style="--i:'+i+'">'+
    '<div class="card__top"><span class="card__id">#'+p.id+'</span><span class="card__cat">'+p.categoria+'</span></div>'+
    '<h3 class="card__title">'+p.titulo+'</h3>'+
    '<p class="card__desc">'+p.para_que_serve+'</p>'+
    '<span class="card__foot">Ver prévia '+iconSvg('arrow',13)+'</span>'+
  '</button>';
}

function renderGrid(list){
  if(!list.length){
    els.grid.hidden = true;
    els.empty.hidden = false;
    els.count.textContent = '';
    return;
  }
  els.grid.hidden = false;
  els.empty.hidden = true;
  els.grid.innerHTML = list.map(cardHtml).join('');
  els.grid.querySelectorAll('.card').forEach(c=>{
    c.addEventListener('click', ()=>openDetail(c.getAttribute('data-id')));
    if(MOTION_OK){
      c.addEventListener('pointermove', e=>{
        const r = c.getBoundingClientRect();
        c.style.setProperty('--mx', (e.clientX-r.left)+'px');
        c.style.setProperty('--my', (e.clientY-r.top)+'px');
      });
    }
  });
  const base = currentQuery.trim() || activeCategory ? list.length+' '+(list.length===1?'prompt encontrado':'prompts encontrados') : 'Mostrando todos os '+list.length+' prompts';
  els.count.textContent = base;
}

function runSearch(){
  const list = search(currentQuery, activeCategory);
  renderGrid(list);
}

function renderSuggestions(){
  const q = currentQuery.trim();
  if(!q){ hideSuggestions(); return; }
  const list = search(q, null).slice(0,5);
  if(!list.length){ hideSuggestions(); return; }
  els.suggestions.innerHTML = list.map(p=>
    '<div class="suggestions__item" data-id="'+p.id+'">'+
      '<span class="suggestions__id">#'+p.id+'</span>'+
      '<span class="suggestions__title">'+p.titulo+'</span>'+
      '<span class="suggestions__cat">'+p.categoria+'</span>'+
    '</div>'
  ).join('');
  els.suggestions.hidden = false;
  requestAnimationFrame(()=>els.suggestions.classList.add('is-open'));
  els.suggestions.querySelectorAll('.suggestions__item').forEach(item=>{
    item.addEventListener('click', ()=>{
      hideSuggestions();
      openDetail(item.getAttribute('data-id'));
    });
  });
}
function hideSuggestions(){
  if(els.suggestions.hidden) return;
  els.suggestions.classList.remove('is-open');
  setTimeout(()=>{ els.suggestions.hidden = true; els.suggestions.innerHTML=''; }, 160);
}

function openDetail(id){
  const p = PROMPTS.find(x=>x.id===id);
  if(!p) return;
  els.panelContent.innerHTML =
    '<p class="panel__eyebrow">'+iconSvg(p.categoria_slug,12)+'<span>'+p.categoria+' · #'+p.id+'</span></p>'+
    '<h2 class="panel__title">'+p.titulo+'</h2>'+
    '<div class="preview">'+
      '<div class="preview__label">'+iconSvg('spark',14)+'<span>Prévia do que você recebe</span></div>'+
      '<p class="preview__result">'+p.resultado_esperado+'</p>'+
      '<p class="preview__example"><b>Exemplo de uso: </b>'+p.exemplo_resultado+'</p>'+
    '</div>'+
    '<div class="section">'+
      '<p class="section__label">Para que serve</p>'+
      '<p class="section__text">'+p.para_que_serve+'</p>'+
    '</div>'+
    '<div class="section">'+
      '<p class="section__label">Prompt completo</p>'+
      '<div class="promptbox"><pre id="promptText">'+p.prompt+'</pre><button class="copybtn" id="copyBtn">Copiar</button></div>'+
    '</div>'+
    '<div class="section">'+
      '<p class="section__label">Como usar</p>'+
      '<p class="section__text">'+p.como_usar+'</p>'+
    '</div>';

  const copyBtn = document.getElementById('copyBtn');
  copyBtn.addEventListener('click', ()=>{
    const text = p.prompt;
    const done = ()=>{
      copyBtn.textContent = 'Copiado!';
      copyBtn.classList.add('is-done');
      setTimeout(()=>{copyBtn.textContent='Copiar';copyBtn.classList.remove('is-done');},1600);
    };
    if(navigator.clipboard && navigator.clipboard.writeText){
      navigator.clipboard.writeText(text).then(done).catch(()=>fallbackCopy(text,done));
    } else {
      fallbackCopy(text, done);
    }
  });

  els.overlay.hidden = false;
  els.panel.scrollTop = 0;
  document.body.style.overflow = 'hidden';
  requestAnimationFrame(()=>els.overlay.classList.add('is-open'));
}
function fallbackCopy(text, cb){
  const ta = document.createElement('textarea');
  ta.value = text; ta.style.position='fixed'; ta.style.opacity='0';
  document.body.appendChild(ta); ta.select();
  try{ document.execCommand('copy'); }catch(e){}
  document.body.removeChild(ta);
  cb();
}
function closeDetail(){
  if(els.overlay.hidden) return;
  els.overlay.classList.remove('is-open');
  setTimeout(()=>{ els.overlay.hidden = true; document.body.style.overflow=''; }, 220);
}

els.input.addEventListener('input', ()=>{
  currentQuery = els.input.value;
  els.clear.hidden = currentQuery.length===0;
  renderSuggestions();
  runSearch();
});
els.input.addEventListener('keydown', e=>{
  if(e.key==='Escape'){ hideSuggestions(); els.input.blur(); }
  if(e.key==='Enter'){
    const first = els.suggestions.querySelector('.suggestions__item');
    if(first){ hideSuggestions(); openDetail(first.getAttribute('data-id')); }
  }
});
els.input.addEventListener('focus', renderSuggestions);
document.addEventListener('click', e=>{
  if(!els.suggestions.contains(e.target) && e.target!==els.input){ hideSuggestions(); }
});
els.clear.addEventListener('click', ()=>{
  els.input.value=''; currentQuery=''; els.clear.hidden=true;
  hideSuggestions(); runSearch(); els.input.focus();
});
els.overlay.addEventListener('click', e=>{ if(e.target===els.overlay) closeDetail(); });
els.closeBtn.addEventListener('click', closeDetail);
document.addEventListener('keydown', e=>{ if(e.key==='Escape') closeDetail(); });

const themeToggle = document.getElementById('themeToggle');
function applyTheme(){
  let t;
  try{ t = localStorage.getItem('brompt-theme'); }catch(e){ t = null; }
  if(t) document.documentElement.setAttribute('data-theme', t);
}
themeToggle.addEventListener('click', ()=>{
  const current = document.documentElement.getAttribute('data-theme');
  const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  const effectiveNow = current || (prefersDark ? 'dark':'light');
  const next = effectiveNow === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', next);
  try{ localStorage.setItem('brompt-theme', next); }catch(e){}
  if(MOTION_OK){
    themeToggle.classList.add('is-spinning');
    setTimeout(()=>themeToggle.classList.remove('is-spinning'), 450);
  }
});
applyTheme();

function runCountUp(){
  if(!MOTION_OK) return;
  document.querySelectorAll('.count').forEach(el=>{
    const target = parseInt(el.getAttribute('data-target'),10) || 0;
    const start = performance.now();
    const dur = 700;
    el.textContent = '0';
    function tick(now){
      const t = Math.min(1,(now-start)/dur);
      const eased = 1-Math.pow(1-t,3);
      el.textContent = Math.round(eased*target);
      if(t<1) requestAnimationFrame(tick);
      else el.textContent = target;
    }
    requestAnimationFrame(tick);
  });
}

renderQuick();
renderChips();
renderGrid(PROMPTS);
runCountUp();
</script>
'''

html = TEMPLATE.replace('__PROMPTS__', json_data).replace('__CATEGORIES__', json_cats).replace('__ICONS__', json_icons)

with open(ROOT / 'index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('written', len(html), 'chars')
