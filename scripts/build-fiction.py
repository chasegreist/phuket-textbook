#!/usr/bin/env python3
"""
Build the "Five-Foot Way" historical-fiction pages from the manuscript.

Reads the chapter markdown in the Cowork manuscript folder and emits:
  - historical-fiction.html      (password gate + blurb + table of contents)
  - fiction-ch1.html .. ch8.html (one reading page per chapter)

Re-run this after editing the manuscripts to regenerate every page.
Usage:  python3 scripts/build-fiction.py
"""

import html
import re
from pathlib import Path

# --- paths -----------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
SRC = Path(
    "/Users/chasegreist/Documents/Cowork/Phuket-Historical-Fiction/03-Manuscript"
)

PASSWORD = "learn"
STORAGE_KEY = "phuket-fiction-unlocked"
CONTENTS_PAGE = "historical-fiction.html"

# --- chapter configuration -------------------------------------------------
# title_html: key word wrapped in <em> for the accent treatment.
# dek:        short mono time-label shown under the chapter title.
# teaser:     one-line orienting blurb shown in the table of contents.
# skip_intro: a standalone manuscript line to drop from the body (it becomes
#             the dek instead).
CHAPTERS = [
    {
        "file": "chapter-01-the-harbour.md",
        "roman": "I", "n": 1,
        "title_html": "The <em>Harbour</em>", "title_text": "The Harbour",
        "dek": "Phuket · 1901",
        "teaser": "Mei goes to the harbour with her father and watches a boat of new arrivals come ashore.",
    },
    {
        "file": "chapter-02-the-alley.md",
        "roman": "II", "n": 2,
        "title_html": "The <em>Alley</em>", "title_text": "The Alley",
        "dek": "Three nights later", "skip_intro": "Three nights later.",
        "teaser": "A sound of breathing in the back alley, after midnight.",
    },
    {
        "file": "chapter-03-the-englishman.md",
        "roman": "III", "n": 3,
        "title_html": "The <em>Englishman</em>", "title_text": "The Englishman",
        "dek": "A week later",
        "teaser": "A young British engineer arrives at the front of the shop — and his machine.",
    },
    {
        "file": "chapter-04-double-life.md",
        "roman": "IV", "n": 4,
        "title_html": "Double <em>Life</em>", "title_text": "Double Life",
        "dek": "The days find a shape",
        "teaser": "Two worlds in one house: the front room and the storage room.",
    },
    {
        "file": "chapter-05-the-question.md",
        "roman": "V", "n": 5,
        "title_html": "The <em>Question</em>", "title_text": "The Question",
        "dek": "An afternoon caller",
        "teaser": "A polite man comes to the shop, asking quiet questions about a runaway.",
    },
    {
        "file": "chapter-06-kathu.md",
        "roman": "VI", "n": 6,
        "title_html": "<em>Kathu</em>", "title_text": "Kathu",
        "dek": "The road to the mines",
        "teaser": "The road to the mines, and the demonstration of the water cannon.",
    },
    {
        "file": "chapter-07-the-dinner.md",
        "roman": "VII", "n": 7,
        "title_html": "The <em>Dinner</em>", "title_text": "The Dinner",
        "dek": "Three families, one table",
        "teaser": "Three families, one official, and a dinner where the words between languages decide things.",
    },
    {
        "file": "chapter-08-the-harbour-ii.md",
        "roman": "VIII", "n": 8,
        "title_html": "The <em>Harbour</em>", "title_text": "The Harbour",
        "dek": "The morning tide",
        "teaser": "A boat on the morning tide, and the same street seen new.",
    },
]


