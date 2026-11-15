"""Build-time clean-up so pages written in the visual editor (or copied from
GitBook) render correctly with MkDocs.

The visual editor writes standard Markdown, where nested lists are indented
by 2 or 3 spaces. MkDocs needs 4 spaces per level, so this hook re-indents
lists while the site is being built. The files in the repository are never
changed.
"""
import re

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


def on_page_markdown(markdown, **kwargs):
    return normalize_lists(markdown)
