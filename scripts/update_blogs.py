#!/usr/bin/env python3
"""
update the Blogs section in README.md by aggregating RSS/Atom feeds and filtering for bayesian optimization.

usage:
  python scripts/update_blogs.py [--readme PATH] [--feeds FILE] [--dry-run]

notes:
  - default feeds are included; you can provide a file with one feed url per line.
  - deduplicates by title.
  - inserts new rows at the top (Title | Author | Platform | Year).
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional, Tuple
from urllib.parse import urlparse
from urllib.request import urlopen
import xml.etree.ElementTree as ET


DEFAULT_FEEDS = [
    "https://distill.pub/rss.xml",
    "http://krasserm.github.io/feed.xml",
    "https://thuijskens.github.io/feed.xml",
    "https://botorch.org/blog/index.xml",
]

KEYWORDS = (
    "bayesian optimization",
    "bayesian optimisation",
    "bayesopt",
)


def read_readme(path: Path) -> List[str]:
    return path.read_text(encoding="utf-8").splitlines()


def write_readme(path: Path, lines: List[str]) -> None:
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def find_section_table_bounds(lines: List[str], heading_prefix: str) -> Tuple[int, int]:
    heading_idx = -1
    for i, line in enumerate(lines):
        if line.strip().lower().startswith(heading_prefix.lower()):
            heading_idx = i
            break
    if heading_idx == -1:
        raise RuntimeError(f"could not find '{heading_prefix}' section in README.md")
    sep_idx = -1
    for i in range(heading_idx + 1, min(heading_idx + 20, len(lines))):
        if re.match(r"^\|\s*-{3,}\s*\|", lines[i]):
            sep_idx = i
            break
    if sep_idx == -1:
        raise RuntimeError("could not find table header separator in Blogs section")
    end_idx = len(lines)
    for i in range(sep_idx + 1, len(lines)):
        if lines[i].startswith("## ") and i > sep_idx + 1:
            end_idx = i
            break
    return sep_idx + 1, end_idx


def extract_existing_titles(lines: List[str], start: int, end: int) -> set:
    titles = set()
    row_re = re.compile(r"^\|\s*\[(?P<title>[^\]]+)\]\([^)]+\)\s*\|", re.IGNORECASE)
    for i in range(start, end):
        m = row_re.match(lines[i].strip())
        if m:
            titles.add(m.group("title").casefold())
    return titles


def normalize_space(s: str) -> str:
    import re as _re
    return _re.sub(r"\s+", " ", s or "").strip()


@dataclass
class BlogEntry:
    title: str
    author: str
    platform: str
    year: int
    url: str


def looks_like_bo(title: str, summary: str) -> bool:
    t = title.lower()
    s = summary.lower()
    for kw in KEYWORDS:
        if kw in t or kw in s:
            return True
    return False


def parse_feed(url: str) -> List[BlogEntry]:
    with urlopen(url) as resp:
        data = resp.read()
    root = ET.fromstring(data)
    entries: List[BlogEntry] = []
    # try Atom
    for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
        title = normalize_space(html.unescape((entry.findtext("{http://www.w3.org/2005/Atom}title") or "")))
        summary = normalize_space(entry.findtext("{http://www.w3.org/2005/Atom}summary") or "")
        link_elem = entry.find("{http://www.w3.org/2005/Atom}link")
        link = link_elem.get("href") if link_elem is not None else ""
        author = (entry.findtext("{http://www.w3.org/2005/Atom}author/{http://www.w3.org/2005/Atom}name") or "").strip()
        updated = entry.findtext("{http://www.w3.org/2005/Atom}updated") or ""
        try:
            year = dt.datetime.fromisoformat(updated.replace("Z", "+00:00")).year
        except Exception:
            year = dt.datetime.utcnow().year
        if title and link and looks_like_bo(title, summary):
            platform = urlparse(link).netloc or urlparse(url).netloc
            entries.append(BlogEntry(title, author, platform, year, link))
    # try RSS
    channel = root.find("channel")
    if channel is not None:
        for item in channel.findall("item"):
            title = normalize_space(html.unescape(item.findtext("title") or ""))
            link = item.findtext("link") or ""
            author = (item.findtext("author") or item.findtext("dc:creator") or "").strip()
            pub_date = item.findtext("pubDate") or ""
            summary = normalize_space(item.findtext("description") or "")
            year_match = re.search(r"(19|20)\d{2}", pub_date)
            year = int(year_match.group(0)) if year_match else dt.datetime.utcnow().year
            if title and link and looks_like_bo(title, summary):
                platform = urlparse(link).netloc or urlparse(url).netloc
                entries.append(BlogEntry(title, author, platform, year, link))
    return entries


def update_blogs(readme_path: Path, feeds: List[str], dry_run: bool) -> int:
    lines = read_readme(readme_path)
    start, end = find_section_table_bounds(lines, "## Blogs")
    existing = extract_existing_titles(lines, start, end)
    new_entries: List[BlogEntry] = []
    for f in feeds:
        try:
            new_entries.extend(parse_feed(f))
        except Exception:
            continue
    # dedupe by title
    uniq = {}
    for e in new_entries:
        key = e.title.casefold()
        if key not in uniq:
            uniq[key] = e
    candidates = [e for k, e in uniq.items() if k not in existing]
    candidates.sort(key=lambda e: (-e.year, e.title.lower()))
    rows = [f"| [{e.title}]({e.url}) | {e.author} | {e.platform} | {e.year} |" for e in candidates]
    if not rows:
        return 0
    updated = lines[:start] + rows + lines[start:]
    if not dry_run:
        write_readme(readme_path, updated)
    return len(rows)


def parse_args(argv: Optional[Iterable[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="update README Blogs from RSS feeds")
    p.add_argument("--readme", type=Path, default=Path(__file__).resolve().parents[1] / "README.md")
    p.add_argument("--feeds", type=Path, default=None, help="file containing feed urls (one per line)")
    p.add_argument("--dry-run", action="store_true")
    return p.parse_args(argv)


def main(argv: Optional[Iterable[str]] = None) -> int:
    print(
        "update_blogs.py is disabled. Blogs are curated by hand "
        "(see contributing.md). Use scripts/update_papers.py for preprints."
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())


