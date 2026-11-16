"""Build-time design helpers. The files in the repository are never changed;
all of this happens while the site is being built, so editors can keep
writing plain text in the visual editor.

What it does:

* Lists: the visual editor indents nested lists by 2 or 3 spaces, MkDocs
  needs 4, so lists are re-indented.
* Page header: every page gets a banner with its section, title, short
  description and (optionally) a cover image chosen in the editor.
* Callouts: a quote that starts with one of the emoji in CALLOUTS becomes a
  coloured note box.
* Link cards: a line that is only an arrow emoji and a link becomes a card.
* Section pages: a page that has sub-pages gets cards for its sub-pages.
* Home page: gets the hero banner and one card per section.
"""
import html
import os
import posixpath
import re

import material
from mkdocs.structure.nav import Section
from mkdocs.utils import get_relative_url, meta as mkdocs_meta

MARKER = re.compile(r"^( *)([*+-]|\d{1,9}[.)])( +)(?=\S)")
FENCE = re.compile(r"^ *(```|~~~)")


def normalize_lists(markdown: str) -> str:
    out = []
    stack = []  # (marker_indent, content_indent) for each open list level
    in_fence = False
    prev_blank = True
    prev_in_list = False
    for line in markdown.split("\n"):
        if not line.strip():
            out.append("")
            prev_blank = True
            continue
        indent = len(line) - len(line.lstrip(" "))
        fence = bool(FENCE.match(line))
        m = None if in_fence else MARKER.match(line)
        if m and not stack and indent > 3:
            m = None  # indented code block, not a list
        if stack:
            lazy = not m and not prev_blank and not in_fence
            if not lazy:
                while stack and indent < stack[-1][1]:
                    stack.pop()
        if m:
            if not stack and not prev_blank and not prev_in_list:
                out.append("")  # a list needs a blank line before it
            level = len(stack)
            out.append(" " * 4 * level + m.group(2) + " " + line[m.end():])
            stack.append((indent, m.end()))
        elif stack:
            extra = max(0, indent - stack[-1][1])
            out.append(" " * (4 * len(stack) + extra) + line.lstrip(" "))
        else:
            out.append(line)
        if fence:
            in_fence = not in_fence
        prev_blank = False
        prev_in_list = bool(stack)
    return "\n".join(out)




# --------------------------------------------------------------------------
# Things an admin may want to tweak
# --------------------------------------------------------------------------

# Icon and one-line blurb for each top-level section (by folder name).
# Icon names come from https://pictogrammers.com/library/mdi/
SECTIONS = {
    "overview": ("compass-outline", "How the DAO is structured, who plays a role, and how the Treasury works."),
    "constitution": ("scale-balance", "The principles and frameworks that the DAO's governance is built on."),
    "governance": ("vote-outline", "Voting power, the life of a proposal, and how to write your own PIP."),
    "archive": ("archive-outline", "Foundational PIPs, the DAO's history, and every Council term."),
    "appendices": ("book-open-page-variant-outline", "Source material and links to everything officially published."),
}
DEFAULT_SECTION = ("file-document-outline", "")

HERO_KICKER = "Star Atlas DAO"
HERO_TITLE = "Codex"
HERO_TEXT = "Everything about how the Star Atlas DAO works: its structure, its governance, and how you can help shape the future of Star Atlas."
HERO_BUTTONS = [  # (label, page file inside docs/)
    # Hidden for now. Remove the "# " at the start of a line to show that button again.
    # ("Join The DAO", "overview/the-star-atlas-dao/index.md"),
    # ("Write a Proposal", "governance/authors-guide/index.md"),
]

# Artwork shown behind the banner at the top of pages. The key is the start
# of a page's location inside docs/ ("" is the fallback for everything); the
# most specific match wins. The pictures live in docs/assets/art/. A page's
# own "Cover image" (set in the visual editor) always takes priority.
ARTWORK = {
    "": "stake-station.jpg",
    "overview/": "stake-station.jpg",
    "overview/the-star-atlas-dao/": "dao-banner.jpg",
    "overview/dao-hierarchy": "armstrong.jpg",
    "overview/our-structure/": "central-space-station.jpg",
    "overview/polis": "polis-atlas.jpg",
    "overview/treasury": "arc-rainbow.jpg",
    "overview/ecosystem-fund": "jungle-city.jpg",
    "overview/roadmap": "armstrong.jpg",
    "constitution/": "council-arena.jpg",
    "governance/": "central-space-station.jpg",
    "governance/polis-voting-power": "polis-atlas.jpg",
    "governance/creating-a-proposal/": "calico-hangar.jpg",
    "governance/authors-guide/": "calico-landing.jpg",
    "governance/active-pips/": "calico-surf.jpg",
    "archive/": "peacebringers-archive.jpg",
    "archive/dao-history": "treaty-table.jpg",
    "archive/council-terms/": "central-space-station.jpg",
    "appendices/": "arc-dark.jpg",
}
# The two pillars shown in the middle of the top bar: (label, link, short label for phones).
# A link starting with "http" opens that site; "" marks the pillar as coming soon;
# "index.md" is this Codex.
PILLARS = [
    ("DAO Dashboard", "", "Dashboard"),
    ("DAO Codex", "index.md", "Codex"),
]

