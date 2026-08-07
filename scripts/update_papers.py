#!/usr/bin/env python3
"""
script to update the papers section in the awesome-bo README using the arxiv api.

usage:
  python scripts/update_papers.py [--readme PATH] [--max-results N] [--arxiv-cap N] [--dry-run]

notes:
  - uses only the python standard library.
  - filters for papers likely about bayesian optimization via keywords.
  - deduplicates by title against what's already in the README (both sections).
  - peer-reviewed papers (venue detected from journal_ref/comment) go into the
    '## Papers' table; everything else lands in '## Recent arXiv Preprints',
    which is capped at --arxiv-cap entries (oldest preprints are dropped once
    the cap is exceeded) so the README doesn't get flooded with unreviewed work.
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional, Tuple
from urllib.parse import quote
from urllib.request import urlopen
import xml.etree.ElementTree as ET


ARXIV_API_URL = "http://export.arxiv.org/api/query"

# keywords to determine whether an arxiv entry is about bayesian optimization
KEYWORDS = (
    "bayesian optimization",
    "bayesian optimisation",
    "bayes opt",
    "bayes-opt",
    "bayesopt",
    "bo for",
)

# known venues to detect from journal_ref or comment
KNOWN_VENUES = (
    "icml",
    "iclr",
    "neurips",
    "nips",
    "aistats",
    "uai",
    "kdd",
    "aaai",
    "jmlr",
    "tmlr",
    "springer",
    "ieee",
)

DEFAULT_ARXIV_CAP = 15


@dataclass
class Paper:
    title: str
    url: str
    venue: str
    year: int

    @property
    def is_peer_reviewed(self) -> bool:
        return self.venue.strip().lower() != "arxiv"


def build_arxiv_query(max_results: int) -> str:
    """build a query url for arxiv api."""
    terms = [
        'all:"bayesian optimization"',
        'ti:"bayesian optimization"',
        'all:"bayesian optimisation"',
        'ti:"bayesian optimisation"',
        'all:"bayesopt"',
        'ti:"bayesopt"',
    ]
    search_query = quote(" OR ".join(terms))
    url = (
        f"{ARXIV_API_URL}?search_query={search_query}"
        f"&start=0&max_results={max_results}&sortBy=lastUpdatedDate&sortOrder=descending"
    )
    return url


def fetch_arxiv_feed(max_results: int) -> ET.Element:
    """fetch arxiv atom feed and return root element."""
    url = build_arxiv_query(max_results=max_results)
    with urlopen(url) as resp:
        data = resp.read()
    root = ET.fromstring(data)
    return root


def extract_text(elem: Optional[ET.Element]) -> str:
    return elem.text.strip() if elem is not None and elem.text else ""


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def looks_like_bo(title: str, summary: str) -> bool:
    """check if the entry looks like bayesian optimization by keywords."""
    t = title.lower()
    s = summary.lower()
    for kw in KEYWORDS:
        if kw in t or kw in s:
            return True
    return False


def infer_venue(journal_ref: str, comment: str) -> str:
    """infer a simple venue string from journal_ref or comment fields."""
    text = f"{journal_ref} {comment}".lower()
    for venue in KNOWN_VENUES:
        if venue in text:
            if venue == "nips":
                return "NeurIPS"
            if venue == "ieee":
                return "IEEE"
            return venue.upper()
    # default to arxiv if nothing else found
    return "arXiv"


def safe_year(published: str, journal_ref: str) -> int:
    """extract year from published date or journal_ref."""
    # try published timestamp first (e.g., 2024-08-14T17:14:01Z)
    try:
        year = dt.datetime.fromisoformat(published.replace("Z", "+00:00")).year
        return year
    except Exception:
        pass
    # fallback: regex search in journal_ref
    m = re.search(r"(19|20)\d{2}", journal_ref)
    if m:
        return int(m.group(0))
    # final fallback: current year
    return dt.datetime.utcnow().year


def parse_arxiv_entries(feed_root: ET.Element) -> List[Paper]:
    """parse arxiv atom xml into paper objects, filtered for bo."""
    ns = {
        "atom": "http://www.w3.org/2005/Atom",
        "arxiv": "http://arxiv.org/schemas/atom",
    }
    papers: List[Paper] = []
    for entry in feed_root.findall("atom:entry", ns):
        title = normalize_space(html.unescape(extract_text(entry.find("atom:title", ns))))
        url = extract_text(entry.find("atom:id", ns))
        summary = normalize_space(extract_text(entry.find("atom:summary", ns)))
        if not looks_like_bo(title, summary):
            continue
        journal_ref = extract_text(entry.find("arxiv:journal_ref", ns))
        comment = extract_text(entry.find("arxiv:comment", ns))
        published = extract_text(entry.find("atom:published", ns))
        venue = infer_venue(journal_ref, comment)
        year = safe_year(published, journal_ref)
        papers.append(Paper(title=title, url=url, venue=venue, year=year))
    # deduplicate by normalized title
    seen = set()
    unique: List[Paper] = []
    for p in papers:
        key = p.title.casefold()
        if key in seen:
            continue
        seen.add(key)
        unique.append(p)
    return unique


def read_readme(path: Path) -> List[str]:
    return path.read_text(encoding="utf-8").splitlines()


def write_readme(path: Path, lines: List[str]) -> None:
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def find_table_section(lines: List[str], heading_prefix: str) -> Tuple[int, int]:
    """return (start_index_of_rows, end_index_exclusive) for a '## ' table section.

    the start index points to the line right after the table header separator.
    the end index points to the line of the next '## ' heading or eof.
    """
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
        raise RuntimeError(f"could not find table header separator for '{heading_prefix}' in README.md")

    end_idx = len(lines)
    for i in range(sep_idx + 1, len(lines)):
        if lines[i].startswith("## ") and i > sep_idx + 1:
            end_idx = i
            break

    return sep_idx + 1, end_idx


def extract_existing_titles(lines: List[str], start: int, end: int) -> set:
    """extract existing paper titles from the markdown table rows."""
    titles = set()
    row_re = re.compile(r"^\|\s*\[(?P<title>[^\]]+)\]\([^)]+\)\s*\|", re.IGNORECASE)
    for i in range(start, end):
        m = row_re.match(lines[i].strip())
        if m:
            titles.add(m.group("title").casefold())
    return titles


def parse_table_rows(lines: List[str], start: int, end: int) -> List[Tuple[str, str, str, int]]:
    """parse existing markdown table rows into (title, url, venue, year) tuples."""
    row_re = re.compile(
        r"^\|\s*\[(?P<title>[^\]]+)\]\((?P<url>[^)]+)\)\s*\|\s*(?P<venue>[^|]+?)\s*\|\s*(?P<year>\d{4})\s*\|"
    )
    rows = []
    for i in range(start, end):
        line = lines[i].strip()
        if not line:
            continue
        m = row_re.match(line)
        if m:
            rows.append((m.group("title"), m.group("url"), m.group("venue"), int(m.group("year"))))
    return rows


def make_table_row(paper: Paper) -> str:
    return f"| [{paper.title}]({paper.url}) | {paper.venue} | {paper.year} |"


def update_readme_with_papers(
    readme_path: Path, papers: List[Paper], arxiv_cap: int, dry_run: bool
) -> Tuple[int, int]:
    """update README with new papers.

    returns (peer_reviewed_added, arxiv_added).
    """
    lines = read_readme(readme_path)

    papers_start, papers_end = find_table_section(lines, "## papers")
    arxiv_start, arxiv_end = find_table_section(lines, "## recent arxiv preprints")

    existing_titles = extract_existing_titles(lines, papers_start, papers_end)
    existing_titles |= extract_existing_titles(lines, arxiv_start, arxiv_end)

    candidates = [p for p in papers if p.title.casefold() not in existing_titles]
    peer_candidates = sorted(
        (p for p in candidates if p.is_peer_reviewed), key=lambda p: (-p.year, p.title.lower())
    )
    arxiv_candidates = sorted(
        (p for p in candidates if not p.is_peer_reviewed), key=lambda p: (-p.year, p.title.lower())
    )

    peer_rows = [make_table_row(p) for p in peer_candidates]

    # rebuild arxiv preprints section: new entries on top, capped, oldest dropped
    existing_arxiv_rows = parse_table_rows(lines, arxiv_start, arxiv_end)
    new_arxiv_rows = [(p.title, p.url, p.venue, p.year) for p in arxiv_candidates]
    combined_arxiv_rows = (new_arxiv_rows + existing_arxiv_rows)[:arxiv_cap]
    arxiv_lines = [f"| [{t}]({u}) | {v} | {y} |" for (t, u, v, y) in combined_arxiv_rows]

    updated_lines = list(lines)
    # replace arxiv section first (higher index) so papers_start/end stay valid
    updated_lines[arxiv_start:arxiv_end] = arxiv_lines + [""]
    updated_lines[papers_start:papers_end] = peer_rows + updated_lines[papers_start:papers_end]

    if (peer_rows or new_arxiv_rows) and not dry_run:
        write_readme(readme_path, updated_lines)

    return len(peer_rows), len(new_arxiv_rows)


def parse_args(argv: Optional[Iterable[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="update README papers from arxiv")
    parser.add_argument(
        "--readme",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "README.md",
        help="path to README.md (default: repo root README.md)",
    )
    parser.add_argument(
        "--max-results",
        type=int,
        default=100,
        help="max results to fetch from arxiv (default: 100)",
    )
    parser.add_argument(
        "--arxiv-cap",
        type=int,
        default=DEFAULT_ARXIV_CAP,
        help=f"max entries to keep in the Recent arXiv Preprints section (default: {DEFAULT_ARXIV_CAP})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="do not write file, just report what would change",
    )
    return parser.parse_args(argv)


def main(argv: Optional[Iterable[str]] = None) -> int:
    args = parse_args(argv)
    readme_path: Path = args.readme
    if not readme_path.exists():
        print(f"readme not found at: {readme_path}")
        return 2

    try:
        feed = fetch_arxiv_feed(max_results=args.max_results)
        papers = parse_arxiv_entries(feed)
    except Exception as exc:
        print(f"failed to fetch or parse arxiv feed: {exc}")
        return 3

    peer_added, arxiv_added = update_readme_with_papers(
        readme_path, papers, arxiv_cap=args.arxiv_cap, dry_run=args.dry_run
    )
    if peer_added or arxiv_added:
        print(f"added {peer_added} peer-reviewed paper(s) and {arxiv_added} arXiv preprint(s)")
    else:
        print("no new papers found to add")
    if args.dry_run:
        print("dry-run mode: no changes written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
