#!/usr/bin/env python3
"""
update the Books section in README.md using Google Books API.

usage:
  python scripts/update_books.py [--readme PATH] [--max-results N] [--dry-run]

notes:
  - no api key required; optional GOOGLE_BOOKS_API_KEY env var supported.
  - deduplicates by title.
  - inserts new rows at the top of the Books table (Title | Author | Year).
"""

from __future__ import annotations

import argparse
import html
import os
import re
from pathlib import Path
from typing import Iterable, List, Optional, Tuple
from urllib.parse import urlencode, quote
from urllib.request import Request, urlopen
import json


def read_readme(path: Path) -> List[str]:
    return path.read_text(encoding="utf-8").splitlines()


def write_readme(path: Path, lines: List[str]) -> None:
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def find_section_table_bounds(lines: List[str], heading_prefix: str) -> Tuple[int, int]:
    # find heading line
    heading_idx = -1
    for i, line in enumerate(lines):
        if line.strip().lower().startswith(heading_prefix.lower()):
            heading_idx = i
            break
    if heading_idx == -1:
        raise RuntimeError(f"could not find '{heading_prefix}' section in README.md")
    # find header separator
    sep_idx = -1
    for i in range(heading_idx + 1, min(heading_idx + 20, len(lines))):
        if re.match(r"^\|\s*-{3,}\s*\|", lines[i]):
            sep_idx = i
            break
    if sep_idx == -1:
        raise RuntimeError("could not find table header separator in Books section")
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


def parse_year(value: str) -> Optional[int]:
    m = re.search(r"(19|20)\d{2}", value or "")
    return int(m.group(0)) if m else None


def fetch_google_books(max_results: int, api_key: Optional[str]) -> List[dict]:
    # intitle: requires the phrase in the book's actual title, not just anywhere
    # in its metadata, so unrelated books that mention BO in passing don't match
    query = 'intitle:"Bayesian Optimization" OR intitle:"Bayesian Optimisation"'
    params = {
        "q": query,
        "maxResults": max_results,
        "orderBy": "newest",
        "printType": "books",
    }
    if api_key:
        params["key"] = api_key
    url = f"https://www.googleapis.com/books/v1/volumes?{urlencode(params)}"
    with urlopen(url) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data.get("items", [])


def normalize_space(s: str) -> str:
    import re as _re
    return _re.sub(r"\s+", " ", s or "").strip()


def to_row(item: dict) -> Optional[Tuple[str, str, int, str]]:
    volume = item.get("volumeInfo", {})
    title = normalize_space(html.unescape(volume.get("title", "").strip()))
    if not title:
        return None
    authors = ", ".join(volume.get("authors", [])[:3]) if volume.get("authors") else ""
    year = parse_year(volume.get("publishedDate", "")) or 0
    link = volume.get("infoLink") or item.get("selfLink") or ""
    if not link:
        return None
    return title, authors, year, link


def update_books(readme_path: Path, items: List[dict], max_new: int, dry_run: bool) -> int:
    lines = read_readme(readme_path)
    start, end = find_section_table_bounds(lines, "## Books")
    existing = extract_existing_titles(lines, start, end)

    rows: List[str] = []
    for it in items:
        parsed = to_row(it)
        if not parsed:
            continue
        title, authors, year, link = parsed
        if title.casefold() in existing:
            continue
        rows.append(f"| [{title}]({link}) | {authors} | {year or ''} |")

    # stable order: newest year desc then title
    def sort_key(r: str) -> Tuple[int, str]:
        m = re.search(r"\|\s*(\d{4})\s*\|\s*$", r)
        yr = int(m.group(1)) if m else 0
        t = r.split("|")[1].lower()
        return (-yr, t)

    rows.sort(key=sort_key)
    rows = rows[:max_new]
    if not rows:
        return 0
    updated = lines[:start] + rows + lines[start:]
    if not dry_run:
        write_readme(readme_path, updated)
    return len(rows)


def parse_args(argv: Optional[Iterable[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="update README Books from Google Books")
    p.add_argument("--readme", type=Path, default=Path(__file__).resolve().parents[1] / "README.md")
    p.add_argument("--max-results", type=int, default=20)
    p.add_argument("--max-new", type=int, default=5, help="max new books to add per run (default: 5)")
    p.add_argument("--dry-run", action="store_true")
    return p.parse_args(argv)


def main(argv: Optional[Iterable[str]] = None) -> int:
    print(
        "update_books.py is disabled. Books are curated by hand "
        "(see contributing.md). Use scripts/update_papers.py for preprints."
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())