HERO_ART = "treaty-hero.jpg"
HERO_LOGO = "assets/logo-dao.png"        # Star Atlas DAO wordmark shown in the home banner
FOOTER_LOGO = "assets/logo-council.png"  # DAO Council wordmark shown in every page footer
ART_DIR = "assets/art/"

# A quote that starts with one of these becomes a coloured note box.
CALLOUTS = {
    "ℹ": ("info", "information-outline"),
    "💡": ("tip", "lightbulb-on-outline"),
    "⚠": ("warning", "alert-outline"),
    "✅": ("success", "check-circle-outline"),
    "🚫": ("danger", "close-octagon-outline"),
}

# --------------------------------------------------------------------------

_ICON_DIR = os.path.join(os.path.dirname(material.__file__), "templates", ".icons", "material")
_nav = None


def icon(name):
    try:
        with open(os.path.join(_ICON_DIR, name + ".svg"), encoding="utf-8") as f:
            return f.read().replace("<svg ", '<svg class="kb-icon" aria-hidden="true" ', 1)
    except OSError:
        return ""


def file_meta(file):
    """Title and description from a page's front matter."""
    try:
        with open(file.abs_src_path, encoding="utf-8-sig") as f:
            _, data = mkdocs_meta.get_data(f.read())
    except OSError:
        data = {}
    return data if isinstance(data, dict) else {}


def first_page(item):
    if isinstance(item, Section):
        for child in item.children:
            page = first_page(child)
            if page:
                return page
        return None
    return item if getattr(item, "file", None) else None


def md_link(target_file, page):
    """A Markdown link target from one page's file to another."""
    start = posixpath.dirname(page.file.src_uri)
    return posixpath.relpath(target_file.src_uri, start or ".")


def artwork_for(src_uri):
    """The artwork file for a page, by the most specific matching location."""
    best = max((k for k in ARTWORK if src_uri.startswith(k)), key=len, default=None)
    return ARTWORK[best] if best is not None else None


def art_url(name, page):
    return get_relative_url(ART_DIR + name, page.url)


def card(title, description, href, icon_name=None, art=None):
    title = html.escape(str(title))
    inner = f"<strong>{title}</strong>"
    if description:
        inner += f"<span>{html.escape(str(description))}</span>"
    if icon_name:
        inner = f'<span class="kb-card__icon">{icon(icon_name)}</span><span class="kb-card__body">{inner}</span>'
    else:
        inner = f'<span class="kb-card__body">{inner}</span>'
    if art:
        inner = (
            f'<span class="kb-card__art" style="background-image:url(\'{html.escape(art)}\')"></span>'
            f'<span class="kb-card__row">{inner}</span>'
        )
    inner = inner.replace("[", "&#91;").replace("]", "&#93;")
    return f"[{inner}]({href}){{ .kb-card }}"


def cards(items, extra_class=""):
    if not items:
        return ""
    return f'<div class="kb-cards {extra_class}" markdown>\n' + "\n".join(items) + "\n</div>\n"


REF = re.compile(r"^(?:➡️?|👉) *\[(.+?)\]\(([^)\s]+)\)(?:\s*[-–—:]\s*(.+?))?\s*$")


def link_cards(markdown, page, files):
    """Turn lines like '➡️ [Title](page.md)' into cards.

    Text after the link ('➡️ [Title](page.md) - Short description') becomes the
    card's description; without it, the linked page's own description is used.
    """
    out, group = [], []

    def flush():
        if group:
            out.append(cards(group, "kb-cards--refs"))
            out.append("")
            group.clear()

    for line in markdown.split("\n"):
        m = REF.match(line)
        if m:
            title, href = m.group(1), m.group(2)
            description = (m.group(3) or "").strip()
            if not description and not re.match(r"^[a-z]+:|^/|^#", href):
                target = posixpath.normpath(posixpath.join(posixpath.dirname(page.file.src_uri), href.split("#")[0]))
                f = files.get_file_from_path(target)
                if f:
                    description = file_meta(f).get("description", "")
            group.append(card(re.sub(r"[*_]", "", title), description, href))
        elif not line.strip() and group:
            continue
        else:
            flush()
            out.append(line)
    flush()
    return "\n".join(out)


