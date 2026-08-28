#!/usr/bin/env python3
"""Mirror README.md list sections into docs/.

The GitHub README is the source of truth (and what awesome-lint checks).
After you add or edit an entry in README.md, run:

  python scripts/sync_docs.py

Docs-only extras are kept: the software comparison table, and a few
Getting started / Community sentences. index.md, contributing.md, and
unmaintained.md are not generated.

Usage:
  python scripts/sync_docs.py [--readme PATH] [--docs-dir PATH] [--check]
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple


SKIP_H2 = {"Contents", "Contributing"}
REQUIRED_H2 = (
    "Getting Started",
    "Books",
    "Software",
    "Papers",
    "Benchmarks",
    "Applications",
    "Community",
    "Videos",
    "Blogs",
    "Recent Preprints",
)

LIST_ITEM_RE = re.compile(r"^- \[.+\]\(.+\).*$")
TABLE_SEP_RE = re.compile(r"^\|[\s:|-]+\|$")


@dataclass
class Block:
    title: str
    intro: str = ""
    items: List[str] = field(default_factory=list)
    subsections: List["Block"] = field(default_factory=list)


def split_h2(lines: List[str]) -> Dict[str, List[str]]:
    sections: Dict[str, List[str]] = {}
    current: Optional[str] = None
    buf: List[str] = []
    for line in lines:
        if line.startswith("## "):
            if current is not None:
                sections[current] = buf
            current = line[3:].strip()
            buf = []
        elif current is not None:
            buf.append(line)
    if current is not None:
        sections[current] = buf
    return sections


def parse_block(title: str, body: List[str]) -> Block:
    intro: List[str] = []
    items: List[str] = []
    subsections: List[Block] = []
    sub_title: Optional[str] = None
    sub_intro: List[str] = []
    sub_items: List[str] = []
    seen_list = False

    def flush_sub() -> None:
        nonlocal sub_title, sub_intro, sub_items
        if sub_title is None:
            return
        subsections.append(
            Block(
                title=sub_title,
                intro=trim_prose(sub_intro),
                items=list(sub_items),
            )
        )
        sub_title = None
        sub_intro = []
        sub_items = []

    for line in body:
        stripped = line.strip()
        if stripped.startswith("### "):
            flush_sub()
            sub_title = stripped[4:].strip()
            seen_list = False
            continue
        if sub_title is not None:
            if LIST_ITEM_RE.match(stripped):
                seen_list = True
                sub_items.append(stripped)
            elif not seen_list:
                sub_intro.append(line)
            continue
        if LIST_ITEM_RE.match(stripped):
            seen_list = True
            items.append(stripped)
        elif not seen_list:
            intro.append(line)

    flush_sub()
    return Block(title=title, intro=trim_prose(intro), items=items, subsections=subsections)


def trim_prose(lines: List[str]) -> str:
    text = "\n".join(lines).strip("\n")
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text


def page(*parts: str) -> str:
    chunks = [p.strip("\n") for p in parts if p and p.strip()]
    return "\n\n".join(chunks) + "\n"


def bullets(items: List[str]) -> str:
    return "\n".join(items)


def extract_table(text: str) -> str:
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.startswith("|") and i + 1 < len(lines) and TABLE_SEP_RE.match(lines[i + 1].strip()):
            start = i
            break
    if start is None:
        return ""
    end = start
    while end < len(lines) and lines[end].startswith("|"):
        end += 1
    return "\n".join(lines[start:end])


def rewrite_software_intro(intro: str) -> str:
    return intro.replace(
        "listed in [unmaintained.md](unmaintained.md).",
        "listed under [Unmaintained](unmaintained.md).",
    )


def rewrite_preprints_intro(intro: str) -> str:
    return intro.replace(
        "matching Papers section",
        "matching [Papers](papers.md) section",
    )


def render_getting_started(block: Block) -> str:
    return page(
        "# Getting started",
        "New to Bayesian optimization? A tutorial, then a book, then a library.",
        bullets(block.items),
        "Skip the GP book if Distill already made sense.",
        "Then a book: [Garnett](books.md) for theory, or "
        "[Bayesian Optimization in Action](https://www.manning.com/books/bayesian-optimization-in-action) "
        "for a Python walkthrough.",
        "Then a library. [Ax](https://ax.dev/) and "
        "[Vizier](https://github.com/google/vizier) are services: you declare "
        "the search space and the metric, and they run the loop. Start with Ax "
        "unless you already use Google's stack.",
        "[BoTorch](https://botorch.org/) is the PyTorch toolkit under Ax. You "
        "write that loop yourself: fit a GPyTorch model, define an acquisition, "
        "optimize it. Use BoTorch when you are implementing a method, or changing "
        "the surrogate or the acquisition.",
        "Other libraries are under [Software](software.md). Lectures are under "
        "[Community](community.md).",
    )


def render_simple(title: str, block: Block) -> str:
    return page(f"# {title}", block.intro, bullets(block.items) if block.items else "")


def render_software(block: Block, existing: str) -> str:
    parts: List[str] = [
        "# Software",
        rewrite_software_intro(block.intro),
        "The table covers every actively maintained library listed here, "
        "not a shortlist.",
    ]
    table = extract_table(existing)
    if table:
        parts.append(table)
    if block.items:
        parts.append("## Active libraries")
        parts.append(bullets(block.items))
    for sub in block.subsections:
        parts.append(f"## {sub.title}")
        if sub.intro:
            parts.append(sub.intro)
        if sub.items:
            parts.append(bullets(sub.items))
    return page(*parts)


def render_papers(block: Block) -> str:
    parts: List[str] = ["# Papers", block.intro]
    for sub in block.subsections:
        parts.append(f"## {sub.title}")
        if sub.intro:
            parts.append(sub.intro)
        if sub.items:
            parts.append(bullets(sub.items))
    return page(*parts)


def render_community(community: Block, videos: Block, blogs: Block) -> str:
    return page(
        "# Community",
        "Workshops, schools, lectures, and write-ups.",
        "## Schools and groups",
        bullets(community.items),
        "## Videos",
        bullets(videos.items),
        "## Blogs",
        bullets(blogs.items),
    )


def render_preprints(block: Block) -> str:
    return page(
        "# Recent preprints",
        rewrite_preprints_intro(block.intro),
        bullets(block.items),
    )


def parse_readme(readme: Path) -> Dict[str, Block]:
    lines = readme.read_text(encoding="utf-8").splitlines()
    raw = split_h2(lines)
    missing = [name for name in REQUIRED_H2 if name not in raw]
    if missing:
        raise RuntimeError("README.md missing sections: " + ", ".join(missing))
    return {name: parse_block(name, raw[name]) for name in REQUIRED_H2}


def planned_pages(readme: Path, docs_dir: Path) -> Dict[Path, str]:
    blocks = parse_readme(readme)
    software_path = docs_dir / "software.md"
    existing_software = software_path.read_text(encoding="utf-8") if software_path.exists() else ""
    return {
        docs_dir / "getting-started.md": render_getting_started(blocks["Getting Started"]),
        docs_dir / "books.md": render_simple("Books", blocks["Books"]),
        docs_dir / "software.md": render_software(blocks["Software"], existing_software),
        docs_dir / "papers.md": render_papers(blocks["Papers"]),
        docs_dir / "benchmarks.md": render_simple("Benchmarks", blocks["Benchmarks"]),
        docs_dir / "applications.md": render_simple("Applications", blocks["Applications"]),
        docs_dir / "community.md": render_community(
            blocks["Community"], blocks["Videos"], blocks["Blogs"]
        ),
        docs_dir / "preprints.md": render_preprints(blocks["Recent Preprints"]),
    }


def write_pages(pages: Dict[Path, str], check: bool) -> Tuple[List[Path], List[Path]]:
    changed: List[Path] = []
    written: List[Path] = []
    for path, content in pages.items():
        old = path.read_text(encoding="utf-8") if path.exists() else None
        if old == content:
            continue
        changed.append(path)
        if not check:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            written.append(path)
    return changed, written


def parse_args(argv: Optional[Iterable[str]] = None) -> argparse.Namespace:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description="Mirror README.md list sections into docs/")
    parser.add_argument("--readme", type=Path, default=root / "README.md")
    parser.add_argument("--docs-dir", type=Path, default=root / "docs")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit 1 if docs/ would change; do not write files",
    )
    return parser.parse_args(argv)


def main(argv: Optional[Iterable[str]] = None) -> int:
    args = parse_args(argv)
    if not args.readme.exists():
        print(f"readme not found at: {args.readme}")
        return 2
    try:
        pages = planned_pages(args.readme, args.docs_dir)
    except Exception as exc:
        print(f"failed to parse README: {exc}")
        return 3
    changed, written = write_pages(pages, check=args.check)
    if args.check:
        if changed:
            print("docs/ out of sync with README.md. Run: python scripts/sync_docs.py")
            for path in changed:
                print(f"  {path}")
            return 1
        print("docs/ matches README.md")
        return 0
    if written:
        print("updated " + ", ".join(p.name for p in written))
    else:
        print("docs/ already matches README.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