# ---------------------------------------------------------------------------
# Vocabulary glossary — EAL click-to-define support.
# The first occurrence of each term in a chapter body is wrapped in a
# <span class="vocab" data-def="..."> so scripts/vocab.js shows a popup.
# Manuscripts stay clean; definitions live here. Covers historical/domain
# words (towkay, ang-yi, alluvial...) and Tier-2 English (bureaucrat,
# obsolete, conviction...). Plain, G8/EAL-friendly definitions.
# ---------------------------------------------------------------------------
_GLOSSARY_SRC = [
    # --- food & home ---
    ("jok", "A rice porridge (also called congee) — rice boiled in lots of water until soft and creamy. A common breakfast across Asia.", "johk"),
    ("you tiao", "A long stick of fried dough eaten at breakfast, often dipped in rice porridge or soy milk.", "yoh-tyao"),
    ("five-foot way", "The covered walkway running along the front of the shophouses, about five feet wide. It gives shelter from sun and rain."),
    ("shophouse", "A narrow building with a shop on the ground floor and the family's home on the floors above — common in old Southeast Asian towns."),
    ("kebaya", "A light, fitted blouse worn by women in the Malay world, usually over a sarong.", "kuh-BAH-yah"),
    ("ancestor shrine", "A small altar in the home honouring dead family members, where incense is burned and prayers are said."),
    # --- peoples & places ---
    ("Hokkien", "A Chinese language from Fujian province in southern China, spoken by most of Phuket's Chinese families.", "HOK-ee-en"),
    ("Fujian", "A province on the southeast coast of China — the home region of most Chinese migrants to Phuket.", "foo-JYEN"),
    ("Quanzhou", "A port city in Fujian, China, that many Phuket migrants set sail from.", "chwan-JOH"),
    ("Penang", "An island and city in present-day Malaysia with a large Chinese community — a major trading partner of Phuket.", "puh-NANG"),
    ("Rangoon", "The main city and port of Burma (now called Yangon, in Myanmar).", "rang-GOON"),
    ("Siamese", "Belonging to Siam, the old name for Thailand (used until 1939). 'Siamese' means Thai.", "sy-uh-MEEZ"),
    ("Kathu", "The main mining area of Phuket, in the hills inland from the town, where tin was first found in 1809.", "kah-TOO"),
    ("Peranakan", "Descendants of early Chinese settlers who married local Malay people, blending both cultures. Also called Baba-Nyonya.", "puh-rah-nah-KAHN"),
    # --- mining & labour ---
    ("coolie", "An old and now offensive word for a poorly paid Asian labourer doing hard manual work. Used here for the indentured mine workers.", "KOO-lee"),
    ("ang-yi", "A Chinese secret society, or 'brotherhood.' In Phuket these groups controlled the mine contracts and much of Chinese life.", "AHNG-yee"),
    ("sipai", "An enforcer for a Chinese secret society — the men who collected debts and hunted down runaways.", "SEE-pai"),
    ("towkay", "A Hokkien word for a wealthy business owner or boss — here, the man who owns and runs a mine.", "toh-KAI"),
    ("barracks", "Plain buildings where many workers were housed together, like crowded dormitories.", "BA-raks"),
    ("overseer", "A boss who watches over workers and forces them to keep working, often harshly.", "OH-ver-see-er"),
    ("porter", "A worker who carries heavy loads — for example, loading and unloading boats at the harbour."),
    ("godown", "A warehouse for storing goods, especially near a harbour — a common word in Asian ports.", "GOH-down"),
    ("concession", "An official right, granted by a government, to use land or run a business such as a mine in a certain area.", "kun-SESH-un"),
    # --- tin technology ---
    ("hydraulic monitor", "A high-pressure water cannon. Aimed at a hillside, it blasts the earth apart so the tin can be washed out — doing the work of many men.", "hy-DROL-ik MON-i-ter"),
    ("hydraulic", "Powered by water moving under high pressure.", "hy-DROL-ik"),
    ("monitor", "Here, short for a hydraulic monitor — a powerful water cannon used to blast tin out of a hillside."),
    ("sluice", "A long wooden channel that water runs through. Miners used it to wash away light soil so the heavy tin would settle and could be collected.", "sloos"),
    ("palong", "A raised wooden sluice box built on a scaffold, used to process large amounts of tin-bearing mud and gravel.", "PAH-long"),
    ("alluvial", "Made of sand, gravel and soil carried and dropped by rivers over a long time. Phuket's tin sat in alluvial gravel, easy to dig out.", "al-LOO-vee-uhl"),
    ("cassiterite", "The most common tin ore — a heavy, dark, almost-black mineral that settles at the bottom of the sluice.", "kuh-SIT-uh-rite"),
    ("sediment", "Tiny bits of sand, mud and rock that settle to the bottom of water.", "SED-i-ment"),
    ("deposit", "An amount of a mineral, such as tin, that has built up naturally in the ground.", "di-POZ-it"),
    ("swivel", "A joint that lets something turn freely from side to side.", "SWIV-uhl"),
    ("scaffolding", "A temporary frame of poles and planks used to support a structure or hold workers up high.", "SKAF-uhl-ding"),
    # --- travel, trade & objects ---
    ("mangrove", "A tree that grows in salty water along tropical coasts, with tangled roots rising out of the mud.", "MANG-grohv"),
    ("junk", "A traditional Chinese wooden sailing ship with broad sails, used for trade and travel across Southeast Asia."),
    ("rickshaw", "A small two-wheeled passenger cart pulled by a person on foot.", "RIK-shaw"),
    ("opium", "An addictive drug made from poppies and smoked to dull pain. It was sold openly in the mines and kept many workers in debt.", "OH-pee-um"),
    ("telegraph", "A machine that sends written messages over long distances as electric signals through wires — the fastest communication of the 1900s.", "TEL-uh-graf"),
    # --- Tier-2 academic English ---
    ("hospitality", "A warm, generous welcome given to guests.", "hos-pi-TAL-i-tee"),
    ("conviction", "A strong, firm belief that you are right.", "kun-VIK-shun"),
    ("obsolete", "No longer useful or needed, because something newer has replaced it.", "OB-suh-leet"),
    ("patriarch", "The most senior and respected male leader of a family.", "PAY-tree-ark"),
    ("negotiate", "To talk and bargain with others in order to reach an agreement.", "ni-GOH-shee-ate"),
    ("transition", "A change from one system or state to another, and the in-between period while it happens.", "tran-ZISH-un"),
    ("bureaucrat", "A government official whose job is to follow official rules and handle paperwork. 'Bureaucratic' describes this careful, rule-bound way of working.", "BYOOR-uh-krat"),
]