def callouts(markdown):
    """Turn quotes that start with a callout emoji into note boxes."""
    lines = markdown.split("\n")
    out, i = [], 0
    while i < len(lines):
        line = lines[i]
        if line.startswith(">") and (i == 0 or not lines[i - 1].startswith(">")):
            j = i
            while j < len(lines) and lines[j].startswith(">"):
                j += 1
            body = [re.sub(r"^> ?", "", l) for l in lines[i:j]]
            first = body[0].lstrip()
            kind = next((v for k, v in CALLOUTS.items() if first.startswith(k)), None)
            if kind:
                body[0] = re.sub(r"^\S+\s*", "", first)
                out.append(f'<div class="kb-callout kb-callout--{kind[0]}" markdown>')
                out.append(f'<span class="kb-callout__icon">{icon(kind[1])}</span>')
                out.append('<div class="kb-callout__body" markdown>')
                out.extend(body)
                out.append("</div>")
                out.append("</div>")
                i = j
                continue
        out.append(line)
        i += 1
    return "\n".join(out)


def top_section(page):
    item, top = page, None
    while item.parent is not None:
        item = item.parent
        top = item
    return top


def section_key(page):
    return page.file.src_uri.split("/")[0] if "/" in page.file.src_uri else ""


def page_header(page):
    trail, item = [], page.parent
    while item is not None:
        trail.insert(0, item.title)
        item = item.parent
    title = page.meta.get("title") or page.title or ""
    # A page that is the landing page of its section should not repeat it.
    if trail and str(trail[-1]).strip() == str(title).strip():
        trail.pop()
    description = page.meta.get("description", "")
    cover = page.meta.get("cover")
    art = None
    if cover:
        art = cover if re.match(r"^[a-z]+:", cover) else get_relative_url(cover.lstrip("/"), page.url)
    else:
        name = artwork_for(page.file.src_uri)
        art = art_url(name, page) if name else None
    cls = f'kb-head kb-sec-{section_key(page) or "home"}'
    if art:
        parts = [f'<header class="{cls} kb-head--art" style="--art:url(\'{html.escape(art)}\')">']
    else:
        parts = [f'<header class="{cls}">']
        mark = icon(SECTIONS.get(section_key(page), DEFAULT_SECTION)[0])
        parts.append(f'<span class="kb-head__mark" aria-hidden="true">{mark}</span>')
    parts.append('<div class="kb-head__text">')
    if trail:
        crumbs = '<span class="kb-head__sep">›</span>'.join(html.escape(str(t)) for t in trail)
        parts.append(f'<p class="kb-head__crumbs">{crumbs}</p>')
    parts.append(f"<h1>{html.escape(str(title))}</h1>")
    if description:
        lead = re.sub(r'(https?://[^\s<]+[^\s<.,;:!?)])', r'<a href="\1">\1</a>', html.escape(str(description)))
        parts.append(f'<p class="kb-head__lead">{lead}</p>')
    parts.append("</div></header>\n\n")
    return "".join(parts)


def child_cards(page):
    """Cards for the sub-pages of a section landing page."""
    if page.file.name != "index" or page.parent is None:
        return ""
    items = []
    for child in page.parent.children:
        if child is page:
            continue
        target = first_page(child)
        if not target:
            continue
        data = file_meta(target.file)
        title = child.title if isinstance(child, Section) else data.get("title") or child.title
        items.append(card(title, data.get("description", ""), md_link(target.file, page)))
    if not items:
        return ""
    return '\n\n<h2 class="kb-subhead" id="in-this-section">In this section</h2>\n\n' + cards(items)


