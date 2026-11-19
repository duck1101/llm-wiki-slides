"""MDE Paper Wiki 的抽取與自動檢查。

用法（在專案根目錄執行）：
  python tools/check.py extract <raw/YYYY_Title>          節點 1：抽取 paper.txt + 檢查 A
  python tools/check.py wiki    <raw/YYYY_Title/paper.txt> [slides/X.outline.md]  節點 3：檢查 C
  python tools/check.py spec    <slides/X.spec.md> <wiki/papers/X.md>   節點 4：檢查 D（含篇幅預算）
  python tools/check.py html    <slides/X.html> <slides/X.spec.md>      節點 5：檢查 E（文字部分）
  python tools/check.py figure  <raw/YYYY_Title> <頁碼> [輸出.png]       將 PDF 某頁輸出成圖片，供架構圖對照

結束碼：0 = 通過，1 = 不通過。
"""
import html as htmlmod
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
LINK_RE = re.compile(r"\[\[([^\]|#\\]+)")
NUM_RE = re.compile(r"(?<![\w.])\d+\.\d+%?|(?<![\w.])\d+%")
FRONTMATTER_KEYS = ("type", "tags", "sources", "updated")


def numbers(text):
    text = text.replace("−", "-")
    # Elsevier 排版寫成「68.7 %」；只合併同一行的空白，避免把「2.039\n% Improvement」誤合併
    text = re.sub(r"(\d)[    ]+%", r"\1%", text)
    return {n for n in NUM_RE.findall(text)}


def report(name, problems, info=(), warnings=()):
    for line in info:
        print(f"  {line}")
    for w in warnings:
        print(f"  警告：{w}")
    if problems:
        print(f"[{name}] 不通過（{len(problems)} 項）")
        for p in problems:
            print(f"  - {p}")
        return 1
    print(f"[{name}] 通過")
    return 0


# ---------- 節點 1 / 檢查 A ----------
def cmd_extract(rawdir):
    import pymupdf

    rawdir = pathlib.Path(rawdir)
    doc = pymupdf.open(rawdir / "paper.pdf")
    parts, problems = [], []
    for i, page in enumerate(doc, 1):
        t = page.get_text()
        if len(t.strip()) < 200:
            problems.append(f"第 {i} 頁文字過少（{len(t.strip())} 字元），可能是圖片或抽取失敗")
        parts.append(f"\n===== PAGE {i} =====\n{t}")
    text = "".join(parts)
    (rawdir / "paper.txt").write_text(text, encoding="utf-8")

    # 章節標題（支援多種排版）：
    #   CVF「1. Introduction」、Elsevier「1.  Introduction」：最多 5 個字，避免把「2. We recognize that ...」條列誤認為章節
    #   ACM「INTRODUCTION」：全大寫、獨立一行、為常見章節名稱
    numbered = re.findall(r"^(\d)\.?\s+([A-Z][A-Za-z]+(?: [A-Za-z]+){0,4})\s*$", text, re.M)
    common = r"INTRODUCTION|RELATED WORKS?|METHODS?|METHODOLOGY|EXPERIMENTS?|RESULTS|DISCUSSION|CONCLUSIONS?"
    caps = re.findall(rf"^({common})\s*$", text, re.M)
    sections = [f"{n}. {s}" for n, s in numbered] or caps
    # Table / Figure 標題：「Table 1.」「Table 1:」「Table 1」（Elsevier）、「Figure 1:」「Fig. 1.」
    tables = sorted({int(n) for n in re.findall(r"^Table (\d+)(?:[.:]|\s*$)", text, re.M)})
    figures = sorted({int(n) for n in re.findall(r"^(?:Figure|Fig\.) (\d+)[.:]", text, re.M)})
    if not sections:
        problems.append("找不到任何章節標題（如 '1. Introduction' 或 'INTRODUCTION'）")
    if not tables and not figures:
        problems.append("找不到任何 Table / Figure 標題")
    for kind, nums in (("Table", tables), ("Figure", figures)):
        if nums and nums != list(range(1, max(nums) + 1)):
            problems.append(f"{kind} 編號不連續：{nums}（可能有標題沒抓到）")
    info = [
        f"頁數：{doc.page_count}，輸出：{rawdir / 'paper.txt'}",
        "章節：" + "、".join(sections),
        f"Table：{tables}　Figure：{figures}",
    ]
    return report("A 抽取完整性", problems, info)


# ---------- 檢查 C ----------
def wiki_pages():
    return {p.stem: p for p in WIKI.rglob("*.md")}


def frontmatter(text):
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    return dict(re.findall(r"^(\w+):\s*(.*)$", m.group(1), re.M))


