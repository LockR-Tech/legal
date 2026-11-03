"""Dựng lại trang Điều khoản dịch vụ / Chính sách bảo mật từ bản gốc trong app.

Bản gốc duy nhất: mobile/assets/markdown/{terms_of_service,privacy_policy}{,_en}.md.
Sửa nội dung ở đó rồi chạy (repo mobile nằm cạnh repo này):

    python tools/build_pages.py            # mặc định đọc ../mobile/assets/markdown
    python tools/build_pages.py <thư mục>  # chỉ định thư mục markdown khác

Không sửa tay các file *.html sinh ra — lần dựng sau sẽ ghi đè.
"""
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT.parent / "mobile" / "assets" / "markdown"
EMAIL = "huynqbse180211@fpt.edu.vn"

# id văn bản trong app -> tên trang trên GitHub Pages (URL đã khai với Google Play / Facebook, đừng đổi).
PAGES = {"terms_of_service": "terms-of-service", "privacy_policy": "privacy-policy"}
LANGS = {
    "vi": {"suffix": "", "html_suffix": "", "other": "en", "switch": "English",
           "deletion": "Hướng dẫn xoá dữ liệu",
           "footer": "Bản gốc của trang này là nội dung hiển thị trong ứng dụng Lock.R."},
    "en": {"suffix": "_en", "html_suffix": "-en", "other": "vi", "switch": "Tiếng Việt",
           "deletion": "Data deletion guide",
           "footer": "This page mirrors the text shown in the Lock.R app."},
}

STYLE = """    :root { --navy: #003d5b; --accent: #0077b6; --muted: #64748b; --line: #e2e8f0; }
    * { box-sizing: border-box; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      color: #0f172a; line-height: 1.7; margin: 0; background: #f8fafc;
    }
    .wrap { max-width: 820px; margin: 0 auto; padding: 32px 24px 80px; background: #fff; }
    nav { display: flex; flex-wrap: wrap; gap: 8px 16px; font-size: 14px; margin-bottom: 24px; }
    nav a { text-decoration: none; }
    nav .lang { margin-left: auto; }
    h1 { font-size: 28px; margin: 0 0 4px; color: var(--navy); }
    h2 { font-size: 20px; margin-top: 36px; color: var(--navy); }
    .updated { color: var(--muted); font-size: 14px; margin-bottom: 24px; }
    a { color: var(--accent); }
    ul { padding-left: 22px; }
    li { margin: 4px 0; }
    footer { margin-top: 48px; color: var(--muted); font-size: 13px; border-top: 1px solid var(--line); padding-top: 16px; }"""


def page_name(doc_id: str, lang: str) -> str:
    return PAGES[doc_id] + LANGS[lang]["html_suffix"] + ".html"


def inline(text: str, lang: str) -> str:
    out = html.escape(text, quote=False)
    out = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", out)

    def link(m: re.Match) -> str:
        label, href = m.group(1), m.group(2)
        if href in PAGES:
            href = page_name(href, lang)
        return f'<a href="{html.escape(href)}">{label}</a>'

    out = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, out)
    return out.replace(EMAIL, f'<a href="mailto:{EMAIL}">{EMAIL}</a>')


def convert(markdown: str, lang: str) -> tuple[str, str, str]:
    """Trả (tiêu đề, dòng phiên bản, thân HTML)."""
    title, meta, body = "", "", []
    paragraph, in_list = [], False

    def flush():
        nonlocal paragraph, in_list, meta
        if paragraph:
            text = " ".join(paragraph)
            if not meta and not any(line.startswith("<h2") for line in body):
                meta = inline(text, lang)
            else:
                body.append(f"    <p>{inline(text, lang)}</p>")
            paragraph = []
        if in_list:
            body.append("    </ul>")
            in_list = False

    for raw in markdown.replace("\r\n", "\n").split("\n"):
        line = raw.strip()
        if not line:
            flush()
        elif line.startswith("## "):
            flush()
            body.append(f"\n    <h2>{inline(line[3:], lang)}</h2>")
        elif line.startswith("# "):
            flush()
            title = line[2:]
        elif line.startswith("- "):
            if paragraph:
                flush()
            if not in_list:
                body.append("    <ul>")
                in_list = True
            body.append(f"      <li>{inline(line[2:], lang)}</li>")
        else:
            paragraph.append(line)
    flush()
    return title, meta, "\n".join(body)


def render(doc_id: str, lang: str) -> str:
    conf = LANGS[lang]
    title, meta, body = convert((SRC / f"{doc_id}{conf['suffix']}.md").read_text(encoding="utf-8"), lang)
    titles = {d: convert((SRC / f"{d}{conf['suffix']}.md").read_text(encoding="utf-8"), lang)[0] for d in PAGES}
    links = [
        f'<a href="{page_name(d, lang)}">{"<strong>" + titles[d] + "</strong>" if d == doc_id else titles[d]}</a>'
        for d in PAGES
    ]
    links.append(f'<a href="data-deletion.html">{conf["deletion"]}</a>')
    links.append(f'<a class="lang" href="{page_name(doc_id, conf["other"])}">{conf["switch"]}</a>')
    nav = "\n      ".join(links)
    return f"""<!DOCTYPE html>
<!-- Sinh tự động bởi tools/build_pages.py từ mobile/assets/markdown/{doc_id}{conf['suffix']}.md — đừng sửa tay. -->
<html lang="{lang}">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{html.escape(title)} | Lock.R</title>
  <style>
{STYLE}
  </style>
</head>
<body>
  <div class="wrap">
    <nav>
      {nav}
    </nav>
    <h1>{html.escape(title)}</h1>
    <div class="updated">{meta}</div>
{body}

    <footer>© 2026 Lock.R. {conf['footer']}</footer>
  </div>
</body>
</html>
"""


def main() -> None:
    for doc_id in PAGES:
        for lang in LANGS:
            target = ROOT / page_name(doc_id, lang)
            target.write_text(render(doc_id, lang), encoding="utf-8", newline="\n")
            print(f"wrote {target.name}")


if __name__ == "__main__":
    main()