GLOSSARY = {}
for _term, _definition, *_rest in _GLOSSARY_SRC:
    GLOSSARY[_term.lower()] = {
        "def": _definition,
        "pron": _rest[0] if _rest else None,
        # match the whole word, allowing a simple plural (s/es), case-insensitive
        "re": re.compile(r"\b" + re.escape(_term) + r"(?:e?s)?\b", re.IGNORECASE),
    }


def _vocab_span(word: str, entry: dict) -> str:
    d = html.escape(entry["def"], quote=True)
    pron = entry.get("pron")
    pron_attr = f' data-pron="{html.escape(pron, quote=True)}"' if pron else ""
    return f'<span class="vocab" data-def="{d}"{pron_attr}>{word}</span>'


def _wrap_text(text: str, used: set) -> str:
    """Wrap the first unused glossary term occurrences inside a plain-text run."""
    out = []
    i, n = 0, len(text)
    while i < n:
        best = None  # (start, end, key)
        for key, entry in GLOSSARY.items():
            if key in used:
                continue
            m = entry["re"].search(text, i)
            if not m:
                continue
            # earliest start wins; on a tie the longer match wins
            if best is None or m.start() < best[0] or (m.start() == best[0] and m.end() > best[1]):
                best = (m.start(), m.end(), key)
        if best is None:
            out.append(text[i:])
            break
        start, end, key = best
        out.append(text[i:start])
        out.append(_vocab_span(text[start:end], GLOSSARY[key]))
        used.add(key)
        i = end
    return "".join(out)


def wrap_vocab(fragment: str, used: set) -> str:
    """Wrap glossary terms in an HTML fragment, skipping inside any tag."""
    parts = re.split(r"(<[^>]+>)", fragment)
    return "".join(
        p if (not p or p.startswith("<")) else _wrap_text(p, used) for p in parts
    )


def md_inline(text: str, vocab_used: set | None = None) -> str:
    """Escape HTML, turn *single-asterisk* spans into <em>, optionally add vocab."""
    text = html.escape(text, quote=False)
    text = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", text)
    if vocab_used is not None:
        text = wrap_vocab(text, vocab_used)
    return text


