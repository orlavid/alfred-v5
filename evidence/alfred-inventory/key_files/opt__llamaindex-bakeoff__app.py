from fastapi import FastAPI, Form, Body, Header, HTTPException
from fastapi.responses import HTMLResponse
from functools import lru_cache
from html import escape
from pathlib import Path
from urllib.parse import unquote

PERSIST = "/opt/llamaindex-bakeoff/index"

app = FastAPI(title="Alfred Retrieval Harness")

@lru_cache(maxsize=1)
def get_retriever():
    from llama_index.core import StorageContext, load_index_from_storage, Settings
    from llama_index.embeddings.huggingface import HuggingFaceEmbedding

    Settings.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
    Settings.llm = None

    storage_context = StorageContext.from_defaults(persist_dir=PERSIST)
    index = load_index_from_storage(storage_context)
    return index.as_retriever(similarity_top_k=20)

ROUTES = {
    "attention": [
        "09 Governance/Human Action Queue",
        "09 Governance/Escalations",
        "09 Governance/Open Loops",
        "09 Governance/Objectives",
        "09 Governance/Watchlists",
        "09 Governance/Daily Governance",
    ],
    "people": [
        "/02 People/",
        "02 People",
        "/People/",
        "LLM Wiki/People",
        "07 AI Memory/Entities",
    ],
    "companies": [
        "04 Companies",
        "Suppliers",
        "LLM Wiki/Suppliers",
        "LLM Wiki/Companies",
    ],
    "projects": [
        "03 Projects",
    ],
}

ROUTE_QUERIES = {
    "attention": [
        "Required Human Actions work",
        "Latest Governance Escalation action required work",
        "active open loop work recommended action",
        "objectives status work",
        "watchlist material development work",
    ],
    "people": [
        "02 People Graham Dawe",
        "People Graham Dawe",
        "{query}",
    ],
    "companies": ["{query}"],
    "projects": ["{query}"],
}

EXCLUDE = [
    "/10 Domains/Personal/",
    "/Trading/",
    "/Finance/Trading/",
    "/98 Archive/",
]

DOMAIN_EXCLUDE = [
    "ibkr",
    "trading dashboard",
    "portfolio",
    "degiro",
    "xlf",
    "vig",
    "fog",
    "pba exception",
    "etf",
    "mtum",
    "ieur",
    "xlk",
    "iusn",
    "is3n",
    "meud",
    "vwce",
]

def classify_route(query: str):
    q = query.lower()
    if any(x in q for x in ["attention", "priority", "priorities", "work items", "deserves attention", "top ten issues", "issues to face", "top ten", "top issues", "issues"]):
        return "attention"
    if any(x in q for x in ["who is", "person", "people", "graham", "grahame", "dawe"]):
        return "people"
    if any(x in q for x in ["company", "supplier", "barclays", "codec", "softcat"]):
        return "companies"
    if "project" in q:
        return "projects"
    return None

def routed_queries(query: str, route: str | None):
    if not route:
        return [query]
    return [x.format(query=query) for x in ROUTE_QUERIES.get(route, [query])]

def allowed_by_route(path: str, route: str | None):
    if not route:
        return True
    prefixes = ROUTES.get(route, [])
    return any(prefix in path for prefix in prefixes)

def object_type(path: str):
    p = path.lower()
    if "/09 governance/human action queue/" in p:
        return "HUMAN ACTION"
    if "/09 governance/escalations/" in p:
        return "ESCALATION"
    if "/09 governance/open loops/" in p:
        return "OPEN LOOP"
    if "/09 governance/objectives/" in p:
        return "OBJECTIVE"
    if "/09 governance/watchlists/" in p:
        return "WATCHLIST"
    if "/09 governance/daily governance/" in p:
        return "DAILY GOVERNANCE"
    if "/07 ai memory/entities/" in p:
        return "ENTITY"
    if "/02 people/" in p:
        return "PERSON RECORD"
    if "/llm wiki/people/" in p:
        return "PERSON WIKI"
    if "/04 companies/" in p:
        return "COMPANY RECORD"
    if "/llm wiki/suppliers/" in p:
        return "SUPPLIER WIKI"
    if "/llm wiki/companies/" in p:
        return "COMPANY WIKI"
    if "/03 projects/" in p:
        return "PROJECT RECORD"
    if "historical capture" in p:
        return "EVIDENCE"
    if "enriched capture" in p:
        return "ENRICHED INSIGHT"
    if "/07 executive briefings/" in p:
        return "GENERATED BRIEFING"
    if "/98 archive/" in p:
        return "ARCHIVE"
    return "OTHER"


