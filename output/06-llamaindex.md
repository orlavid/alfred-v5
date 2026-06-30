# LlamaIndex Evidence Engine

Generated: 2026-06-30T21:41:58.616587


## Purpose

Defines semantic retrieval and ChatGPT Action evidence packaging.

## Responsibilities

- Index the live Obsidian vault.
- Retrieve semantically relevant evidence.
- Package evidence for ChatGPT reasoning.
- Support the Custom GPT Action endpoint.

## Inputs

- /docker/obsidian-vault
- Embedding model
- User question

## Outputs

- Evidence package
- Source paths
- Similarity-scored nodes

## Dependencies

- FastAPI app
- alfred.py
- LlamaIndex index folder
- Python virtual environment

## Failure Modes

- API not running.
- Index stale or missing.
- Evidence package returned but GPT instructions misaligned.
- Subprocess output includes warnings before JSON.

## Recovery Procedure

- Run alfred.py directly with --json.
- Test local API on 127.0.0.1:8788.
- Rebuild index from the live vault if needed.
- Confirm GPT Action instructions treat API output as evidence package.

## Source Evidence

### llamaindex/index_summary.txt

Size: 2621 bytes

```text
===== index size =====
170M	/opt/llamaindex-bakeoff/index
===== files =====
2026-06-28 17:39 1093927 /opt/llamaindex-bakeoff/index/index_store.json
2026-06-28 17:39 117946088 /opt/llamaindex-bakeoff/index/default__vector_store.json
2026-06-28 17:39 18 /opt/llamaindex-bakeoff/index/graph_store.json
2026-06-28 17:39 58865656 /opt/llamaindex-bakeoff/index/docstore.json
2026-06-28 17:39 72 /opt/llamaindex-bakeoff/index/image__vector_store.json
===== requirements =====
aiohappyeyeballs==2.6.2
aiohttp==3.14.1
aiosignal==1.4.0
aiosqlite==0.22.1
annotated-doc==0.0.4
annotated-types==0.7.0
anyio==4.14.1
attrs==26.1.0
banks==2.4.4
certifi==2026.6.17
charset-normalizer==3.4.7
click==8.4.2
colorama==0.4.6
cuda-bindings==13.3.1
cuda-pathfinder==1.5.5
cuda-toolkit==13.0.2
dataclasses-json==0.6.7
Deprecated==1.3.1
dirtyjson==1.0.8
distro==1.9.0
fastapi==0.138.1
filelock==3.29.4
filetype==1.2.0
frozenlist==1.8.0
fsspec==2026.6.0
greenlet==3.5.3
griffe==2.1.0
griffecli==2.1.0
griffelib==2.1.0
h11==0.16.0
hf-xet==1.5.1
httpcore==1.0.9
httpx==0.28.1
huggingface_hub==1.21.0
idna==3.18
Jinja2==3.1.6
jiter==0.15.0
joblib==1.5.3
llama-index==0.14.23
llama-index-core==0.14.23
llama-index-embeddings-huggingface==0.7.0
llama-index-embeddings-openai==0.6.0
llama-index-instrumentation==0.5.0
llama-index-llms-openai==0.7.9
llama-index-workflows==2.22.1
markdown-it-py==4.2.0
MarkupSafe==3.0.3
marshmallow==3.26.2
mdurl==0.1.2
mpmath==1.3.0
multidict==6.7.1
mypy_extensions==1.1.0
narwhals==2.22.1
nest-asyncio==1.6.0
networkx==3.6.1
nltk==3.9.4
numpy==2.5.0
nvidia-cublas==13.1.1.3
nvidia-cuda-cupti==13.0.85
nvidia-cuda-nvrtc==13.0.88
nvidia-cuda-runtime==13.0.96
nvidia-cudnn-cu13==9.20.0.48
nvidia-cufft==12.0.0.61
nvidia-cufile==1.15.1.6
nvidia-curand==10.4.0.35
nvidia-cusolver==12.0.4.66
nvidia-cusparse==12.6.3.3
nvidia-cusparselt-cu13==0.8.1
nvidia-nccl-cu13==2.29.7
nvidia-nvjitlink==13.0.88
nvidia-nvshmem-cu13==3.4.5
nvidia-nvtx==13.0.85
openai==2.44.0
packaging==26.2
pillow==12.2.0
platformdirs==4.10.0
propcache==0.5.2
pydantic==2.13.4
pydantic_core==2.46.4
Pygments==2.20.0
PyYAML==6.0.3
regex==2026.5.9
requests==2.34.2
rich==15.0.0
safetensors==0.8.0
scikit-learn==1.9.0
scipy==1.18.0
sentence-transformers==5.6.0
setuptools==81.0.0
shellingham==1.5.4
sniffio==1.3.1
SQLAlchemy==2.0.51
starlette==1.3.1
sympy==1.14.0
tenacity==9.1.4
threadpoolctl==3.6.0
tiktoken==0.13.0
tinytag==2.2.1
tokenizers==0.22.2
torch==2.12.1
tqdm==4.68.3
transformers==5.12.1
triton==3.7.1
typer==0.25.1
typing-inspect==0.9.0
typing-inspection==0.4.2
typing_extensions==4.15.0
urllib3==2.7.0
uvicorn==0.49.0
wrapt==2.2.2
yarl==1.24.2

```

