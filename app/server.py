from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from jinja2 import Template
import json
from app.core.lifespan import lifespan
from app.api.routers import kotiki


app = FastAPI(lifespan=lifespan, root_path="/api")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

app.include_router(kotiki.router, prefix="/v1/files", tags=["files"])


@app.get("/index", response_class=HTMLResponse, tags=["pages"])
async def index(request: Request):
    root_path = request.scope.get("root_path") or ""
    initial_keys: list[str] = []
    badges = ["purrfect", "floofy", "silly", "tiny lions", "mlem"]
    template = Template("""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <meta name=\"api-base\" content=\"{{ api_base }}\">
  <title>{{ page_title }}</title>
  <style>
    :root { color-scheme: dark; }
    body { margin: 0; font-family: -apple-system, system-ui, sans-serif; background: #0f1115; color: #f0f3f7; }
    header { position: sticky; top: 0; z-index: 5; background: rgba(15,17,21,0.8); backdrop-filter: blur(8px); padding: 16px 20px; border-bottom: 1px solid #232734; }
    h1 { margin: 0; font-size: 20px; letter-spacing: 0.3px; }
    p { margin: 6px 0 0; color: #a6b0c2; font-size: 14px; }
    .badges { display: flex; flex-wrap: wrap; gap: 8px; margin: 10px 0 0; padding: 0; list-style: none; }
    .badges li { padding: 4px 10px; border: 1px solid #2a3145; border-radius: 999px; font-size: 12px; color: #9fb0d3; }
    #stream { display: grid; gap: 18px; padding: 18px 0 60px; }
    .card { width: 100%; background: #161a22; border-top: 1px solid #222738; border-bottom: 1px solid #222738; box-shadow: 0 10px 30px rgba(0,0,0,0.25); }
    .card img { display: block; width: 100vw; max-width: 100%; height: auto; }
    .caption { padding: 8px 16px 12px; color: #7d8799; font-size: 12px; text-align: right; }
    #status { text-align: center; color: #7d8799; font-size: 13px; padding: 16px 0 40px; }
  </style>
</head>
<body>
  <header>
    <h1>{{ page_title }}</h1>
    <p>{{ page_subtitle }}</p>
    <ul class=\"badges\">
      {% for badge in badges %}
        <li>#{{ badge }}</li>
      {% endfor %}
    </ul>
  </header>
  <main id=\"stream\">
    {% for key in initial_keys %}
      <article class=\"card\">
        <img loading=\"lazy\" alt=\"kotik {{ key }}\" src=\"{{ api_base }}/v1/files/download/{{ key | urlencode }}\">
        <div class=\"caption\">kotik #{{ key }}</div>
      </article>
    {% endfor %}
  </main>
  <div id=\"status\">Loading kotiki...</div>
  <script>
    const config = {{ config_json }};
    const stream = document.getElementById('stream');
    const status = document.getElementById('status');
    const sentinel = document.createElement('div');
    stream.appendChild(sentinel);
    let loading = false;

    const listUrl = () => (
      `${config.apiBase}/v1/files/kotiki?limit=${config.limit}&offset=0`
    );

    const downloadUrl = (key) => (
      `${config.apiBase}/v1/files/download/${encodeURIComponent(key)}`
    );

    function addCard(key) {
      const card = document.createElement('article');
      card.className = 'card';

      const img = document.createElement('img');
      img.loading = 'lazy';
      img.alt = `kotik ${key}`;
      img.src = downloadUrl(key);

      const caption = document.createElement('div');
      caption.className = 'caption';
      caption.textContent = `kotik #${key}`;

      card.appendChild(img);
      card.appendChild(caption);
      stream.insertBefore(card, sentinel);
    }

    async function loadMore() {
      if (loading) return;
      loading = true;
      status.textContent = 'Fetching more kotiki...';
      try {
        const response = await fetch(listUrl());
        if (!response.ok) {
          status.textContent = 'Failed to load kotiki. Try again later.';
          return;
        }
        const data = await response.json();
        const items = Array.isArray(data.items) ? data.items : [];

        if (items.length === 0) {
          status.textContent = 'No kotiki yet. Add some and scroll again.';
          return;
        }

        items.forEach((item) => {
          const key = item.id || item.key;
          if (key) addCard(key);
        });
        status.textContent = 'Scroll for more.';
      } catch (error) {
        status.textContent = 'Error loading kotiki.';
      } finally {
        loading = false;
      }
    }


    const observer = new IntersectionObserver((entries) => {
      if (entries.some((entry) => entry.isIntersecting)) {
        loadMore();
      }
    }, { rootMargin: '400px 0px' });

    observer.observe(sentinel);
    loadMore();
  </script>
</body>
</html>""")
    config = {"apiBase": root_path, "limit": 10}
    html = template.render(
        api_base=root_path,
        config_json=json.dumps(config),
        page_title="Infinite Kotiki Parade",
        page_subtitle="Scroll down for more purr-fect surprises.",
        initial_keys=initial_keys,
        badges=badges,
    )
    return HTMLResponse(content=html)


@app.get("/health", tags=["system"])
async def health():
    return {"status": "ok"}