def filename_people_matches(query: str):
    root = Path("/docker/obsidian-vault")
    q = query.lower()
    candidates = []

    aliases = {
        "grahame dawe": "graham dawe",
        "graham dawe": "graham dawe",
    }

    target = None
    for k, v in aliases.items():
        if k in q:
            target = v
            break

    if not target:
        return []

    wanted = target.replace(" ", "*")

    search_dirs = [
        root / "02 People",
        root / "People",
        root / "LLM Wiki" / "People",
    ]

    for d in search_dirs:
        if not d.exists():
            continue
        for f in d.rglob("*.md"):
            name = f.stem.lower().replace("-", " ")
            if target in name:
                candidates.append(f)

    return candidates


def page(query="", results=""):
    return f"""<html>
<head>
<title>Alfred Retrieval Harness</title>
<style>
body {{ font-family: Arial; max-width: 1100px; margin: 2rem auto; }}
textarea {{ width: 100%; height: 90px; }}
.result {{ border: 1px solid #ddd; padding: 1rem; margin: 1rem 0; border-radius: 8px; }}
.path {{ font-weight: bold; color: #333; }}
.score {{ color: #666; }}
pre {{ white-space: pre-wrap; }}
</style>
</head>
<body>
<h1>Alfred Retrieval Harness</h1>
<p>Read-only LlamaIndex test over Obsidian vault copy.</p>
<form method="post">
<textarea name="query">{escape(query)}</textarea><br><br>
<button type="submit">Search</button>
</form>
<hr>
{results}
</body>
</html>"""

@app.get("/", response_class=HTMLResponse)
def home():
    return page("What work items deserve attention?", "")

@app.post("/", response_class=HTMLResponse)
def search(query: str = Form(...)):
    retriever = get_retriever()
    route = classify_route(query)

    raw = []
    for rq in routed_queries(query, route):
        raw.extend(retriever.retrieve(rq))

    rows = []
    seen = set()
    themes = {}

    if route == "people":
        import subprocess
        try:
            summary = subprocess.check_output(
                ["python3", "entity_summary.py", "person", (
                    query.lower()
                    .replace("who is ", "")
                    .replace("tell me about ", "")
                    .replace("what do you know about ", "")
                    .strip(" ?.")
                )],
                text=True,
                timeout=30
            )
        except Exception as e:
            summary = f"People summary failed: {e}"

        return page(query, f"""
        <div class="result">
          <div class="path">[PEOPLE INTELLIGENCE]</div>
          <div class="score">route=people | source=entity_summary.py</div>
          <pre>{escape(summary[:8000])}</pre>
        </div>
        """)

    if route == "people":
        for f in filename_people_matches(query):
            path = str(f)
            if path in seen:
                continue
            seen.add(path)
            typ = object_type(path)
            try:
                raw_text = f.read_text(errors="ignore")
            except Exception:
                raw_text = ""
            safe_path = escape(path, quote=True)
            rows.append(f"""
            <div class="result">
              <div class="path">
                [{escape(typ)}]
                <a href="/view?path={safe_path}">{safe_path}</a>
              </div>
              <div class="score">route=people | source=filename-match</div>
              <pre>{escape(raw_text[:1200])}</pre>
            </div>
            """)

    theme_terms = [
        "strategic_drift",
        "dora",
        "supplier_risk",
        "platform_resilience",
        "cyber_incidents",
        "ai_regulation",
    ]

    for r in raw:
        path = r.metadata.get("file_path", "unknown")
        raw_text = str(r.node.text)
        raw_text_lower = raw_text.lower()

        if any(x in path for x in EXCLUDE):
            continue
        if not allowed_by_route(path, route):
            continue
        if route == "attention" and any(term in raw_text_lower for term in DOMAIN_EXCLUDE):
            continue

        if route == "people":
            low_value_entity = (
                "/07 AI Memory/Entities/" in path
                and (
                    "appears " in raw_text_lower
                    or "curation status" in raw_text_lower
                    or "review description" in raw_text_lower
                    or "confirm whether this is a strategic theme" in raw_text_lower
                )
            )
            if low_value_entity:
                continue
        if path in seen:
            continue

        seen.add(path)
        typ = object_type(path)
        score = r.score or 0
        text = escape(raw_text[:1200])
        safe_path = escape(path, quote=True)

        theme = None
        lower_path = path.lower()
        for t in theme_terms:
            if t in lower_path:
                theme = t
                break

        if route == "attention" and theme:
            if theme not in themes:
                themes[theme] = {
                    "count": 0,
                    "path": path,
                    "type": typ,
                    "score": score,
                }
            themes[theme]["count"] += 1
            continue

        rows.append(f"""
        <div class="result">
          <div class="path">
            [{escape(typ)}]
            <a href="/view?path={safe_path}">{safe_path}</a>
          </div>
          <div class="score">route={escape(str(route))} | score={score:.4f}</div>
          <pre>{text}</pre>
        </div>
        """)

    if route == "attention":
        for theme, data in sorted(themes.items(), key=lambda x: x[1]["count"], reverse=True):
            label = theme.replace("_", " ").title()
            rows.append(f"""
            <div class="result">
              <div class="path">
                [{escape(data['type'])}]
                <a href="/view_theme?theme={theme}">{escape(label)}</a>
              </div>
              <div class="score">occurrences={data['count']} | route=attention</div>
            </div>
            """)

    results = "\n".join(rows) if rows else "<p>No results after filters.</p>"
    return page(query, results)