def cmd_wiki(paper_txt, outline_md=None):
    paper_txt = pathlib.Path(paper_txt)
    paper_id = paper_txt.parent.name
    src_nums = numbers(paper_txt.read_text(encoding="utf-8"))
    pages = wiki_pages()
    problems = []
    inbound = {k: 0 for k in pages}

    for stem, path in pages.items():
        text = path.read_text(encoding="utf-8")
        for link in set(LINK_RE.findall(text)):
            if link.startswith("raw/"):
                if not (ROOT / link).exists():
                    problems.append(f"{path.relative_to(ROOT)}：斷連結 [[{link}]]")
            elif link not in pages:
                problems.append(f"{path.relative_to(ROOT)}：斷連結 [[{link}]]")
            elif link != stem:
                inbound[link] += 1
        if stem in ("index", "log"):
            continue
        fm = frontmatter(text)
        if fm is None:
            problems.append(f"{path.relative_to(ROOT)}：缺少 frontmatter")
            continue
        missing = [k for k in FRONTMATTER_KEYS if k not in fm]
        if missing:
            problems.append(f"{path.relative_to(ROOT)}：frontmatter 缺 {missing}")
        if paper_id in fm.get("sources", ""):
            body = text.split("---", 2)[2]
            # 跨論文頁面：數值可以來自 frontmatter sources 列出的任一篇論文
            allowed = set()
            for src in re.findall(r"[\w.-]+", fm.get("sources", "")):
                txt = ROOT / "raw" / src / "paper.txt"
                if txt.exists():
                    allowed |= {s.lstrip("+-") for s in numbers(txt.read_text(encoding="utf-8"))}
                else:
                    problems.append(f"{path.relative_to(ROOT)}：sources 的 {src} 沒有 paper.txt")
            bad = sorted(n for n in numbers(body) if n.lstrip("+-") not in allowed)
            if bad:
                problems.append(f"{path.relative_to(ROOT)}：原文找不到的數值 {bad}")

    orphans = [k for k, c in inbound.items() if c == 0 and k not in ("index", "log")]
    if orphans:
        problems.append(f"孤兒頁（沒有被任何頁面連到）：{orphans}")
    index_links = set(LINK_RE.findall(pages["index"].read_text(encoding="utf-8")))
    not_indexed = [k for k in pages if k not in index_links and k not in ("index", "log")]
    if not_indexed:
        problems.append(f"index.md 沒有列出：{not_indexed}")
    warnings = []
    if outline_md:
        outline = pathlib.Path(outline_md).read_text(encoding="utf-8")
        paper_page = pages.get(paper_id)
        if paper_page is None:
            problems.append(f"找不到 paper 頁 wiki/papers/{paper_id}.md")
        else:
            heads = headings(paper_page.read_text(encoding="utf-8"))
            for sec in re.findall(r"→ 段落：(.+)$", outline, re.M):
                for s in sec.split("、"):  # 只以頓號分隔，段落名稱本身可能含逗號（如 §3.1, Fig. 2）
                    s = s.strip()
                    if s and s not in heads:
                        problems.append(f"大綱預定的段落不在 paper 頁：「{s}」")
        planned = set()
        m = re.search(r"^## 預計頁面\n(.*?)(?=^## |\Z)", outline, re.S | re.M)
        if m:
            planned = set(LINK_RE.findall(m.group(1)))
        for name in sorted(planned - set(pages)):
            problems.append(f"大綱預計的頁面沒有建立：[[{name}]]")
        for stem, path in pages.items():
            if stem in (paper_id, "index", "log") or stem in planned:
                continue
            fm = frontmatter(path.read_text(encoding="utf-8")) or {}
            if paper_id in fm.get("sources", ""):
                warnings.append(f"大綱外新增或更新：[[{stem}]]（需在 log 說明）")
    return report("C Wiki", problems, [f"頁面數：{len(pages) - 2}（不含 index、log）"], warnings)


# ---------- 檢查 D ----------
def headings(md):
    return {h.strip() for h in re.findall(r"^#{1,6} (.+)$", md, re.M)}