### key_files/opt__llamaindex-bakeoff__app.py

Size: 15157 bytes

```text
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


```

### key_files/opt__llamaindex-bakeoff__alfred.py

Size: 1790 bytes

```text
#!/usr/bin/env python3
import json
import sys
from pathlib import Path
import contextlib

BASE = Path(__file__).parent
PERSIST = str(BASE / "index")

args = sys.argv[1:]
json_mode = False

if args and args[0] == "--json":
    json_mode = True
    args = args[1:]

if not args:
    raise SystemExit('Usage: alfred.py [--json] "question"')

question = " ".join(args)

with contextlib.redirect_stdout(sys.stderr):
    from llama_index.core import StorageContext, load_index_from_storage, Settings
    from llama_index.embeddings.huggingface import HuggingFaceEmbedding

    Settings.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
    Settings.llm = None

    storage_context = StorageContext.from_defaults(persist_dir=PERSIST)
    index = load_index_from_storage(storage_context)
    retriever = index.as_retriever(similarity_top_k=12)

    nodes = retriever.retrieve(question)

evidence = []
for i, node in enumerate(nodes, 1):
    meta = getattr(node.node, "metadata", {}) or {}
    path = meta.get("file_path") or meta.get("filename") or meta.get("source") or "unknown"
    text = node.node.get_content()[:2500]
    score = getattr(node, "score", None)
    evidence.append(
        f"### Evidence {i}\n"
        f"Source: {path}\n"
        f"Score: {score}\n\n"
        f"{text}"
    )

answer = f"""You are Alfred's evidence package.

Question:
{question}

Instructions for ChatGPT:
Use only the evidence below. If the evidence is insufficient, say so clearly. Do not use public knowledge or memory.

Evidence:
{chr(10).join(evidence)}
"""

payload = {
    "question": question,
    "answer": answer,
    "quality_gate": "EVIDENCE_PACKAGE_ONLY_CHATGPT_MUST_REASON",
    "source": "alfred.py",
}

print(json.dumps(payload) if json_mode else answer)

```

### key_files/opt__llamaindex-bakeoff__test_index.py

Size: 707 bytes

```text
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

VAULT = "/docker/obsidian-vault"
PERSIST = "./index"

Settings.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
Settings.llm = None

print(f"Loading markdown files from: {VAULT}")
docs = SimpleDirectoryReader(
    VAULT,
    recursive=True,
    required_exts=[".md"],
).load_data()

print(f"Loaded documents: {len(docs)}")
print("Building index...")
index = VectorStoreIndex.from_documents(docs)

print(f"Persisting index to: {PERSIST}")
index.storage_context.persist(persist_dir=PERSIST)

print("Index build complete")

```