@app.get("/view_theme", response_class=HTMLResponse)
def view_theme(theme: str):

    root = Path("/docker/obsidian-vault")

    matches = []

    allowed_dirs = [
        "/09 Governance/Open Loops/",
        "/09 Governance/Watchlists/",
        "/09 Governance/Escalations/",
        "/09 Governance/Objectives/",
        "/09 Governance/Human Action Queue/",
    ]

    for md in root.rglob("*.md"):
        sp = str(md)
        if not any(d in sp for d in allowed_dirs):
            continue
        name = md.name.lower()
        t = theme.lower()

        if t == "dora":
            ok = (
                name.endswith("watchlist - dora.md")
                or name.endswith("open loop - watchlist - dora.md")
            )
        elif t == "supplier_risk":
            ok = "supplier_risk" in name or "supplier risk" in name
        elif t == "strategic_drift":
            ok = "strategic_drift" in name or "strategic drift" in name
        elif t == "platform_resilience":
            ok = "platform_resilience" in name or "platform resilience" in name
        elif t == "cyber_incidents":
            ok = "cyber_incidents" in name or "cyber incidents" in name
        elif t == "ai_regulation":
            ok = "ai_regulation" in name or "ai regulation" in name
        else:
            ok = t in name

        if ok:
            matches.append(md)

    matches = sorted(matches, reverse=True)

    groups = {}

    for m in matches:
        typ = object_type(str(m))
        groups.setdefault(typ, []).append(m)

    sections = []

    for typ, files in sorted(groups.items()):
        rows = []
        files = sorted(files, reverse=True)[:5]

        for m in files:
            rows.append(
                f'<li><a href="/view?path={escape(str(m), quote=True)}">{escape(m.name)}</a></li>'
            )

        sections.append(f"""
        <h3>{escape(typ)} ({len(files)})</h3>
        <ul>
          {''.join(rows)}
        </ul>
        """)

    return f"""
    <html>
    <body style="font-family: Arial; max-width: 1200px; margin: 2rem auto;">
      <p><a href="/">Back to search</a></p>
      <h2>{escape(theme)}</h2>

      <p><b>Latest Watchlist:</b><br>
      {escape(next((m.name for m in sorted(matches, reverse=True) if 'watchlist' in m.name.lower() and 'open loop' not in m.name.lower()), 'None'))}
      </p>

      <p><b>Latest Open Loop:</b><br>
      {escape(next((m.name for m in sorted(matches, reverse=True) if 'open loop' in m.name.lower()), 'None'))}
      </p>

      <p><b>Occurrences:</b> {len(matches)}</p>

      <h3>Outstanding Actions</h3>

      <ul>
      {
        ''.join(
          f'<li>{escape(line.strip()[2:])}</li>'
          for line in [
            line
            for line in next(
              (
                Path(m).read_text(errors='ignore').splitlines()
                for m in sorted(matches, reverse=True)
                if 'open loop' in m.name.lower()
              ),
              []
            )
            if line.strip().startswith('- ')
          ][:5]
        )
      }
      </ul>

      {''.join(sections)}
    </body>
    </html>
    """

@app.get("/view", response_class=HTMLResponse)
def view(path: str):
    p = Path(unquote(path))

    if not p.exists():
        return "<h1>File not found</h1>"

    try:
        content = p.read_text(errors="ignore")
    except Exception as e:
        return f"<h1>Error</h1><pre>{escape(str(e))}</pre>"

    return f"""
    <html>
    <body style="font-family: Arial; max-width: 1200px; margin: 2rem auto;">
      <p><a href="/">Back to search</a></p>
      <h2>{escape(str(p))}</h2>
      <pre style="white-space: pre-wrap;">{escape(content)}</pre>
    </body>
    </html>
    """



@app.post("/alfred")
def alfred_api(payload: dict = Body(...), authorization: str | None = Header(default=None)):
    import subprocess
    import sys

    expected = Path("/opt/llamaindex-bakeoff/.alfred_api_token").read_text().strip()
    if authorization != f"Bearer {expected}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    question = (payload.get("question") or "").strip()
    if not question:
        return {"error": "Missing question"}

    try:
        answer = subprocess.check_output(
            [sys.executable, "alfred.py", "--json", question],
            cwd="/opt/llamaindex-bakeoff",
            text=True,
            timeout=300,
        )
        import json
        return json.loads(answer.splitlines()[-1])
    except subprocess.TimeoutExpired:
        return {"error": "Alfred timed out"}
    except Exception as e:
        return {"error": str(e)}

