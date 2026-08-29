#!/usr/bin/env python3
"""Propose new method preprints for Recent Preprints.

This script never writes to the curated Papers sections. It merges
title-matching arXiv entries into README.md, sorts newest first by arXiv
id, then runs scripts/sync_docs.py so docs/preprints.md matches. Humans
still review the weekly pull request.

Usage:
  python scripts/update_papers.py [--readme PATH] [--max-results N] [--arxiv-cap N] [--dry-run]
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional, Tuple
from urllib.parse import quote
from urllib.request import urlopen
import xml.etree.ElementTree as ET


ARXIV_API_URL = "http://export.arxiv.org/api/query"

# Title must contain one of these. Abstract-only mentions are not enough.
TITLE_KEYWORDS = (
    "bayesian optimization",
    "bayesian optimisation",
    "bayesopt",
    "bayes-opt",
)

DEFAULT_ARXIV_CAP = 20

LIST_ITEM_RE = re.compile(
    r"^- \[(?P<title>[^\]]+)\]\((?P<url>[^)]+)\) - (?P<rest>.+)$"
)
ARXIV_ID_RE = re.compile(r"arxiv\.org/abs/(\d+)\.(\d+)")


@dataclass
class Paper:
    title: str
    url: str
    year: int


def build_arxiv_query(max_results: int) -> str:
    terms = [
        'ti:"bayesian optimization"',
        'ti:"bayesian optimisation"',
        'ti:"bayesopt"',
    ]
    search_query = quote(" OR ".join(terms))
    return (
        f"{ARXIV_API_URL}?search_query={search_query}"
        f"&start=0&max_results={max_results}&sortBy=lastUpdatedDate&sortOrder=descending"
    )


def fetch_arxiv_feed(max_results: int) -> ET.Element:
    with urlopen(build_arxiv_query(max_results)) as resp:
        data = resp.read()
    return ET.fromstring(data)


def extract_text(elem: Optional[ET.Element]) -> str:
    return elem.text.strip() if elem is not None and elem.text else ""


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def title_is_bo(title: str) -> bool:
    t = title.lower()
    return any(kw in t for kw in TITLE_KEYWORDS)


def canonical_arxiv_url(entry_id: str) -> str:
    # http://arxiv.org/abs/2608.25116v1 -> https://arxiv.org/abs/2608.25116
    m = re.search(r"arxiv\.org/abs/(\d+\.\d+)", entry_id)
    if m:
        return f"https://arxiv.org/abs/{m.group(1)}"
    return entry_id.replace("http://", "https://")


def parse_year(published: str) -> int:
    try:
        return dt.datetime.fromisoformat(published.replace("Z", "+00:00")).year
    except Exception:
        return dt.datetime.now(dt.timezone.utc).year


def parse_arxiv_entries(feed_root: ET.Element) -> List[Paper]:
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    papers: List[Paper] = []
    seen = set()
    for entry in feed_root.findall("atom:entry", ns):
        title = normalize_space(html.unescape(extract_text(entry.find("atom:title", ns))))
        if not title_is_bo(title):
            continue
        key = title.casefold()
        if key in seen:
            continue
        seen.add(key)
        url = canonical_arxiv_url(extract_text(entry.find("atom:id", ns)))
        published = extract_text(entry.find("atom:published", ns))
        papers.append(Paper(title=title, url=url, year=parse_year(published)))
    return papers


def read_readme(path: Path) -> List[str]:
    return path.read_text(encoding="utf-8").splitlines()


def write_readme(path: Path, lines: List[str]) -> None:
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def find_preprints_section(lines: List[str], heading: str = "## Recent Preprints") -> Tuple[int, int]:
    start = next((i for i, line in enumerate(lines) if line.strip() == heading), -1)
    if start == -1:
        raise RuntimeError(f"could not find '{heading}'")
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if lines[i].startswith("## "):
            end = i
            break
    return start, end


def existing_titles(lines: List[str]) -> set:
    titles = set()
    for line in lines:
        m = re.match(r"^- \[([^\]]+)\]\(", line.strip())
        if m:
            titles.add(m.group(1).casefold())
    return titles


def parse_preprint_items(lines: List[str], start: int, end: int) -> List[str]:
    items = []
    for line in lines[start:end]:
        if LIST_ITEM_RE.match(line.strip()):
            items.append(line.rstrip())
    return items


def make_item(paper: Paper) -> str:
    return f"- [{paper.title}]({paper.url}) - {paper.year}."


def arxiv_sort_key(item: str) -> Tuple[int, int]:
    m = ARXIV_ID_RE.search(item)
    if not m:
        return (0, 0)
    return (int(m.group(1)), int(m.group(2)))


def arxiv_id_token(item: str) -> str:
    m = ARXIV_ID_RE.search(item)
    return f"{m.group(1)}.{m.group(2)}" if m else item


def merge_preprints(old_items: List[str], new_items: List[str], arxiv_cap: int) -> List[str]:
    merged: List[str] = []
    seen: set[str] = set()
    for item in new_items + old_items:
        token = arxiv_id_token(item)
        if token in seen:
            continue
        seen.add(token)
        merged.append(item)
    merged.sort(key=arxiv_sort_key, reverse=True)
    return merged[:arxiv_cap]


def rewrite_preprints_section(
    lines: List[str], start: int, end: int, items: List[str]
) -> List[str]:
    intro: List[str] = []
    for i in range(start + 1, end):
        stripped = lines[i].strip()
        if stripped.startswith("- ["):
            break
        intro.append(lines[i])

    rebuilt = [lines[start], *intro]
    if rebuilt[-1].strip() != "":
        rebuilt.append("")
    rebuilt.extend(items)
    rebuilt.append("")

    tail = lines[end:]
    if tail and tail[0] != "":
        rebuilt.append("")
    return lines[:start] + rebuilt + tail


def update_readme(readme_path: Path, papers: List[Paper], arxiv_cap: int, dry_run: bool) -> int:
    lines = read_readme(readme_path)
    start, end = find_preprints_section(lines)
    already = existing_titles(lines)
    new_papers = [p for p in papers if p.title.casefold() not in already]
    old_items = parse_preprint_items(lines, start, end)
    new_items = [make_item(p) for p in new_papers]
    combined = merge_preprints(old_items, new_items, arxiv_cap)

    if combined != old_items:
        updated = rewrite_preprints_section(lines, start, end, combined)
        if not dry_run:
            write_readme(readme_path, updated)
    return len(new_items)


def parse_args(argv: Optional[Iterable[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Propose Recent Preprints from arXiv (title match only)")
    root = Path(__file__).resolve().parents[1]
    parser.add_argument(
        "--readme",
        type=Path,
        default=root / "README.md",
    )
    parser.add_argument("--max-results", type=int, default=100)
    parser.add_argument("--arxiv-cap", type=int, default=DEFAULT_ARXIV_CAP)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args(argv)


def sync_docs(readme: Path, dry_run: bool) -> int:
    script = Path(__file__).resolve().parent / "sync_docs.py"
    cmd = [sys.executable, str(script), "--readme", str(readme)]
    if dry_run:
        return 0
    return int(subprocess.run(cmd, check=False).returncode)


def main(argv: Optional[Iterable[str]] = None) -> int:
    args = parse_args(argv)
    if not args.readme.exists():
        print(f"readme not found at: {args.readme}")
        return 2
    try:
        feed = fetch_arxiv_feed(max_results=args.max_results)
        papers = parse_arxiv_entries(feed)
    except Exception as exc:
        print(f"failed to fetch or parse arxiv feed: {exc}")
        return 3
    added = update_readme(args.readme, papers, arxiv_cap=args.arxiv_cap, dry_run=args.dry_run)
    print(f"{'dry-run: ' if args.dry_run else ''}proposed {added} preprint(s)")
    if args.dry_run:
        return 0
    return sync_docs(args.readme, dry_run=False)


if __name__ == "__main__":
    sys.exit(main())
