#!/usr/bin/env python3
"""Check relative links and #anchors in this repo's Markdown, for both ways it is read.

Purpose: the site is read two ways. On github.com, a link must name the actual file
(`reports/hash_commitment.md`). On GitHub Pages (Jekyll, `permalink: pretty`, with the
default jekyll-relative-links plugin), `.md` links are rewritten to the page URL, while
extensionless "pretty" links (`reports/hash_commitment/`) work on Pages but 404 on github.com.
After files were renamed and moved, some links broke in one view or both. This reports,
per link: whether the target exists, whether the link form works on github.com, whether it
works on Pages, and whether the #anchor matches a heading in the target.

Usage: python3 -I src/check_links.py [ROOT]          (exit 1 if any problem is found)
       python3 -I src/check_links.py [ROOT] --fix    rewrite pretty-URL links as .md file links

--fix resolves each pretty-URL link the way Pages does (relative to the page's own pretty URL,
so `../x/` from reports/README.md means reports/x.md) and rewrites it as a path to the .md file,
keeping any #anchor. Such links work on github.com and, through jekyll-relative-links, on Pages.
"""
import os
import pathlib
import re
import sys
import urllib.parse

LINK = re.compile(r"(?<!!)\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")


def slug(text: str) -> str:
    """GitHub-style heading anchor (kramdown's auto ids are close enough for these files)."""
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"[`*_~]", "", text).strip().lower()
    text = re.sub(r"[^\w\- ]", "", text)
    return text.replace(" ", "-")


def anchors(path: pathlib.Path) -> set:
    out, seen, fence = set(), {}, False
    for line in path.read_text(errors="replace").splitlines():
        if line.lstrip().startswith(("```", "~~~")):
            fence = not fence
        if fence:
            continue
        m = HEADING.match(line)
        if m:
            s = slug(m.group(2))
            n = seen.get(s, 0)
            seen[s] = n + 1
            out.add(s if n == 0 else f"{s}-{n}")
        for a in re.findall(r"<a\s+(?:name|id)=\"([^\"]+)\"", line):
            out.add(a)
    return out


def resolve(src: pathlib.Path, target: str, root: pathlib.Path):
    """Return (file, works_on_github, works_on_pages) for a relative link target."""
    p = (src.parent / target).resolve() if not target.startswith("/") else (root / target.lstrip("/")).resolve()
    if p.is_file():
        is_md = p.suffix == ".md"
        return p, True, True if is_md or not target.endswith("/") else False
    if p.is_dir():
        idx = next((p / n for n in ("index.md", "README.md") if (p / n).is_file()), None)
        return idx, idx is not None, idx is not None and (p / "index.md").is_file()
    stem = pathlib.Path(str(p).rstrip("/"))
    for cand in (stem.with_suffix(".md"), stem / "index.md"):
        if cand.is_file():
            return cand, False, True  # pretty URL: fine on Pages, 404 on github.com
    return None, False, False


def pages_target(src: pathlib.Path, target: str, root: pathlib.Path):
    """Resolve a link the way Pages does, relative to src's pretty URL; return the .md file."""
    base = src.parent if src.stem == "index" else src.parent / src.stem
    p = pathlib.Path(str((base / target).resolve()).rstrip("/"))
    for cand in (p.with_suffix(".md"), p / "index.md"):
        if cand.is_file() and root in cand.parents:
            return cand
    return None


def fix_file(md: pathlib.Path, root: pathlib.Path) -> int:
    changed = 0

    def repl(m):
        nonlocal changed
        text, url = m.group(1), m.group(2)
        if re.match(r"^[a-z]+:", url) or url.startswith(("//", "#")):
            return m.group(0)
        path, sep, frag = url.partition("#")
        f, gh, _ = resolve(md, urllib.parse.unquote(path), root)
        if f is not None and gh:
            return m.group(0)
        f = pages_target(md, urllib.parse.unquote(path), root)
        if f is None:
            return m.group(0)
        rel = pathlib.Path(os.path.relpath(f, md.parent))
        changed += 1
        return m.group(0).replace(f"({url}", f"({rel.as_posix()}{sep}{frag}", 1)

    new = LINK.sub(repl, md.read_text())
    if changed:
        md.write_text(new)
    return changed


def main(root: str = ".", *flags) -> int:
    root_p = pathlib.Path(root).resolve()
    if "--fix" in flags:
        for md in sorted(root_p.rglob("*.md")):
            if ".git" not in md.parts:
                n = fix_file(md, root_p)
                if n:
                    print(f"fixed {n} link(s) in {md.relative_to(root_p)}")
    problems = 0
    for md in sorted(root_p.rglob("*.md")):
        if ".git" in md.parts:
            continue
        own = anchors(md)
        for n, line in enumerate(md.read_text(errors="replace").splitlines(), 1):
            for text, url in LINK.findall(line):
                if re.match(r"^[a-z]+:", url) or url.startswith("//"):
                    continue
                path, _, frag = urllib.parse.unquote(url).partition("#")
                issues = []
                if path:
                    f, gh, pages = resolve(md, path, root_p)
                    if f is None:
                        issues.append("target missing")
                    else:
                        if not gh:
                            issues.append("404 on github.com (pretty URL form)")
                        if not pages:
                            issues.append("may 404 on Pages")
                        if frag and f.suffix == ".md" and frag not in anchors(f):
                            issues.append(f"anchor #{frag} not in {f.relative_to(root_p)}")
                elif frag and frag not in own:
                    issues.append(f"anchor #{frag} not in this file")
                if issues:
                    problems += 1
                    print(f"{md.relative_to(root_p)}:{n}: [{text[:50]}]({url}) -> {'; '.join(issues)}")
    print(f"{problems} problem link(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