def home(page, files):
    buttons = []
    for n, (label, path) in enumerate(HERO_BUTTONS):
        if files.get_file_from_path(path):
            cls = ".kb-btn" + (" .kb-btn--primary" if n == 0 else "")
            buttons.append(f"[{label}]({path}){{ {cls} }}")
    hero = (
        '<section class="kb-hero" markdown>\n'
        f'<div class="kb-hero__art" aria-hidden="true" style="background-image:url(\'{art_url(HERO_ART, page)}\')"></div>\n'
        '<div class="kb-hero__text" markdown>\n'
        f'<h1 class="kb-hero__logo"><img src="{art_url_raw(HERO_LOGO, page)}" alt="{html.escape(HERO_KICKER)}"></h1>\n'
        f'<p class="kb-hero__lead">{html.escape(HERO_TEXT)}</p>\n\n'
        + (('<p class="kb-hero__buttons" markdown>' + " ".join(buttons) + "</p>") if buttons else "")
        + "\n\n</div>\n</section>\n\n"
    )
    items = []
    for item in _nav.items if _nav else []:
        if not isinstance(item, Section):
            continue
        target = first_page(item)
        if not target:
            continue
        key = target.file.src_uri.split("/")[0]
        icon_name, blurb = SECTIONS.get(key, DEFAULT_SECTION)
        count = sum(1 for _ in _pages(item))
        blurb = blurb or file_meta(target.file).get("description", "")
        name = artwork_for(key + "/")
        items.append(
            card(item.title, blurb, target.file.src_uri, icon_name, art_url(name, page) if name else None).replace(
                "{ .kb-card }", f"{{ .kb-card .kb-card--section .kb-sec-{key} data-count=\"{count} page{'' if count == 1 else 's'}\" }}"
            )
        )
    return hero + '<h2 class="kb-subhead" id="explore">Explore</h2>\n\n' + cards(items, "kb-cards--sections") + "\n"


def _pages(item):
    if isinstance(item, Section):
        for child in item.children:
            yield from _pages(child)
    elif getattr(item, "file", None):
        yield item


def on_nav(nav, **kwargs):
    global _nav
    _nav = nav
    return nav


def art_url_raw(path, page):
    return get_relative_url(path, page.url or ".")


def pillars(page):
    parts = []
    for label, link, short in PILLARS:
        inner = f'<span class="kb-pillar__full">{html.escape(label)}</span><span class="kb-pillar__short">{html.escape(short)}</span>'
        if not link:
            parts.append(f'<span class="kb-pillar kb-pillar--soon" title="Coming soon">{inner}<em>Soon</em></span>')
        elif link.startswith("http"):
            parts.append(f'<a class="kb-pillar" href="{html.escape(link)}">{inner}</a>')
        else:
            parts.append(f'<a class="kb-pillar kb-pillar--active" href="{art_url_raw("index.html", page)}" aria-current="true">{inner}</a>')
    return '<nav class="kb-pillars" aria-label="Star Atlas DAO Council">' + "".join(parts) + "</nav>\n"


def on_post_page(output, page, config, **kwargs):
    """Put each section's icon next to its heading in the sidebar, and the Council logo in the footer."""
    # Links to other websites open in a new tab.
    output = re.sub(
        r'<a (?![^>]*\btarget=)([^>]*\bhref="https?://[^"]*"[^>]*)>',
        r'<a \1 target="_blank" rel="noopener">',
        output,
    )
    output = output.replace('<div class="md-header__title"', pillars(page) + '<div class="md-header__title"', 1)
    output = output.replace(
        '<div class="md-copyright">',
        f'<a class="kb-footer-logo" href="{art_url_raw("index.html", page)}"><img src="{art_url_raw(FOOTER_LOGO, page)}" alt="Star Atlas DAO Council"></a>\n<div class="md-copyright">',
        1,
    )
    for item in _nav.items if _nav else []:
        if not isinstance(item, Section):
            continue
        target = first_page(item)
        if not target:
            continue
        key = target.file.src_uri.split("/")[0]
        mark = icon(SECTIONS.get(key, DEFAULT_SECTION)[0])
        pattern = re.compile(
            r'(<label class="md-nav__link" for="__nav_\d+" id="__nav_\d+_label"[^>]*>\s*<span class="md-ellipsis">)(\s*'
            + re.escape(html.escape(str(item.title), quote=False))
            + r"\s*</span>)"
        )
        output = pattern.sub(
            lambda m: f'{m.group(1)}<span class="kb-nav-icon kb-sec-{key}">{mark}</span>{m.group(2)}', output
        )
    return output


def on_page_markdown(markdown, page, config, files, **kwargs):
    # Web addresses typed or pasted as plain text become clickable links.
    markdown = re.sub(r"\b(https?)\\:", r"\1:", markdown)
    markdown = link_cards(markdown, page, files)
    markdown = callouts(markdown)
    markdown = normalize_lists(markdown)
    if page.is_homepage:
        # The home page has no need for the "table of contents" column.
        hide = page.meta.get("hide") or []
        page.meta["hide"] = list(hide) + ["toc"]
        return home(page, files) + markdown
    return page_header(page) + markdown + child_cards(page)
