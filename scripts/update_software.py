#!/usr/bin/env python3
"""
update the Software section in README.md using GitHub repository search.

usage:
  export GITHUB_TOKEN=...  # optional, improves rate limits
  python scripts/update_software.py [--readme PATH] [--per-page N] [--dry-run]

notes:
  - searches repositories mentioning bayesian optimization in name/description/readme.
  - deduplicates by repository name.
  - inserts new rows at the top (Name | Description).
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
from pathlib import Path
from typing import Iterable, List, Optional, Tuple
from urllib.parse import urlencode
from urllib.request import Request, urlopen


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
        raise RuntimeError("could not find table header separator in Software section")
    end_idx = len(lines)
    for i in range(sep_idx + 1, len(lines)):
        if lines[i].startswith("## ") and i > sep_idx + 1:
            end_idx = i
            break
    return sep_idx + 1, end_idx


def extract_existing_names(lines: List[str], start: int, end: int) -> set:
    names = set()
    row_re = re.compile(r"^\|\s*\[(?P<name>[^\]]+)\]\([^)]+\)\s*\|", re.IGNORECASE)
    for i in range(start, end):
        m = row_re.match(lines[i].strip())
        if m:
            names.add(m.group("name").casefold())
    return names


def fetch_github_repos(per_page: int, token: Optional[str]) -> List[dict]:
    # restrict to name/description (not full readme) so unrelated repos that
    # merely mention "bayesian optimization" once in a long readme don't match
    query = (
        '"bayesian optimization" in:name,description '
        'OR "bayesian optimisation" in:name,description'
    )
    params = {
        "q": query,
        "sort": "stars",
        "order": "desc",
        "per_page": per_page,
    }
    url = f"https://api.github.com/search/repositories?{urlencode(params)}"
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = Request(url, headers=headers)
    with urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data.get("items", [])


def to_row(repo: dict) -> Optional[Tuple[str, str, str]]:
    name = repo.get("name")
    html_url = repo.get("html_url")
    desc = html.unescape((repo.get("description") or "").strip())
    if not name or not html_url:
        return None
    return name, html_url, desc


def update_software(
    readme_path: Path, repos: List[dict], min_stars: int, max_new: int, dry_run: bool
) -> int:
    lines = read_readme(readme_path)
    start, end = find_section_table_bounds(lines, "## Software")
    existing = extract_existing_names(lines, start, end)
    rows: List[str] = []
    for r in repos:
        if r.get("archived"):
            continue
        if r.get("stargazers_count", 0) < min_stars:
            continue
        parsed = to_row(r)
        if not parsed:
            continue
        name, url, desc = parsed
        if name.casefold() in existing:
            continue
        rows.append(f"| [{name}]({url}) | {desc} |")
    # already sorted by stars desc from the API; keep only the top max_new
    rows = rows[:max_new]
    rows.sort(key=lambda x: x.split("|")[1].lower())
    if not rows:
        return 0
    updated = lines[:start] + rows + lines[start:]
    if not dry_run:
        write_readme(readme_path, updated)
    return len(rows)


def parse_args(argv: Optional[Iterable[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="update README Software from GitHub search")
    p.add_argument("--readme", type=Path, default=Path(__file__).resolve().parents[1] / "README.md")
    p.add_argument("--per-page", type=int, default=30)
    p.add_argument("--min-stars", type=int, default=100, help="minimum stars to be considered (default: 100)")
    p.add_argument("--max-new", type=int, default=5, help="max new repos to add per run (default: 5)")
    p.add_argument("--dry-run", action="store_true")
    return p.parse_args(argv)


def main(argv: Optional[Iterable[str]] = None) -> int:
    print(
        "update_software.py is disabled. Software is curated by hand "
        "(see contributing.md). Use scripts/update_papers.py for preprints."
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())