def parse_chapter(path: Path, skip_intro: str | None):
    """Return (body_html, note_html) from a chapter markdown file."""
    raw = path.read_text(encoding="utf-8")
    body_part, _, note_part = raw.partition("**Author's Historical Note**")

    # ---- body ----
    blocks = []
    for block in re.split(r"\n\s*\n", body_part.strip()):
        b = block.strip()
        if not b:
            continue
        if b.startswith("# "):            # the "# Chapter N: Title" heading
            continue
        if skip_intro and b == skip_intro:  # time-label promoted to the dek
            continue
        if re.fullmatch(r"-{3,}", b):
            blocks.append(("hr", None))
        else:
            blocks.append(("p", " ".join(b.split("\n"))))

    # drop dangling scene breaks at either end (e.g. the ---  before the note)
    while blocks and blocks[0][0] == "hr":
        blocks.pop(0)
    while blocks and blocks[-1][0] == "hr":
        blocks.pop()

    used = set()  # first-occurrence-per-chapter vocab tracking
    body_html = []
    for kind, val in blocks:
        if kind == "hr":
            body_html.append('    <hr class="scene-break" />')
        else:
            body_html.append(f"    <p>{md_inline(val, used)}</p>")
    body = "\n".join(body_html)

    # ---- author's note ----
    note_paras = [p.strip() for p in re.split(r"\n\s*\n", note_part.strip()) if p.strip()]
    note = "\n".join(f"      <p>{md_inline(p)}</p>" for p in note_paras)

    return body, note


CHAPTER_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>{title_text} · Chapter {roman} — Five-Foot Way</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles/textbook.css">
<link rel="stylesheet" href="styles/fiction.css">
<script>
  // Soft gate: only readable once the password has been entered on the
  // contents page in this browser session. Runs before the body paints.
  try {{
    if (sessionStorage.getItem('{key}') !== 'yes') {{
      location.replace('{contents}');
    }}
  }} catch (e) {{ /* sessionStorage unavailable — fall through */ }}
</script>
</head>
<body>

<nav class="site-nav">
  <a class="home-link" href="{contents}">Contents</a>
  <span>Chapter {roman} · {title_text}</span>
  {top_next}
</nav>

<article class="chapter">

  <header class="chapter-header">
    <div class="chapter-dek">Chapter {roman} &nbsp;·&nbsp; {dek}</div>
    <h1>{title_html}</h1>
  </header>

  <div class="chapter-body">
{body}
  </div>

  <aside class="author-note">
    <h3>Author's Historical Note</h3>
{note}
  </aside>

  <nav class="chapter-footer">
    {prev_link}
    {next_link}
  </nav>

</article>

