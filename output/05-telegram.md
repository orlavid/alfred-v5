# Telegram Interface

Generated: 2026-06-30T21:41:58.616568


## Purpose

Defines Telegram as Alfred's mobile executive interface.

## Responsibilities

- Receive user messages.
- Pass free-text queries to Alfred Router.
- Return validated responses in manageable parts.
- Preserve useful legacy deterministic routes.

## Inputs

- Telegram messages
- Bot token
- Router output

## Outputs

- Telegram replies
- Parted long responses
- Operational logs

## Dependencies

- hermes-telegram.service
- /root/hermes-telegram.py
- alfred_router.sh
- OpenRouter env for legacy synthesis

## Failure Modes

- Service inactive.
- Service override points to old container.
- OpenRouter env file not loaded.
- Router withholds answer due to strategy failure.

## Recovery Procedure

- Check hermes-telegram.service status.
- Inspect systemctl cat hermes-telegram.service.
- Check journalctl logs.
- Run the same query through alfred_router.sh manually.

## Source Evidence

### telegram/service.txt

Size: 655 bytes

```text
# /etc/systemd/system/hermes-telegram.service
[Unit]
Description=Hermes Telegram Bot
After=network.target docker.service
Requires=docker.service

[Service]
Type=simple
User=root
WorkingDirectory=/root
ExecStart=/usr/bin/python3 /root/hermes-telegram.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target

# /etc/systemd/system/hermes-telegram.service.d/20-authoritative-vault.conf
[Service]
Environment=HERMES_CONTAINER=hermes-agent-mctr-hermes-agent-1
Environment=HERMES_KEY_CONTAINER=hermes-agent-mctr-hermes-agent-1

# /etc/systemd/system/hermes-telegram.service.d/30-openrouter-env.conf
[Service]
EnvironmentFile=/root/.openrouter.env

```

### telegram/status.txt

Size: 677 bytes

```text
● hermes-telegram.service - Hermes Telegram Bot
     Loaded: loaded (/etc/systemd/system/hermes-telegram.service; enabled; preset: enabled)
    Drop-In: /etc/systemd/system/hermes-telegram.service.d
             └─20-authoritative-vault.conf, 30-openrouter-env.conf
     Active: active (running) since Sun 2026-06-28 21:09:59 IST; 1h 7min ago
   Main PID: 13945 (python3)
      Tasks: 3 (limit: 9483)
     Memory: 38.7M (peak: 66.3M)
        CPU: 2.387s
     CGroup: /system.slice/hermes-telegram.service
             └─13945 /usr/bin/python3 /root/hermes-telegram.py

Jun 28 21:09:59 orlavid-hermes systemd[1]: Started hermes-telegram.service - Hermes Telegram Bot.

```

### telegram/script.py

Size: 38338 bytes

