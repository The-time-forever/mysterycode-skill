#!/usr/bin/env python3
"""Validate an Obsidian mystery vault for missing links and stale indexes."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:\|[^\]]+)?\]\]")
BOOKS_DIR_NAME = "Books"
ANALYSIS_DIR_NAME = "Analysis"
CHARACTERS_DIR_NAME = "Characters"


@dataclass
class Finding:
    level: str
    message: str
    path: Path | None = None

    def render(self, root: Path) -> str:
        prefix = f"[{self.level}]"
        if self.path is None:
            return f"{prefix} {self.message}"
        try:
            rel = self.path.relative_to(root)
        except ValueError:
            rel = self.path
        return f"{prefix} {rel}: {self.message}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a mystery-analysis Obsidian vault."
    )
    parser.add_argument("vault", help="Path to the vault root directory.")
    return parser.parse_args()


def markdown_files(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("*.md") if path.is_file())


def chapter_files(root: Path) -> list[Path]:
    books_dir = root / BOOKS_DIR_NAME
    if not books_dir.exists():
        return []
    return sorted(
        path
        for path in books_dir.rglob("*.md")
        if path.name != "00-书籍信息.md" and not is_placeholder_chapter(path)
    )


def is_placeholder_chapter(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    return "#todo" in text or "尚未整理" in text


def extract_links(text: str) -> list[str]:
    return [match.group(1) for match in WIKILINK_RE.finditer(text)]


def title_from_markdown(path: Path) -> str | None:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return None


def build_target_map(files: list[Path]) -> dict[str, Path]:
    targets: dict[str, Path] = {}
    for path in files:
        targets[path.stem] = path
    return targets


def validate_structure(root: Path, findings: list[Finding]) -> None:
    required = [
        root / "Home.md",
        root / ANALYSIS_DIR_NAME / "线索追踪.md",
    ]
    for required_path in required:
        if not required_path.exists():
            findings.append(Finding("ERROR", "missing required file", required_path))
    books_dir = root / BOOKS_DIR_NAME
    if not books_dir.exists():
        findings.append(Finding("ERROR", "missing Books directory", books_dir))
        return
    info_pages = list(books_dir.rglob("00-书籍信息.md"))
    if not info_pages:
        findings.append(Finding("ERROR", "missing 00-书籍信息.md under Books/", books_dir))


def validate_empty_pages(files: list[Path], findings: list[Finding]) -> None:
    for path in files:
        text = path.read_text(encoding="utf-8")
        if not text.strip():
            findings.append(Finding("ERROR", "empty markdown page", path))


def validate_links(files: list[Path], findings: list[Finding]) -> None:
    target_map = build_target_map(files)
    for path in files:
        text = path.read_text(encoding="utf-8")
        for raw_link in extract_links(text):
            leaf = Path(raw_link).name
            if leaf not in target_map:
                findings.append(
                    Finding("ERROR", f"missing link target [[{raw_link}]]", path)
                )


def validate_book_indexes(root: Path, findings: list[Finding]) -> None:
    books_root = root / BOOKS_DIR_NAME
    if not books_root.exists():
        return
    for book_dir in sorted(path for path in books_root.iterdir() if path.is_dir()):
        info_path = book_dir / "00-书籍信息.md"
        chapter_paths = sorted(
            path
            for path in book_dir.glob("*.md")
            if path.name != "00-书籍信息.md" and not is_placeholder_chapter(path)
        )
        if not info_path.exists():
            findings.append(Finding("ERROR", "missing book info page", book_dir))
            continue
        info_text = info_path.read_text(encoding="utf-8")
        for chapter_path in chapter_paths:
            if chapter_path.stem not in info_text:
                findings.append(
                    Finding(
                        "ERROR",
                        f"chapter not listed in 00-书籍信息.md: {chapter_path.stem}",
                        info_path,
                    )
                )


def validate_home_recent(root: Path, findings: list[Finding]) -> None:
    home_path = root / "Home.md"
    if not home_path.exists():
        return
    chapter_paths = chapter_files(root)
    if not chapter_paths:
        return
    latest = max(chapter_paths, key=lambda path: path.name)
    home_text = home_path.read_text(encoding="utf-8")
    if latest.stem not in home_text:
        findings.append(
            Finding(
                "WARN",
                f"Home.md does not mention latest chapter {latest.stem}",
                home_path,
            )
        )


def validate_chapter_navigation(root: Path, findings: list[Finding]) -> None:
    chapters = chapter_files(root)
    if not chapters:
        return
    names = [path.stem for path in chapters]
    for index, path in enumerate(chapters):
        text = path.read_text(encoding="utf-8")
        previous_expected = names[index - 1] if index > 0 else "00-书籍信息"
        next_expected = names[index + 1] if index + 1 < len(names) else None
        previous_line = next((line for line in text.splitlines() if line.startswith("Previous: ")), None)
        next_line = next((line for line in text.splitlines() if line.startswith("Next: ")), None)
        if previous_line is None or previous_expected not in previous_line:
            findings.append(
                Finding(
                    "WARN",
                    f"unexpected Previous link, expected {previous_expected}",
                    path,
                )
            )
        if next_expected is not None and (next_line is None or next_expected not in next_line):
            findings.append(
                Finding(
                    "WARN",
                    f"unexpected Next link, expected {next_expected}",
                    path,
                )
            )


def validate_alias_redirects(root: Path, findings: list[Finding]) -> None:
    characters_dir = root / CHARACTERS_DIR_NAME
    if not characters_dir.exists():
        return
    for path in sorted(characters_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        title = title_from_markdown(path)
        if not title:
            findings.append(Finding("WARN", "character page has no H1 title", path))
            continue
        has_alias_note = "见 [[" in text or "别名" in text or "旧称" in text
        if title != path.stem and not has_alias_note:
            findings.append(
                Finding(
                    "WARN",
                    f"file name '{path.stem}' differs from H1 '{title}' without alias note",
                    path,
                )
            )


def validate_root_clutter(root: Path, findings: list[Finding]) -> None:
    allowed = {"Home.md"}
    for path in sorted(root.glob("*.md")):
        if path.name in allowed:
            continue
        findings.append(
            Finding(
                "WARN",
                "markdown page is in vault root; prefer Characters/, Locations/, Objects/, Analysis/, Timeline/, or Books/",
                path,
            )
        )


def main() -> int:
    args = parse_args()
    root = Path(args.vault).resolve()
    if not root.exists() or not root.is_dir():
        print(f"Vault path not found: {root}", file=sys.stderr)
        return 2

    files = markdown_files(root)
    findings: list[Finding] = []

    validate_structure(root, findings)
    validate_empty_pages(files, findings)
    validate_links(files, findings)
    validate_book_indexes(root, findings)
    validate_home_recent(root, findings)
    validate_chapter_navigation(root, findings)
    validate_alias_redirects(root, findings)
    validate_root_clutter(root, findings)

    if findings:
        for finding in findings:
            print(finding.render(root))
        if any(finding.level == "ERROR" for finding in findings):
            return 1
        return 0

    print("Vault validation passed with no findings.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