<script src="scripts/vocab.js"></script>
</body>
</html>
"""


def build_chapter(ch, prev_ch, next_ch):
    href = lambda c: f"fiction-ch{c['n']}.html"

    # top-right nav link
    if next_ch:
        top_next = f'<a class="next-link" href="{href(next_ch)}">{next_ch["title_text"]}</a>'
    else:
        top_next = '<a class="next-link" href="index.html">The Book</a>'

    # footer prev
    if prev_ch:
        prev_link = f'<a class="prev" href="{href(prev_ch)}">Chapter {prev_ch["roman"]} · {prev_ch["title_text"]}</a>'
    else:
        prev_link = f'<a class="prev" href="{CONTENTS_PAGE}">Story Contents</a>'

    # footer next
    if next_ch:
        next_link = f'<a class="next" href="{href(next_ch)}">Chapter {next_ch["roman"]} · {next_ch["title_text"]}</a>'
    else:
        next_link = f'<a class="next" href="{CONTENTS_PAGE}">Back to Contents</a>'

    body, note = parse_chapter(SRC / ch["file"], ch.get("skip_intro"))

    out = CHAPTER_TEMPLATE.format(
        title_text=ch["title_text"],
        title_html=ch["title_html"],
        roman=ch["roman"],
        dek=ch["dek"],
        key=STORAGE_KEY,
        contents=CONTENTS_PAGE,
        top_next=top_next,
        prev_link=prev_link,
        next_link=next_link,
        body=body,
        note=note,
    )
    (ROOT / f"fiction-ch{ch['n']}.html").write_text(out, encoding="utf-8")


def build_contents():
    # opening blurb -> intro paragraphs
    blurb = (SRC / "opening-blurb.md").read_text(encoding="utf-8")
    # keep only prose paragraphs (skip the "# ..." title and the bold dateline)
    intro_paras = []
    for block in re.split(r"\n\s*\n", blurb.strip()):
        b = block.strip()
        if not b or b.startswith("#") or b.startswith("**"):
            continue
        intro_paras.append(f'      <p>{md_inline(" ".join(b.split(chr(10))))}</p>')
    intro = "\n".join(intro_paras)

    toc_rows = []
    for ch in CHAPTERS:
        toc_rows.append(
            f'''      <a class="toc-chapter" href="fiction-ch{ch['n']}.html">
        <div class="toc-num">{ch['roman']}</div>
        <div>
          <div class="toc-chapter-title">{ch['title_html']}</div>
          <div class="toc-chapter-teaser">{ch['teaser']}</div>
        </div>
      </a>'''
        )
    toc = "\n".join(toc_rows)

    out = CONTENTS_TEMPLATE.format(
        key=STORAGE_KEY,
        password=PASSWORD,
        intro=intro,
        toc=toc,
    )
    (ROOT / CONTENTS_PAGE).write_text(out, encoding="utf-8")


CONTENTS_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Five-Foot Way · Historical Fiction — Phuket</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles/textbook.css">
<link rel="stylesheet" href="styles/fiction.css">
</head>
<body>

<nav class="site-nav">
  <a class="home-link" href="index.html">The Book</a>
  <span>Historical Fiction</span>
  <span></span>
</nav>

<!-- ========================================================== -->
<!-- Password gate                                                -->
<!-- ========================================================== -->
<section id="gate" class="gate" aria-label="Password gate">
  <div class="gate-card">
    <div class="gate-eyebrow">A story for our class</div>
    <h1><em>Five-Foot Way</em></h1>
    <p>Phuket, 1901. Enter the password to read on.</p>
    <form id="gate-form" class="gate-form" autocomplete="off">
      <input
        type="password"
        id="gate-input"
        placeholder="password"
        aria-label="Password"
        autocomplete="off"
        autocapitalize="off"
        autocorrect="off"
        spellcheck="false"
      />
      <button type="submit">Open the story →</button>
      <div id="gate-error" class="gate-error" aria-live="polite"></div>
    </form>
    <div class="gate-hint">Ask your teacher for the password</div>
  </div>
</section>

<!-- ========================================================== -->
<!-- Story contents (revealed after password entry)               -->
<!-- ========================================================== -->
<article id="content" class="chapter" hidden>

  <header class="chapter-header">
    <div class="chapter-dek">Historical Fiction &nbsp;·&nbsp; Phuket · 1901</div>
    <h1><em>Five-Foot Way</em></h1>
    <p class="chapter-sub">
      An eight-chapter story set in Phuket Town in 1901 — the world of Hokkien
      tin merchants, Chinese mining coolies, and the first British engineers
      arriving with their machines. Each chapter ends with a short author's
      note about the real history behind it.
    </p>
  </header>

  <div class="story-intro">
{intro}
  </div>

  <div class="story-toc-label">The Chapters</div>
  <nav class="story-toc" aria-label="Chapters">
{toc}
  </nav>

  <nav class="chapter-footer">
    <a class="prev" href="index.html">The Book</a>
    <a class="next" href="fiction-ch1.html">Start reading · Chapter I</a>
  </nav>

</article>

<script>
(function() {{
  const KEY = '{key}';
  const PASSWORD = '{password}';
  const gate    = document.getElementById('gate');
  const content = document.getElementById('content');
  const form    = document.getElementById('gate-form');
  const input   = document.getElementById('gate-input');
  const errorEl = document.getElementById('gate-error');

  function unlock() {{
    gate.style.display = 'none';
    content.hidden = false;
  }}

  // Already unlocked in this browser session? Skip the gate.
  try {{
    if (sessionStorage.getItem(KEY) === 'yes') {{
      unlock();
      return;
    }}
  }} catch (e) {{ /* sessionStorage may be unavailable; fall through */ }}

  setTimeout(() => {{ try {{ input.focus(); }} catch (e) {{}} }}, 50);

  form.addEventListener('submit', (e) => {{
    e.preventDefault();
    const guess = (input.value || '').trim().toLowerCase();
    if (guess === PASSWORD) {{
      try {{ sessionStorage.setItem(KEY, 'yes'); }} catch (e) {{}}
      errorEl.textContent = '';
      unlock();
    }} else {{
      errorEl.textContent = 'Incorrect password. Try again.';
      input.value = '';
      input.focus();
    }}
  }});
}})();
</script>

</body>
</html>
"""


def main():
    for i, ch in enumerate(CHAPTERS):
        prev_ch = CHAPTERS[i - 1] if i > 0 else None
        next_ch = CHAPTERS[i + 1] if i < len(CHAPTERS) - 1 else None
        build_chapter(ch, prev_ch, next_ch)
        print(f"  wrote fiction-ch{ch['n']}.html")
    build_contents()
    print(f"  wrote {CONTENTS_PAGE}")


if __name__ == "__main__":
    main()