```text
#!/usr/bin/env python3

# ALFRED_AGENT_ORG_IMPORT_START
import sys as _alfred_agent_sys
_ALFRED_AGENT_SCRIPTS = "/opt/second-brain/scripts"
if _ALFRED_AGENT_SCRIPTS not in _alfred_agent_sys.path:
    _alfred_agent_sys.path.insert(0, _ALFRED_AGENT_SCRIPTS)
from telegram_agent_commands import ALFRED_AGENT_COMMAND_HANDLERS
# ALFRED_AGENT_ORG_IMPORT_END
import os
import re
import subprocess
from pathlib import Path
from datetime import datetime

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile, InlineKeyboardButton, InlineKeyboardMarkup, InputFile, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

OLD_BOT = Path("/root/hermes-telegram.py.previous")
CURRENT = Path("/root/hermes-telegram.py")

BOT_TOKEN = os.environ.get("HERMES_TELEGRAM_BOT_TOKEN")

if not BOT_TOKEN:
    # recover token from latest backup if hard-coded there
    backups = sorted(Path("/root").glob("hermes-telegram.py.bak*"), key=lambda p: p.stat().st_mtime, reverse=True)
    for b in backups:
        txt = b.read_text(errors="ignore")
        m = re.search(r'BOT_TOKEN\s*=\s*["\']([^"\']+)["\']', txt)
        if m:
            BOT_TOKEN = m.group(1)
            break

if not BOT_TOKEN:
    raise SystemExit("BOT token not found. Set HERMES_TELEGRAM_BOT_TOKEN or restore previous bot.")

VAULT = Path("/docker/obsidian-vault")
CAPTURE_DIR = VAULT / "00 Inbox" / "Captures"
CAPTURE_DIR.mkdir(parents=True, exist_ok=True)

HERMES_CONTAINER = os.environ.get("HERMES_CONTAINER", "hermes-authoritative-vault")


def capture_note(text: str, source: str = "telegram") -> Path:
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = CAPTURE_DIR / f"Capture - {ts}.md"
    path.write_text(
        f"# Telegram Capture - {ts}\n\n"
        f"Source: {source}\n"
        f"Captured: {datetime.now().isoformat(timespec='seconds')}\n\n"
        f"## Message\n\n{text.strip()}\n",
        encoding="utf-8"
    )

    try:
        subprocess.run(
            ["/opt/second-brain/scripts/enrich_capture.py", str(path)],
            capture_output=True,
            text=True,
            timeout=30
        )

        subprocess.run(
            ["python3", "/opt/second-brain/scripts/update_open_loops.py"],
            capture_output=True,
            text=True,
            timeout=30
        )

        subprocess.Popen(
            ["python3", "/opt/second-brain/scripts/hermes_enrich_capture.py", str(path)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except Exception:
        pass

    return path


def run_semantic_reindex():
    candidates = [
        ["/opt/second-brain/scripts/reindex.sh"],
        ["/opt/second-brain/scripts/semantic_reindex.sh"],
        ["python3", "/semantic/reindex.py"],
    ]
    for cmd in candidates:
        try:
            if Path(cmd[0]).exists():
                subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return
        except Exception:
            pass





def ask_hermes(prompt: str) -> str:
    try:
        r = subprocess.run(
            ["/opt/second-brain/scripts/alfred_router.sh", prompt],
            capture_output=True,
            text=True,
            timeout=650
        )
        out = (r.stdout or r.stderr or "").strip()
        if not out:
            out = "Alfred returned no usable response."
        return out
    except Exception as e:
        return f"Hermes response failed: {e}"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        "Alfred is online. Send me a message and I will answer it. Use /capture <note> when you want something saved into the second brain."
    )


async def health(update: Update, context: ContextTypes.DEFAULT_TYPE):
    checks = []
    checks.append(f"Vault exists: {VAULT.exists()}")
    checks.append(f"Capture dir exists: {CAPTURE_DIR.exists()}")
    p = subprocess.run(["ps", "aux"], capture_output=True, text=True)
    checks.append(f"Obsidian headless sync process: {'ob sync --path /docker/obsidian-vault --continuous' in p.stdout}")
    checks.append(f"Hermes container: {HERMES_CONTAINER}")
    await update.effective_message.reply_text("Hermes Telegram Health\n" + "\n".join(checks))


async def capture_only(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args).strip()
    if not text:
        await update.effective_message.reply_text("Usage: /capture <note>")
        return
    path = capture_note(text)
    run_semantic_reindex()
    await update.effective_message.reply_text(f"Captured: {path}")



SEARCH_CONTEXT_TTL_SECONDS = 30 * 60


def extract_search_subject(text: str) -> str:
    """Remove conversational search wrappers and retain the actual subject."""
    import re

    subject = (text or "").strip()

    patterns = [
        r"^\s*what\s+do\s+my\s+notes\s+say\s+about\s+",
        r"^\s*what\s+does\s+my\s+vault\s+say\s+about\s+",
        r"^\s*what\s+do\s+i\s+have\s+on\s+",
        r"^\s*tell\s+me\s+about\s+",
        r"^\s*find\s+(?:all\s+)?(?:references\s+to\s+)?",
        r"^\s*search\s+(?:my\s+)?(?:notes|vault)\s+for\s+",
        r"^\s*show\s+me\s+(?:everything\s+)?(?:about|on)\s+",
    ]

    for pattern in patterns:
        subject = re.sub(pattern, "", subject, flags=re.IGNORECASE)

    return subject.strip(" \t\r\n?.!,:;")


def is_substantive_vault_search(text: str) -> bool:
    import re

    value = (text or "").lower()

    return bool(
        re.search(
            r"\b(notes?|vault|search|find|references?|mentions?|"
            r"what do i have|what do my notes|what does my vault)\b",
            value,
        )
    )


def is_contextual_search_followup(text: str) -> bool:
    """Recognise only clear continuation wording, not arbitrary short messages."""
    import re

    value = (text or "").strip().lower()

    followup_patterns = [
        r"^have\s+a\s+look\b",
        r"^look\s+(?:in|under|at|through|there)\b",
        r"^also\s+look\b",
        r"^check\s+(?:in|under|the|those|there)\b",
        r"^also\s+check\b",
        r"^search\s+(?:in|under|within|those)\b",
        r"^what\s+about\b",
        r"^and\s+what\s+about\b",
        r"^where\s+else\b",
        r"^show\s+me\s+more\b",
        r"^give\s+me\s+more\s+detail\b",
        r"^more\s+detail\b",
        r"^try\s+(?:the|in|under)\b",
    ]

    return any(re.search(pattern, value) for pattern in followup_patterns)


def prepare_contextual_search(
    text: str,
    context: ContextTypes.DEFAULT_TYPE,
) -> str:
    """
    Carry forward the prior search subject only for a clear, recent follow-up.
    State is scoped to the Telegram chat and is intentionally short-lived.
    """
    import time

    now = time.time()
    state = context.chat_data

    previous_subject = state.get("last_search_subject")
    previous_at = float(state.get("last_search_at", 0))

    within_window = (
        previous_subject
        and previous_at
        and now - previous_at <= SEARCH_CONTEXT_TTL_SECONDS
    )

    if is_contextual_search_followup(text) and within_window:
        state["last_search_at"] = now

        return (
            f"Continue the previous vault search about: {previous_subject}. "
            f"Apply this refinement or search scope: {text}"
        )

    if is_substantive_vault_search(text):
        subject = extract_search_subject(text)

        if subject:
            state["last_search_subject"] = subject
            state["last_search_at"] = now

    return text



def split_telegram_message(
    text: str,
    limit: int = 3400,
) -> list[str]:
    """
    Split a long response without losing content.

    The limit is kept below Telegram's hard maximum so that continuation
    labels and Unicode characters cannot push a message over the boundary.
    """
    remaining = (text or "").strip()

    if not remaining:
        return ["Alfred returned an empty response."]

    chunks: list[str] = []

    while len(remaining) > limit:
        candidates = [
            remaining.rfind("\n\n", 0, limit),
            remaining.rfind("\n", 0, limit),
            remaining.rfind(". ", 0, limit),
            remaining.rfind(" ", 0, limit),
        ]

        split_at = max(candidates)

        # Avoid creating a very small first fragment.
        if split_at < int(limit * 0.55):
            split_at = limit
        elif remaining[split_at:split_at + 2] == ". ":
            split_at += 1

        chunk = remaining[:split_at].rstrip()

        if not chunk:
            chunk = remaining[:limit]
            split_at = limit

        chunks.append(chunk)
        remaining = remaining[split_at:].lstrip()

    if remaining:
        chunks.append(remaining)

    return chunks


async def send_long_reply(message, text: str) -> None:
    """Send every response chunk sequentially and in the correct order."""
    chunks = split_telegram_message(text)

    for number, chunk in enumerate(chunks, start=1):
        if len(chunks) > 1:
            content = f"Part {number}/{len(chunks)}\n\n{chunk}"
        else:
            content = chunk

        await message.reply_text(content)


async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args).strip()
    if not text:
        await update.effective_message.reply_text("Usage: /ask <question>")
        return
    effective_text = prepare_contextual_search(text, context)
    reply = ask_hermes(effective_text)
    await send_long_reply(update.effective_message, reply)
async def hybrid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args).strip()

    if not text:
        await update.effective_message.reply_text("Usage: /hybrid <question>")
        return

    await update.effective_message.reply_text("Assessing best model for hybrid local + external reasoning...")

    path = capture_note(text, source="telegram /hybrid model-routed research")

    try:
        result = subprocess.run(
            [
                "python3",
                "/opt/second-brain/scripts/hybrid_openrouter.py",
                "recommend",
                text,
            ],
            capture_output=True,
            text=True,
            timeout=240,
        )

        raw = (result.stdout or result.stderr or "").strip()

        import json
        rec = json.loads(raw)

        request_id = rec["id"]
        recommended = rec["recommended"]
        reason = rec.get("reason", "No reason supplied.")

        keyboard = [
            [
                InlineKeyboardButton(
                    f"Run recommended: {recommended}",
                    callback_data=f"hybrid|{request_id}|recommended"
                )
            ],
            [
                InlineKeyboardButton("Run GPT", callback_data=f"hybrid|{request_id}|gpt"),
                InlineKeyboardButton("Run Claude", callback_data=f"hybrid|{request_id}|claude"),
            ],
            [
                InlineKeyboardButton("Run Gemini", callback_data=f"hybrid|{request_id}|gemini"),
                InlineKeyboardButton("Run Perplexity", callback_data=f"hybrid|{request_id}|perplexity"),
            ],
        ]

        await update.effective_message.reply_text(
            f"Recommended model: {recommended}\nReason: {reason}\n\nChoose how to run it:",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

        await update.effective_message.reply_text(f"Captured into second brain: {path.name}")

    except Exception as e:
        await update.effective_message.reply_text(f"Hybrid recommendation failed: {e}")


async def hybrid_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    try:
        _, request_id, choice = query.data.split("|", 2)

        await query.edit_message_text(
            f"Running hybrid request {request_id} using: {choice}"
        )

        result = subprocess.run(
            [
                "python3",
                "/opt/second-brain/scripts/hybrid_openrouter.py",
                "run",
                request_id,
                choice,
            ],
            capture_output=True,
            text=True,
            timeout=420,
        )

        reply = (result.stdout or result.stderr or "").strip()

        if not reply:
            reply = "Hybrid model returned no usable response."

        await send_long_reply(query.message, reply)
        feedback_keyboard = [
            [
                InlineKeyboardButton("👍 Good", callback_data=f"hybridfb|{request_id}|good"),
                InlineKeyboardButton("👎 Poor", callback_data=f"hybridfb|{request_id}|poor"),
            ]
        ]

        await query.message.reply_text(
            "Was this model choice useful?",
            reply_markup=InlineKeyboardMarkup(feedback_keyboard),
        )

    except Exception as e:
        await query.message.reply_text(f"Hybrid run failed: {e}")





async def perplexity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args).strip()

    if not text:
        await update.effective_message.reply_text("Usage: /perplexity <research question>")
        return

    await update.effective_message.reply_text(
        "Running hybrid Perplexity research with local Obsidian context..."
    )

    path = capture_note(text, source="telegram /perplexity hybrid research")

    try:
        result = subprocess.run(
            [
                "python3",
                "/opt/second-brain/scripts/perplexity_with_memory.py",
                text,
            ],
            capture_output=True,
            text=True,
            timeout=360,
        )

        reply = (result.stdout or result.stderr or "").strip()

        if not reply:
            reply = "Perplexity returned no usable response."

    except Exception as e:
        reply = f"Hybrid Perplexity research failed: {e}"

    run_semantic_reindex()

    await send_long_reply(update.effective_message, reply)
    await update.effective_message.reply_text(f"Captured into second brain: {path.name}")





async def operate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text("Starting Hermes Agent Operating Cycle. This may take several minutes.")
    try:
        r = subprocess.run(
            ["/opt/second-brain/scripts/run_agent_operating_cycle.sh"],
            capture_output=True,
            text=True,
            timeout=1800
        )
        out = (r.stdout or r.stderr or "").strip()
        await update.effective_message.reply_text(out[-3900:] if out else "Agent operating cycle completed.")
    except Exception as e:
        await update.effective_message.reply_text(f"Agent operating cycle failed: {e}")




async def brief(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text("Generating executive briefing...")
    try:
        subprocess.run(["/opt/second-brain/scripts/generate_daily_briefing.sh"], timeout=600)
        today = datetime.now().strftime("%Y-%m-%d")
        path = Path(f"/docker/obsidian-vault/07 Executive Briefings/{today} Daily Second Brain Briefing.md")
        out = path.read_text(encoding="utf-8", errors="ignore") if path.exists() else "Briefing file not found."
        await update.effective_message.reply_text(out[:3900])
    except Exception as e:
        await update.effective_message.reply_text(f"Briefing failed: {e}")


async def themes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text("Analysing emerging themes...")
    try:
        r = subprocess.run(
            ["/opt/second-brain/scripts/query_memory.py", "--quiet", "what themes are emerging from my captures and enriched memory"],
            capture_output=True,
            text=True,
            timeout=420
        )
        await update.effective_message.reply_text(((r.stdout or r.stderr or "No response").strip())[:3900])
    except Exception as e:
        await update.effective_message.reply_text(f"Themes query failed: {e}")


async def risks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text("Analysing risks...")
    try:
        r = subprocess.run(
            ["/opt/second-brain/scripts/query_memory.py", "--quiet", "what are the main unresolved governance operational trading and second brain risks"],
            capture_output=True,
            text=True,
            timeout=420
        )
        await update.effective_message.reply_text(((r.stdout or r.stderr or "No response").strip())[:3900])
    except Exception as e:
        await update.effective_message.reply_text(f"Risk query failed: {e}")


async def stalled(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text("Checking stalled open loops...")
    try:
        subprocess.run(["python3", "/opt/second-brain/scripts/open_loop_escalation.py"], timeout=180)
        path = Path("/docker/obsidian-vault/08 Open Loops/Escalation/Latest Open Loop Escalation Report.md")
        out = path.read_text(encoding="utf-8", errors="ignore") if path.exists() else "Open loop escalation report not found."
        await update.effective_message.reply_text(out[:3900])
    except Exception as e:
        await update.effective_message.reply_text(f"Stalled loop check failed: {e}")


async def watchlists(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text("Refreshing strategic watchlists...")
    try:
        subprocess.run(["python3", "/opt/second-brain/scripts/strategic_watchlists.py"], timeout=180)
        path = Path("/docker/obsidian-vault/09 Governance/Watchlists/Latest Strategic Watchlist Summary.md")
        out = path.read_text(encoding="utf-8", errors="ignore") if path.exists() else "Watchlist summary not found."
        await update.effective_message.reply_text(out[:3900])
    except Exception as e:
        await update.effective_message.reply_text(f"Watchlist refresh failed: {e}")


async def councilpack(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text("Running agent council pack...")
    try:
        subprocess.run(["python3", "/opt/second-brain/scripts/agent_council_pack.py"], timeout=900)
        path = Path("/docker/obsidian-vault/07 AI Memory/Agent Council/Latest Agent Council Pack.md")
        out = path.read_text(encoding="utf-8", errors="ignore") if path.exists() else "Council pack not found."
        await update.effective_message.reply_text(out[:3900])
    except Exception as e:
        await update.effective_message.reply_text(f"Council pack failed: {e}")



async def decisions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text("Generating decision intelligence...")
    try:
        subprocess.run(["python3", "/opt/second-brain/scripts/decision_intelligence.py"], timeout=240)
        path = Path("/docker/obsidian-vault/09 Governance/Decision Intelligence/Latest Decision Intelligence.md")
        out = path.read_text(encoding="utf-8", errors="ignore")
        await update.effective_message.reply_text(out[:3900])
    except Exception as e:
        await update.effective_message.reply_text(f"Decision intelligence failed: {e}")


async def delegatequeue(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text("Generating delegation queue...")
    try:
        subprocess.run(["python3", "/opt/second-brain/scripts/delegation_engine.py"], timeout=240)
        path = Path("/docker/obsidian-vault/09 Governance/Delegation Queue/Latest Delegation Queue.md")
        out = path.read_text(encoding="utf-8", errors="ignore")
        await update.effective_message.reply_text(out[:3900])
    except Exception as e:
        await update.effective_message.reply_text(f"Delegation queue failed: {e}")


async def memory(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args).strip()
    if not text:
        await update.effective_message.reply_text("Usage: /memory <question>")
        return

    await update.effective_message.reply_text("Searching enriched memory and synthesising answer...")

    try:
        r = subprocess.run(
            ["/opt/second-brain/scripts/query_memory.py", "--quiet", text],
            capture_output=True,
            text=True,
            timeout=420
        )
        out = (r.stdout or r.stderr or "").strip()
        if not out:
            out = "No memory response returned."

        # Telegram message limit safety
        await update.effective_message.reply_text(out[-3900:])
    except Exception as e:
        await update.effective_message.reply_text(f"Memory query failed: {e}")


async def delegate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args).strip()
    if not text:
        await update.effective_message.reply_text("Usage: /delegate <request>")
        return

    await update.effective_message.reply_text("Delegating request to specialist agent...")

    try:
        r = subprocess.run(
            ["python3", "/opt/second-brain/scripts/delegate_request.py", text],
            capture_output=True,
            text=True,
            timeout=420
        )
        out = (r.stdout or r.stderr or "").strip()
        await update.effective_message.reply_text(out[-3900:] if out else "Delegation completed.")
    except Exception as e:
        await update.effective_message.reply_text(f"Delegation failed: {e}")


async def council(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text("Starting Hermes Agent Council review. This may take several minutes.")
    try:
        r = subprocess.run(
            ["python3", "/opt/second-brain/scripts/agent_council.py"],
            capture_output=True,
            text=True,
            timeout=1200
        )
        out = (r.stdout or r.stderr or "").strip()
        await update.effective_message.reply_text(out[-3900:] if out else "Agent Council completed.")
    except Exception as e:
        await update.effective_message.reply_text(f"Agent Council failed: {e}")


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (update.message.text or "").strip()
    if not text:
        return

    effective_text = prepare_contextual_search(text, context)
    reply = ask_hermes(effective_text)

    reply = (reply or "").strip()

    if not reply:
        reply = (
            "Alfred produced no usable response. "
            "Try /semantic if this is a memory search, or ask again with 'draft' or 'write' "
            "if you want a generated answer."
        )

    await send_long_reply(update.effective_message, reply)
async def hybrid_debate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args).strip()

    if not text:
        await update.effective_message.reply_text("Usage: /debate <question>")
        return

    await update.effective_message.reply_text("Running multi-model debate: GPT + Claude + Gemini...")

    path = capture_note(text, source="telegram /debate multi-model")
    try:
        result = subprocess.run(
            [
                "python3",
                "/opt/second-brain/scripts/hybrid_openrouter.py",
                "debate",
                text,
            ],
            capture_output=True,
            text=True,
            timeout=900,
        )

        reply = (result.stdout or result.stderr or "").strip() or "Debate returned no usable response."
        await send_long_reply(update.effective_message, reply)
        if len(reply) > 3900:
            await update.effective_message.reply_text(reply[3900:7800])

    except Exception as e:
        await update.effective_message.reply_text(f"Hybrid debate failed: {e}")

    run_semantic_reindex()
    await update.effective_message.reply_text(f"Captured into second brain: {path.name}")


async def hybrid_chain(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args).strip()

    if not text:
        await update.effective_message.reply_text("Usage: /chain <question>")
        return

    await update.effective_message.reply_text("Running hybrid chain: Perplexity research → Claude analysis → GPT action plan...")

    path = capture_note(text, source="telegram /chain hybrid")
    try:
        result = subprocess.run(
            [
                "python3",
                "/opt/second-brain/scripts/hybrid_openrouter.py",
                "chain",
                text,
            ],
            capture_output=True,
            text=True,
            timeout=1000,
        )

        reply = (result.stdout or result.stderr or "").strip() or "Hybrid chain returned no usable response."

        for i in range(0, min(len(reply), 11700), 3900):
            await update.effective_message.reply_text(reply[i:i+3900])

    except Exception as e:
        await update.effective_message.reply_text(f"Hybrid chain failed: {e}")

    run_semantic_reindex()
    await update.effective_message.reply_text(f"Captured into second brain: {path.name}")





async def hybrid_feedback_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    try:
        _, request_id, rating = query.data.split("|", 2)

        subprocess.run(
            [
                "python3",
                "/opt/second-brain/scripts/hybrid_openrouter.py",
                "feedback",
                request_id,
                rating,
            ],
            capture_output=True,
            text=True,
            timeout=60,
        )

        await query.edit_message_text(f"Feedback recorded: {rating}")

    except Exception as e:
        await query.message.reply_text(f"Feedback failed: {e}")





async def image_artifact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args).strip()

    if not text:
        await update.effective_message.reply_text("Usage: /image <image prompt>")
        return

    await update.effective_message.reply_text("Creating image artifact from local memory and visual prompt routing...")

    path = capture_note(text, source="telegram /image artifact")

    try:
        result = subprocess.run(
            [
                "python3",
                "/opt/second-brain/scripts/image_artifact.py",
                text,
            ],
            capture_output=True,
            text=True,
            timeout=420,
        )

        raw = (result.stdout or result.stderr or "").strip()

        import json
        data = json.loads(raw)

        if data.get("ok") and data.get("image_path"):
            image_path = data["image_path"]

            with open(image_path, "rb") as img:
                await update.message.reply_photo(
                    photo=InputFile(img),
                    caption="Generated image artifact"
                )

            await update.effective_message.reply_text(
                f"Image saved: {image_path}\nVault record: {data.get('vault_record')}"
            )

        else:
            message = data.get("message", "Image generation did not complete.")
            spec = data.get("visual_spec", "")

            reply = (
                "Image file was not generated, but the visual specification was created.\n\n"
                f"Reason: {message}\n\n"
                f"{spec}"
            )

            for i in range(0, min(len(reply), 7800), 3900):
                await update.effective_message.reply_text(reply[i:i+3900])

            await update.effective_message.reply_text(
                f"Vault record: {data.get('vault_record')}"
            )

    except Exception as e:
        await update.effective_message.reply_text(f"Image artifact generation failed: {e}")

    run_semantic_reindex()
    await update.effective_message.reply_text(f"Captured into second brain: {path.name}")




async def titan(update, context):
    import subprocess
    result = subprocess.run(
        ["/opt/second-brain/scripts/titan_status.sh"],
        capture_output=True,
        text=True,
        timeout=30
    )
    output = (result.stdout or result.stderr or "Titan returned no output").strip()
    await update.effective_message.reply_text(output[:3900])








async def opinions(update, context):
    import subprocess
    topic = " ".join(context.args).strip()
    if not topic:
        await update.effective_message.reply_text("Usage: /opinions <topic for the board>")
        return

    result = subprocess.run(
        ["/opt/second-brain/scripts/agent_opinions.py", topic],
        capture_output=True,
        text=True,
        timeout=300
    )
    await update.effective_message.reply_text((result.stdout or result.stderr or "No agent opinions output.")[:3900])

async def governancereview(update, context):
    import subprocess
    result = subprocess.run(
        ["/opt/second-brain/scripts/athena_governance_review.py"],
        capture_output=True,
        text=True,
        timeout=60
    )
    await update.effective_message.reply_text((result.stdout or result.stderr or "No Athena governance review output.")[:3900])

async def gov(update, context):
    import subprocess
    result = subprocess.run(
        ["/opt/second-brain/scripts/governance_register.py", "summary"],
        capture_output=True,
        text=True,
        timeout=30
    )
    await update.effective_message.reply_text((result.stdout or result.stderr or "No governance register output.")[:3900])

async def decision(update, context):
    import subprocess
    text = " ".join(context.args).strip()
    if not text:
        await update.effective_message.reply_text("Usage: /decision <decision text>")
        return
    result = subprocess.run(
        ["/opt/second-brain/scripts/governance_register.py", "decision", text],
        capture_output=True,
        text=True,
        timeout=30
    )
    await update.effective_message.reply_text((result.stdout or result.stderr or "No output.")[:3900])

async def risk(update, context):
    import subprocess
    text = " ".join(context.args).strip()
    if not text:
        await update.effective_message.reply_text("Usage: /risk <risk text>")
        return
    result = subprocess.run(
        ["/opt/second-brain/scripts/governance_register.py", "risk", text],
        capture_output=True,
        text=True,
        timeout=30
    )
    await update.effective_message.reply_text((result.stdout or result.stderr or "No output.")[:3900])

async def action(update, context):
    import subprocess
    text = " ".join(context.args).strip()
    if not text:
        await update.effective_message.reply_text("Usage: /action <action text>")
        return
    result = subprocess.run(
        ["/opt/second-brain/scripts/governance_register.py", "action", text],
        capture_output=True,
        text=True,
        timeout=30
    )
    await update.effective_message.reply_text((result.stdout or result.stderr or "No output.")[:3900])

async def board(update, context):
    import subprocess, pathlib
    result = subprocess.run(
        ["/opt/second-brain/scripts/run_agent_council.sh"],
        capture_output=True,
        text=True,
        timeout=120
    )
    out = (result.stdout or result.stderr or "").strip()
    latest = pathlib.Path("/docker/obsidian-vault/09 Governance/Agent Governance/Latest Agent Council.md")
    body = latest.read_text(encoding="utf-8") if latest.exists() else out
    await update.effective_message.reply_text(body[:3900] or "Board meeting produced no output.")

async def boardpack(update, context):
    import subprocess, pathlib
    result = subprocess.run(
        ["python3", "/opt/second-brain/scripts/agent_council_pack.py"],
        capture_output=True,
        text=True,
        timeout=180
    )
    out = (result.stdout or result.stderr or "").strip()
    latest = pathlib.Path("/docker/obsidian-vault/07 AI Memory/Agent Council/Latest Agent Council Pack.md")
    if latest.exists():
        body = latest.read_text(encoding="utf-8")
        response = body[:3400] + "\n\nSaved to:\n" + str(latest)
    else:
        response = out[:3900]
    await update.effective_message.reply_text(response or "Board pack produced no output.")

async def approveboard(update, context):
    import subprocess
    result = subprocess.run(
        ["/opt/second-brain/scripts/titan_executor.py"],
        capture_output=True,
        text=True,
        timeout=330
    )
    output = ((result.stdout or "") + "\n" + (result.stderr or "")).strip()
    await update.effective_message.reply_text(output[:3900] or "Titan completed with no output.")

async def titanqueue(update, context):
    import json, pathlib, datetime

    playbook_path = pathlib.Path("/opt/second-brain/playbooks/titan_actions.json")
    actions = json.loads(playbook_path.read_text())
    allowed = sorted(actions.keys())

    if not context.args:
        await update.effective_message.reply_text(
            "Usage: /titanqueue <action>\n\nAllowed actions:\n" + "\n".join(allowed)
        )
        return

    action = context.args[0].strip()

    if action not in actions:
        await update.effective_message.reply_text(
            "Rejected: action is not allowed.\n\nAllowed actions:\n" + "\n".join(allowed)
        )
        return

    risk = actions[action].get("risk", "unknown")
    description = actions[action].get("description", action)

    ts = datetime.datetime.now(datetime.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    safe_ts = ts.replace(":", "").replace("-", "")
    action_id = f"telegram-{action}-{safe_ts}"

    req = {
        "id": action_id,
        "agent": "systems_devops_agent",
        "persona": "Titan",
        "action": action,
        "reason": "Queued from Telegram by Founder",
        "approved_by": "Hermes Prime",
        "status": "pending",
        "created_at": ts,
        "risk": risk,
        "description": description
    }

    q = pathlib.Path("/opt/second-brain/action-queue") / f"{action_id}.json"
    q.write_text(json.dumps(req, indent=2) + "\n")

    await update.effective_message.reply_text(
        f"Queued Titan action:\n{action}\n\nDescription: {description}\nRisk: {risk}\n\nRun /titanrun to execute."
    )


async def titanrun(update, context):
    import subprocess
    result = subprocess.run(
        ["/opt/second-brain/scripts/titan_executor.py"],
        capture_output=True,
        text=True,
        timeout=330
    )
    output = ((result.stdout or "") + "\n" + (result.stderr or "")).strip()
    if not output:
        output = "Titan completed with no output."
    await update.effective_message.reply_text(output[:3900])



async def reviewportfolio(update, context):
    import subprocess
    result = subprocess.run(
        ["python3", "/opt/hermes-trading/scripts/telegram_portfolio_review.py"],
        capture_output=True,
        text=True,
        timeout=60
    )
    output = ((result.stdout or "") + "\n" + (result.stderr or "")).strip()
    await update.effective_message.reply_text(output[:3900] or "Portfolio review produced no output.")

async def portfolio(update, context):
    await reviewportfolio(update, context)


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("health", health))
    app.add_handler(CommandHandler("capture", capture_only))
    app.add_handler(CommandHandler("ask", ask))
    app.add_handler(CommandHandler("hybrid", hybrid))
    app.add_handler(CommandHandler("image", image_artifact))
    app.add_handler(CommandHandler("debate", hybrid_debate))
    app.add_handler(CommandHandler("chain", hybrid_chain))
    app.add_handler(CommandHandler("perplexity", perplexity))
    app.add_handler(CommandHandler("council", council))
    app.add_handler(CommandHandler("delegate", delegate))
    app.add_handler(CommandHandler("memory", memory))
    app.add_handler(CommandHandler("councilpack", councilpack))
    app.add_handler(CommandHandler("decisions", decisions))
    app.add_handler(CommandHandler("delegatequeue", delegatequeue))
    app.add_handler(CommandHandler("watchlists", watchlists))
    app.add_handler(CommandHandler("stalled", stalled))
    app.add_handler(CommandHandler("risks", risks))
    app.add_handler(CommandHandler("themes", themes))
    app.add_handler(CommandHandler("brief", brief))
    app.add_handler(CommandHandler("operate", operate))
    app.add_handler(CommandHandler("opinions", opinions))
    app.add_handler(CommandHandler("governancereview", governancereview))
    app.add_handler(CommandHandler("gov", gov))
    app.add_handler(CommandHandler("decision", decision))
    app.add_handler(CommandHandler("risk", risk))
    app.add_handler(CommandHandler("action", action))
    app.add_handler(CommandHandler("board", board))
    app.add_handler(CommandHandler("boardpack", boardpack))
    app.add_handler(CommandHandler("approveboard", approveboard))
    app.add_handler(CommandHandler("titanqueue", titanqueue))
    app.add_handler(CommandHandler("titanrun", titanrun))
    app.add_handler(CommandHandler("titan", titan))
    app.add_handler(CommandHandler("reviewportfolio", reviewportfolio))
    app.add_handler(CommandHandler("portfolio", portfolio))

    # ALFRED_AGENT_ORG_REGISTER_START
    for _alfred_agent_command, _alfred_agent_handler in ALFRED_AGENT_COMMAND_HANDLERS.items():
        try:
            app.add_handler(CommandHandler(_alfred_agent_command, _alfred_agent_handler), group=-1)
        except TypeError:
            app.add_handler(CommandHandler(_alfred_agent_command, _alfred_agent_handler))
    # ALFRED_AGENT_ORG_REGISTER_END


    app.add_handler(CallbackQueryHandler(hybrid_callback, pattern="^hybrid\\|"))
    app.add_handler(CallbackQueryHandler(hybrid_feedback_callback, pattern="^hybridfb\\|"))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    app.run_polling()


if __name__ == "__main__":
    main()

```
