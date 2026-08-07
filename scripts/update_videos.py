#!/usr/bin/env python3
"""
update the Videos section in README.md using YouTube Data API.

usage:
  export YOUTUBE_API_KEY=...
  python scripts/update_videos.py [--readme PATH] [--max-results N] [--dry-run]

notes:
  - requires YOUTUBE_API_KEY; if missing, runs as a no-op.
  - maps channel/title keywords to an 'Event' field when possible, else 'YouTube'.
  - inserts new rows at the top (Title | Presenter | Event | Year).
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import os
import re
from pathlib import Path
from typing import Iterable, List, Optional, Tuple
from urllib.parse import urlencode
from urllib.request import urlopen


EVENT_KEYWORDS = {
    "pydata": "PyData",
    "informs": "INFORMS",
    "uai": "UAI",
    "icml": "ICML",
    "neurips": "NeurIPS",
    "aistats": "AISTATS",
    "probabilistic numerics": "Probabilistic Numerics",
    "summer school": "Summer School",
}


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
        raise RuntimeError("could not find table header separator in Videos section")
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


def infer_event(title: str, channel: str) -> str:
    s = f"{title} {channel}".lower()
    for key, label in EVENT_KEYWORDS.items():
        if key in s:
            return label
    return "YouTube"


def fetch_youtube(max_results: int, api_key: str) -> List[dict]:
    params = {
        "part": "snippet",
        "q": "\"Bayesian Optimization\"",
        "type": "video",
        "order": "date",
        "maxResults": max_results,
        "key": api_key,
    }
    url = f"https://www.googleapis.com/youtube/v3/search?{urlencode(params)}"
    with urlopen(url) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data.get("items", [])


def to_row(item: dict) -> Optional[Tuple[str, str, str, int, str]]:
    snippet = item.get("snippet", {})
    title = html.unescape(snippet.get("title", "").strip())
    channel = snippet.get("channelTitle", "").strip()
    published = snippet.get("publishedAt", "")
    try:
        year = dt.datetime.fromisoformat(published.replace("Z", "+00:00")).year
    except Exception:
        year = 0
    vid_id = (item.get("id") or {}).get("videoId")
    if not title or not vid_id:
        return None
    url = f"https://www.youtube.com/watch?v={vid_id}"
    event = infer_event(title, channel)
    return title, channel, event, year, url


def update_videos(readme_path: Path, items: List[dict], dry_run: bool) -> int:
    lines = read_readme(readme_path)
    start, end = find_section_table_bounds(lines, "## Videos")
    existing = extract_existing_titles(lines, start, end)
    rows: List[str] = []
    for it in items:
        parsed = to_row(it)
        if not parsed:
            continue
        title, presenter, event, year, url = parsed
        if title.casefold() in existing:
            continue
        rows.append(f"| [{title}]({url}) | {presenter} | {event} | {year or ''} |")
    # sort newest first
    def sort_key(r: str) -> Tuple[int, str]:
        m = re.search(r"\|\s*(\d{4})\s*\|\s*$", r)
        yr = int(m.group(1)) if m else 0
        t = r.split("|")[1].lower()
        return (-yr, t)
    rows.sort(key=sort_key)
    if not rows:
        return 0
    updated = lines[:start] + rows + lines[start:]
    if not dry_run:
        write_readme(readme_path, updated)
    return len(rows)


def parse_args(argv: Optional[Iterable[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="update README Videos from YouTube")
    p.add_argument("--readme", type=Path, default=Path(__file__).resolve().parents[1] / "README.md")
    p.add_argument("--max-results", type=int, default=25)
    p.add_argument("--dry-run", action="store_true")
    return p.parse_args(argv)


def main(argv: Optional[Iterable[str]] = None) -> int:
    args = parse_args(argv)
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        print("missing YOUTUBE_API_KEY; skipping videos update")
        return 0
    try:
        items = fetch_youtube(args.max_results, api_key)
    except Exception as exc:
        print(f"failed to fetch from youtube: {exc}")
        return 2
    added = update_videos(args.readme, items, dry_run=args.dry_run)
    print(("dry-run: " if args.dry_run else "") + f"added {added} video(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


