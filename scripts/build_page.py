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
/* Layout: a library catalog drawer — a left index card-drawer switches between the full shelf and today's pull list; picking a card opens it into a reading panel.
   Identity: a catalog ledger, not a SaaS dashboard — ink-plum paper, brass stamp accent, serif captions standing in for the usual tracked-uppercase eyebrow. */
:root{
  --bg:#171023;
  --surface:#20182f;
  --fg:#f1ece0;
  --muted:#9c8fac;
  --accent:#d99a3b;
  --accent-fg:#241400;
  --line:#352a48;

  --font-display:'Fraunces',Georgia,serif;
  --font-body:'Work Sans',system-ui,-apple-system,sans-serif;
  --font-mono:'IBM Plex Mono','SFMono-Regular',Menlo,monospace;
  color-scheme:dark;
}
@media (prefers-color-scheme: light){
  :root:not([data-theme="dark"]){
    --bg:#f3ede0;
    --surface:#fffaf0;
    --fg:#241a33;
    --muted:#746a82;
    --accent:#a8671c;
    --accent-fg:#fff6e8;
    --line:#e2d6bd;
    color-scheme:light;
  }
}
:root[data-theme="light"]{
  --bg:#f3ede0;
  --surface:#fffaf0;
  --fg:#241a33;
  --muted:#746a82;
  --accent:#a8671c;
  --accent-fg:#fff6e8;
  --line:#e2d6bd;
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

.shell{max-width:1180px;margin:0 auto;padding-block:40px 80px;position:relative;z-index:2;display:flex;gap:40px;align-items:flex-start;}

.sidebar{width:206px;flex:none;position:sticky;top:max(24px, calc(env(safe-area-inset-top,0px) + 12px));display:flex;flex-direction:column;gap:20px;}
.sidebar__brandrow{display:flex;align-items:center;justify-content:space-between;gap:10px;}
.brand{font-family:var(--font-display);font-weight:700;font-size:22px;letter-spacing:-0.01em;}
.brand__dot{color:var(--accent);}
.brand__meta{font-family:var(--font-display);font-style:italic;font-size:13.5px;color:var(--muted);font-variant-numeric:tabular-nums;}

.theme-toggle{
  border:1px solid var(--line);background:var(--surface);color:var(--muted);
  width:32px;height:32px;border-radius:999px;display:flex;align-items:center;justify-content:center;
  cursor:pointer;flex:none;transition:color .15s ease,border-color .15s ease,transform .15s ease;
}
.theme-toggle:hover{color:var(--fg);border-color:var(--accent);}
.theme-toggle:active{transform:scale(.92);}
.theme-toggle svg{transition:transform .45s cubic-bezier(.34,1.56,.64,1);}
.theme-toggle.is-spinning svg{transform:rotate(180deg);}

.nav{display:flex;flex-direction:column;gap:4px;}
.nav__item{
  display:flex;align-items:center;gap:10px;
  padding:10px 12px;border-radius:11px;border:1px solid transparent;
  background:none;color:var(--muted);
  font-family:var(--font-body);font-size:14px;font-weight:500;
  cursor:pointer;text-align:left;width:100%;
  transition:background .15s ease,color .15s ease,border-color .15s ease;
}
.nav__item svg{flex:none;opacity:.85;}
.nav__item:hover{color:var(--fg);}
.nav__item.is-active{background:var(--surface);border-color:var(--line);color:var(--fg);}
.nav__item.is-active svg{color:var(--accent);opacity:1;}

.main{flex:1;min-width:0;}

.hero{margin-bottom:36px;}
.hero__title{
  font-family:var(--font-display);
  font-weight:600;
  font-size:clamp(26px,4.2vw,42px);
  line-height:1.1;
  letter-spacing:-0.015em;
  margin:0 0 14px;
  max-width:17ch;
  display:flex;flex-direction:column;
}
.reveal-line{display:block;}
.reveal-accent{color:var(--accent);}
.hero__sub{
  font-size:15.5px;
  color:var(--muted);
  max-width:48ch;
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
.suggestions__id{font-family:var(--font-mono);font-size:10.5px;color:var(--muted);flex:none;}
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
.chip__count{font-size:12px;opacity:.75;font-variant-numeric:tabular-nums;}

.results__head{
  display:flex;align-items:baseline;justify-content:space-between;
  margin:36px 0 16px;
  padding-bottom:10px;
  border-bottom:1px solid var(--line);
}
.results__count{font-family:var(--font-display);font-style:italic;font-size:14px;color:var(--muted);font-variant-numeric:tabular-nums;}

.grid{
  display:grid;
  grid-template-columns:repeat(auto-fill,minmax(250px,1fr));
  gap:14px;
}
.card{
  text-align:left;
  background:var(--surface);
  border:1px solid var(--line);
  border-left:3px solid var(--line);
  border-radius:3px 13px 3px 3px;
  padding:17px 18px;
  cursor:pointer;
  font-family:inherit;color:inherit;
  display:flex;flex-direction:column;gap:10px;
  min-width:0;position:relative;
  transition:border-color .18s ease, transform .18s ease;
}
.card:hover{border-color:var(--accent);transform:translateX(3px);}
.card:active{transform:translateX(1px);}
.card__top{display:flex;align-items:center;justify-content:space-between;gap:8px;}
.card__id{font-family:var(--font-mono);font-size:10px;color:var(--muted);border:1px solid var(--line);border-radius:3px;padding:2px 6px;}
.card__cat{font-size:12px;color:var(--muted);overflow:hidden;text-overflow:ellipsis;white-space:nowrap;min-width:0;}
.card__title{font-family:var(--font-display);font-weight:600;font-size:18px;line-height:1.22;margin:0;transition:color .18s ease;}
.card:hover .card__title{color:var(--accent);}
.card__desc{font-size:13.5px;color:var(--muted);line-height:1.5;margin:0;
  display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;}

.empty{
  text-align:center;padding:56px 20px;color:var(--muted);
  border:1px dashed var(--line);border-radius:16px;
}
.empty strong{color:var(--fg);display:block;font-family:var(--font-display);font-size:19px;margin-bottom:6px;font-weight:600;}

.footer{margin-top:60px;padding-top:20px;border-top:1px solid var(--line);
  display:flex;flex-wrap:wrap;gap:8px;justify-content:space-between;color:var(--muted);font-size:12.5px;}

/* Ideias de hoje view */
.today-intro{margin-bottom:26px;}
.today-intro__eyebrow{font-family:var(--font-display);font-style:italic;font-size:15px;color:var(--accent);margin:0 0 10px;}
.today-intro__title{font-family:var(--font-display);font-weight:600;font-size:clamp(26px,4.2vw,38px);line-height:1.12;margin:0 0 12px;max-width:20ch;text-wrap:balance;}
.today-intro__sub{font-size:15px;color:var(--muted);line-height:1.55;max-width:52ch;margin:0;}

.productbar{
  display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin-bottom:24px;
}
.productbar__box{
  flex:1 1 280px;min-width:0;display:flex;align-items:center;gap:10px;
  background:var(--surface);border:1.5px solid var(--line);border-radius:14px;padding:13px 16px;
  transition:border-color .18s ease, box-shadow .18s ease;
}
.productbar__box:focus-within{border-color:var(--accent);box-shadow:0 0 0 4px color-mix(in srgb, var(--accent) 16%, transparent);}
.productbar__box svg{flex:none;color:var(--muted);}
.productbar__box input{
  flex:1;min-width:0;background:none;border:none;outline:none;
  font-family:var(--font-body);font-size:15.5px;color:var(--fg);padding:2px 0;
}
.productbar__box input::placeholder{color:var(--muted);}
.ideashuffle{
  flex:none;display:flex;align-items:center;gap:7px;
  font-family:var(--font-body);font-size:13.5px;font-weight:600;color:var(--fg);
  background:var(--surface);border:1px solid var(--line);border-radius:999px;
  padding:12px 17px;cursor:pointer;transition:border-color .15s ease, transform .1s ease;
}
.ideashuffle:hover{border-color:var(--accent);}
.ideashuffle:active{transform:scale(.96);}
.ideashuffle svg{transition:transform .35s cubic-bezier(.34,1.56,.64,1);}
.ideashuffle.is-spinning svg{transform:rotate(180deg);}

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
.panel__eyebrow{display:flex;align-items:center;gap:7px;font-family:var(--font-display);font-style:italic;font-size:15px;color:var(--accent);margin:0 0 10px;}
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
.section__label{font-family:var(--font-display);font-style:italic;font-size:14.5px;color:var(--muted);margin:0 0 8px;}
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

@media (max-width:880px){
  .shell{flex-direction:column;gap:22px;padding-block:28px 60px;}
  .sidebar{position:static;width:100%;flex-direction:row;flex-wrap:wrap;align-items:center;}
  .sidebar__brandrow{flex:1 1 auto;}
  .brand__meta{display:none;}
  .nav{flex-direction:row;gap:8px;flex:1 1 100%;order:3;}
  .nav__item{flex:1;justify-content:center;}
  .panel{width:100%;}
  .grid{grid-template-columns:1fr 1fr;}
}
@media (max-width:420px){
  .grid{grid-template-columns:1fr;}
}
</style>

<script>try{if(window.matchMedia && matchMedia('(prefers-reduced-motion: no-preference)').matches){document.documentElement.classList.add('motion-ok');}}catch(e){}</script>
<div class="grain" aria-hidden="true"></div>

<div class="shell">
  <aside class="sidebar">
    <div class="sidebar__brandrow reveal" style="--d:0">
      <span class="brand">Brompt<span class="brand__dot">.</span></span>
      <button class="theme-toggle" id="themeToggle" title="Alternar tema" aria-label="Alternar tema">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="5"></circle><path d="M12 1v2M12 21v2M4.2 4.2l1.4 1.4M18.4 18.4l1.4 1.4M1 12h2M21 12h2M4.2 19.8l1.4-1.4M18.4 5.6l1.4-1.4"></path></svg>
      </button>
    </div>
    <span class="brand__meta reveal" style="--d:1"><span class="count" data-target="120">120</span> prompts em <span class="count" data-target="10">10</span> categorias</span>
    <nav class="nav reveal" style="--d:2">
      <button class="nav__item is-active" data-view="catalogo" type="button">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7" rx="1.5"></rect><rect x="14" y="3" width="7" height="7" rx="1.5"></rect><rect x="3" y="14" width="7" height="7" rx="1.5"></rect><rect x="14" y="14" width="7" height="7" rx="1.5"></rect></svg>
        <span>Catálogo</span>
      </button>
      <button class="nav__item" data-view="hoje" type="button">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="17" rx="2"></rect><path d="M3 9h18M8 2v4M16 2v4"></path><circle cx="8.5" cy="14" r="1.3"></circle></svg>
        <span>Ideias de hoje</span>
      </button>
    </nav>
  </aside>

  <main class="main">
    <section id="view-catalogo">
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
        <span>Brompt, biblioteca de prompts com IA.</span>
        <span>Baseado em 120 Prompts Poderosos para Empreender com IA</span>
      </footer>
    </section>

    <section id="view-hoje" hidden>
      <div class="today-intro">
        <p class="today-intro__eyebrow">Ideias de hoje</p>
        <h1 class="today-intro__title">O que a modelo grava com o produto de hoje?</h1>
        <p class="today-intro__sub">Diz qual produto entra no vídeo e a gente monta 5 jeitos da sua modelo de IA interagir com ele — segurando, vestindo, experimentando, de perto, de longe. É só colar no Google Flow.</p>
      </div>

      <div class="productbar">
        <label class="productbar__box">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.59 13.41L11 3.83A2 2 0 0 0 9.59 3.17H4a1 1 0 0 0-1 1v5.59a2 2 0 0 0 .59 1.41l9.59 9.58a2 2 0 0 0 2.82 0l4.59-4.59a2 2 0 0 0 0-2.58z"></path><circle cx="7.5" cy="7.5" r="1.1"></circle></svg>
          <input id="productInput" type="text" placeholder="Qual produto vai aparecer no vídeo hoje? Ex.: tênis branco" autocomplete="off" aria-label="Produto de hoje">
        </label>
        <button class="ideashuffle" id="ideaShuffle" type="button">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 4 23 10 17 10"></polyline><polyline points="1 20 1 14 7 14"></polyline><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"></path></svg>
          <span>Quero outras 5</span>
        </button>
      </div>

      <div class="grid" id="ideaGrid"></div>
    </section>
  </main>
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
function escapeHtml(s){
  return String(s||'').replace(/[&<>"']/g, c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
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
  ideaGrid: document.getElementById('ideaGrid'),
  ideaShuffle: document.getElementById('ideaShuffle'),
  productInput: document.getElementById('productInput'),
};

function iconSvg(slug, size){
  size = size || 14;
  return '<svg width="'+size+'" height="'+size+'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'+(ICONS[CAT_ICON[slug]]||ICONS[slug]||'')+'</svg>';
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
    '<div class="card__top"><span class="card__id">Nº '+p.id+'</span><span class="card__cat">'+p.categoria+'</span></div>'+
    '<h3 class="card__title">'+p.titulo+'</h3>'+
    '<p class="card__desc">'+p.para_que_serve+'</p>'+
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
      '<span class="suggestions__id">Nº '+p.id+'</span>'+
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

function openDetailObj(p){
  els.panelContent.innerHTML =
    '<p class="panel__eyebrow">'+iconSvg(p.categoria_slug,13)+'<span>'+escapeHtml(p.categoria)+(p.id?' (nº '+p.id+')':'')+'</span></p>'+
    '<h2 class="panel__title">'+escapeHtml(p.titulo)+'</h2>'+
    '<div class="preview">'+
      '<div class="preview__label">'+iconSvg('spark',14)+'<span>Prévia do que você recebe</span></div>'+
      '<p class="preview__result">'+escapeHtml(p.resultado_esperado)+'</p>'+
      '<p class="preview__example"><b>Exemplo de uso: </b>'+escapeHtml(p.exemplo_resultado)+'</p>'+
    '</div>'+
    '<div class="section">'+
      '<p class="section__label">Para que serve</p>'+
      '<p class="section__text">'+escapeHtml(p.para_que_serve)+'</p>'+
    '</div>'+
    '<div class="section">'+
      '<p class="section__label">Prompt completo</p>'+
      '<div class="promptbox"><pre id="promptText">'+escapeHtml(p.prompt)+'</pre><button class="copybtn" id="copyBtn">Copiar</button></div>'+
    '</div>'+
    '<div class="section">'+
      '<p class="section__label">Como usar</p>'+
      '<p class="section__text">'+escapeHtml(p.como_usar)+'</p>'+
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
function openDetail(id){
  const p = PROMPTS.find(x=>x.id===id);
  if(p) openDetailObj(p);
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

/* ---- view switching (left nav) ---- */
const VIEWS = {
  catalogo: document.getElementById('view-catalogo'),
  hoje: document.getElementById('view-hoje'),
};
function setView(name){
  if(!VIEWS[name]) name = 'catalogo';
  Object.keys(VIEWS).forEach(k=>{ VIEWS[k].hidden = k!==name; });
  document.querySelectorAll('.nav__item').forEach(b=>b.classList.toggle('is-active', b.getAttribute('data-view')===name));
  if(location.hash.slice(1)!==name){ history.replaceState(null,'','#'+name); }
}
document.querySelectorAll('.nav__item').forEach(b=>{
  b.addEventListener('click', ()=>setView(b.getAttribute('data-view')));
});
window.addEventListener('hashchange', ()=>setView(location.hash.slice(1)));

/* ---- ideias de hoje: gerador de prompt de vídeo com produto ---- */
const IDEA_TEMPLATES = [
  {id:'segura', acao:'Segurando e observando', preview:'Vídeo curto da modelo segurando o produto e mostrando os detalhes de perto.',
   prompt:"VEO 3: AI model holds the {PRODUTO} close to the camera, turning it slowly to show every angle, soft admiring expression, warm natural lighting, lifestyle photography feel, 8 seconds.",
   dica:'Boa abertura de vídeo — use nos primeiros segundos pra prender a atenção antes de falar o preço ou benefício.'},
  {id:'textura', acao:'Passando a mão / sentindo a textura', preview:'Close-up da mão da modelo passando pelo produto, destacando o material e a sensação de qualidade.',
   prompt:"VEO 3: Close-up of the AI model's hand gently running fingers over the {PRODUTO}, feeling the texture, slow and sensory movement, soft focus background, satisfying tactile feel, natural light.",
   dica:'Funciona bem como corte de transição no meio do vídeo, enquanto a legenda fala do material ou acabamento.'},
  {id:'veste', acao:'Vestindo / experimentando', preview:'A modelo veste ou experimenta o produto na frente da câmera, com reação natural.',
   prompt:"VEO 3: AI model puts on the {PRODUTO}, adjusts it naturally in front of a mirror, confident smile, casual home or studio setting, candid lifestyle feel, medium shot.",
   dica:'Ideal pra roupas, calçados e acessórios — mostra como o produto fica no corpo real.'},
  {id:'unboxing', acao:'Unboxing', preview:'A modelo abre a caixa do produto na câmera, com reação de surpresa no reveal.',
   prompt:"VEO 3: AI model opens the box of the {PRODUTO} on camera, excited reaction, slow reveal, soft overhead lighting, clean desk or table setup, satisfying unboxing feel.",
   dica:'Vídeo clássico que viraliza sozinho — funciona pra quase qualquer categoria de produto.'},
  {id:'giro', acao:'Giro 360°', preview:'A modelo gira lentamente segurando ou vestindo o produto, mostrando todos os ângulos.',
   prompt:"VEO 3: AI model wearing or holding the {PRODUTO} does a slow 360-degree turn in front of the camera, natural studio lighting, confident posture, clean minimal background.",
   dica:'Ótimo pra fechar o vídeo mostrando o produto por inteiro antes do CTA de compra.'},
  {id:'detalhe', acao:'Detalhe em movimento', preview:'Câmera bem próxima do produto enquanto as mãos da modelo se movem sobre ele, mostrando acabamento e qualidade.',
   prompt:"VEO 3: Extreme close-up on the {PRODUTO} as the AI model's hands move slowly across it, showing fine details and material quality, shallow depth of field, soft directional light.",
   dica:'Use quando o diferencial do produto está no acabamento, textura ou detalhe que de longe não aparece.'},
  {id:'antesdepois', acao:'Antes e depois usando', preview:'Tela dividida: de um lado a modelo sem o produto, do outro já usando — mostrando a diferença.',
   prompt:"VEO 3: Split screen, left: AI model without the {PRODUTO}, right: same model using or wearing the {PRODUTO}, confident transformation, same lighting and angle on both sides.",
   dica:'Prompt forte pra produto de transformação (beleza, styling, acessório que muda o visual).'},
  {id:'recomenda', acao:'Recomendando pra câmera', preview:'A modelo segura o produto de frente pra câmera e fala com entusiasmo direto pro espectador, estilo depoimento.',
   prompt:"VEO 3: AI model holds up the {PRODUTO} towards the camera, speaks enthusiastically straight to the lens about why she loves it, natural handheld camera feel, authentic UGC style.",
   dica:'Combine com uma legenda de dor/solução — funciona como o "rosto" do anúncio.'},
  {id:'diaadia', acao:'No dia a dia', preview:'A modelo usa o produto naturalmente numa cena do cotidiano, sem parecer um anúncio.',
   prompt:"VEO 3: AI model using the {PRODUTO} naturally during an everyday routine (getting ready, walking, at a cafe), candid motion, soft golden hour light, realistic UGC feel.",
   dica:'O estilo que mais engaja no TikTok Shop — parece conteúdo orgânico, não propaganda.'},
  {id:'reacao', acao:'Reação de close no rosto', preview:'Close no rosto da modelo sorrindo genuinamente enquanto segura o produto ao lado do rosto.',
   prompt:"VEO 3: AI model's face lights up with a genuine smile while holding the {PRODUTO} next to her face, warm lighting, shallow depth of field, authentic reaction shot.",
   dica:'Bom gancho emocional — usa a expressão da modelo pra vender a sensação, não só o produto.'}
];

function seededShuffle(arr, rand){
  const a = arr.slice();
  for(let i=a.length-1;i>0;i--){
    const j = Math.floor(rand()*(i+1));
    [a[i],a[j]] = [a[j],a[i]];
  }
  return a;
}
function currentProduct(){
  const v = (els.productInput.value||'').trim();
  return v || '[PRODUTO]';
}
function fillTemplate(tpl, product){
  return tpl.split('{PRODUTO}').join(product);
}
let todayPicks = [];
function pickIdeas(n, excludeIds){
  excludeIds = excludeIds || [];
  const pool = IDEA_TEMPLATES.filter(t=>!excludeIds.includes(t.id));
  const base = pool.length>=n ? pool : IDEA_TEMPLATES;
  return seededShuffle(base, Math.random).slice(0,n);
}
function ideaCardHtml(t, product, i){
  return '<button class="card" data-i="'+i+'" style="--i:'+i+'">'+
    '<div class="card__top"><span class="card__id">Ideia '+(i+1)+'</span><span class="card__cat">Vídeo para TikTok Shop</span></div>'+
    '<h3 class="card__title">'+escapeHtml(t.acao)+'</h3>'+
    '<p class="card__desc">'+escapeHtml(t.preview)+'</p>'+
  '</button>';
}
function renderIdeas(){
  const product = currentProduct();
  els.ideaGrid.innerHTML = todayPicks.map((t,i)=>ideaCardHtml(t, product, i)).join('');
  els.ideaGrid.querySelectorAll('.card').forEach((c,i)=>{
    c.addEventListener('click', ()=>{
      const t = todayPicks[i];
      openDetailObj({
        categoria:'Vídeo pra TikTok Shop',
        categoria_slug:'videos',
        id:null,
        titulo:t.acao,
        resultado_esperado:t.preview,
        exemplo_resultado:'Cole no Google Flow com a sua modelo de IA já configurada e grave direto.',
        para_que_serve:'Ideia de vídeo pronta pra gravar hoje com o produto que você está divulgando.',
        prompt:fillTemplate(t.prompt, product),
        como_usar:t.dica,
      });
    });
  });
}
function initIdeas(){
  todayPicks = pickIdeas(5);
  renderIdeas();
}
els.productInput.addEventListener('input', renderIdeas);
els.ideaShuffle.addEventListener('click', ()=>{
  todayPicks = pickIdeas(5, todayPicks.map(t=>t.id));
  renderIdeas();
  if(MOTION_OK){
    els.ideaShuffle.classList.add('is-spinning');
    setTimeout(()=>els.ideaShuffle.classList.remove('is-spinning'), 450);
  }
});

renderQuick();
renderChips();
renderGrid(PROMPTS);
runCountUp();
initIdeas();
setView(location.hash.slice(1) || 'catalogo');
</script>
'''

html = TEMPLATE.replace('__PROMPTS__', json_data).replace('__CATEGORIES__', json_cats).replace('__ICONS__', json_icons)

with open(ROOT / 'index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('written', len(html), 'chars')