def cmd_spec(spec_md, paper_md):
    spec = pathlib.Path(spec_md).read_text(encoding="utf-8")
    paper = pathlib.Path(paper_md).read_text(encoding="utf-8")
    paper_stem = pathlib.Path(paper_md).stem
    problems = []
    slides = re.split(r"^## (S\d+ · .+)$", spec, flags=re.M)[1:]
    slides = list(zip(slides[0::2], slides[1::2]))
    if not 8 <= len(slides) <= 12:
        problems.append(f"總張數 {len(slides)}，不在 8～12 之間")
    paper_heads = headings(paper)
    paper_nums = {n.lstrip("+-") for n in numbers(paper)}
    for title, body in slides:
        for field in ("標題", "內容", "出處", "Wiki"):
            if not re.search(rf"^- {field}：", body, re.M):
                problems.append(f"{title}：缺少「{field}」欄位")
        for target in re.findall(r"\[\[([^\]|]+)\]\]", body):
            page, _, anchor = target.partition("#")
            if page != paper_stem:
                problems.append(f"{title}：Wiki 對應到非本篇頁面 [[{target}]]")
            elif anchor and anchor not in paper_heads:
                problems.append(f"{title}：paper 頁沒有段落「{anchor}」")
        bad = sorted(n for n in numbers(body) if n.lstrip("+-") not in paper_nums)
        if bad:
            problems.append(f"{title}：paper 頁找不到的數值 {bad}")
        problems += [f"{title}：{p}" for p in budget(body)]
    return report("D Spec", problems, [f"張數：{len(slides)}", f"篇幅預算：條列 ≤ {MAX_BULLETS}（有表格 ≤ {MAX_BULLETS_WITH_TABLE}）、每條 ≤ {MAX_CHARS} 字元、表格 ≤ {MAX_ROWS} 列"])


MAX_BULLETS, MAX_BULLETS_WITH_TABLE, MAX_CHARS, MAX_ROWS = 9, 6, 100, 7


def field_block(body, field):
    m = re.search(rf"^- {field}：(.*?)(?=^- \S+：|\Z)", body, re.S | re.M)
    return m.group(1) if m else ""


def budget(body):
    problems = []
    content = field_block(body, "內容")
    bullets = [re.sub(r"^\s+- ", "", l) for l in content.splitlines() if re.match(r"^\s+- ", l)]
    figure = field_block(body, "圖表")
    tables, rows = [], None
    for line in figure.splitlines():
        if "欄：" in line:
            rows = 0
            tables.append(rows)
        elif "｜" in line and tables:
            tables[-1] += 1
    limit = MAX_BULLETS_WITH_TABLE if tables else MAX_BULLETS
    if len(bullets) > limit:
        problems.append(f"內容條列 {len(bullets)} 條，超過預算 {limit}")
    for b in bullets:
        if len(b) > MAX_CHARS:
            problems.append(f"條列過長（{len(b)} 字元）：{b[:20]}…")
    for k, n in enumerate(tables, 1):
        if n > MAX_ROWS:
            problems.append(f"第 {k} 個表格 {n} 列，超過預算 {MAX_ROWS}")
    if "架構圖" in figure:
        for key in ("節點：", "連線：", "對照："):
            if key not in figure:
                problems.append(f"架構圖缺少「{key}」")
    return problems


# ---------- 檢查 E（文字部分） ----------
def html_text(raw):
    raw = re.sub(r"(?s)<(style|script)\b.*?</\1>", "", raw)
    return htmlmod.unescape(re.sub(r"<[^>]+>", " ", raw))


def cmd_html(html_path, spec_md):
    raw = pathlib.Path(html_path).read_text(encoding="utf-8")
    spec = pathlib.Path(spec_md).read_text(encoding="utf-8")
    problems = []
    n_html = len(re.findall(r'<section class="slide', raw))
    n_spec = len(re.findall(r"^## S\d+ · ", spec, re.M))
    if n_html != n_spec:
        problems.append(f"投影片數不一致：HTML {n_html} 張，spec {n_spec} 張")
    h = {n.lstrip("+-") for n in numbers(html_text(raw))}
    # 「Wiki：」欄位是段落連結（例如 設定（§4.1–4.3）），不是投影片內容，不納入比對
    spec_content = "\n".join(l for l in spec.splitlines() if not l.startswith("- Wiki："))
    s = {n.lstrip("+-") for n in numbers(spec_content)}
    if h - s:
        problems.append(f"HTML 有、spec 沒有的數值：{sorted(h - s)}")
    if s - h:
        problems.append(f"spec 有、HTML 漏掉的數值：{sorted(s - h)}")
    return report("E HTML（文字）", problems, [f"張數：HTML {n_html} / spec {n_spec}"])


# ---------- 架構圖對照用：輸出 PDF 頁面圖片 ----------
def cmd_figure(rawdir, page, out=None):
    import pymupdf
    import tempfile

    rawdir = pathlib.Path(rawdir)
    doc = pymupdf.open(rawdir / "paper.pdf")
    out = pathlib.Path(out) if out else pathlib.Path(tempfile.gettempdir()) / f"{rawdir.name}_p{page}.png"
    doc[int(page) - 1].get_pixmap(dpi=110).save(out)
    print(out)
    return 0


if __name__ == "__main__":
    cmds = {"extract": cmd_extract, "wiki": cmd_wiki, "spec": cmd_spec, "html": cmd_html, "figure": cmd_figure}
    if len(sys.argv) < 3 or sys.argv[1] not in cmds:
        print(__doc__)
        sys.exit(2)
    sys.exit(cmds[sys.argv[1]](*sys.argv[2:]))
